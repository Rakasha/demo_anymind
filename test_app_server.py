import pytest
import app_server


@pytest.fixture
def client():
    app_server.app.config['TESTING'] = True
    client = app_server.app.test_client()
    yield client


def test_root_url(client):
    r = client.get('/')
    assert r.data == b'hello'
    assert r.status_code == 200

