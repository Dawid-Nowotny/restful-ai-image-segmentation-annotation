import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, status

from src.user.service import UserServices
from src.models import User

@pytest.fixture
def user_services():
    return UserServices()

@pytest.fixture
def mock_db():
    return MagicMock()

def test_check_if_user_exists_username_taken(user_services, mock_db):
    username = "test_user"
    email = "test@example.com"
    mock_db.query.return_value.filter.return_value.first.side_effect = [User(username=username), None]

    with pytest.raises(HTTPException) as exc_info:
        user_services.check_if_user_exists(username, email, mock_db)
    
    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc_info.value.detail == "Nazwa użytkownika zajęta"

def test_check_if_user_exists_email_taken(user_services, mock_db):
    username = "test_user"
    email = "test@example.com"
    mock_db.query.return_value.filter.return_value.first.side_effect = [None, User(email=email)]

    with pytest.raises(HTTPException) as exc_info:
        user_services.check_if_user_exists(username, email, mock_db)
    
    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc_info.value.detail == "E-mail zajęty"

def test_check_if_user_exists_no_conflict(user_services, mock_db):
    username = "test_user"
    email = "test@example.com"
    mock_db.query.return_value.filter.return_value.first.side_effect = [None, None]

    result = user_services.check_if_user_exists(username, email, mock_db)

    assert result is None