"""
Tests for authentication endpoints — registration, login, and profile.
"""


class TestRegistration:
    """Tests for POST /auth/register."""

    def test_register_success(self, client):
        """Should register a new user and return user data."""
        response = client.post("/auth/register", json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "password123",
            "full_name": "New User",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "new@example.com"
        assert data["full_name"] == "New User"
        assert data["is_active"] is True
        assert "id" in data

    def test_register_duplicate_username(self, client):
        """Should reject registration with an existing username."""
        user_data = {
            "username": "duplicate",
            "email": "first@example.com",
            "password": "password123",
        }
        client.post("/auth/register", json=user_data)

        user_data["email"] = "second@example.com"
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_register_duplicate_email(self, client):
        """Should reject registration with an existing email."""
        client.post("/auth/register", json={
            "username": "user1",
            "email": "same@example.com",
            "password": "password123",
        })
        response = client.post("/auth/register", json={
            "username": "user2",
            "email": "same@example.com",
            "password": "password123",
        })
        assert response.status_code == 400

    def test_register_invalid_email(self, client):
        """Should reject registration with an invalid email format."""
        response = client.post("/auth/register", json={
            "username": "badmail",
            "email": "not-an-email",
            "password": "password123",
        })
        assert response.status_code == 422

    def test_register_short_password(self, client):
        """Should reject passwords shorter than 6 characters."""
        response = client.post("/auth/register", json={
            "username": "shortpw",
            "email": "short@example.com",
            "password": "12345",
        })
        assert response.status_code == 422


class TestLogin:
    """Tests for POST /auth/login."""

    def test_login_success(self, client):
        """Should return a JWT token on valid credentials."""
        client.post("/auth/register", json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "password123",
        })
        response = client.post("/auth/login", json={
            "username": "loginuser",
            "password": "password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client):
        """Should return 401 on incorrect password."""
        client.post("/auth/register", json={
            "username": "wrongpw",
            "email": "wrongpw@example.com",
            "password": "correctpass",
        })
        response = client.post("/auth/login", json={
            "username": "wrongpw",
            "password": "wrongpassword",
        })
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        """Should return 401 for a user that doesn't exist."""
        response = client.post("/auth/login", json={
            "username": "ghost",
            "password": "password123",
        })
        assert response.status_code == 401


class TestUserProfile:
    """Tests for GET /users/me."""

    def test_get_profile(self, authenticated_client):
        """Should return the authenticated user's profile."""
        response = authenticated_client.get("/users/me")
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"

    def test_get_profile_unauthorized(self, client):
        """Should return 401 without a valid token."""
        response = client.get("/users/me")
        assert response.status_code == 401
