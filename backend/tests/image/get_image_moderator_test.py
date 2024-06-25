import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, status

from src.image.service import ImageServices
from src.models import Image, User

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.mark.parametrize("image_id, moderator, expected_result, expected_exception", [
    (1, User(id=1, username="moderator1"), User(id=1, username="moderator1"), None),
    (2, None, None, HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie znaleziono moderatora dla danego zdjecia")),
])
def test_get_image_moderator(image_id, moderator, expected_result, expected_exception, mock_db):
    image_services = ImageServices()

    mock_image = MagicMock(spec=Image)
    mock_image.moderator = moderator

    image_services.get_single_image = MagicMock(return_value=mock_image)

    if expected_exception:
        with pytest.raises(type(expected_exception)) as exc_info:
            image_services.get_image_moderator(image_id, mock_db)
        assert exc_info.value.status_code == expected_exception.status_code
        assert exc_info.value.detail == expected_exception.detail
    else:
        result = image_services.get_image_moderator(image_id, mock_db)
        assert result.id == expected_result.id
        assert result.username == expected_result.username

    image_services.get_single_image.assert_called_once_with(image_id, mock_db)