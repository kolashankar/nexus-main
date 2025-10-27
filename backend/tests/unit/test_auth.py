"""Unit tests for authentication system."""
import pytest
from backend.core.security import get_password_hash as hash_password, verify_password, create_access_token, decode_access_token
from datetime import timedelta


class TestPasswordHashing:
    """Test password hashing and verification."""

    def test_hash_password(self):
        """Test password hashing."""
        password = "testpassword123"
        hashed = hash_password(password)

        assert hashed != password
        assert len(hashed) > 20
        assert hashed.startswith("$2b$")

    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        password = "testpassword123"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        password = "testpassword123"
        hashed = hash_password(password)

        assert verify_password("wrongpassword", hashed) is False

    def test_different_hashes_same_password(self):
        """Test that same password produces different hashes (salt)."""
        password = "testpassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        assert hash1 != hash2
        assert verify_password(password, hash1)
        assert verify_password(password, hash2)


class TestJWTTokens:
    """Test JWT token creation and verification."""

    def test_create_token(self):
        """Test JWT token creation."""
        data = {"sub": "testuser"}
        token = create_access_token(data)

        assert isinstance(token, str)
        assert len(token) > 50
        assert token.count(".") == 2  # JWT has 3 parts

    def test_decode_token(self):
        """Test JWT token decoding."""
        username = "testuser"
        data = {"sub": username}
        token = create_access_token(data)

        decoded = decode_access_token(token)
        assert decoded["sub"] == username

    def test_token_expiry(self):
        """Test JWT token expiry."""
        data = {"sub": "testuser"}
        token = create_access_token(data, expires_delta=timedelta(seconds=-1))

        with pytest.raises(Exception):
            decode_access_token(token)

    def test_invalid_token(self):
        """Test decoding invalid token."""
        invalid_token = "invalid.token.here"

        with pytest.raises(Exception):
            decode_access_token(invalid_token)