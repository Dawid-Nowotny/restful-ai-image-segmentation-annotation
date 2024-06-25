import pytest
import pyotp

from src.user.service import TOTPServices

@pytest.fixture
def totp_services():
    return TOTPServices()

@pytest.mark.asyncio
async def test_generate_secret_key(totp_services):
    secret_key = await totp_services.generate_secret_key()

    assert isinstance(secret_key, str)
    assert len(secret_key) == 32
    
    assert all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567' for c in secret_key)

    try:
        pyotp.TOTP(secret_key)
    except Exception as e:
        pytest.fail(f"Nie można utworzyć obiektu TOTP z wygenerowanym kluczem: {str(e)}")

@pytest.mark.asyncio
async def test_generate_secret_key_uniqueness(totp_services):
    secret_key1 = await totp_services.generate_secret_key()
    secret_key2 = await totp_services.generate_secret_key()

    assert secret_key1 != secret_key2

@pytest.mark.asyncio
async def test_generate_secret_key_multiple_calls(totp_services):
    keys = [await totp_services.generate_secret_key() for _ in range(100)]

    # Assert
    assert len(set(keys)) == 100