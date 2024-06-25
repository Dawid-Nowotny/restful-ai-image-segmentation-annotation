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
    user.secret_key = None
    return user

@pytest.mark.asyncio
async def test_set_secret_key(totp_services, mock_db, mock_user):
    secret_key = "JBSWY3DPEHPK3PXP"

    await totp_services.set_secret_key(mock_user, secret_key, mock_db)

    assert mock_user.secret_key == secret_key
    mock_db.add.assert_called_once_with(mock_user)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_user)

@pytest.mark.asyncio
async def test_set_secret_key_overwrite(totp_services, mock_db, mock_user):
    initial_secret_key = "INITIAL12345678"
    new_secret_key = "NEWSECRET123456"
    mock_user.secret_key = initial_secret_key

    await totp_services.set_secret_key(mock_user, new_secret_key, mock_db)

    assert mock_user.secret_key == new_secret_key
    mock_db.add.assert_called_once_with(mock_user)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_user)

@pytest.mark.asyncio
async def test_set_secret_key_db_error(totp_services, mock_db, mock_user):
    secret_key = "TESTSECRET12345"
    mock_db.commit.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        await totp_services.set_secret_key(mock_user, secret_key, mock_db)

    assert mock_user.secret_key == secret_key
    mock_db.add.assert_called_once_with(mock_user)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_not_called()