"""
Eventyay SDK Data Models

Pydantic models for all API resources.
Each model maps directly to a resource returned by the Eventyay REST API
(which follows the JSON:API specification with dasherized field names).

All models use ``ConfigDict(extra="ignore")`` so that unexpected fields
from the API never cause validation errors — this ensures forward
compatibility when new fields are added to the server.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict

# ── Core Resources ───────────────────────────────────────────


class Organizer(BaseModel):
    """Represents an organization or individual hosting events on Eventyay."""

    id: int
    name: str
    description: Optional[str] = None
    url: Optional[str] = None
    logo_url: Optional[str] = None

    model_config = ConfigDict(extra="ignore")

    def __str__(self):
        return f"Organizer(id={self.id}, name='{self.name}')"

    def __repr__(self):
        return self.__str__()


class Event(BaseModel):
    """
    Represents an event (conference, meetup, etc.) hosted on Eventyay.

    Fields match the server's EventSchemaPublic (Marshmallow-JSONAPI).
    The API returns dasherized keys; our JSON:API parser converts them
    to snake_case before constructing this model.
    """

    id: int
    name: str
    identifier: Optional[str] = None
    description: Optional[str] = None
    starts_at: Optional[str] = None
    ends_at: Optional[str] = None
    timezone: Optional[str] = None
    privacy: Optional[str] = "public"
    state: Optional[str] = None  # "published" or "draft"
    online: bool = False

    # Location
    location_name: Optional[str] = None
    searchable_location_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    # Images
    logo_url: Optional[str] = None
    original_image_url: Optional[str] = None
    thumbnail_image_url: Optional[str] = None
    large_image_url: Optional[str] = None
    icon_image_url: Optional[str] = None

    # Streaming
    public_stream_link: Optional[str] = None
    stream_loop: bool = False
    stream_autoplay: bool = False

    # Ticketing & Payment
    ticket_url: Optional[str] = None
    show_remaining_tickets: bool = False
    is_tax_enabled: bool = False
    is_billing_info_mandatory: bool = False
    is_donation_enabled: bool = False
    payment_country: Optional[str] = None
    payment_currency: Optional[str] = None
    can_pay_by_paypal: bool = False
    can_pay_by_stripe: bool = False
    can_pay_by_cheque: bool = False
    can_pay_by_bank: bool = False
    can_pay_by_invoice: bool = False
    can_pay_onsite: bool = False
    can_pay_by_omise: bool = False
    can_pay_by_alipay: bool = False
    can_pay_by_paytm: bool = False

    # Features
    is_sessions_speakers_enabled: bool = False
    is_sponsors_enabled: bool = False
    is_featured: bool = False
    is_promoted: bool = False
    is_announced: bool = False
    is_ticket_form_enabled: bool = True
    is_cfs_enabled: bool = False
    is_chat_enabled: bool = False
    is_videoroom_enabled: bool = False
    is_document_enabled: bool = False
    is_map_shown: bool = False
    is_badges_enabled: bool = True

    # Owner
    owner_name: Optional[str] = None
    owner_description: Optional[str] = None
    has_owner_info: bool = False
    is_oneclick_signup_enabled: bool = False

    # Content
    code_of_conduct: Optional[str] = None
    after_order_message: Optional[str] = None
    refund_policy: Optional[str] = None
    external_event_url: Optional[str] = None

    # Export URLs (read-only)
    pentabarf_url: Optional[str] = None
    ical_url: Optional[str] = None
    xcal_url: Optional[str] = None

    # Timestamps
    created_at: Optional[str] = None
    schedule_published_on: Optional[str] = None

    # Payment details
    cheque_details: Optional[str] = None
    bank_details: Optional[str] = None
    onsite_details: Optional[str] = None
    invoice_details: Optional[str] = None
    paypal_email: Optional[str] = None
    is_stripe_linked: Optional[bool] = False
    chat_room_name: Optional[str] = None

    model_config = ConfigDict(extra="ignore")

    def __str__(self):
        return f"Event(id={self.id}, name='{self.name}', date={self.starts_at})"

    def __repr__(self):
        return self.__str__()


class Attendee(BaseModel):
    """Represents a participant registered for an event."""

    id: int
    email: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    is_checked_in: bool = False
    # Also accept the camelCase version the API might return
    isCheckedIn: Optional[bool] = None
    checkin_times: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    job_title: Optional[str] = None
    phone: Optional[str] = None
    tax_business_info: Optional[str] = None
    billing_address: Optional[str] = None
    company: Optional[str] = None
    is_verified: bool = False

    model_config = ConfigDict(extra="ignore")

    def __str__(self):
        name = f"{self.firstname or ''} {self.lastname or ''}".strip() or "N/A"
        return f"Attendee(id={self.id}, name='{name}')"

    def __repr__(self):
        return self.__str__()


class Speaker(BaseModel):
    """
    Represents a speaker presenting at an event.
    Fields match the server's SpeakerSchema.
    """

    id: int
    name: str
    email: Optional[str] = None
    photo_url: Optional[str] = None
    thumbnail_image_url: Optional[str] = None
    small_image_url: Optional[str] = None
    icon_image_url: Optional[str] = None
    short_biography: Optional[str] = None
    long_biography: Optional[str] = None
    speaking_experience: Optional[str] = None
    mobile: Optional[str] = None
    website: Optional[str] = None
    twitter: Optional[str] = None
    facebook: Optional[str] = None
    github: Optional[str] = None
    mastodon: Optional[str] = None
    linkedin: Optional[str] = None
    instagram: Optional[str] = None
    organisation: Optional[str] = None
    position: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    gender: Optional[str] = None
    is_featured: bool = False
    order: Optional[int] = 0
    heard_from: Optional[str] = None
    sponsorship_required: Optional[str] = None

    model_config = ConfigDict(extra="ignore")

    def __str__(self):
        return f"Speaker(id={self.id}, name='{self.name}')"

    def __repr__(self):
        return self.__str__()


class Session(BaseModel):
    """
    Represents a talk, workshop, or session within an event.
    Fields match the server's SessionSchema.
    """

    id: int
    title: str
    subtitle: Optional[str] = None
    description: Optional[str] = None
    short_abstract: Optional[str] = None
    long_abstract: Optional[str] = None
    comments: Optional[str] = None
    starts_at: Optional[str] = None
    ends_at: Optional[str] = None
    language: Optional[str] = None
    level: Optional[str] = None
    slides_url: Optional[str] = None
    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    signup_url: Optional[str] = None
    website: Optional[str] = None
    twitter: Optional[str] = None
    facebook: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    instagram: Optional[str] = None
    gitlab: Optional[str] = None
    mastodon: Optional[str] = None
    state: Optional[str] = None  # pending/accepted/confirmed/rejected/draft/canceled/withdrawn
    created_at: Optional[str] = None
    submitted_at: Optional[str] = None
    is_mail_sent: Optional[bool] = None
    is_locked: bool = False
    last_modified_at: Optional[str] = None
    average_rating: Optional[float] = None
    rating_count: Optional[int] = None
    favourite_count: Optional[int] = None

    model_config = ConfigDict(extra="ignore")

    def __str__(self):
        return f"Session(id={self.id}, title='{self.title}')"

    def __repr__(self):
        return self.__str__()


class Track(BaseModel):
    """Represents an event track or category."""

    id: int
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    font_color: Optional[str] = None

    model_config = ConfigDict(extra="ignore")

    def __str__(self):
        return f"Track(id={self.id}, name='{self.name}')"

    def __repr__(self):
        return self.__str__()


class Microlocation(BaseModel):
    """Represents a specific room or location within an event venue."""

    id: int
    name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    floor: Optional[int] = None
    room: Optional[str] = None

    model_config = ConfigDict(extra="ignore")

    def __str__(self):
        return f"Microlocation(id={self.id}, name='{self.name}')"

    def __repr__(self):
        return self.__str__()


class Ticket(BaseModel):
    """
    Represents a ticket type available for an event.
    Fields match the server's TicketSchemaPublic.
    """

    id: int
    name: str
    description: Optional[str] = None
    type: Optional[str] = None  # 'free', 'paid', 'donation'
    price: Optional[float] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    quantity: Optional[int] = None
    position: Optional[int] = None
    is_description_visible: bool = False
    is_fee_absorbed: Optional[bool] = None
    sales_starts_at: Optional[str] = None
    sales_ends_at: Optional[str] = None
    is_hidden: bool = False
    min_order: Optional[int] = None
    max_order: Optional[int] = None
    is_checkin_restricted: bool = True
    auto_checkin_enabled: bool = False
    form_id: Optional[str] = None
    badge_id: Optional[str] = None

    model_config = ConfigDict(extra="ignore")

    def __str__(self):
        type_str = f" - ${self.price}" if self.type == "paid" else f" - {self.type}"
        return f"Ticket(id={self.id}, name='{self.name}'{type_str})"

    def __repr__(self):
        return self.__str__()


class Sponsor(BaseModel):
    """Represents a sponsor for an event."""

    id: int
    name: str
    description: Optional[str] = None
    url: Optional[str] = None
    logo_url: Optional[str] = None
    level: Optional[str] = None
    type: Optional[str] = None

    model_config = ConfigDict(extra="ignore")

    def __str__(self):
        return f"Sponsor(id={self.id}, name='{self.name}', level='{self.level}')"

    def __repr__(self):
        return self.__str__()


class DiscountCode(BaseModel):
    """Represents a discount or promo code for event tickets."""

    id: int
    code: str
    discount_url: Optional[str] = None
    value: Optional[float] = None
    type: Optional[str] = None  # 'percent' or 'amount'
    is_active: bool = True
    tickets_number: Optional[int] = None
    min_quantity: Optional[int] = None
    max_quantity: Optional[int] = None
    valid_from: Optional[str] = None
    valid_till: Optional[str] = None

    model_config = ConfigDict(extra="ignore")

    def __str__(self):
        return f"DiscountCode(id={self.id}, code='{self.code}', active={self.is_active})"

    def __repr__(self):
        return self.__str__()


class Order(BaseModel):
    """
    Represents an order (ticket purchase) for an event.
    Fields match the server's OrderSchema.
    """

    id: int
    identifier: Optional[str] = None
    amount: Optional[float] = None
    status: Optional[str] = None  # initializing/pending/cancelled/completed/placed/expired
    payment_mode: Optional[str] = (
        None  # free/stripe/paypal/bank/cheque/onsite/omise/alipay/paytm/invoice
    )
    paid_via: Optional[str] = None
    is_billing_enabled: bool = False

    # Billing details
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zipcode: Optional[str] = None
    company: Optional[str] = None
    tax_business_info: Optional[str] = None

    # Payment card info (read-only)
    brand: Optional[str] = None
    exp_month: Optional[str] = None
    exp_year: Optional[str] = None
    last4: Optional[str] = None

    # Metadata
    transaction_id: Optional[str] = None
    discount_code_id: Optional[str] = None
    cancel_note: Optional[str] = None
    order_notes: Optional[str] = None
    payment_url: Optional[str] = None
    tickets_pdf_url: Optional[str] = None

    # Timestamps
    created_at: Optional[str] = None
    completed_at: Optional[str] = None

    model_config = ConfigDict(extra="ignore")

    def __str__(self):
        return f"Order(id={self.id}, identifier='{self.identifier}', status='{self.status}')"

    def __repr__(self):
        return self.__str__()


class Tax(BaseModel):
    """Represents tax configuration for an event."""

    id: int
    name: Optional[str] = None
    rate: Optional[float] = None
    is_tax_included_in_price: bool = False
    country: Optional[str] = None

    model_config = ConfigDict(extra="ignore")

    def __str__(self):
        return f"Tax(id={self.id}, name='{self.name}', rate={self.rate}%)"

    def __repr__(self):
        return self.__str__()


class User(BaseModel):
    """Represents a user profile on the Eventyay platform."""

    id: int
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    details: Optional[str] = None
    contact: Optional[str] = None
    avatar_url: Optional[str] = None
    is_admin: Optional[bool] = None
    is_verified: Optional[bool] = None
    is_super_admin: Optional[bool] = None

    model_config = ConfigDict(extra="ignore")

    def __str__(self):
        return f"User(id={self.id}, email='{self.email}')"

    def __repr__(self):
        return self.__str__()


class Role(BaseModel):
    """Represents a role assigned to users."""

    id: int
    name: str
    title_name: Optional[str] = None

    model_config = ConfigDict(extra="ignore")

    def __str__(self):
        return f"Role(id={self.id}, name='{self.name}')"

    def __repr__(self):
        return self.__str__()


class Feedback(BaseModel):
    """Represents feedback submitted by an attendee."""

    id: int
    rating: Optional[float] = None
    comment: Optional[str] = None
    session_id: Optional[int] = None
    event_id: Optional[int] = None

    model_config = ConfigDict(extra="ignore")

    def __str__(self):
        return f"Feedback(id={self.id}, rating={self.rating})"

    def __repr__(self):
        return self.__str__()


class Setting(BaseModel):
    """Global application settings."""

    id: int
    app_environment: Optional[str] = None
    app_name: Optional[str] = None
    frontend_url: Optional[str] = None

    model_config = ConfigDict(extra="ignore")

    def __str__(self):
        return f"Setting(id={self.id}, app_name='{self.app_name}')"

    def __repr__(self):
        return self.__str__()


# ── Paginated Response Wrappers ──────────────────────────────


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


class TicketList(BaseModel):
    """Paginated response containing a list of tickets."""

    data: List[Ticket]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


class SponsorList(BaseModel):
    """Paginated response containing a list of sponsors."""

    data: List[Sponsor]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


class DiscountCodeList(BaseModel):
    """Paginated response containing a list of discount codes."""

    data: List[DiscountCode]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


class OrderList(BaseModel):
    """Paginated response containing a list of orders."""

    data: List[Order]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


class TaxList(BaseModel):
    """Paginated response containing a list of tax entries."""

    data: List[Tax]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


class UserList(BaseModel):
    """Paginated response containing a list of users."""

    data: List[User]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


class RoleList(BaseModel):
    """Paginated response containing a list of roles."""

    data: List[Role]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


class FeedbackList(BaseModel):
    """Paginated response containing a list of feedback entries."""

    data: List[Feedback]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")


class SettingList(BaseModel):
    """List of settings returned by the API."""

    data: List[Setting]
    links: Optional[Dict[str, Optional[str]]] = None
    meta: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(extra="ignore")
