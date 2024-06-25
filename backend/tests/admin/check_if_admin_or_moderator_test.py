import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from src.admin.service import ModeratorServices
from src.models import User

@pytest.fixture
def moderator_service():
    return ModeratorServices()

@pytest.mark.parametrize("user_role, should_raise", [
    ("Admin", False),
    ("Moderator", False),
    ("User", True),
    ("", True),
    (None, True),
])
def test_check_if_admin_or_moderator(moderator_service, user_role, should_raise):
    mock_user = MagicMock(spec=User)
    mock_user.role = user_role

    if should_raise:
        with pytest.raises(HTTPException) as exc_info:
            moderator_service.check_if_admin_or_moderator(mock_user)
        assert exc_info.value.status_code == 403
        assert exc_info.value.detail == "Dostęp tylko dla administratora lub moderatora"
    else:
        try:
            moderator_service.check_if_admin_or_moderator(mock_user)
        except HTTPException:
            pytest.fail("HTTPException raised unexpectedly")
