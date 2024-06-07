import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, status

from src.image.service import ImageServices

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.mark.parametrize("image_id, expected_result", [
    (1, MagicMock()),
    (2, None)
])
def test_get_single_image(image_id, expected_result, mock_db):
    image_service = ImageServices()

    mock_db.query().filter().first.return_value = expected_result

    if expected_result is None:
        with pytest.raises(HTTPException) as exc_info:
            image_service.get_single_image(image_id, mock_db)
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc_info.value.detail == "Nie znaleziono obrazu"
    else:
        result = image_service.get_single_image(image_id, mock_db)
        assert result == expected_result

    mock_db.query().filter().first.assert_called_once_with()