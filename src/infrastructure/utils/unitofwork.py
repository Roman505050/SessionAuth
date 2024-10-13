from sqlalchemy.ext.asyncio import AsyncSession

from application.utils.iunitofwork import IUnitOfWork
from infrastructure.database.connext import async_session_maker
from infrastructure.modules.session.repositories.session import (
    SessionRepository,
)
from infrastructure.modules.user.repositories.user import UserRepository


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()

        self.user_repo = UserRepository(self.session)
        self.session_repo = SessionRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type is not None:
            print(exc_type, " | ", exc, " | ", tb)
            await self.rollback()
        await self.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def close(self):
        await self.session.close()
