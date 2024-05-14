import pytest
from unittest.mock import MagicMock

from src.user.service import UserServices

@pytest.fixture
def mock_db():
    return MagicMock()

def test_create_user(mock_db):
    username = "test_user"
    email = "test@example.com"
    password = "test_password"

    user_services = UserServices()

    user = user_services.create_user(username, email, password, mock_db)

    mock_db.add.assert_called_once_with(user)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(user)

    assert user.username == username
    assert user.email == email
    assert user.role == "User"
    assert user.verify_password(password)