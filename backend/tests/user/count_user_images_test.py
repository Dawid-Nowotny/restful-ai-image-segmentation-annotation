import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.user.service import UserServices
from src.models import User, Image

@pytest.fixture
def user_services():
    return UserServices()

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

@pytest.fixture
def mock_user():
    user = MagicMock(spec=User)
    user.id = 1
    return user

def test_count_user_images_with_images(user_services, mock_db, mock_user):
    expected_count = 5
    mock_db.query.return_value.filter.return_value.scalar.return_value = expected_count

    result = user_services.count_user_images(mock_user, mock_db)

    assert result == expected_count
    mock_db.query.assert_called_once()
    mock_db.query.return_value.filter.assert_called_once()
    mock_db.query.return_value.filter.return_value.scalar.assert_called_once()

    query_arg = mock_db.query.call_args[0][0]
    assert isinstance(query_arg, func.count().__class__)
    
    filter_arg = mock_db.query.return_value.filter.call_args[0][0]
    assert str(filter_arg) == str(Image.uploader_id == mock_user.id)

def test_count_user_images_no_images(user_services, mock_db, mock_user):
    mock_db.query.return_value.filter.return_value.scalar.return_value = 0

    result = user_services.count_user_images(mock_user, mock_db)

    assert result == 0
    mock_db.query.assert_called_once()
    mock_db.query.return_value.filter.assert_called_once()
    mock_db.query.return_value.filter.return_value.scalar.assert_called_once()

def test_count_user_images_db_error(user_services, mock_db, mock_user):
    mock_db.query.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        user_services.count_user_images(mock_user, mock_db)

    mock_db.query.assert_called_once()