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
