from abc import ABC, abstractmethod


class IEmailSender(ABC):
    @abstractmethod
    async def send_email(self, email: str, subject: str, body: str) -> None:
        pass
