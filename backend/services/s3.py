import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException
import uuid
from typing import Optional
from ..settings import settings

class S3Service:
    def __init__(self, bucket_name: str, region: str):
        self.bucket_name = bucket_name
        self.s3 = boto3.client(
            's3',
            region_name=region,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

    async def generate_presigned_url(self, file_name: str, content_type: str) -> dict:
        try:
            # Generate a unique key for the file
            file_key = f"{uuid.uuid4()}/{file_name}"

            # Generate presigned URL for upload
            presigned_url = self.s3.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': file_key,
                    'ContentType': content_type
                },
                ExpiresIn=3600  # URL expires in 1 hour
            )

            return {
                'upload_url': presigned_url,
                'file_key': file_key,
                'public_url': f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{file_key}"
            }

        except ClientError as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_file(self, file_key: str) -> bool:
        try:
            self.s3.delete_object(
                Bucket=self.bucket_name,
                Key=file_key
            )
            return True
        except ClientError as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_file_url(self, file_key: str) -> Optional[str]:
        try:
            # Check if file exists
            self.s3.head_object(
                Bucket=self.bucket_name,
                Key=file_key
            )
            return f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{file_key}"
        except ClientError:
            return None

    async def upload_file(self, file, filename: str) -> str:
        try:
            self.s3.upload_fileobj(file, self.bucket_name, filename)
            file_url = f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{filename}"
            return file_url
        except ClientError as e:
            raise Exception(e.response['Error']['Message']) 