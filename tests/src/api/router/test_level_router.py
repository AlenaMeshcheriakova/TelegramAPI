from unittest.mock import patch
from pydantic import UUID4
import uuid

from src.grpc.level_service.level_service import LevelService
from tests.conftest import client
from tests.src.test_data_preparation import DataPreparation


class TestLevelRouter:

    @patch('src.api.auth.jwt_manager.JwtManager.verify_token')
    @patch('src.api.auth.jwt_manager.JwtManager.get_current_user')
    def test_get_all_levels(self, mock_verify_token, mock_get_current_user):
        # Mock token verification
        mock_verify_token.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }
        mock_get_current_user.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }

        # Mock LevelService behavior
        with patch.object(LevelService, 'get_levels', return_value=["Level 1", "Level 2"]) as mock_service:
            response = client.get("/level/levels", cookies={"access_token": "valid_token"})

            # Validate response
            assert response.status_code == 200
            assert response.json() == ["Level 1", "Level 2"]
            mock_service.assert_called_once()

    @patch('src.api.auth.jwt_manager.JwtManager.verify_token')
    @patch('src.api.auth.jwt_manager.JwtManager.get_current_user')
    def test_create_level(self, mock_verify_token, mock_get_current_user):
        # Mock token verification
        mock_verify_token.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }
        mock_get_current_user.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }

        # Mock LevelService behavior
        with patch.object(LevelService, 'create_level') as mock_service:
            level_data = {
                "new_lang_level": "Advanced"
            }
            response = client.post("/level/", json=level_data, cookies={"access_token": "valid_token"})

            # Validate response
            assert response.status_code == 200
            assert response.json() == {"message": "Level was created successfully"}
            mock_service.assert_called_once_with("Advanced")

    @patch('src.api.auth.jwt_manager.JwtManager.verify_token')
    @patch('src.api.auth.jwt_manager.JwtManager.get_current_user')
    def test_get_level_by_id(self, mock_verify_token, mock_get_current_user):
        # Mock token verification
        mock_verify_token.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }
        mock_get_current_user.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }

        # Mock LevelService behavior
        with patch.object(LevelService, 'get_level_by_id', return_value={"level_id": "123", "name": "Intermediate"}) as mock_service:
            level_id = str(uuid.uuid4())
            response = client.get(f"/level/{level_id}", cookies={"access_token": "valid_token"})

            # Validate response
            assert response.status_code == 200
            assert response.json() == {"level_id": "123", "name": "Intermediate"}
            mock_service.assert_called_once_with(UUID4(level_id))

    @patch('src.api.auth.jwt_manager.JwtManager.verify_token')
    @patch('src.api.auth.jwt_manager.JwtManager.get_current_user')
    def test_update_level(self, mock_verify_token, mock_get_current_user):
        # Mock token verification
        mock_verify_token.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }
        mock_get_current_user.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }

        # Mock LevelService behavior
        with patch.object(LevelService, 'update_level') as mock_service:
            level_data = {
                "id": str(uuid.uuid4()),
                "new_lang_level": "Advanced"
            }
            response = client.put("/level/", json=level_data, cookies={"access_token": "valid_token"})

            # Validate response
            assert response.status_code == 200
            assert response.json() == {"message": "Level updated successfully"}
            mock_service.assert_called_once_with(uuid.UUID(level_data["id"]), "Advanced")

    @patch('src.api.auth.jwt_manager.JwtManager.verify_token')
    @patch('src.api.auth.jwt_manager.JwtManager.get_current_user')
    def test_delete_level(self, mock_verify_token, mock_get_current_user):
        # Mock token verification
        mock_verify_token.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }
        mock_get_current_user.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }

        # Mock LevelService behavior
        with patch.object(LevelService, 'delete_level') as mock_service:
            level_id = str(uuid.uuid4())
            response = client.delete(f"/level/{level_id}", cookies={"access_token": "valid_token"})

            # Validate response
            assert response.status_code == 200
            assert response.json() == {"message": "Level deleted successfully"}
            mock_service.assert_called_once_with(UUID4(level_id))