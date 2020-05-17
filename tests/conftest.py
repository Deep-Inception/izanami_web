import sys
sys.path.append("../")
sys.path.append("../app/")

import pytest
from app import run

@pytest.fixture
def test_app():
    application = run.app
    application.config['TESTING'] = True
    yield application

@pytest.fixture
def client(test_app):
    return test_app.test_client()