from pydantic_settings import BaseSettings, SettingsConfigDict


class SessionSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_prefix="SESSION_"
    )

    EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # 1 week
    SECURE: bool = True
    MAX_SESSIONS: int = 5


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_prefix="POSTGRES_"
    )

    USER: str
    PASSWORD: str
    HOST: str
    DB: str

    @property
    def db_uri_asyncpg(self):
        return (
            f"postgresql+asyncpg://{self.USER}:"
            f"{self.PASSWORD}@{self.HOST}:"
            f"5432/{self.DB}"
        )


class SmtpSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_prefix="SMTP_"
    )
    HOST: str
    PORT: int
    USERNAME: str
    PASSWORD: str


class RabbitMQSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_prefix="RABBITMQ_"
    )
    USER: str
    PASS: str
    HOST: str
    PORT: int
    VHOST: str

    @property
    def rabbitmq_url(self):
        return (
            f"amqp://{self.USER}:"
            f"{self.PASS}@{self.HOST}:"
            f"{self.PORT}/{self.VHOST}"
        )


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_prefix="REDIS_"
    )
    HOST: str
    PORT: int
    USERNAME: str
    PASSWORD: str
    DB: int

    @property
    def redis_url(self):
        return (
            f"redis://{self.USERNAME}:{self.PASSWORD}@"
            f"{self.HOST}:{self.PORT}/{self.DB}"
        )
