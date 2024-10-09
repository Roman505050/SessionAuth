import pytest
from tests.fixtures.database import setup_database
from tests.fixtures.clients import ac

pytest_plugins = [
    "fixtures.database",
    "fixtures.clients",
]