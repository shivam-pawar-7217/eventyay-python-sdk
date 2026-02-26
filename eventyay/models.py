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
    model_config = ConfigDict(extra="ignore")

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

    model_config = ConfigDict(extra="ignore")

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
    model_config = ConfigDict(extra="ignore")


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
    model_config = ConfigDict(extra="ignore")


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
    model_config = ConfigDict(extra="ignore")


# Response Wrappers for Pagination
class OrganizerList(BaseModel):
    """Paginated response containing a list of organizers."""

    data: List[Organizer]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


class EventList(BaseModel):
    """Paginated response containing a list of events."""

    data: List[Event]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


class AttendeeList(BaseModel):
    """Paginated response containing a list of attendees."""

    data: List[Attendee]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


class SpeakerList(BaseModel):
    """Paginated response containing a list of speakers."""

    data: List[Speaker]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


class SessionList(BaseModel):
    """Paginated response containing a list of sessions."""

    data: List[Session]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


class Track(BaseModel):
    """
    Represents an event track or category.

    Attributes:
        id (int): Unique identifier for the track.
        name (str): The name of the track.
        description (Optional[str]): A description of what this track covers.
        color (Optional[str]): Background color code for UI elements.
        font_color (Optional[str]): Font color code for UI elements.
    """

    id: int
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    font_color: Optional[str] = None
    model_config = ConfigDict(extra="ignore")


class Microlocation(BaseModel):
    """
    Represents a specific physical location or room within an event venue.

    Attributes:
        id (int): Unique identifier for the microlocation.
        name (str): Name of the room/location (e.g. 'Main Hall', 'Room A').
        latitude (Optional[float]): Geographic coordinate.
        longitude (Optional[float]): Geographic coordinate.
        floor (Optional[int]): Floor level within the building.
        room (Optional[str]): Room number or identifier.
    """

    id: int
    name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    floor: Optional[int] = None
    room: Optional[str] = None
    model_config = ConfigDict(extra="ignore")


class TrackList(BaseModel):
    """Paginated response containing a list of tracks."""

    data: List[Track]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


class MicrolocationList(BaseModel):
    """Paginated response containing a list of microlocations."""

    data: List[Microlocation]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


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

    model_config = ConfigDict(extra="ignore")

    def __str__(self):
        type_str = f" - ${self.price}" if self.type == "paid" else f" - {self.type}"
        return f"Ticket(id={self.id}, name='{self.name}'{type_str})"


class TicketList(BaseModel):
    """Paginated response containing a list of tickets."""

    data: List[Ticket]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


class Sponsor(BaseModel):
    """
    Represents a sponsor for an event.

    Attributes:
        id (int): Unique identifier for the sponsor.
        name (str): The name of the sponsoring organization.
        description (Optional[str]): A brief description of the sponsor.
        url (Optional[str]): Sponsor's website URL.
        logo_url (Optional[str]): URL to the sponsor's logo.
        level (Optional[str]): Sponsorship tier (e.g., 'Gold', 'Silver').
        type (Optional[str]): Type identifier.
    """

    id: int
    name: str
    description: Optional[str] = None
    url: Optional[str] = None
    logo_url: Optional[str] = None
    level: Optional[str] = None
    type: Optional[str] = None
    model_config = ConfigDict(extra="ignore")


class SponsorList(BaseModel):
    """Paginated response containing a list of sponsors."""

    data: List[Sponsor]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


class DiscountCode(BaseModel):
    """
    Represents a discount or promo code for event tickets.

    Attributes:
        id (int): Unique identifier for the discount code.
        code (str): The actual discount code string.
        discount_url (Optional[str]): URL for applying the discount.
        value (Optional[float]): Discount value (amount or percentage).
        type (Optional[str]): Discount type ('percent' or 'amount').
        is_active (bool): Whether the code is currently active.
        tickets_number (Optional[int]): Max tickets this code applies to.
        min_quantity (Optional[int]): Minimum ticket quantity required.
        max_quantity (Optional[int]): Maximum ticket quantity allowed.
        valid_from (Optional[str]): Start of validity period.
        valid_till (Optional[str]): End of validity period.
    """

    id: int
    code: str
    discount_url: Optional[str] = None
    value: Optional[float] = None
    type: Optional[str] = None
    is_active: bool = True
    tickets_number: Optional[int] = None
    min_quantity: Optional[int] = None
    max_quantity: Optional[int] = None
    valid_from: Optional[str] = None
    valid_till: Optional[str] = None
    model_config = ConfigDict(extra="ignore")


class DiscountCodeList(BaseModel):
    """Paginated response containing a list of discount codes."""

    data: List[DiscountCode]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


class Order(BaseModel):
    """
    Represents an order (ticket purchase) for an event.

    Attributes:
        id (int): Unique identifier for the order.
        identifier (Optional[str]): Human-readable order identifier.
        status (Optional[str]): Order status (e.g., 'completed', 'pending', 'placed').
        amount (Optional[float]): Total order amount.
        paid_via (Optional[str]): Payment method used (e.g., 'stripe', 'free').
        created_at (Optional[str]): Order creation timestamp.
        completed_at (Optional[str]): Order completion timestamp.
    """

    id: int
    identifier: Optional[str] = None
    status: Optional[str] = None
    amount: Optional[float] = None
    paid_via: Optional[str] = None
    created_at: Optional[str] = None
    completed_at: Optional[str] = None
    model_config = ConfigDict(extra="ignore")

    def __str__(self):
        return f"Order(id={self.id}, identifier='{self.identifier}', status='{self.status}')"


class OrderList(BaseModel):
    """Paginated response containing a list of orders."""

    data: List[Order]
    id: int
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    font_color: Optional[str] = None
    model_config = ConfigDict(extra="ignore")


class Microlocation(BaseModel):
    """
    Represents a specific physical location or room within an event venue.

    Attributes:
        id (int): Unique identifier for the microlocation.
        name (str): Name of the room/location (e.g. 'Main Hall', 'Room A').
        latitude (Optional[float]): Geographic coordinate.
        longitude (Optional[float]): Geographic coordinate.
        floor (Optional[int]): Floor level within the building.
        room (Optional[str]): Room number or identifier.
    """

    id: int
    name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    floor: Optional[int] = None
    room: Optional[str] = None
    model_config = ConfigDict(extra="ignore")


class TrackList(BaseModel):
    """Paginated response containing a list of tracks."""

    data: List[Track]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


class MicrolocationList(BaseModel):
    """Paginated response containing a list of microlocations."""

    data: List[Microlocation]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


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

    model_config = ConfigDict(extra="ignore")

    def __str__(self):
        type_str = f" - ${self.price}" if self.type == "paid" else f" - {self.type}"
        return f"Ticket(id={self.id}, name='{self.name}'{type_str})"


class TicketList(BaseModel):
    """Paginated response containing a list of tickets."""

    data: List[Ticket]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


class Sponsor(BaseModel):
    """
    Represents a sponsor for an event.

    Attributes:
        id (int): Unique identifier for the sponsor.
        name (str): The name of the sponsoring organization.
        description (Optional[str]): A brief description of the sponsor.
        url (Optional[str]): Sponsor's website URL.
        logo_url (Optional[str]): URL to the sponsor's logo.
        level (Optional[str]): Sponsorship tier (e.g., 'Gold', 'Silver').
        type (Optional[str]): Type identifier.
    """

    id: int
    name: str
    description: Optional[str] = None
    url: Optional[str] = None
    logo_url: Optional[str] = None
    level: Optional[str] = None
    type: Optional[str] = None
    model_config = ConfigDict(extra="ignore")


class SponsorList(BaseModel):
    """Paginated response containing a list of sponsors."""

    data: List[Sponsor]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


class DiscountCode(BaseModel):
    """
    Represents a discount or promo code for event tickets.

    Attributes:
        id (int): Unique identifier for the discount code.
        code (str): The actual discount code string.
        discount_url (Optional[str]): URL for applying the discount.
        value (Optional[float]): Discount value (amount or percentage).
        type (Optional[str]): Discount type ('percent' or 'amount').
        is_active (bool): Whether the code is currently active.
        tickets_number (Optional[int]): Max tickets this code applies to.
        min_quantity (Optional[int]): Minimum ticket quantity required.
        max_quantity (Optional[int]): Maximum ticket quantity allowed.
        valid_from (Optional[str]): Start of validity period.
        valid_till (Optional[str]): End of validity period.
    """

    id: int
    code: str
    discount_url: Optional[str] = None
    value: Optional[float] = None
    type: Optional[str] = None
    is_active: bool = True
    tickets_number: Optional[int] = None
    min_quantity: Optional[int] = None
    max_quantity: Optional[int] = None
    valid_from: Optional[str] = None
    valid_till: Optional[str] = None
    model_config = ConfigDict(extra="ignore")


class DiscountCodeList(BaseModel):
    """Paginated response containing a list of discount codes."""

    data: List[DiscountCode]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


class Order(BaseModel):
    """
    Represents an order (ticket purchase) for an event.

    Attributes:
        id (int): Unique identifier for the order.
        identifier (Optional[str]): Human-readable order identifier.
        status (Optional[str]): Order status (e.g., 'completed', 'pending', 'placed').
        amount (Optional[float]): Total order amount.
        paid_via (Optional[str]): Payment method used (e.g., 'stripe', 'free').
        created_at (Optional[str]): Order creation timestamp.
        completed_at (Optional[str]): Order completion timestamp.
    """

    id: int
    identifier: Optional[str] = None
    status: Optional[str] = None
    amount: Optional[float] = None
    paid_via: Optional[str] = None
    created_at: Optional[str] = None
    completed_at: Optional[str] = None
    model_config = ConfigDict(extra="ignore")

    def __str__(self):
        return f"Order(id={self.id}, identifier='{self.identifier}', status='{self.status}')"


class OrderList(BaseModel):
    """Paginated response containing a list of orders."""

    data: List[Order]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


class Tax(BaseModel):
    """
    Represents tax configuration for an event.

    Attributes:
        id (int): Unique identifier for the tax record.
        name (Optional[str]): Name of the tax (e.g., 'GST', 'VAT').
        rate (Optional[float]): Tax rate as a percentage.
        is_tax_included_in_price (bool): Whether the ticket price already includes tax.
        country (Optional[str]): Country code for the tax jurisdiction.
    """

    id: int
    name: Optional[str] = None
    rate: Optional[float] = None
    is_tax_included_in_price: bool = False
    country: Optional[str] = None
    model_config = ConfigDict(extra="ignore")

    def __str__(self):
        return f"Tax(id={self.id}, name='{self.name}', rate={self.rate}%)"


class User(BaseModel):
    """
    Represents a user profile on the Eventyay platform.

    Attributes:
        id (int): Unique identifier for the user.
        email (Optional[str]): Primary email address.
        first_name (Optional[str]): First name of the user.
        last_name (Optional[str]): Last name of the user.
        details (Optional[str]): Bio or extra details.
        contact (Optional[str]): Contact number or details.
        avatar_url (Optional[str]): Profile picture URL.
    """

    id: int
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    details: Optional[str] = None
    contact: Optional[str] = None
    avatar_url: Optional[str] = None
    model_config = ConfigDict(extra="ignore")

    def __str__(self):
        return f"User(id={self.id}, email='{self.email}')"


class UserList(BaseModel):
    """Paginated response containing a list of users."""

    data: List[User]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


class Role(BaseModel):
    """
    Represents a role assigned to users (e.g., admin, co-organizer, volunteer).

    Attributes:
        id (int): Unique identifier for the role.
        name (str): The name/title of the role.
        title_name (Optional[str]): Human-readable title name.
    """

    id: int
    name: str
    title_name: Optional[str] = None
    model_config = ConfigDict(extra="ignore")

    def __str__(self):
        return f"Role(id={self.id}, name='{self.name}')"


class RoleList(BaseModel):
    """Paginated response containing a list of roles."""

    data: List[Role]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


class Feedback(BaseModel):
    """
    Represents feedback submitted by an attendee for an event or session.

    Attributes:
        id (int): Unique identifier for the feedback entry.
        rating (Optional[float]): Numeric rating given by the attendee.
        comment (Optional[str]): Textual feedback or comments.
        session_id (Optional[int]): The session this feedback is for.
        event_id (Optional[int]): The event this feedback belongs to.
    """

    id: int
    rating: Optional[float] = None
    comment: Optional[str] = None
    session_id: Optional[int] = None
    event_id: Optional[int] = None
    model_config = ConfigDict(extra="ignore")

    def __str__(self):
        return f"Feedback(id={self.id}, rating={self.rating})"


class FeedbackList(BaseModel):
    """Paginated response containing a list of feedback entries."""

    data: List[Feedback]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


class Setting(BaseModel):
    """
    Global application settings from the Eventyay platform.

    Attributes:
        id (int): Setting ID.
        app_environment (Optional[str]): E.g. 'production' or 'development'.
        app_name (Optional[str]): Application name.
        frontend_url (Optional[str]): Frontend URL.
    """

    id: int
    app_environment: Optional[str] = None
    app_name: Optional[str] = None
    frontend_url: Optional[str] = None
    
    # Allow extra fields to prevent errors if the API returns more configuration flags
    model_config = ConfigDict(extra="ignore")

    def __str__(self):
        return f"Setting(id={self.id}, app_name='{self.app_name}')"


class SettingList(BaseModel):
    """List of settings returned by the API."""

    data: List[Setting]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")
