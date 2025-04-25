import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException
from typing import Optional
import uuid
from ..settings import settings

class AuthService:
    def __init__(self, user_pool_id: str, client_id: str, region: str):
        self.user_pool_id = user_pool_id
        self.client_id = client_id
        self.cognito = boto3.client(
            'cognito-idp',
            region_name=region,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

    async def register_user(self, email: str, password: str, name: str):
        try:
            response = self.cognito.sign_up(
                ClientId=self.client_id,
                Username=email,
                Password=password,
                UserAttributes=[
                    {'Name': 'email', 'Value': email},
                    {'Name': 'name', 'Value': name}
                ]
            )
            return response
        except ClientError as e:
            raise Exception(e.response['Error']['Message'])

    async def login_user(self, email: str, password: str):
        try:
            response = self.cognito.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password
                }
            )
            return response['AuthenticationResult']
        except ClientError as e:
            raise Exception(e.response['Error']['Message'])

    async def verify_token(self, token: str):
        try:
            response = self.cognito.get_user(AccessToken=token)
            return response
        except ClientError:
            return None

    async def refresh_token(self, refresh_token: str) -> dict:
        try:
            response = self.cognito.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='REFRESH_TOKEN_AUTH',
                AuthParameters={
                    'REFRESH_TOKEN': refresh_token
                }
            )

            return {
                'access_token': response['AuthenticationResult']['AccessToken'],
                'id_token': response['AuthenticationResult']['IdToken']
            }

        except ClientError as e:
            raise HTTPException(status_code=401, detail="Invalid refresh token") 