from typing import Optional, List, Dict, Any
from pydantic import BaseModel, HttpUrl, ConfigDict, Field

class Organizer(BaseModel):
    """
    Organizer model representing a user or group organizing events.
    """
    id: int
    name: str
    description: Optional[str] = None
    url: Optional[str] = None
    logo_url: Optional[str] = None
    
    # Allow extra fields to prevent errors if API adds new fields
    model_config = ConfigDict(extra='ignore')

    def __str__(self):
        return f"Organizer(id={self.id}, name='{self.name}')"

class Event(BaseModel):
    """
    Event model representing a conference, meetup, or gathering.
    """
    id: int
    name: str
    identifier: str
    starts_at: Optional[str] = None
    ends_at: Optional[str] = None
    timezone: Optional[str] = None
    privacy: Optional[str] = "public"
    location_name: Optional[str] = None
    online: bool = False
    
    model_config = ConfigDict(extra='ignore')

    def __str__(self):
        return f"Event(id={self.id}, name='{self.name}', date={self.starts_at})"

class Attendee(BaseModel):
    """Note: Represents an attendee at an event."""
    id: int
    email: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    isCheckedIn: bool = False
    model_config = ConfigDict(extra='ignore')

class Speaker(BaseModel):
    """Note: Represents a speaker at an event."""
    id: int
    name: str
    email: Optional[str] = None
    photo_url: Optional[str] = None
    short_biography: Optional[str] = None
    model_config = ConfigDict(extra='ignore')

class Session(BaseModel):
    """Note: Represents a session (talk/workshop) at an event."""
    id: int
    title: str
    description: Optional[str] = None
    starts_at: Optional[str] = None
    ends_at: Optional[str] = None
    model_config = ConfigDict(extra='ignore')
