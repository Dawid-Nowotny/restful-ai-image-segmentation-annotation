import pytest
from unittest.mock import MagicMock
from src.image.service import CommentServices
from src.models import Tag

@pytest.fixture
def comment_services():
    return CommentServices()

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.mark.asyncio
async def test_create_tag(comment_services, mock_db):
    tag_name = "TestTag"
    expected_tag = Tag(id=1, tag=tag_name)

    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = lambda tag: setattr(tag, "id", 1)

    created_tag = await comment_services.create_tag(tag_name, mock_db)

    assert isinstance(created_tag, Tag)
    assert created_tag.id == expected_tag.id
    assert created_tag.tag == expected_tag.tag
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()