import pytest
from unittest.mock import patch, MagicMock
import requests

from src.image.service import AiAnnotationServices
from src.image.constants import LABELS_URL

@pytest.fixture
def ai_annotation_services():
    return AiAnnotationServices()

@patch('requests.get')
def test_get_labels_success(mock_requests_get, ai_annotation_services):
    expected_labels = ['Welsh Springer Spaniel', 'Cocker Spaniels', 'Kuvasz']
    mock_response = MagicMock()
    mock_response.json.return_value = expected_labels
    mock_requests_get.return_value = mock_response
    
    labels = ai_annotation_services._AiAnnotationServices__get_labels()
    
    assert isinstance(labels, list)
    assert labels == expected_labels
    mock_requests_get.assert_called_once_with(LABELS_URL)

@patch('requests.get')
def test_get_labels_failure(mock_requests_get, ai_annotation_services):
    mock_requests_get.side_effect = requests.exceptions.RequestException("Server is down")
    
    with pytest.raises(requests.exceptions.RequestException):
        ai_annotation_services._AiAnnotationServices__get_labels()
    mock_requests_get.assert_called_once_with(LABELS_URL)