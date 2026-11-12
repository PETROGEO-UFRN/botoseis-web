import os

import pytest
from dotenv import load_dotenv, find_dotenv

from server.app.create_app import create_app
from server.app.tests.httpClient import GenericHttpClient

dotenv_path = find_dotenv()
result = load_dotenv(dotenv_path, override=True)

# *** Base URL of the API under test
API_URL = os.getenv("API_URL", "http://localhost:8080")

# *** App instance for direct database access (reset and seeding), not for requests.
# *** The server at API_URL must use the same test database.
_app = create_app("TEST")


def pytest_configure():
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
