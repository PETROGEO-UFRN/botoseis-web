import pytest
from dotenv import load_dotenv, find_dotenv

from server.app.create_app import create_app

dotenv_path = find_dotenv()
result = load_dotenv(dotenv_path, override=True)
_app = create_app("TEST")


def _client():
    return _app.test_client()


def pytest_configure():
    pytest.client = _client()


def pytest_collection_modifyitems(items):
    CLASS_ORDER = [
        "TestUserRouter",
        "TestProjectRouter",
        "TestLineRouter",
        "TestWorkflowRouter",
        "TestProgramGroupRouter",
        "TestProgramRouter",
        "TestParameterRouter",
        "TestCommandRouter",
        "TestSuFileRouter",
        "TestSuFilePathRouter",
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
