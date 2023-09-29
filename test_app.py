# Bouthasone Rajasombat
# 11552013
import pytest
import json
from app import app

@pytest.fixture
def client():
    # Set app in testing mode
    app.config['TESTING'] = True
    with app.test_client() as client:
        # This will provide a test client to use in your tests
        yield client

def test_auth(client):
    # Make a POST request to the /auth endpoint
    response = client.post('/auth')
    # Assert that the status code of the response is 200
    assert response.status_code == 200
    # Load the response data as JSON
    data = json.loads(response.data)
    # Assert that there is a 'token' key in the response data
    assert 'token' in data

def test_jwks(client):
    # Make a GET request to the /.well-known/jwks.json endpoint
    response = client.get('/.well-known/jwks.json')
    # Assert that the status code of the response is 200
    assert response.status_code == 200
    # Load the response data as JSON
    data = json.loads(response.data)
    # Assert that there is a 'keys' key in the response data
    assert 'keys' in data


