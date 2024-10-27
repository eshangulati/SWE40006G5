# test_app.py

from app import app
import pytest

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_homepage(client):
    """Test the homepage returns a 200 status code"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to my website" in response.data

def test_add(client):
    """Test the add route works correctly"""
    response = client.post('/add', data={'num1': '10', 'num2': '5'})
    assert b"The sum of 10 and 5 is 15" in response.data
