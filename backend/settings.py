from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # AWS Configuration
    AWS_REGION: str = "eu-north-1"
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None

    # RDS Configuration
    DB_HOST: str = "shreegaud-connect-db.cx42aai6ywex.eu-north-1.rds.amazonaws.com"
    DB_PORT: int = 5432
    DB_NAME: str = "shreegaud_connect"
    DB_USER: str
    DB_PASSWORD: str

    # Cognito Configuration
    COGNITO_USER_POOL_ID: str = "eu-north-1_zJARSgqY8"
    COGNITO_CLIENT_ID: str = "40veq4tkbbae1iisics8ji547h"

    # S3 Configuration
    S3_BUCKET_NAME: str

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 