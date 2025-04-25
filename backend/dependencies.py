from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from .services.auth import AuthService
from .services.s3 import S3Service
from .settings import Settings

settings = Settings()

security = HTTPBearer()

def get_auth_service() -> AuthService:
    return AuthService(
        user_pool_id=settings.COGNITO_USER_POOL_ID,
        client_id=settings.COGNITO_CLIENT_ID,
        region=settings.AWS_REGION
    )

def get_s3_service() -> S3Service:
    return S3Service(
        bucket_name=settings.S3_BUCKET_NAME,
        region=settings.AWS_REGION
    )

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> dict:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    token = credentials.credentials
    user = await auth_service.verify_token(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    return user 