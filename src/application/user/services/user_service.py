from application.user.dto.register_user import RegisterUser
from application.user.dto.user import UserDTO
from application.user.exceptions.user_already_exist import (
    UserAlreadyExistException,
)
from application.user.exceptions.user_not_found import UserNotFoundException
from application.user.interfaces.repositories.user import IUserRepository
from application.user.interfaces.services.cryptography import (
    ICryptographyService,
)
from application.user.interfaces.services.email import IEmailService
from domain.user.entities.user import UserEntity
from domain.code.enums import Purpose


class UserService:
    def __init__(
        self,
        user_repo: IUserRepository,
        cryptography_service: ICryptographyService,
        email_service: IEmailService,
    ):
        self.user_repo = user_repo
        self.cryptography_service = cryptography_service
        self.email_service = email_service

    async def register(self, data: RegisterUser) -> UserDTO:
        try:
            if await self.user_repo.get_by_email(data.email):
                raise UserAlreadyExistException(
                    f"User with email {data.email} already exists"
                )
        except UserNotFoundException:
            pass

        try:
            if await self.user_repo.get_by_username(data.username):
                raise UserAlreadyExistException(
                    f"User with username {data.username} already exists"
                )
        except UserNotFoundException:
            pass

        salt = self.cryptography_service.generate_salt()
        hashed_password = self.cryptography_service.hash_password(
            data.password, salt
        )

        user = UserEntity.factory(
            email=data.email,
            username=data.username,
            password_hash=hashed_password,
            roles=[],
        )

        user = await self.user_repo.save(user)
        await self.user_repo.commit()

        # await self.email_service.send_verification_code(
        #     user_uuid=user.uuid, email=user.email, purpose=Purpose.REGISTRATION
        # )
        await self.email_service.send_email(
            email=user.email,
            subject="Registration",
            body="You have been registered",
        )

        return UserDTO.from_entity(user)
