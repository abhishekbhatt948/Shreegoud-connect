from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import Optional
from ..services.auth import AuthService
from ..dependencies import get_auth_service, get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

class UserRegistration(BaseModel):
    email: str
    password: str
    name: str

class UserLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    id_token: str
    user_id: str
    email: str
    name: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

@router.post("/register", response_model=TokenResponse)
async def register(
    user_data: UserRegistration,
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        # Register user in Cognito
        user_id = await auth_service.register_user(
            email=user_data.email,
            password=user_data.password,
            name=user_data.name
        )

        # Login user to get tokens
        tokens = await auth_service.login_user(
            email=user_data.email,
            password=user_data.password
        )

        return tokens

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", response_model=TokenResponse)
async def login(
    user_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        tokens = await auth_service.login_user(
            email=user_data.email,
            password=user_data.password
        )
        return tokens
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/refresh", response_model=dict)
async def refresh_token(
    token_data: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        tokens = await auth_service.refresh_token(token_data.refresh_token)
        return tokens
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return current_user 