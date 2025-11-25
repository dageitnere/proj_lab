import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from app.backend.main import app
from app.backend.services.userService import _login_user, _COOKIE
from unittest.mock import patch

client = TestClient(app)

@patch("app.backend.services.userService.login_user")
def test_login_success(mock_login_user):
    mock_login_user.return_value = ("fake-token-123", "john")

    payload = {"login": "john", "password": "pass123"}
    response = client.post("/auth/login", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert data["ok"] is True
    assert data["username"] == "john"

    # Check cookie was set
    cookies = response.cookies
    assert _COOKIE in cookies
    assert cookies[_COOKIE] == "fake-token-123"

@patch("app.backend.services.userService.login_user")
def test_login_wrong_password(mock_login_user):
    mock_login_user.side_effect = ValueError("Invalid credentials")

    payload = {"login": "john", "password": "wrong"}
    response = client.post("/auth/login", json=payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

@patch("app.backend.services.userService.login_user")
def test_login_email_not_verified(mock_login_user):
    mock_login_user.side_effect = ValueError("Email not verified")

    payload = {"login": "john", "password": "something"}
    response = client.post("/auth/login", json=payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Email not verified"