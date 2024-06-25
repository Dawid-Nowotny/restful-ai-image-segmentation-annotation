import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from src.admin.service import ModeratorServices
from src.models import User, Image  # Zakładamy, że masz takie importy

@pytest.fixture
def moderator_service():
    return ModeratorServices()

@pytest.mark.parametrize("user_role, user_id, moderator_id, should_raise", [
    ("Moderator", 1, 1, False),  # Moderator przypisany do obrazu
    ("Moderator", 1, 2, True),   # Moderator nieprzypisany do obrazu
    ("Admin", 1, 2, False),      # Admin zawsze ma dostęp
    ("User", 1, 1, False),        # Zwykły użytkownik nie ma dostępu
    ("User", 1, 2, True),        # Zwykły użytkownik nie ma dostępu
])
def test_check_if_moderator_is_assigned_to_image(moderator_service, user_role, user_id, moderator_id, should_raise):
    # Arrange
    mock_user = MagicMock(spec=User)
    mock_user.id = user_id
    mock_user.role = user_role

    mock_image = MagicMock(spec=Image)
    mock_image.moderator_id = moderator_id

    # Act & Assert
    if should_raise:
        with pytest.raises(HTTPException) as exc_info:
            moderator_service.check_if_moderator_is_assigned_to_image(mock_image, mock_user)
        assert exc_info.value.status_code == 403
        assert exc_info.value.detail == "Nie masz permisji do dodania super-tagów do tego obrazu"
    else:
        try:
            moderator_service.check_if_moderator_is_assigned_to_image(mock_image, mock_user)
        except HTTPException:
            pytest.fail("HTTPException raised unexpectedly")
