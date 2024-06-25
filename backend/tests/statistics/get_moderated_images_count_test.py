import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from src.statistics.service import UserStatsServices

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

def test_get_moderated_images_count(mock_db):
    user_stats_services = UserStatsServices()

    mock_result = [
        ("user1", 5),
        ("user2", 3),
        ("user3", 2),
    ]

    mock_db.query.return_value.join.return_value.join.return_value.filter.return_value.group_by.return_value.order_by.return_value.limit.return_value.all.return_value = mock_result        

    result = user_stats_services.get_moderated_images_count(limit=3, db=mock_db)

    assert isinstance(result, list)
    assert len(result) == len(mock_result)
    for i in range(len(result)):
        assert isinstance(result[i], tuple)
        assert len(result[i]) == 2
        assert isinstance(result[i][0], str)
        assert isinstance(result[i][1], int)
