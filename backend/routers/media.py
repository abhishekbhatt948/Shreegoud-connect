from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Media
from ..dependencies import get_current_user, get_s3_service
from ..services.s3 import S3Service
import uuid

router = APIRouter()

@router.post("/upload")
async def upload_media(
    file: UploadFile = File(...),
    event_id: str = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    s3_service: S3Service = Depends(get_s3_service)
):
    try:
        # Generate unique filename
        file_extension = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{file_extension}"
        
        # Upload to S3
        file_url = await s3_service.upload_file(file.file, filename)
        
        # Save to database
        media = Media(
            url=file_url,
            type="image" if file_extension.lower() in ["jpg", "jpeg", "png", "gif"] else "video",
            user_id=current_user["sub"],
            event_id=event_id
        )
        
        db.add(media)
        db.commit()
        db.refresh(media)
        
        return media
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_media(
    event_id: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Media)
    if event_id:
        query = query.filter(Media.event_id == event_id)
    media = query.all()
    return media 