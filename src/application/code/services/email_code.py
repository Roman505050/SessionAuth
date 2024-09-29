from typing import Literal
from uuid import UUID
import random
import string
import datetime

from application.code.interfaces.repositories.email_code import (
    IEmailCodeRepository,
)
from domain.code.entities.email_code import EmailCodeEntity
from domain.code.enums import Purpose


class EmailCodeService:
    def __init__(self, email_code_repo: IEmailCodeRepository):
        self.email_code_repo = email_code_repo

    async def create_email_code(
        self,
        user_uuid: UUID,
        purpose: Purpose,
    ) -> str:
        random_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )

        code_entity = EmailCodeEntity.factory(
            user_uuid=user_uuid,
            purpose=purpose,
            code=random_code,
            expires_at=datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(minutes=5),
        )

        await self.email_code_repo.save(code_entity)

        return random_code
