from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Event, User
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/")
async def create_event(
    title: str,
    description: str,
    date: str,
    time: str,
    location: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    event = Event(
        title=title,
        description=description,
        date=date,
        time=time,
        location=location,
        organizer_id=current_user["sub"]
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@router.get("/")
async def get_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return events

@router.get("/{event_id}")
async def get_event(event_id: str, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.post("/{event_id}/attend")
async def attend_event(
    event_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    user = db.query(User).filter(User.id == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    event.attendees.append(user)
    db.commit()
    return {"message": "Successfully registered for event"} 