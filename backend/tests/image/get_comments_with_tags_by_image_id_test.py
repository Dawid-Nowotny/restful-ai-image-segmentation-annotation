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
def mock_comment():
    comment = MagicMock(spec=Comment)
    comment.id = 1
    comment.user = MagicMock()
    comment.user.username = "test_user"
    comment.tags = [MagicMock(tag="tag1"), MagicMock(tag="tag2")]
    return comment

def test_get_comments_with_tags_by_image_id_success(comment_services, mock_db, mock_comment):
    image_id = 1
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_comment]

    result = comment_services.get_comments_with_tags_by_image_id(image_id, mock_db)

    mock_db.query.assert_called_once_with(Comment)
    assert str(mock_db.query.return_value.filter.call_args[0][0]) == str(Comment.image_id == image_id)
    
    assert len(result) == 1
    assert result[0]["comment_id"] == 1
    assert result[0]["username"] == "test_user"
    assert result[0]["tags"] == ["tag1", "tag2"]

def test_get_comments_with_tags_by_image_id_not_found(comment_services, mock_db):
    image_id = 1
    mock_db.query.return_value.filter.return_value.all.return_value = []

    with pytest.raises(HTTPException) as exc_info:
        comment_services.get_comments_with_tags_by_image_id(image_id, mock_db)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Nie znaleziono komentarzy dla danego obrazu"

    mock_db.query.assert_called_once_with(Comment)
    assert str(mock_db.query.return_value.filter.call_args[0][0]) == str(Comment.image_id == image_id)

def test_get_comments_with_tags_by_image_id_db_error(comment_services, mock_db):
    image_id = 1
    mock_db.query.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        comment_services.get_comments_with_tags_by_image_id(image_id, mock_db)

    mock_db.query.assert_called_once_with(Comment)