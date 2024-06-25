import pytest
from unittest.mock import MagicMock
from src.admin.service import AdminServices
from src.models import User

@pytest.fixture
def mock_db():
    return MagicMock()

def test_get_moderators():
    admin_service = AdminServices()
    mock_db = MagicMock()
    
    mock_moderators = [
        User(id=1, username="mod1", role="Moderator"),
        User(id=2, username="mod2", role="Moderator"),
    ]
    mock_non_moderators = [
        User(id=3, username="user1", role="User"),
        User(id=4, username="admin1", role="Admin"),
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_moderators
    
    result = admin_service.get_moderators(mock_db)

    assert len(result) == 2
    assert all(user.role == "Moderator" for user in result)
    assert all(user in mock_moderators for user in result)
    assert all(user not in mock_non_moderators for user in result)
    
    mock_db.query.assert_called_once_with(User)
    mock_db.query.return_value.filter.assert_called_once()
    mock_db.query.return_value.filter.return_value.all.assert_called_once()
