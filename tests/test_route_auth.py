from unittest.mock import MagicMock

from src.database.models import User


def test_create_user(client, user, monkeypatch):
    """
    The test_create_user function tests the /api/auth/signup endpoint.
    It does so by making a POST request to that endpoint with a JSON payload containing the user's email and password.
    The test then asserts that the response status code is 201, which indicates success, and also checks that 
    the returned data contains an id key.
    
    :param client: Make requests to the api
    :param user: Pass the user data to the test function
    :param monkeypatch: Mock the send_email function
    :return: The response
    :doc-author: Trelent
    """
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post(
        "/api/auth/signup",
        json=user,
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["user"]["email"] == user.get("email")
    assert "id" in data["user"]


def test_repeat_create_user(client, user):
    """
    The test_repeat_create_user function tests that a user cannot be created twice.
        It does this by creating a user, then attempting to create the same user again.
        The second attempt should fail with an HTTP 409 status code and an error message.
    
    :param client: Make requests to the flask application
    :param user: Pass in the user object to the test function
    :return: A 409 status code
    :doc-author: Trelent
    """
    response = client.post(
        "/api/auth/signup",
        json=user,
    )
    assert response.status_code == 409, response.text
    data = response.json()
    assert data["detail"] == "Account already exists"


def test_login_user_not_confirmed(client, user):
    """
    The test_login_user_not_confirmed function tests that a user cannot login if they have not confirmed their email address.
        The test_login_user_not_confirmed function takes two arguments: client and user.
        The client argument is the Flask test client, which allows us to make requests to our application without running an actual server.
        The user argument is a fixture that returns a dictionary of data for creating a new User object in the database.
    
    :param client: Make requests to the application
    :param user: Create a user in the database
    :return: An error message if the user is not confirmed
    :doc-author: Trelent
    """
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Email not confirmed"


def test_login_user(client, session, user):
    """
    The test_login_user function tests the login functionality of the application.
    It first creates a user and then logs in with that user's credentials.
    
    
    :param client: Make requests to the application
    :param session: Access the database
    :param user: Pass in the user data from the fixture
    :return: A token_type of &quot;bearer&quot;
    :doc-author: Trelent
    """
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, user):
    """
    The test_login_wrong_password function tests the login endpoint with a wrong password.
    It should return a 401 status code and an error message.
    
    :param client: Make a request to the server
    :param user: Create a user in the database
    :return: The response
    :doc-author: Trelent
    """
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": 'password'},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid password"


def test_login_wrong_email(client, user):
    """
    The test_login_wrong_email function tests the login endpoint with a wrong email.
    It should return a 401 status code and an error message.
    
    :param client: Make requests to the application
    :param user: Create a user in the database
    :return: 401 status code
    :doc-author: Trelent
    """
    response = client.post(
        "/api/auth/login",
        data={"username": 'email', "password": user.get('password')},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid email"
    
def test_request_email(client, user, monkeypatch):
    """
    The test_request_email function tests the /api/auth/request_email endpoint.
    It does this by mocking out the send_email function, which is used in that endpoint.
    The test then makes a POST request to that endpoint with some JSON data and asserts that it returns a 200 status code.
    
    :param client: Make a request to the api
    :param user: Create a user object that is used to test the request_email function
    :param monkeypatch: Mock the send_email function
    :return: A 200 status code
    :doc-author: Trelent
    """
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post("/api/auth/request_email", json=user)
    assert response.status_code == 200, response.text