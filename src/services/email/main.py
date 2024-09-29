from loguru import logger
import asyncio
import aio_pika
import json

from infrastructure.services.email_service import EmailSenderService
from config import smtp_settings, rabbitmq_settings


async def process_message(
    queue_name, message: aio_pika.IncomingMessage, retry: int = 3
):
    try:
        async with message.process():
            body = json.loads(message.body)
            logger.info(f"Received new message: {body}")

            email_service = EmailSenderService(
                smtp_host=smtp_settings.HOST,
                smtp_port=smtp_settings.PORT,
                smtp_username=smtp_settings.USERNAME,
                smtp_password=smtp_settings.PASSWORD,
            )  # Note: SOLID principles are not followed here

            match queue_name:
                case "email_queue":
                    await email_service.send_email(
                        recipient=body["recipient"],
                        subject=body["subject"],
                        body=body["body"],
                        content_type=body["content_type"],
                    )

                case "email_verification_code_queue":
                    raise NotImplementedError(
                        "Verification code email not implemented"
                    )

            logger.success(f"Message processed successfully: {body}")
            await asyncio.sleep(1)
    except Exception as e:
        logger.error(f"Error processing message: {e}\n{body}")
        await asyncio.sleep(1)
        if retry > 0:
            await process_message(queue_name, message, retry - 1)
        else:
            logger.error("Max retries reached")


async def consume_queue(queue_name, channel):
    queue = await channel.declare_queue(queue_name, durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            await process_message(queue_name, message)


async def main():
    connection = await aio_pika.connect_robust(rabbitmq_settings.rabbitmq_url)
    logger.success("Connected to RabbitMQ")
    async with connection:
        channel = await connection.channel()

        queue1_task = asyncio.create_task(
            consume_queue("email_queue", channel)
        )
        logger.success("Consuming queue email_queue - Started")
        # queue2_task = asyncio.create_task(
        #     consume_queue("email_verification_code_queue", channel)
        # )
        # logger.success("Consuming queue email_verification_code_queue - Started")

        logger.success("Started consuming queues")
        await asyncio.gather(queue1_task)


if __name__ == "__main__":
    asyncio.run(main())
