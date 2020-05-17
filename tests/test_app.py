import pytest

def test_top(test_app, client):
    result = client.get('/top')
    assert result.status_code == 200

def test_index_without_login(test_app, client):
    result = client.get('/')
    assert result.status_code == 302