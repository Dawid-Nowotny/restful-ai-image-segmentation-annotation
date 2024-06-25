import pytest
from unittest.mock import MagicMock, patch
from io import BytesIO

from src.image.service import ImageServices

@pytest.fixture
def mock_bytesio():
    with patch('io.BytesIO', autospec=True) as mock:
        yield mock

@pytest.mark.parametrize("images_dict, expected_files", [
    ({1: b'image1', 2: b'image2'}, ['1.jpg', '2.jpg']),
    ({100: b'image100'}, ['100.jpg']),
    ({}, []),
])
def test_zip_images(images_dict, expected_files, mock_bytesio):
    image_services = ImageServices()

    with patch('zipfile.ZipFile', autospec=True) as mock_zipfile:
        mock_zip_instance = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip_instance
        
        result = image_services.zip_images(images_dict)

    assert isinstance(result, BytesIO)
    mock_zipfile.assert_called_once()
    
    assert mock_zip_instance.writestr.call_count == len(images_dict)
    
    for (args, kwargs) in mock_zip_instance.writestr.call_args_list:
        assert args[0] in [f'{id}.jpg' for id in images_dict.keys()]
        assert args[1] in images_dict.values()
    
    assert set(args[0] for args, _ in mock_zip_instance.writestr.call_args_list) == set(expected_files)