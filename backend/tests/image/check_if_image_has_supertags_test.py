import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.image.service import CommentServices
from src.models import Comment

@pytest.fixture
def comment_services():
    return CommentServices()

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

@pytest.fixture
def mock_image():
    image = MagicMock()
    image.id = 1
    return image

def test_check_if_image_has_supertags_no_supertags(comment_services, mock_db, mock_image):
    mock_db.query.return_value.filter.return_value.all.return_value = []

    comment_services.check_if_image_has_supertags(mock_image, mock_db)

    mock_db.query.assert_called_once_with(Comment)
    mock_db.query.return_value.filter.assert_called_once()
    filter_args = mock_db.query.return_value.filter.call_args[0]
    assert len(filter_args) == 2
    assert str(filter_args[0]) == str(Comment.image_id == mock_image.id)
    assert str(filter_args[1]) == str(Comment.super_tag == True)

def test_check_if_image_has_supertags_with_supertags(comment_services, mock_db, mock_image):
    mock_db.query.return_value.filter.return_value.all.return_value = [MagicMock(), MagicMock()]  # Two mock comments

    with pytest.raises(HTTPException) as exc_info:
        comment_services.check_if_image_has_supertags(mock_image, mock_db)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "To zdjęcie już ma supertagi"

    mock_db.query.assert_called_once_with(Comment)
    mock_db.query.return_value.filter.assert_called_once()

def test_check_if_image_has_supertags_db_error(comment_services, mock_db, mock_image):
    mock_db.query.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        comment_services.check_if_image_has_supertags(mock_image, mock_db)

    mock_db.query.assert_called_once_with(Comment)