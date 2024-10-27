from loguru import logger

from application.code.enums.email_code_type import EmailCodeType
from application.code.interfaces.email_code_service import IEmailCodeService
from application.session.dto.session import SessionDTO
from application.session.interfaces.session_service import ISessionService
from application.user.dto.register_user import RegisterUser
from application.user.dto.user import UserDTO
from application.user.exceptions.user_already_exist import (
    UserAlreadyExistException,
)
from application.user.exceptions.user_is_deactivate import (
    UserIsDeactivateException,
)
from application.user.exceptions.user_not_confirm_email import (
    UserNotConfirmEmailException,
)
from application.user.exceptions.user_not_found import UserNotFoundException
from application.user.ports.repositories.user import IUserRepository
from application.user.ports.services.cryptography import (
    ICryptographyService,
)
from application.utils.iunitofwork import IUnitOfWork
from domain.session.value_objects.user_agent import UserAgent
from domain.user.entities.user import UserEntity
from shared.validators.email import validate_email


class UserService:
    def __init__(
        self,
        user_repo: IUserRepository,
        cryptography_service: ICryptographyService,
        email_code_service: IEmailCodeService,
        session_service: ISessionService,
        uow: IUnitOfWork,
    ):
        self._user_repo = user_repo
        self._cryptography_service = cryptography_service
        self._email_code_service = email_code_service
        self._session_service = session_service
        self._uow = uow

    async def _get_user_by_session_id(self, session_id: str) -> UserEntity:
        session = await self._session_service.validate_session(session_id)
        user = await self._user_repo.get_by_uuid(session.user_uuid)

        return user

    async def register(
        self, data: RegisterUser, user_agent: UserAgent, ip_address: str
    ) -> tuple[UserDTO, list[SessionDTO], str]:
        # Validate email
        validate_email(data.email)

        try:
            if await self._user_repo.get_by_email(data.email):
                raise UserAlreadyExistException(
                    f"User with email {data.email} already exists"
                )
        except UserNotFoundException:
            pass

        try:
            if await self._user_repo.get_by_username(data.username):
                raise UserAlreadyExistException(
                    f"User with username {data.username} already exists"
                )
        except UserNotFoundException:
            pass

        salt = self._cryptography_service.generate_salt()
        hashed_password = self._cryptography_service.hash_password(
            data.password, salt
        )

        user = UserEntity.factory(
            email=data.email,
            username=data.username,
            password_hash=hashed_password,
            roles=[],
        )
        user_dto = UserDTO.from_entity(user)

        # We'll use the session entity and store it right here to ensure
        # transactional between creating a user
        # and their session in a single transaction.
        session = self._session_service.create_session_entity(
            user=user_dto,
            user_agent=user_agent,
            ip_address=ip_address,
        )

        async with self._uow:
            await self._uow.user_repo.save(user)
            await self._uow.session_repo.save(session)
            await self._uow.commit()

        try:
            await self._email_code_service.send_code(
                code_type=EmailCodeType.VERIFICATION,
                email=user.email,
                user_uuid=user.uuid,
            )
        except Exception as e:
            logger.error(f"Error sending email: {e}")

        return (
            user_dto,
            [SessionDTO.from_entity(session, is_current=True)],
            session.session_id,
        )

    async def authenticate_by_session_id(self, session_id: str) -> UserDTO:
        user = await self._get_user_by_session_id(session_id)

        if not user.email_verified:
            raise UserNotConfirmEmailException()
        if not user.is_active:
            raise UserIsDeactivateException()

        return UserDTO.from_entity(user)

    async def verify_email(self, session_id: str, code: str) -> UserDTO:
        user = await self._get_user_by_session_id(session_id)

        if await self._email_code_service.validate_code(
            EmailCodeType.VERIFICATION, code, user_uuid=user.uuid
        ):
            user.email_verified = True
            await self._user_repo.update(user)
            await self._user_repo.commit()

        return UserDTO.from_entity(user)
