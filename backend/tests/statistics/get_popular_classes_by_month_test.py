import pytest
from unittest.mock import MagicMock
from datetime import datetime

from src.statistics.service import ImageStatsServices

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.mark.parametrize("mock_data, expected_result", [
    (
        [
            MagicMock(coordinates_classes={"pred_class": ["class1", "class2"]}, upload_date=datetime(2023, 1, 1)),
            MagicMock(coordinates_classes={"pred_class": ["class1", "class3"]}, upload_date=datetime(2023, 1, 15)),
            MagicMock(coordinates_classes={"pred_class": ["class2", "class3"]}, upload_date=datetime(2023, 2, 1)),
            MagicMock(coordinates_classes={"pred_class": ["class1", "class2"]}, upload_date=datetime(2023, 2, 15)),
        ],
        [
            {"year": 2023, "month": "January", "top_classes": {"class_name": "class1", "count": 2}},
            {"year": 2023, "month": "February", "top_classes": {"class_name": "class2", "count": 2}},
        ]
    ),
    (
        [
            MagicMock(coordinates_classes={"pred_class": ["class1"]}, upload_date=datetime(2023, 1, 1)),
            MagicMock(coordinates_classes={"pred_class": ["class2"]}, upload_date=datetime(2023, 2, 1)),
            MagicMock(coordinates_classes={"pred_class": ["class3"]}, upload_date=datetime(2023, 3, 1)),
        ],
        [
            {"year": 2023, "month": "January", "top_classes": {"class_name": "class1", "count": 1}},
            {"year": 2023, "month": "February", "top_classes": {"class_name": "class2", "count": 1}},
            {"year": 2023, "month": "March", "top_classes": {"class_name": "class3", "count": 1}},
        ]
    ),
    (
        [],
        []
    ),
])
def test_get_popular_classes_by_month(mock_db, mock_data, expected_result):
    mock_db.query.return_value = mock_data

    image_stats_services = ImageStatsServices()
    result = image_stats_services.get_popular_classes_by_month(mock_db)

    assert result == expected_result

    mock_db.query.assert_called_once()