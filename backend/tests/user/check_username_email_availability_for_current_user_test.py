import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.user.service import UserServices
from src.user.schemas import UserUpdateSchema
from src.models import User

@pytest.fixture
def user_services():
    return UserServices()

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

@pytest.fixture
def current_user():
    user = MagicMock(spec=User)
    user.id = 1
    user.username = "current_user"
    user.email = "current_user@example.com"
    user.verify_password.return_value = True
    return user

@pytest.fixture
def user_data_update():
    return UserUpdateSchema(
        username="new_user",
        email="new_user@example.com",
        password="new_password",
        old_password="old_password"
    )

def test_no_changes_made(user_services, mock_db, current_user):
    user_data_update = UserUpdateSchema(
        username="current_user",
        email="current_user@example.com",
        password=None,
        old_password="old_password"
    )

    with pytest.raises(HTTPException) as exc_info:
        user_services.check_username_email_availability_for_current_user(user_data_update, current_user, mock_db)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Nie wprowadzono żadnych zmian"

def test_username_taken(user_services, mock_db, current_user, user_data_update):
    mock_db.query.return_value.filter.return_value.first.return_value = MagicMock(spec=User)

    with pytest.raises(HTTPException) as exc_info:
        user_services.check_username_email_availability_for_current_user(user_data_update, current_user, mock_db)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Nazwa użytkownika zajęta"

def test_email_taken(user_services, mock_db, current_user, user_data_update):
    mock_query = MagicMock()
    mock_filter = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_filter

    mock_filter.first.side_effect = [None, MagicMock(spec=User)]

    with pytest.raises(HTTPException) as exc_info:
        user_services.check_username_email_availability_for_current_user(user_data_update, current_user, mock_db)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "E-mail zajęty"

    assert mock_db.query.call_count == 2
    assert mock_query.filter.call_count == 2
    assert mock_filter.first.call_count == 2

def test_valid_update(user_services, mock_db, current_user, user_data_update):
    mock_db.query.return_value.filter.return_value.first.return_value = None

    user_services.check_username_email_availability_for_current_user(user_data_update, current_user, mock_db)

    mock_db.query.assert_any_call(User)
    assert mock_db.query.return_value.filter.call_count == 2
    assert mock_db.query.return_value.filter.return_value.first.call_count == 2