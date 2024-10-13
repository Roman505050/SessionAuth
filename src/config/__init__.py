from config.settings import (
    PostgresSettings,
    RabbitMQSettings,
    SmtpSettings,
    SessionSettings,
    RedisSettings,
)


postgres_settings = PostgresSettings()  # type: ignore[call-arg]
rabbitmq_settings = RabbitMQSettings()  # type: ignore[call-arg]
smtp_settings = SmtpSettings()  # type: ignore[call-arg]
session_settings = SessionSettings()  # type: ignore[call-arg]
redis_settings = RedisSettings()  # type: ignore[call-arg]

__all__ = (
    "postgres_settings",
    "rabbitmq_settings",
    "smtp_settings",
    "session_settings",
    "redis_settings",
)
