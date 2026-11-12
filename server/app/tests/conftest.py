import os

import pytest
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine, text

from server.app.config.database import get_db_uri
from server.app.tests.httpClient import GenericHttpClient

dotenv_path = find_dotenv()
result = load_dotenv(dotenv_path, override=True)

# *** Base URL of the API under test
API_URL = os.getenv("API_URL", "http://localhost:8080")

# *** Database of the API under test, used only to reset it between test classes
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL") or get_db_uri("TEST")

# *** Schema version tables are kept, so the migrated schema survives a reset
PRESERVED_TABLES = ("alembic_version",)

database_engine = create_engine(TEST_DATABASE_URL)


def reset_database():
    """Empty every table of the public schema and restart its id sequences."""
    with database_engine.begin() as connection:
        tables = [
            row[0] for row in connection.execute(
                text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
            )
            if row[0] not in PRESERVED_TABLES
        ]
        if tables:
            table_list = ", ".join(f'"{table}"' for table in tables)
            connection.execute(
                text(f"TRUNCATE TABLE {table_list} RESTART IDENTITY CASCADE")
            )


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "file_routes: tests for file routes (su-file, su-file-path, helper-file)",
    )
    # *** Created at configure time: test classes read `pytest.client` on import
    pytest.client = GenericHttpClient(API_URL)


def pytest_unconfigure():
    client = getattr(pytest, "client", None)
    if isinstance(client, GenericHttpClient):
        client.close()


@pytest.fixture(scope="session")
def client():
    yield pytest.client


def pytest_collection_modifyitems(items):
    CLASS_ORDER = [
        "TestUserRouter",
        "TestSessionRouter",

        "TestProjectRouter",
        "TestLineRouter",
        "TestWorkflowRouter",

        "TestProgramGroupRouter",
        "TestProgramRouter",
        "TestParameterRouter",

        "TestCommandRouter",
        "TestSuFileRouter",
        "TestSuFilePathRouter",

        "TestSubPathTables",
        "TestSubPathModels",
    ]
    class_mapping = {}
    sorted_items = []

    for item in items:
        if hasattr(item, 'cls') and item.cls:
            class_mapping[item] = item.cls.__name__

    for class_ in CLASS_ORDER:
        current_class_items = []

        for item in items:
            if class_mapping[item] == class_:
                current_class_items.append(item)

        sorted_items += current_class_items

    items[:] = sorted_items
