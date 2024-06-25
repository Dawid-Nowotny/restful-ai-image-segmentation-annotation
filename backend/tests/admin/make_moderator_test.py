import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from src.admin.service import AdminServices
from src.models import User 

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.mark.asyncio
async def test_make_moderator():

    admin_service = AdminServices()
    mock_db = MagicMock()
    
    user1 = User(id=1, username="user1", role="User")
    mock_db.query.return_value.filter.return_value.first.return_value = user1
    
    await admin_service.make_moderator("user1", mock_db)
    assert user1.role == "Moderator"
    mock_db.add.assert_called_once_with(user1)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(user1)
    
    mock_db.reset_mock()
    
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    with pytest.raises(HTTPException) as exc_info:
        await admin_service.make_moderator("nonexistent", mock_db)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Użytkownik nie został znaleziony"
    
    mock_db.reset_mock()
    
    user3 = User(id=3, username="mod1", role="Moderator")
    mock_db.query.return_value.filter.return_value.first.return_value = user3
    
    with pytest.raises(HTTPException) as exc_info:
        await admin_service.make_moderator("mod1", mock_db)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Użytkownik jest już moderatorem"
    
    mock_db.add.assert_not_called()
    mock_db.commit.assert_not_called()
    mock_db.refresh.assert_not_called()
