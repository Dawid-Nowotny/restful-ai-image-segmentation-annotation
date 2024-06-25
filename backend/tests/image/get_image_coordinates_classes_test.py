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

def test_get_image_coordinates_classes_success(image_services, mock_db):
    image_id = 1
    expected_coordinates_classes = {"x": 10, "y": 20, "class": "A"}
    mock_query = MagicMock()
    mock_db.query.return_value.filter.return_value = mock_query
    mock_query.first.return_value = (expected_coordinates_classes,)

    result = image_services.get_image_coordinates_classes(image_id, mock_db)

    mock_db.query.assert_called_once_with(Image.coordinates_classes)
    mock_db.query.return_value.filter.assert_called_once_with(ANY)
    mock_query.first.assert_called_once()
    assert result == expected_coordinates_classes

def test_get_image_coordinates_classes_not_found(image_services, mock_db):
    image_id = 1
    mock_query = MagicMock()
    mock_db.query.return_value.filter.return_value = mock_query
    mock_query.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        image_services.get_image_coordinates_classes(image_id, mock_db)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Brak koordynatów klas"