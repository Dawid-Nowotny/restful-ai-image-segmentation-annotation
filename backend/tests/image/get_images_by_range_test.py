import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.image.service import ImageServices
from src.models import Image

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

@pytest.mark.parametrize("start_id, end_id, mock_images, expected_result, expected_exception", [
    (
        1, 3,
        [
            MagicMock(id=1, image="image1"),
            MagicMock(id=2, image="image2"),
            MagicMock(id=3, image="image3"),
            MagicMock(id=4, image="image4"),
        ],
        {
            1: "image1",
            2: "image2",
            3: "image3"
        },
        None
    ),
    (
        2, 4,
        [
            MagicMock(id=1, image="image1"),
            MagicMock(id=2, image="image2"),
            MagicMock(id=3, image="image3"),
            MagicMock(id=4, image="image4"),
        ],
        {
            2: "image2",
            3: "image3",
            4: "image4"
        },
        None
    ),
    (
        1, 5,
        [],
        None,
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie znaleziono obrazów w podanym zakresie")
    ),
])
def test_get_images_by_range(start_id, end_id, mock_images,expected_result, expected_exception, mock_db):
    image_services = ImageServices()

    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.all.return_value = mock_images

    def mock_get_images_in_range(images, start, end):
        return {img.id: img.image for img in images if start <= img.id <= end}
    
    with patch('src.image.service.get_images_in_range', side_effect=mock_get_images_in_range):
        if expected_exception:
            with pytest.raises(type(expected_exception)) as exc_info:
                image_services.get_images_by_range(start_id, end_id, mock_db)
            assert exc_info.value.status_code == expected_exception.status_code
            assert exc_info.value.detail == expected_exception.detail
        else:
            result = image_services.get_images_by_range(start_id, end_id, mock_db)
            assert result == expected_result

    mock_db.query.assert_called_once_with(Image)
    mock_query.all.assert_called_once()