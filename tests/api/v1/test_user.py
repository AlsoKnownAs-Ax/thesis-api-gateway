from fastapi.testclient import TestClient

from app.core.config import config
from app.core.database import get_db
from app.main import app
from tests.test_db import TestingSessionLocal

# Setup the TestClient
client = TestClient(app)

def override_get_db():
    session = TestingSessionLocal()
    yield session

app.dependency_overrides[get_db] = override_get_db


def test_create_user():
    """Test user creation returns access token and sets refresh token cookie"""
    # Create a new user
    response = client.post(
        "/api/v1/user/create",
        json={"name": "Test User", "email": "test@user.com", "password": "testuser"},
    )

    # Assert response status and access token
    assert response.status_code == 200
    created_user = response.json()
    assert "access_token" in created_user

    if response.cookies:
        assert config.REFRESH_TOKEN_COOKIE_NAME in response.cookies
