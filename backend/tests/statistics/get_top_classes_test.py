import pytest
from unittest.mock import MagicMock

from src.statistics.service import ImageStatsServices

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.mark.parametrize("mock_data, limit, expected_result", [
    (
        [
            MagicMock(coordinates_classes={"pred_class": ["class1", "class2", "class1"]}),
            MagicMock(coordinates_classes={"pred_class": ["class2", "class3"]}),
            MagicMock(coordinates_classes={"pred_class": ["class1", "class3", "class4"]}),
        ],
        3,
        [
            {"class_name": "class1", "count": 3},
            {"class_name": "class2", "count": 2},
            {"class_name": "class3", "count": 2},
        ]
    ),
    (
        [
            MagicMock(coordinates_classes={"pred_class": ["class1", "class2"]}),
            MagicMock(coordinates_classes={"pred_class": ["class2", "class3"]}),
        ],
        2,
        [
            {"class_name": "class2", "count": 2},
            {"class_name": "class1", "count": 1},
        ]
    ),
    (
        [],
        5,
        []
    ),
])
def test_get_top_classes(mock_db, mock_data, limit, expected_result):
    mock_db.query().all.return_value = mock_data

    image_stats_services = ImageStatsServices()
    result = image_stats_services.get_top_classes(limit, mock_db)

    assert result == expected_result

    mock_db.query.assert_called()
    mock_db.query().all.assert_called_once()