from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict

class Organizer(BaseModel):
    """
    Represents an organization or individual hosting events on Eventyay.

    Attributes:
        id (int): Unique identifier for the organizer.
        name (str): The name of the organization.
        description (Optional[str]): A brief summary or bio of the organizer.
        url (Optional[str]): Official website link.
        logo_url (Optional[str]): URL to the organizer's logo image.
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
    Represents an event (conference, meetup, etc.) hosted on Eventyay.

    Attributes:
        id (int): Unique identifier for the event.
        name (str): The title of the event.
        identifier (str): A unique slug used in URLs.
        starts_at (Optional[str]): Opening time in ISO 8601 format.
        ends_at (Optional[str]): Closing time in ISO 8601 format.
        timezone (Optional[str]): Event timezone (e.g., 'UTC').
        privacy (Optional[str]): Access level ('public' or 'private').
        location_name (Optional[str]): Physical location or venue name.
        online (bool): Whether the event is accessible remotely.
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
    """
    Represents a participant registered for an event.

    Attributes:
        id (int): Unique identifier for the attendee record.
        email (Optional[str]): Contact email.
        firstname (Optional[str]): First name.
        lastname (Optional[str]): Last name.
        isCheckedIn (bool): Ticket check-in status.
    """
    id: int
    email: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    isCheckedIn: bool = False
    model_config = ConfigDict(extra='ignore')

class Speaker(BaseModel):
    """
    Represents a speaker presenting at an event.

    Attributes:
        id (int): Unique identifier for the speaker.
        name (str): Full name.
        email (Optional[str]): Contact email.
        photo_url (Optional[str]): Link to speaker's profile photo.
        short_biography (Optional[str]): A brief bio.
    """
    id: int
    name: str
    email: Optional[str] = None
    photo_url: Optional[str] = None
    short_biography: Optional[str] = None
    model_config = ConfigDict(extra='ignore')

class Session(BaseModel):
    """
    Represents a talk, workshop, or session within an event.

    Attributes:
        id (int): Unique identifier for the session.
        title (str): Title of the talk.
        description (Optional[str]): Full description of the session.
        starts_at (Optional[str]): Session start time.
        ends_at (Optional[str]): Session end time.
    """
    id: int
    title: str
    description: Optional[str] = None
    starts_at: Optional[str] = None
    ends_at: Optional[str] = None
    model_config = ConfigDict(extra='ignore')

# Response Wrappers for Pagination
class OrganizerList(BaseModel):
    """Paginated response containing a list of organizers."""
    data: List[Organizer]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra='ignore')

class EventList(BaseModel):
    """Paginated response containing a list of events."""
    data: List[Event]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra='ignore')

class AttendeeList(BaseModel):
    """Paginated response containing a list of attendees."""
    data: List[Attendee]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra='ignore')

class SpeakerList(BaseModel):
    """Paginated response containing a list of speakers."""
    data: List[Speaker]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra='ignore')

class SessionList(BaseModel):
    """Paginated response containing a list of sessions."""
    data: List[Session]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra='ignore')

class Ticket(BaseModel):
    """
    Represents a ticket type available for an event.

    Attributes:
        id (int): Unique identifier for the ticket.
        name (str): Name of the ticket (e.g., 'General Admission', 'VIP').
        description (Optional[str]): Description of what the ticket includes.
        type (Optional[str]): Type of ticket (e.g., 'free', 'paid', 'donation').
        price (Optional[float]): Price of the ticket.
        quantity (Optional[int]): Total number of tickets available.
        sales_starts_at (Optional[str]): When ticket sales begin.
        sales_ends_at (Optional[str]): When ticket sales end.
        is_hidden (bool): Whether the ticket is hidden from the public event page.
    """
    id: int
    name: str
    description: Optional[str] = None
    type: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    sales_starts_at: Optional[str] = None
    sales_ends_at: Optional[str] = None
    is_hidden: bool = False
    
    model_config = ConfigDict(extra='ignore')

    def __str__(self):
        type_str = f" - ${self.price}" if self.type == 'paid' else f" - {self.type}"
        return f"Ticket(id={self.id}, name='{self.name}'{type_str})"

class TicketList(BaseModel):
    """Paginated response containing a list of tickets."""
    data: List[Ticket]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra='ignore')
