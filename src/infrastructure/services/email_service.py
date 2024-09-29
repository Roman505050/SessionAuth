import aio_pika
from aiosmtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Literal
from uuid import UUID
import json

from domain.code.enums import Purpose
from application.user.interfaces.services.email import IEmailService


class RabbitMQEmailService(IEmailService):
    def __init__(self, rabbitmq_url: str):
        self.rabbitmq_url = rabbitmq_url

    async def send_email(
        self,
        email: str,
        subject: str,
        body: str,
        content_type: Literal["plain", "html"] = "plain",
    ) -> None:
        data = {
            "recipient": email,
            "subject": subject,
            "body": body,
            "content_type": content_type,
        }
        queue_name = "email_queue"

        async with await aio_pika.connect_robust(
            self.rabbitmq_url
        ) as connection:
            async with connection.channel() as channel:
                await channel.declare_queue(queue_name, durable=True)
                await channel.default_exchange.publish(
                    aio_pika.Message(
                        body=json.dumps(data).encode(), delivery_mode=2
                    ),
                    routing_key=queue_name,
                )

    async def send_verification_code(
        self,
        user_uuid: UUID,
        email: str,
        purpose: Purpose,
    ) -> None:
        data = {
            "user_uuid": str(user_uuid),
            "recipient": email,
            "purpose": purpose.value,
        }
        queue_name = "email_verification_code_queue"

        async with await aio_pika.connect_robust(
            self.rabbitmq_url
        ) as connection:
            async with connection.channel() as channel:
                await channel.declare_queue(queue_name, durable=True)
                await channel.default_exchange.publish(
                    aio_pika.Message(
                        body=json.dumps(data).encode(), delivery_mode=2
                    ),
                    routing_key=queue_name,
                )


class EmailSenderService:
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        smtp_username: str,
        smtp_password: str,
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password

    async def send_email(
        self,
        recipient: str,
        subject: str,
        body: str,
        content_type: Literal["plain", "html"] = "plain",
    ):
        message = MIMEMultipart()
        message["From"] = self.smtp_username
        message["To"] = recipient
        message["Subject"] = subject
        message.attach(MIMEText(body, content_type))

        async with SMTP(
            hostname=self.smtp_host,
            port=self.smtp_port,
            username=self.smtp_username,
            password=self.smtp_password,
        ) as smtp:
            await smtp.send_message(message)
