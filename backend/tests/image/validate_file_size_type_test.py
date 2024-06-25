import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, status
from io import BytesIO
import filetype

from src.image.service import ImageServices

@pytest.fixture
def image_services():
    return ImageServices()

@pytest.mark.asyncio
async def test_validate_file_size_type(image_services):
    valid_file = MagicMock()
    valid_file.file = BytesIO(b'dummy_content')
    valid_file.content_type = "image/jpeg"

    invalid_file_type = MagicMock()
    invalid_file_type.file = BytesIO(b'dummy_content')
    invalid_file_type.content_type = "application/pdf"

    oversized_file = MagicMock()
    oversized_file.file = BytesIO(b'dummy_content' * 1024 * 1024 * 6)  # 6 MB file
    oversized_file.content_type = "image/jpeg"

    def mock_filetype_guess(file):
        if file is valid_file.file or file is oversized_file.file:
            return filetype.Type(extension='jpg', mime='image/jpeg')
        return None

    filetype.guess = MagicMock(side_effect=mock_filetype_guess)

    await image_services.validate_file_size_type(valid_file)

    with pytest.raises(HTTPException) as exc_info_type:
        await image_services.validate_file_size_type(invalid_file_type)
    assert exc_info_type.value.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

    with pytest.raises(HTTPException) as exc_info_size:
        await image_services.validate_file_size_type(oversized_file)
    assert exc_info_size.value.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
