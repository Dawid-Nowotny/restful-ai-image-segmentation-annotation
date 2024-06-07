import pytest
from unittest.mock import MagicMock

from src.statistics.service import ImageStatsServices

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.mark.parametrize("limit, mock_tags, expected_top_tags", [
    (2, [
        MagicMock(tag="Tag1"),
        MagicMock(tag="Tag2"),
        MagicMock(tag="Tag1"),
        MagicMock(tag="Tag3"),
        MagicMock(tag="Tag2"),
        MagicMock(tag="Tag1"),
    ], [
        {"tag": "tag1", "count": 3},
        {"tag": "tag2", "count": 2},
    ]),
    (1, [
        MagicMock(tag="Tag1"),
        MagicMock(tag="Tag2"),
        MagicMock(tag="Tag1"),
        MagicMock(tag="Tag3"),
        MagicMock(tag="Tag2"),
        MagicMock(tag="Tag1"),
    ], [
        {"tag": "tag1", "count": 3},
    ]),
    (3, [
        MagicMock(tag="Tag1"),
        MagicMock(tag="Tag2"),
        MagicMock(tag="Tag1"),
        MagicMock(tag="Tag3"),
        MagicMock(tag="Tag2"),
        MagicMock(tag="Tag1"),
    ], [
        {"tag": "tag1", "count": 3},
        {"tag": "tag2", "count": 2},
        {"tag": "tag3", "count": 1},
    ]),
    (0, [
        MagicMock(tag="Tag1"),
        MagicMock(tag="Tag2"),
        MagicMock(tag="Tag1"),
        MagicMock(tag="Tag3"),
        MagicMock(tag="Tag2"),
        MagicMock(tag="Tag1"),
    ], []),
])
def test_get_top_tags(mock_db, limit, mock_tags, expected_top_tags):
    image_stats_services = ImageStatsServices()

    mock_db.query().all.return_value = mock_tags
    top_tags = image_stats_services.get_top_tags(limit=limit, db=mock_db)

    assert top_tags == expected_top_tags

    mock_db.query().all.assert_called_once()