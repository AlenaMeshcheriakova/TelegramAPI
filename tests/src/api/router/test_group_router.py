from unittest.mock import patch
from pydantic import UUID4
import uuid

from src.grpc.group_service.group_service import GroupService
from tests.conftest import client
from tests.src.test_data_preparation import DataPreparation


class TestGroupRouter:

    @patch('src.api.auth.jwt_manager.JwtManager.verify_token')
    @patch('src.api.auth.jwt_manager.JwtManager.get_current_user')
    def test_get_group(self, mock_verify_token, mock_get_current_user):
        # Mock token verification
        mock_verify_token.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }
        mock_get_current_user.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }

        # Mock GroupService behavior
        with patch.object(GroupService, 'get_groups_name_by_user_name',
                          return_value=["group1", "group2"]) as mock_service:
            response = client.get("/group/groups?user_name="+ DataPreparation.TEST_USER_NAME,
                                  cookies={"access_token": "valid_token"})

            # Validate response
            assert response.status_code == 200
            assert response.json() == {"group_names": ["group1", "group2"]}
            mock_service.assert_called_once_with(DataPreparation.TEST_USER_NAME)

    @patch('src.api.auth.jwt_manager.JwtManager.verify_token')
    @patch('src.api.auth.jwt_manager.JwtManager.get_current_user')
    def test_add_group(self, mock_get_current_user, mock_verify_token):
        # Mock token verification
        mock_verify_token.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }
        mock_get_current_user.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }

        # Mock GroupService behavior
        with patch.object(GroupService, 'create_group') as mock_service:
            group_data = {
                "id": str(uuid.uuid4()),
                "group_name": "new_group",
                "user_id": str(uuid.uuid4())
            }
            response = client.post("/group/", json=group_data, cookies={"access_token": "valid_token"})

            # Validate response
            assert response.status_code == 200
            assert response.json() is None
            mock_service.assert_called_once()

    @patch('src.api.auth.jwt_manager.JwtManager.verify_token')
    @patch('src.api.auth.jwt_manager.JwtManager.get_current_user')
    def test_update_group(self, mock_get_current_user, mock_verify_token):
        # Mock token verification
        mock_verify_token.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }
        mock_get_current_user.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }

        # Mock GroupService behavior
        with patch.object(GroupService, 'update_group') as mock_service:
            group_data = {
                "id": str(uuid.uuid4()),
                "new_group_name": "updated_group_name"
            }
            response = client.put("/group/", json=group_data, cookies={"access_token": "valid_token"})

            # Validate response
            assert response.status_code == 200
            assert response.json() == {"status": "success"}
            mock_service.assert_called_once()

    @patch('src.api.auth.jwt_manager.JwtManager.verify_token')
    @patch('src.api.auth.jwt_manager.JwtManager.get_current_user')
    def test_delete_group(self, mock_get_current_user, mock_verify_token):
        # Mock token verification
        mock_verify_token.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }
        mock_get_current_user.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }

        # Mock GroupService behavior
        with patch.object(GroupService, 'delete_group') as mock_service:
            group_id = str(uuid.uuid4())
            response = client.delete(f"/group/{group_id}", cookies={"access_token": "valid_token"})

            # Validate response
            assert response.status_code == 200
            assert response.json() == {"status": "success"}
            mock_service.assert_called_once_with(UUID4(group_id))