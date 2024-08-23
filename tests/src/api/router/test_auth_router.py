from unittest.mock import MagicMock, patch
from fastapi import HTTPException

from tests.conftest import client
from tests.src.test_data_preparation import DataPreparation, test_login


class TestAuthRouter:

    @patch('src.grpc.auth_service.auth_service.AuthService.login')
    def test_login_success(self, mock_login):
        # Setup mock response for AuthService.login
        mock_login.return_value = MagicMock(token="mock_token")

        # Do test
        response = client.post("/auth/login", params={
            "telegram_user_id": DataPreparation.TEST_USER_ID,
            "email": DataPreparation.TEST_USER_EMAIL,
            "username": DataPreparation.TEST_USER_NAME,
            "password": DataPreparation.TEST_PASS
        })

        # Validate response
        assert response.status_code == 200
        assert response.json() == {"message": "Login successful"}
        assert "access_token=mock_token" in response.headers.get("set-cookie")

    @patch('src.grpc.auth_service.auth_service.AuthService.login')
    def test_login_failure_invalid_credentials(self, mock_login):
        # Setup mock response for AuthService.login to return no token
        mock_login.return_value = MagicMock(token=None)

        # Send POST request to /auth/login
        response = client.post("/auth/login", params={
            "telegram_user_id": DataPreparation.TEST_USER_ID,
            "email": DataPreparation.TEST_USER_EMAIL,
            "username": DataPreparation.TEST_USER_NAME,
            "password": DataPreparation.TEST_PASS
        })

        # Validate response
        assert response.status_code == 401
        assert response.json() == {"message": "Invalid credentials"}

    @patch('src.api.auth.jwt_manager.JwtManager.verify_token')
    @patch('src.api.auth.jwt_manager.JwtManager.get_current_user')
    def test_check_auth_success(self, mock_verify_token, mock_get_current_user):
        # Setup mock response for JwtManager
        mock_verify_token.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }
        mock_get_current_user.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }

        # Do test
        response = client.get("/auth/check_auth", cookies={"access_token": "valid_token"})

        # Validate response
        assert response.status_code == 200
        assert response.json() == {"check": "You are authorised"}

    @patch('src.api.auth.jwt_manager.JwtManager.get_current_user')
    def test_check_auth_failure(self, mock_get_current_user, test_login):
        # Setup mock to raise an exception (e.g., user not authenticated)
        mock_get_current_user.side_effect = HTTPException(status_code=401, detail="Not authorized")

        # Do test
        response = client.get("/auth/check_auth")

        # Validate response
        assert response.status_code == 401
        assert response.json() == {"message": "Not authenticated"}