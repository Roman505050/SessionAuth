from application.code.ports.services.email import IEmailSender


class MockEmailSender(IEmailSender):
    async def send_email(self, email: str, subject: str, body: str) -> None:
        print(
            f"Mocked email sent to {email} with subject {subject} and body {body}"
        )
