from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from application.user.exceptions.user_not_found import UserNotFoundException
from application.user.ports.repositories.user import IUserRepository
from domain.user.entities.user import UserEntity
from infrastructure.modules.user.models.user import User


class UserRepository(IUserRepository):
    model = User

    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self) -> None:
        await self.session.commit()

    async def save(self, user: UserEntity) -> UserEntity:
        stmt = (
            insert(self.model)
            .values(
                uuid=user.uuid,
                username=user.username,
                email=user.email,
                password_hash=user.password_hash,
                email_verified=user.email_verified,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        user_model = result.scalars().first()
        if not user_model:
            raise Exception("Error saving user.")
        return user_model.to_entity()

    async def get_by_uuid(self, uuid: UUID) -> UserEntity:
        stmt = select(self.model).filter_by(uuid=uuid)
        result = await self.session.execute(stmt)
        user_mdl = result.scalars().first()
        if not user_mdl:
            raise UserNotFoundException(f"User with UUID {uuid} not found.")
        return user_mdl.to_entity()

    async def get_by_email(self, email: str) -> UserEntity:
        stmt = select(self.model).filter_by(email=email)
        result = await self.session.execute(stmt)
        user_mdl = result.scalars().first()
        if not user_mdl:
            raise UserNotFoundException(f"User with email {email} not found.")
        return user_mdl.to_entity()

    async def get_by_username(self, username: str) -> UserEntity:
        stmt = select(self.model).filter_by(username=username)
        result = await self.session.execute(stmt)
        user_mdl = result.scalars().first()
        if not user_mdl:
            raise UserNotFoundException(
                f"User with username {username} not found."
            )
        return user_mdl.to_entity()

    async def update(self, user: UserEntity) -> UserEntity:
        stmt = (
            update(self.model)
            .values(
                uuid=user.uuid,
                username=user.username,
                email=user.email,
                password_hash=user.password_hash,
                email_verified=user.email_verified,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        user_model = result.scalars().first()
        if not user_model:
            raise UserNotFoundException(
                f"User with UUID {user.uuid} not found."
            )
        return user_model.to_entity()

    async def delete(self, uuid: UUID) -> None:
        stmt = delete(self.model).filter_by(uuid=uuid)
        await self.session.execute(stmt)
