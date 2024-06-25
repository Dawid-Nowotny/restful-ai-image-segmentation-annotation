import pytest
from unittest.mock import MagicMock, ANY
from fastapi import HTTPException, status
from src.user.service import UserServices
from src.models import User

@pytest.fixture
def user_services():
    return UserServices()

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def mock_user():
    user = MagicMock(spec=User)
    user.id = 1
    user.username = "test_user"
    user.email = "test@example.com"
    user.verify_password = MagicMock(return_value=True)
    return user

def test_authenticate_user_not_found(user_services, mock_db):
    username = "non_existent_user"
    password = "password123"
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        user_services.authenticate_user(username, password, mock_db)
    
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Niewłaściwa nazwa użytkownika"

def test_authenticate_user_wrong_password(user_services, mock_db, mock_user):
    username = "test_user"
    password = "wrong_password"
    mock_user.verify_password.return_value = False
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    with pytest.raises(HTTPException) as exc_info:
        user_services.authenticate_user(username, password, mock_db)
    
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Niepoprawne hasło"

def test_authenticate_user_with_email(user_services, mock_db, mock_user):
    username = "test@example.com"
    password = "correct_password"
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    authenticated_user = user_services.authenticate_user(username, password, mock_db)

    assert authenticated_user == mock_user
    mock_db.query.return_value.filter.assert_called_with(ANY)

def test_authenticate_user_with_username(user_services, mock_db, mock_user):
    username = "test_user"
    password = "correct_password"
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    authenticated_user = user_services.authenticate_user(username, password, mock_db)

    assert authenticated_user == mock_user
    mock_db.query.return_value.filter.assert_called_with(ANY)

def test_authenticate_user_success(user_services, mock_db, mock_user):
    # Arrange
    username = "test_user"
    password = "correct_password"
    mock_user.verify_password.return_value = True
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    authenticated_user = user_services.authenticate_user(username, password, mock_db)

    assert authenticated_user == mock_user