import sys
sys.path.append("../")
sys.path.append("../backend/")

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