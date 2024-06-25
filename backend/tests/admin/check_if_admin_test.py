import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock

from src.admin.service import AdminServices

@pytest.fixture
def mock_user():
    return MagicMock()

@pytest.mark.parametrize("user_role, expected_exception", [
    ("Admin", None),
    ("User", HTTPException(status_code=403, detail="Dostęp tylko dla administratora")),
])
def test_check_if_admin(mock_user, user_role, expected_exception):
    mock_user.role = user_role
    admin_service = AdminServices()

    if expected_exception:
        with pytest.raises(type(expected_exception)) as exc_info:
            admin_service.check_if_admin(mock_user)
        assert exc_info.value.status_code == expected_exception.status_code
        assert exc_info.value.detail == expected_exception.detail
    else:
        admin_service.check_if_admin(mock_user)
        assert True