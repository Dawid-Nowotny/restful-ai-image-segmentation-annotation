import pytest
from unittest.mock import MagicMock, ANY
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.image.service import ImageServices
from src.models import User, Comment, Image

@pytest.fixture
def image_services():
    return ImageServices()

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

def test_get_super_tag_author_by_image_success(image_services, mock_db):
    image_id = 1
    expected_username = "test_user"
    mock_query = MagicMock()
    mock_db.query.return_value.join.return_value.join.return_value.filter.return_value = mock_query
    mock_query.first.return_value = (expected_username,)

    result = image_services.get_super_tag_author_by_image(image_id, mock_db)

    mock_db.query.assert_called_once_with(User.username)
    
    mock_db.query.return_value.join.assert_called_once_with(Comment, ANY)
    mock_db.query.return_value.join.return_value.join.assert_called_once_with(Image, ANY)
    
    mock_db.query.return_value.join.return_value.join.return_value.filter.assert_called_once_with(ANY)
    
    mock_query.first.assert_called_once()
    
    assert result == expected_username

def test_get_super_tag_author_by_image_not_found(image_services, mock_db):
    image_id = 1
    mock_query = MagicMock()
    mock_db.query.return_value.join.return_value.join.return_value.filter.return_value = mock_query
    mock_query.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        image_services.get_super_tag_author_by_image(image_id, mock_db)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Brak autora supertagów"

def test_get_super_tag_author_by_image_db_error(image_services, mock_db):
    image_id = 1
    mock_db.query.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        image_services.get_super_tag_author_by_image(image_id, mock_db)

    mock_db.query.assert_called_once_with(User.username)