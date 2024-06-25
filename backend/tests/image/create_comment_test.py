import pytest
from unittest.mock import MagicMock
from datetime import date
from sqlalchemy.orm import Session
from src.image.service import CommentServices
from src.models import Comment

@pytest.fixture
def comment_services():
    return CommentServices()

@pytest.fixture
def mock_db():
    db = MagicMock(spec=Session)
    db.add = MagicMock()
    db.commit = MagicMock()
    db.refresh = MagicMock()
    return db

@pytest.fixture
def mock_user():
    user = MagicMock()
    user.id = 1
    return user

@pytest.fixture
def mock_comment_data():
    comment_data = MagicMock()
    comment_data.super_tag = True
    return comment_data

@pytest.mark.asyncio
async def test_create_comment(comment_services, mock_db, mock_user, mock_comment_data):
    image_id = 1
    tags = [MagicMock(), MagicMock()]

    await comment_services.create_comment(image_id, mock_user, mock_comment_data, tags, mock_db)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    called_with = mock_db.add.call_args[0][0]
    assert isinstance(called_with, Comment)
    assert called_with.super_tag == mock_comment_data.super_tag
    assert called_with.comment_date == date.today()
    assert called_with.image_id == image_id
    assert called_with.user_id == mock_user.id
    assert called_with.tags == tags

@pytest.mark.asyncio
async def test_create_comment_db_error(comment_services, mock_db, mock_user, mock_comment_data):
    image_id = 1
    tags = [MagicMock(), MagicMock()]
    mock_db.commit.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        await comment_services.create_comment(image_id, mock_user, mock_comment_data, tags, mock_db)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_not_called()

@pytest.mark.asyncio
async def test_create_comment_no_tags(comment_services, mock_db, mock_user, mock_comment_data):
    image_id = 1
    tags = []

    await comment_services.create_comment(image_id, mock_user, mock_comment_data, tags, mock_db)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    called_with = mock_db.add.call_args[0][0]
    assert isinstance(called_with, Comment)
    assert called_with.tags == []