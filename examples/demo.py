"""
Eventyay SDK Demo

Demonstrates key features of the Eventyay Python SDK:
- Synchronous client usage
- Auto-pagination
- Pydantic model access
- Error handling
- Context manager
"""

from eventyay import EventyayClient
from eventyay.exceptions import EventyayNotFoundError, EventyayAuthenticationError


def demo_basic_usage():
    """Basic synchronous client usage."""
    print("=== Basic Usage ===")

    client = EventyayClient(api_key="YOUR_API_KEY")

    # Fetch a page of events
    events = client.get_events(page=1, page_size=5)
    print(f"Fetched {len(events.data)} events")

    for event in events.data:
        print(f"  - {event.name} (ID: {event.id})")
        print(f"    Starts: {event.starts_at}")
        print(f"    Privacy: {event.privacy}")


def demo_auto_pagination():
    """Auto-pagination: fetch all results."""
    print("\n=== Auto-Pagination ===")

    client = EventyayClient(api_key="YOUR_API_KEY")

    # Fetches ALL events across all pages
    all_events = client.get_all_events()
    print(f"Total events: {len(all_events)}")

    # Same for organizers
    all_orgs = client.get_all_organizers()
    print(f"Total organizers: {len(all_orgs)}")


def demo_context_manager():
    """Using the client as a context manager."""
    print("\n=== Context Manager ===")

    with EventyayClient(api_key="YOUR_API_KEY") as client:
        events = client.get_events()
        for event in events.data:
            print(f"  {event.name}")
    # Session is automatically closed when exiting the `with` block


def demo_error_handling():
    """Graceful error handling with typed exceptions."""
    print("\n=== Error Handling ===")

    client = EventyayClient(api_key="YOUR_API_KEY")

    try:
        event = client.get_event(99999)
    except EventyayNotFoundError as e:
        print(f"Event not found (HTTP {e.status_code}): {e.message}")
    except EventyayAuthenticationError as e:
        print(f"Auth error: {e.message}")


def demo_event_details():
    """Fetch detailed event sub-resources."""
    print("\n=== Event Details ===")

    client = EventyayClient(api_key="YOUR_API_KEY")
    event_id = "my-event-slug"

    # Tickets
    tickets = client.get_event_tickets(event_id)
    for t in tickets.data:
        price = f"${t.price}" if t.price else "Free"
        print(f"  Ticket: {t.name} - {price}")

    # Speakers
    speakers = client.get_event_speakers(event_id)
    for s in speakers.data:
        print(f"  Speaker: {s.name}")

    # Sessions
    sessions = client.get_event_sessions(event_id)
    for sess in sessions.data:
        print(f"  Session: {sess.title}")


if __name__ == "__main__":
    print("Eventyay Python SDK Demo")
    print("=" * 40)
    print("\nNote: Replace 'YOUR_API_KEY' with a real key to run live.\n")

    # Uncomment the demo you want to try:
    # demo_basic_usage()
    # demo_auto_pagination()
    # demo_context_manager()
    # demo_error_handling()
    # demo_event_details()
