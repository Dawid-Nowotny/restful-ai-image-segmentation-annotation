import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from src.admin.service import AdminServices
from src.models import User, Image

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.mark.asyncio
async def test_assign_moderator_to_image():

    admin_service = AdminServices()
    mock_db = MagicMock()
    
    image = Image(id=1)
    moderator = User(id=1, username="mod1", role="Moderator")
    
    mock_db.query.side_effect = [
        MagicMock(filter=MagicMock(return_value=MagicMock(first=MagicMock(return_value=image)))),
        MagicMock(filter=MagicMock(return_value=MagicMock(first=MagicMock(return_value=moderator))))
    ]
    
    await admin_service.assign_moderator_to_image(1, "mod1", mock_db)
    
    assert image.moderator_id == moderator.id
    mock_db.add.assert_called_once_with(image)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(image)
    
    mock_db.reset_mock()
    
    mock_db.query.side_effect = [
        MagicMock(filter=MagicMock(return_value=MagicMock(first=MagicMock(return_value=None)))),
    ]
    
    with pytest.raises(HTTPException) as exc_info:
        await admin_service.assign_moderator_to_image(2, "mod1", mock_db)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Obraz nie został znaleziony"
    
    mock_db.reset_mock()
    
    mock_db.query.side_effect = [
        MagicMock(filter=MagicMock(return_value=MagicMock(first=MagicMock(return_value=image)))),
        MagicMock(filter=MagicMock(return_value=MagicMock(first=MagicMock(return_value=None))))
    ]
    
    with pytest.raises(HTTPException) as exc_info:
        await admin_service.assign_moderator_to_image(1, "nonexistent", mock_db)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Moderator nie został znaleziony"
    
    mock_db.add.assert_not_called()
    mock_db.commit.assert_not_called()
    mock_db.refresh.assert_not_called()
