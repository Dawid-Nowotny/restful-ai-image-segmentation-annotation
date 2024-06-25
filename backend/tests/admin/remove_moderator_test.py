import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from src.admin.service import AdminServices
from src.models import User

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.mark.asyncio
async def test_remove_moderator_role():

    admin_service = AdminServices()
    mock_db = MagicMock()
    
    moderator = User(id=1, username="mod1", role="Moderator")
    mock_db.query.return_value.filter.return_value.first.return_value = moderator
    
    await admin_service.remove_moderator_role("mod1", mock_db)
    assert moderator.role == "User"
    mock_db.add.assert_called_once_with(moderator)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(moderator)
    
    mock_db.reset_mock()
    
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    with pytest.raises(HTTPException) as exc_info:
        await admin_service.remove_moderator_role("nonexistent", mock_db)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Użytkownik nie został znaleziony"
    
    mock_db.reset_mock()
    
    regular_user = User(id=2, username="user1", role="User")
    mock_db.query.return_value.filter.return_value.first.return_value = regular_user
    
    with pytest.raises(HTTPException) as exc_info:
        await admin_service.remove_moderator_role("user1", mock_db)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Użytkownik nie jest moderatorem"
    
    mock_db.add.assert_not_called()
    mock_db.commit.assert_not_called()
    mock_db.refresh.assert_not_called()
