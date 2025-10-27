"""Integration tests for authentication flow."""
import pytest
from httpx import AsyncClient
from backend.server import app


class TestAuthenticationFlow:
    """Test complete authentication flows."""

    @pytest.mark.asyncio
    async def test_register_new_user(self, clean_db):
        """Test registering a new user."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/api/auth/register", json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "securepass123"
            })

            assert response.status_code == 200
            data = response.json()
            assert "access_token" in data
            assert data["username"] == "newuser"

    @pytest.mark.asyncio
    async def test_register_duplicate_username(self, test_user):
        """Test that duplicate usernames are rejected."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/api/auth/register", json={
                "username": test_user["username"],
                "email": "another@example.com",
                "password": "pass123"
            })

            assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_login_with_correct_credentials(self, test_user):
        """Test logging in with correct credentials."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/api/auth/login", json={
                "username": test_user["username"],
                "password": "testpass123"
            })

            assert response.status_code == 200
            data = response.json()
            assert "access_token" in data
            assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_with_wrong_password(self, test_user):
        """Test that wrong password is rejected."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/api/auth/login", json={
                "username": test_user["username"],
                "password": "wrongpassword"
            })

            assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_access_protected_route_with_token(self, auth_headers):
        """Test accessing protected route with valid token."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/player/profile",
                headers=auth_headers
            )

            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_access_protected_route_without_token(self):
        """Test that protected route requires authentication."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/player/profile")

            assert response.status_code == 401