import pytest
import pyotp
import pyqrcode
import io
from PIL import Image

from src.user.service import TOTPServices

@pytest.fixture
def totp_services():
    return TOTPServices()

def test_generate_qr_code(totp_services):
    username = "testuser"
    secret_key = pyotp.random_base32()

    qr_code_bytes = totp_services.generate_qr_code(username, secret_key)

    assert isinstance(qr_code_bytes, bytes)
    
    try:
        image = Image.open(io.BytesIO(qr_code_bytes))
        assert image.format == "PNG"
    except Exception as e:
        pytest.fail(f"Nie można otworzyć wygenerowanego kodu QR jako obrazu PNG: {str(e)}")

    uri = pyotp.totp.TOTP(secret_key).provisioning_uri(username, issuer_name="RAISA")
    qr_code = pyqrcode.create(uri)
    buffer = io.BytesIO()
    qr_code.png(buffer, scale=5)
    expected_qr_code_bytes = buffer.getvalue()

    assert qr_code_bytes == expected_qr_code_bytes

def test_generate_qr_code_different_users(totp_services):
    username1 = "user1"
    username2 = "user2"
    secret_key = pyotp.random_base32()

    qr_code1 = totp_services.generate_qr_code(username1, secret_key)
    qr_code2 = totp_services.generate_qr_code(username2, secret_key)

    assert qr_code1 != qr_code2

def test_generate_qr_code_different_secrets(totp_services):
    username = "testuser"
    secret_key1 = pyotp.random_base32()
    secret_key2 = pyotp.random_base32()

    qr_code1 = totp_services.generate_qr_code(username, secret_key1)
    qr_code2 = totp_services.generate_qr_code(username, secret_key2)

    # Assert
    assert qr_code1 != qr_code2