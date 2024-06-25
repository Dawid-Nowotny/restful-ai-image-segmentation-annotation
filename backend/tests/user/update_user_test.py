import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from src.user.service import UserServices
from src.user.schemas import UserUpdateSchema
from src.models import User

@pytest.fixture
def user_services():
    return UserServices()

@pytest.fixture
def mock_db():
    db = MagicMock(spec=Session)
    db.commit = MagicMock()
    db.refresh = MagicMock()
    return db

@pytest.fixture
def current_user():
    user = MagicMock(spec=User)
    user.username = "old_username"
    user.email = "old_email@example.com"
    user.set_password = MagicMock()
    return user

@pytest.mark.asyncio
async def test_update_user_all_fields(user_services, mock_db, current_user):
    user_data_update = UserUpdateSchema(
        username="new_username",
        email="new_email@example.com",
        password="new_password",
        old_password="old_password"
    )

    updated_user = await user_services.update_user(current_user, user_data_update, mock_db)

    assert updated_user.username == "new_username"
    assert updated_user.email == "new_email@example.com"
    current_user.set_password.assert_called_once_with("new_password")
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(current_user)

@pytest.mark.asyncio
async def test_update_user_only_username(user_services, mock_db, current_user):
    user_data_update = UserUpdateSchema(
        username="new_username",
        email=None,
        password=None,
        old_password="old_password"
    )

    updated_user = await user_services.update_user(current_user, user_data_update, mock_db)

    assert updated_user.username == "new_username"
    assert updated_user.email == "old_email@example.com"
    current_user.set_password.assert_not_called()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(current_user)

@pytest.mark.asyncio
async def test_update_user_only_email(user_services, mock_db, current_user):
    user_data_update = UserUpdateSchema(
        username=None,
        email="new_email@example.com",
        password=None,
        old_password="old_password"
    )

    updated_user = await user_services.update_user(current_user, user_data_update, mock_db)

    assert updated_user.username == "old_username"
    assert updated_user.email == "new_email@example.com"
    current_user.set_password.assert_not_called()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(current_user)

@pytest.mark.asyncio
async def test_update_user_only_password(user_services, mock_db, current_user):
    user_data_update = UserUpdateSchema(
        username=None,
        email=None,
        password="new_password",
        old_password="old_password"
    )

    updated_user = await user_services.update_user(current_user, user_data_update, mock_db)

    assert updated_user.username == "old_username"
    assert updated_user.email == "old_email@example.com"
    current_user.set_password.assert_called_once_with("new_password")
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(current_user)

@pytest.mark.asyncio
async def test_update_user_no_changes(user_services, mock_db, current_user):
    user_data_update = UserUpdateSchema(
        username=None,
        email=None,
        password=None,
        old_password="old_password"
    )

    updated_user = await user_services.update_user(current_user, user_data_update, mock_db)

    assert updated_user.username == "old_username"
    assert updated_user.email == "old_email@example.com"
    current_user.set_password.assert_not_called()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(current_user)