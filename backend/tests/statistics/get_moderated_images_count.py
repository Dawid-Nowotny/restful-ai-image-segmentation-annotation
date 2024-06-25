import pytest
from unittest.mock import MagicMock

from src.statistics.service import UserStatsServices

@pytest.mark.parametrize("mock_data, limit, expected_result", [
    (
        [
            ("moderator1", 10),
            ("moderator2", 8),
            ("moderator3", 5),
        ],
        2,
        [
            {"username": "moderator1", "moderated_count": 10},
            {"username": "moderator2", "moderated_count": 8},
        ]
    ),
    (
        [
            ("moderator1", 10),
            ("moderator2", 8),
            ("moderator3", 5),
        ],
        3,
        [
            {"username": "moderator1", "moderated_count": 10},
            {"username": "moderator2", "moderated_count": 8},
            {"username": "moderator3", "moderated_count": 5},
        ]
    ),
    (
        [],
        5,
        []
    ),
])
def test_get_moderated_images_count(mock_db, mock_data, limit, expected_result):
    mock_query = MagicMock()
    mock_query.join.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.group_by.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = mock_data
    mock_db.query.return_value = mock_query

    user_stats_services = UserStatsServices()
    result = user_stats_services.get_moderated_images_count(limit, mock_db)

    assert result == [{"username": username, "moderated_count": count} for username, count in mock_data][:limit]

    mock_db.query.assert_called_once()
    assert mock_query.join.call_count == 2
    mock_query.filter.assert_called_once()
    mock_query.group_by.assert_called_once()
    mock_query.order_by.assert_called_once()
    mock_query.limit.assert_called_once_with(limit)
    mock_query.all.assert_called_once()