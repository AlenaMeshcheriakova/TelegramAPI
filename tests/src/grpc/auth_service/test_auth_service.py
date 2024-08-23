import unittest

from src.grpc.auth_service.auth_service import AuthService


class TestAuthService:

    def test_is_group_created(self):
        # Do tests
        result = AuthService.login(username='username', password='password',
                                   email='email', telegram_user_id='telegram_id')

        # Check results
        print(result)
        assert result is True

if __name__ == '__main__':
    unittest.main()