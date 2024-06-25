import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO
from PIL import Image as PILImage, UnidentifiedImageError

from src.image.service import ImageServices

@pytest.fixture
def image_services():
    return ImageServices()

@pytest.mark.parametrize("image_blob, expected_format", [
    (b'fake_jpeg_data', 'JPEG'),
    (b'fake_png_data', 'PNG'),
    (b'fake_gif_data', 'GIF'),
])
def test_blob_to_image(image_services, image_blob, expected_format):
    mock_image = MagicMock(spec=PILImage.Image)
    mock_image.format = expected_format

    with patch('PIL.Image.open', return_value=mock_image) as mock_open:
        result = image_services.blob_to_image(image_blob)

    mock_open.assert_called_once()
    assert isinstance(mock_open.call_args[0][0], BytesIO)
    assert mock_open.call_args[0][0].getvalue() == image_blob
    assert result == mock_image
    assert result.format == expected_format

def test_blob_to_image_invalid_data(image_services):
    invalid_blob = b'invalid_image_data'

    with pytest.raises(UnidentifiedImageError):
        image_services.blob_to_image(invalid_blob)

@pytest.mark.parametrize("image_blob, expected_error", [
    (None, UnidentifiedImageError),
    ("", TypeError),
    ([], TypeError),
    ({}, TypeError),
])
def test_blob_to_image_invalid_type(image_services, image_blob, expected_error):
    with pytest.raises(expected_error):
        image_services.blob_to_image(image_blob)