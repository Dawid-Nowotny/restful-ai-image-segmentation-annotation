import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.user.service import UserServices
from src.models import User

def test_get_user_by_username_success():
    mock_db = MagicMock(spec=Session)
    mock_user = MagicMock(spec=User)
    mock_user.username = "test_user"
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    result = UserServices.get_user_by_username("test_user", mock_db)

    assert result == mock_user
    mock_db.query.assert_called_once_with(User)
    assert str(mock_db.query.return_value.filter.call_args[0][0]) == str(User.username == "test_user")
    mock_db.query.return_value.filter.return_value.first.assert_called_once()

def test_get_user_by_username_not_found():
    mock_db = MagicMock(spec=Session)
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        UserServices.get_user_by_username("non_existent_user", mock_db)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Nie znaleziono użytkownika"
    mock_db.query.assert_called_once_with(User)
    assert str(mock_db.query.return_value.filter.call_args[0][0]) == str(User.username == "non_existent_user")
    mock_db.query.return_value.filter.return_value.first.assert_called_once()

def test_get_user_by_username_db_error():
    mock_db = MagicMock(spec=Session)
    mock_db.query.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        UserServices.get_user_by_username("test_user", mock_db)

    mock_db.query.assert_called_once_with(User)