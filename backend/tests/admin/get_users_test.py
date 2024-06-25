import pytest
from unittest.mock import MagicMock
from src.admin.service import AdminServices
from src.models import User

@pytest.fixture
def mock_db():
    return MagicMock()

def test_get_users():

    admin_service = AdminServices()
    mock_db = MagicMock()
    
    mock_users = [
        User(id=1, username="user1", role="User"),
        User(id=2, username="user2", role="User"),
    ]
    mock_non_users = [
        User(id=3, username="mod1", role="Moderator"),
        User(id=4, username="admin1", role="Admin"),
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_users
    
    result = admin_service.get_users(mock_db)
    
    assert len(result) == 2
    assert all(user.role == "User" for user in result)
    assert all(user in mock_users for user in result)
    assert all(user not in mock_non_users for user in result)
    
    mock_db.query.assert_called_once_with(User)
    mock_db.query.return_value.filter.assert_called_once()
    mock_db.query.return_value.filter.return_value.all.assert_called_once()
