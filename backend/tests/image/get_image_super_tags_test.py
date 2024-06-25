import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.image.service import ImageServices
from src.models import Comment

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

@pytest.mark.parametrize("image_id, mock_comments, expected_result, expected_exception", [
    (
        1,
        [
            MagicMock(
                user=MagicMock(username="user1"),
                tags=[MagicMock(tag="tag1"), MagicMock(tag="tag2")]
            )
        ],
        {"author": "user1", "tags": ["tag1", "tag2"]},
        None
    ),
    (
        2,
        [],
        None,
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie znaleziono supertagów dla danego zdjecia")
    ),
])
def test_get_image_super_tags(image_id, mock_comments, expected_result, expected_exception, mock_db):
    image_services = ImageServices()

    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = mock_comments

    if expected_exception:
        with pytest.raises(type(expected_exception)) as exc_info:
            image_services.get_image_super_tags(image_id, mock_db)
        assert exc_info.value.status_code == expected_exception.status_code
        assert exc_info.value.detail == expected_exception.detail
    else:
        result = image_services.get_image_super_tags(image_id, mock_db)
        assert result["author"] == expected_result["author"]
        assert [tag.tag for tag in result["tags"]] == expected_result["tags"]

    mock_db.query.assert_called_once_with(Comment)
    mock_query.filter.assert_called_once()
    filter_call = mock_query.filter.call_args[0]
    assert str(filter_call[0]) == str(Comment.image_id == image_id)
    assert str(filter_call[1]) == str(Comment.super_tag == True)
    mock_query.all.assert_called_once()