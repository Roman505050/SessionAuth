from sqlalchemy import insert, update, select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from application.code.exceptions.code_not_found import CodeNotFoundException
from application.code.interfaces.repositories.email_code import (
    IEmailCodeRepository,
)
from domain.code.entities.email_code import EmailCodeEntity
from domain.code.enums import Purpose
from infrastructure.modules.code.models.email_code import EmailCode


class EmailCodeRepository(IEmailCodeRepository):
    model = EmailCode

    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self) -> None:
        await self.session.commit()

    async def save(self, code: EmailCodeEntity) -> EmailCodeEntity:
        stmt = (
            insert(self.model)
            .values(
                uuid=code.uuid,
                code=code.code,
                status=code.status,
                purpose=code.purpose,
                attempts=code.attempts,
                max_attempts=code.max_attempts,
                expires_at=code.expires_at,
                created_at=code.created_at,
                updated_at=code.updated_at,
            )
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        code_model = result.scalars().first()
        if not code_model:
            raise CodeNotFoundException("Code not saved")
        return code_model.to_entity()

    async def update(self, code: EmailCodeEntity) -> EmailCodeEntity:
        stmt = (
            update(self.model)
            .filter_by(uuid=code.uuid)
            .values(
                code=code.code,
                status=code.status,
                purpose=code.purpose,
                attempts=code.attempts,
                max_attempts=code.max_attempts,
                expires_at=code.expires_at,
                updated_at=code.updated_at,
            )
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        code_model = result.scalars().first()
        if not code_model:
            raise CodeNotFoundException(
                f"Code with uuid {code.uuid} not found"
            )
        return code_model.to_entity()

    async def get_by_code(self, user_uuid: UUID, code: str) -> EmailCodeEntity:
        stmt = select(self.model).filter_by(user_uuid=user_uuid, code=code)
        result = await self.session.execute(stmt)
        code_model = result.scalars().first()
        if not code_model:
            raise CodeNotFoundException(f"Code {code} not found")

        return code_model.to_entity()

    async def get_by_purpose(
        self, user_uuid: UUID, purpose: Purpose
    ) -> EmailCodeEntity:
        stmt = select(self.model).filter_by(
            user_uuid=user_uuid, purpose=purpose
        )
        result = await self.session.execute(stmt)
        code_model = result.scalars().first()
        if not code_model:
            raise CodeNotFoundException(
                f"Code with purpose {purpose.value} not found"
            )

        return code_model.to_entity()
