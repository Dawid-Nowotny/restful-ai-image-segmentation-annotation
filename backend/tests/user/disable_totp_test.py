import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from src.user.service import TOTPServices
from src.models import User

@pytest.fixture
def totp_services():
    return TOTPServices()

@pytest.fixture
def mock_db():
    db = MagicMock(spec=Session)
    db.add = MagicMock()
    db.commit = MagicMock()
    db.refresh = MagicMock()
    return db

@pytest.fixture
def mock_user():
    user = MagicMock(spec=User)
    user.secret_key = "SOME_SECRET_KEY"
    return user

@pytest.mark.asyncio
async def test_disable_totp_success(totp_services, mock_db, mock_user):
    await totp_services.disable_totp(mock_user, mock_db)

    assert mock_user.secret_key is None
    mock_db.add.assert_called_once_with(mock_user)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_user)

@pytest.mark.asyncio
async def test_disable_totp_already_disabled(totp_services, mock_db, mock_user):
    mock_user.secret_key = None

    await totp_services.disable_totp(mock_user, mock_db)

    assert mock_user.secret_key is None
    mock_db.add.assert_called_once_with(mock_user)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_user)

@pytest.mark.asyncio
async def test_disable_totp_db_error(totp_services, mock_db, mock_user):
    mock_db.commit.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        await totp_services.disable_totp(mock_user, mock_db)

    assert mock_user.secret_key is None
    mock_db.add.assert_called_once_with(mock_user)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_not_called()