import pytest

from flask import session


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post(
        '/authentication/register',
        data={'user_name': 'david123', 'password': 'GoldenGoose175!'}
    )
    assert response.headers['Location'] == '/authentication/login'

def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Checks that logging out correctly clears session.
        auth.logout()
        assert 'user_id' not in session

def test_index(client):
    # Checks that the home page is retrieved correctly
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to our assignment website!' in response.data
