import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
import pytest
import manage

@pytest.fixture
def test_app():
    application = manage.app
    application.config['TESTING'] = True
    yield application

@pytest.fixture
def client(test_app):
    return test_app.test_client()