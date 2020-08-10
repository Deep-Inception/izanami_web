def test_top(client):
    result = client.get('/top')
    assert result.status_code == 200

def test_index_without_login(client):
    result = client.get('/')
    assert result.status_code == 200