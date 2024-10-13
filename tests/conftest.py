import pytest
from tests.fixtures.database_fixture import setup_database
from tests.fixtures.clients import ac

pytest_plugins = [
    "fixtures.database_fixture",
    "fixtures.redis_fixture",
    "fixtures.clients",
]
