import pytest
from unittest.mock import MagicMock

from src.statistics.service import UserStatsServices

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.mark.parametrize("mock_data, limit, expected_result", [
    (
        [
            ("user1", 10),
            ("user2", 8),
            ("user3", 5),
        ],
        2,
        [
            {"username": "user1", "comment_count": 10},
            {"username": "user2", "comment_count": 8},
        ]
    ),
    (
        [
            ("user1", 10),
            ("user2", 8),
            ("user3", 5),
        ],
        3,
        [
            {"username": "user1", "comment_count": 10},
            {"username": "user2", "comment_count": 8},
            {"username": "user3", "comment_count": 5},
        ]
    ),
    (
        [],
        5,
        []
    ),
])
def test_get_top_commenters(mock_db, mock_data, limit):
    mock_query = MagicMock()
    mock_query.join.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.group_by.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = mock_data
    mock_db.query.return_value = mock_query

    user_stats_services = UserStatsServices()
    result = user_stats_services.get_top_commenters(limit, mock_db)

    assert result == [{"username": username, "comment_count": count} for username, count in mock_data][:limit]

    mock_db.query.assert_called_once()
    mock_query.join.assert_called_once()
    mock_query.filter.assert_called_once()
    mock_query.group_by.assert_called_once()
    mock_query.order_by.assert_called_once()
    mock_query.limit.assert_called_once_with(limit)
    mock_query.all.assert_called_once()