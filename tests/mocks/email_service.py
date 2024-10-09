from uuid import UUID
from domain.code.enums import Purpose
from application.user.interfaces.services.email import IEmailService

class MockEmailService(IEmailService):
    async def send_email(self, email: str, subject: str, body: str) -> None:
        print(f"Mocked email sent to {email} with subject {subject}")

    async def send_verification_code(
        self, user_uuid: UUID, email: str, purpose: Purpose
    ) -> None:
        print(f"Mocked verification code sent to {email} for {purpose}")
