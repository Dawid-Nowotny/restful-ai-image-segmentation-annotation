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
            ("tag1", datetime(2023, 1, 1)),
            ("tag2", datetime(2023, 1, 2)),
            ("tag1", datetime(2023, 1, 3)),
            ("tag3", datetime(2023, 2, 1)),
            ("tag2", datetime(2023, 2, 2)),
            ("tag3", datetime(2023, 2, 3)),
        ],
        [
            {"year": 2023, "month": "January", "top_tag": {"tag": "tag1", "count": 2}},
            {"year": 2023, "month": "February", "top_tag": {"tag": "tag3", "count": 2}},
        ]
    ),
    (
        [
            ("tag1", datetime(2023, 1, 1)),
            ("tag2", datetime(2023, 2, 1)),
            ("tag3", datetime(2023, 3, 1)),
        ],
        [
            {"year": 2023, "month": "January", "top_tag": {"tag": "tag1", "count": 1}},
            {"year": 2023, "month": "February", "top_tag": {"tag": "tag2", "count": 1}},
            {"year": 2023, "month": "March", "top_tag": {"tag": "tag3", "count": 1}},
        ]
    ),
    (
        [],
        []
    ),
])
def test_get_popular_tags_by_month(mock_data, expected_result):
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_query.join.return_value = mock_data
    mock_db.query.return_value = mock_query

    image_stats_services = ImageStatsServices()
    result = image_stats_services.get_popular_tags_by_month(mock_db)

    assert result == expected_result

    mock_db.query.assert_called_once()
    mock_query.join.assert_called_once()