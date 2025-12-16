import json
import pytest

from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as c:
        yield c


def test_health(client):
    r = client.get('/health')
    assert r.status_code == 200
    j = r.get_json()
    assert 'status' in j


def test_chat_rule_based(client):
    # Ensure chat POST returns a response using rule-based mode (works without OPENAI key)
    payload = {
        'message': 'Tell me about brand strategy',
        'session_id': 'test-session',
        'history': []
    }
    r = client.post('/api/chat', data=json.dumps(payload), content_type='application/json')
    assert r.status_code == 200
    j = r.get_json()
    assert 'response' in j
    assert isinstance(j['response'], str)
