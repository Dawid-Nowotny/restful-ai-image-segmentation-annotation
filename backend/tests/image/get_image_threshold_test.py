import pytest
from unittest.mock import MagicMock, ANY
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.image.service import ImageServices
from src.models import Image

@pytest.fixture
def image_services():
    return ImageServices()

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

def test_get_image_threshold_success(image_services, mock_db):
    image_id = 1
    expected_threshold = 0.5
    mock_query = MagicMock()
    mock_db.query.return_value.filter.return_value = mock_query
    mock_query.first.return_value = (expected_threshold,)

    result = image_services.get_image_threshold(image_id, mock_db)

    mock_db.query.assert_called_once_with(Image.threshold)
    mock_db.query.return_value.filter.assert_called_once_with(ANY)
    mock_query.first.assert_called_once()
    assert result == expected_threshold

def test_get_image_threshold_not_found(image_services, mock_db):
    image_id = 1
    mock_query = MagicMock()
    mock_db.query.return_value.filter.return_value = mock_query
    mock_query.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        image_services.get_image_threshold(image_id, mock_db)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Brak progu detekcji"