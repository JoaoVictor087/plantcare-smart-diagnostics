import importlib.util
from pathlib import Path

import pytest


ROOT_DIR = Path(__file__).resolve().parents[1]
APP_PATH = ROOT_DIR / "ai-api" / "app.py"


@pytest.fixture
def app_module():
    spec = importlib.util.spec_from_file_location("plantcare_app", APP_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def client(app_module):
    app_module.app.config.update({
        "TESTING": True
    })

    return app_module.app.test_client()