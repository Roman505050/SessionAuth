from redis.asyncio import Redis
import json
import datetime

from application.code.enums.email_code_type import (
    EmailCodeType,
    EMAIL_CODE_FORMATS,
)
from application.code.exceptions.code_not_found import (
    EmailCodeNotFoundException,
)
from application.code.ports.repositories.email_code import IEmailCodeRepository
from domain.code.entities.email_code import EmailCodeEntity


class EmailCodeRepository(IEmailCodeRepository):

    def __init__(self, redis_client: Redis):
        self._redis_client = redis_client

    @staticmethod
    def _from_entity(entity: EmailCodeEntity):
        return {
            "code": entity.code,
            "created_at": str(entity.created_at),
            "expires_at": str(entity.expires_at),
            "attempts": entity.attempts,
            "max_attempts": entity.max_attempts,
        }

    @staticmethod
    def _to_entity(data: dict):
        return EmailCodeEntity(
            code=data["code"],
            created_at=datetime.datetime.fromisoformat(data["created_at"]),
            expires_at=datetime.datetime.fromisoformat(data["expires_at"]),
            attempts=data["attempts"],
            max_attempts=data["max_attempts"],
        )

    async def save(
        self, code_type: EmailCodeType, code: EmailCodeEntity, **kwargs
    ):
        key_format = EMAIL_CODE_FORMATS[code_type]
        key = key_format.build_key(**kwargs)

        ttl = int((code.expires_at - code.created_at).total_seconds())

        await self._redis_client.set(
            key, json.dumps(self._from_entity(code)), ex=ttl
        )

    async def get(self, code_type: EmailCodeType, **kwargs):
        key_format = EMAIL_CODE_FORMATS[code_type]
        key = key_format.build_key(**kwargs)

        data = await self._redis_client.get(key)
        if not data:
            raise EmailCodeNotFoundException("Email code not found")

        return self._to_entity(json.loads(data))

    async def delete(self, code_type: EmailCodeType, **kwargs):
        key_format = EMAIL_CODE_FORMATS[code_type]
        key = key_format.build_key(**kwargs)

        await self._redis_client.delete(key)

    async def update(
        self, code_type: EmailCodeType, code: EmailCodeEntity, **kwargs
    ):
        key_format = EMAIL_CODE_FORMATS[code_type]
        key = key_format.build_key(**kwargs)

        if not await self._redis_client.exists(key):
            raise EmailCodeNotFoundException("Email code not found")

        now = datetime.datetime.now(datetime.timezone.utc)
        ttl = int((code.expires_at - now).total_seconds())

        if ttl < 0:
            raise EmailCodeNotFoundException("Email code not found")

        await self._redis_client.set(
            key, json.dumps(self._from_entity(code)), ex=ttl
        )
