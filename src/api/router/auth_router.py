from fastapi import APIRouter, Depends
from http.client import HTTPException
from fastapi import HTTPException, Response
import grpc

from src.api.auth.jwt_manager import JwtManager
from src.grpc.auth_service.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/login")
def login(http_response: Response, telegram_user_id: str, email: str, username: str, password:str):
    try:
        response = AuthService.login(username=username, password=password,
                                     email=email, telegram_user_id=telegram_user_id)

        http_response.set_cookie(key="access_token", value=response.token, httponly=True, secure=True)
        if not response.token:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"message": "Login successful"}
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail="Login failed")

@router.get("/check_auth")
def read_users_me(current_user: dict = Depends(JwtManager.get_current_user)):
    return {"check": "You are authorised"}
