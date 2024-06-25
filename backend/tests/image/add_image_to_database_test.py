import pytest
from unittest.mock import MagicMock
from datetime import date
from fastapi import UploadFile
import json
from PIL import Image as PILImage

from src.image.service import ImageServices
from src.models import Image

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def mock_segmentation_services():
    return MagicMock()

@pytest.fixture
def image_services():
    return ImageServices()

@pytest.mark.asyncio
async def test_add_image_to_database(mock_db, mock_segmentation_services):
    # Arrange
    db = mock_db
    segmented_image = PILImage.new('RGB', (100, 100))
    segmentation_data = '{"boxes": [[10, 20, 30, 40]], "classes": ["A"]}'
    image_data = MagicMock()
    image_data.threshold = 0.5
    uploader_id = 1
    mock_upload_file = MagicMock(spec=UploadFile)
    type(mock_upload_file).file = MagicMock()

    mock_upload_file.file.read.return_value = b'binary_data'

    image_services = ImageServices()
    image_services.rename_file = MagicMock()
    image_services.validate_file_size_type = MagicMock()
    image_services.validate_file_size_type.return_value = None
    image_services.get_current_user = MagicMock()
    image_services.get_current_user.id = uploader_id

    mock_segmentation_services.get_prediction = MagicMock()
    mock_segmentation_services.get_prediction.return_value = ([], [[10, 20, 30, 40]], ["A"])
    mock_segmentation_services.get_segmented_image = MagicMock()
    mock_segmentation_services.get_segmented_image.return_value = segmented_image
    convert_to_json = MagicMock()
    convert_to_json.return_value = segmentation_data

    await image_services.add_image_to_database(db, segmented_image, segmentation_data, image_data, uploader_id, mock_upload_file)

    db.add.assert_called_once()
    assert isinstance(db.add.call_args[0][0], Image)
    assert db.add.call_args[0][0].image == b'binary_data'
    assert db.add.call_args[0][0].coordinates_classes == json.loads(segmentation_data)
    assert db.add.call_args[0][0].threshold == image_data.threshold
    assert db.add.call_args[0][0].upload_date == date.today()
    assert db.add.call_args[0][0].uploader_id == uploader_id
    assert db.add.call_args[0][0].moderator_id is None
    db.commit.assert_called_once()
    db.refresh.assert_called_once()