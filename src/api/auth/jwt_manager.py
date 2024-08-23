import logging
from fastapi import HTTPException
from typing import Optional

import grpc
import jwt
from fastapi import Request

from src.grpc.auth_service.auth_service import AuthService

class JwtManager:
    @staticmethod
    def verify_token(token: str):
        try:
            response = AuthService.validate_token(token)
            if not response.is_valid:
                raise HTTPException(status_code=401, detail="Invalid token")
            return response
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except grpc.RpcError as e:
            raise HTTPException(status_code=500, detail="Token verification failed")

    @staticmethod
    def get_current_user(request: Request) -> Optional[dict]:
        # Extract the JWT token from the cookies
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="Not authenticated")

        # Validate the token and extract user information
        payload = JwtManager.verify_token(token)
        return payload