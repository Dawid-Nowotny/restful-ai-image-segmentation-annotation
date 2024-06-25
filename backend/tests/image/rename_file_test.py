import pytest
from unittest.mock import MagicMock
from fastapi import UploadFile
import os
import uuid

from src.image.service import ImageServices

@pytest.fixture
def image_services():
    return ImageServices()

@pytest.mark.asyncio
async def test_rename_file(image_services):
    original_filename = "test_image.jpg"
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = original_filename

    image_services.rename_file(mock_file)

    assert mock_file.filename is not None
    assert os.path.splitext(mock_file.filename)[1] in [".jpg", ".jpeg", ".png", ".gif"]
    assert len(mock_file.filename) > len(original_filename)
    assert uuid.UUID(mock_file.filename.split('.')[0])
