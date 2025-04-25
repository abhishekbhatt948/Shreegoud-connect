from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# Association table for many-to-many relationship between users and events
user_event_association = Table(
    'user_event_association',
    Base.metadata,
    Column('user_id', String, ForeignKey('users.id')),
    Column('event_id', String, ForeignKey('events.id'))
)

class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    events = relationship('Event', secondary=user_event_association, back_populates='attendees')
    created_events = relationship('Event', back_populates='organizer')

class Event(Base):
    __tablename__ = 'events'

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    date = Column(DateTime, nullable=False)
    time = Column(String, nullable=False)
    location = Column(String, nullable=False)
    image_url = Column(String)
    organizer_id = Column(String, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organizer = relationship('User', back_populates='created_events')
    attendees = relationship('User', secondary=user_event_association, back_populates='events')

class Media(Base):
    __tablename__ = 'media'

    id = Column(String, primary_key=True)
    url = Column(String, nullable=False)
    type = Column(String, nullable=False)  # 'image' or 'video'
    user_id = Column(String, ForeignKey('users.id'))
    event_id = Column(String, ForeignKey('events.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 