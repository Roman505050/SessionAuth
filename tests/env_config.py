from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_USER = os.getenv("TEST_POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("TEST_POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("TEST_POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("TEST_POSTGRES_PORT", "5432")
POSTGRES_NAME = os.getenv("TEST_POSTGRES_NAME", "postgres")

REDIS_HOST = os.getenv("TEST_REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("TEST_REDIS_PORT", "6379")
REDIS_USERNAME = os.getenv("TEST_REDIS_USERNAME", "admin")
REDIS_PASSWORD = os.getenv("TEST_REDIS_PASSWORD", "password")
REDIS_DB = os.getenv("TEST_REDIS_DB", "0")

DATABASE_URL_TEST = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"
)
REDIS_URL_TEST = (
    f"redis://{REDIS_USERNAME}:{REDIS_PASSWORD}@"
    f"{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
)
