import pytest
from unittest.mock import MagicMock

from src.user.service import UserServices

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.mark.asyncio
@pytest.mark.parametrize("username, email, password, expected_role", [
    ("test_user", "test@example.com", "test_password", "User"),
    ("admin_user", "admin@example.com", "admin_password", "User"),
])
async def test_create_user(mock_db, username, email, password, expected_role):
    user_services = UserServices()

    user = await user_services.create_user(username, email, password, mock_db)

    mock_db.add.assert_called_once_with(user)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(user)

    assert user.username == username
    assert user.email == email
    assert user.role == expected_role
    assert user.verify_password(password)