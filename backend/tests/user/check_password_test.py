import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, status

from src.user.service import UserServices, User

@pytest.fixture
def user_services():
    return UserServices()

@pytest.fixture
def mock_user():
    user = MagicMock(spec=User)
    user.id = 1
    user.username = "test_user"
    user.email = "test@example.com"
    return user

def test_check_password_success(user_services, mock_user):
    password = "correct_password"
    mock_user.verify_password.return_value = True

    try:
        user_services.check_password(mock_user, password)
    except HTTPException:
        pytest.fail("HTTPException was raised unexpectedly")

    mock_user.verify_password.assert_called_with(password)

def test_check_password_failure(user_services, mock_user):
    password = "wrong_password"
    mock_user.verify_password.return_value = False

    with pytest.raises(HTTPException) as exc_info:
        user_services.check_password(mock_user, password)
    
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Niepoprawne hasło"
    mock_user.verify_password.assert_called_with(password)