import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from src.image.service import ImageServices
from src.models import Image

@pytest.fixture
def image_services():
    return ImageServices()

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

def test_get_images_number_with_images(image_services, mock_db):
    expected_count = 5
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.count.return_value = expected_count

    result = image_services.get_images_number(mock_db)

    mock_db.query.assert_called_once_with(Image)
    mock_query.count.assert_called_once()
    assert result == expected_count

def test_get_images_number_no_images(image_services, mock_db):
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.count.return_value = 0

    result = image_services.get_images_number(mock_db)

    mock_db.query.assert_called_once_with(Image)
    mock_query.count.assert_called_once()
    assert result == 0

def test_get_images_number_db_error(image_services, mock_db):
    mock_db.query.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        image_services.get_images_number(mock_db)

    mock_db.query.assert_called_once_with(Image)