"""
Eventyay SDK Demo — Showcasing the Python SDK Features

This script demonstrates how to use the Eventyay Python SDK
for common event management tasks.
"""

from eventyay.client import EventyayClient
from eventyay.exceptions import (
    EventyayConnectionError,
    EventyayNotFoundError,
    EventyayAPIError,
)


def main():
    print("=" * 60)
    print("  🚀 Eventyay Python SDK — Demo")
    print("=" * 60)

    # Initialize the client (no API key = public endpoints only)
    client = EventyayClient()

    # ── 1. Fetch Public Events ──────────────────────────────
    print("\n📅 Fetching public events...")
    try:
        event_list = client.get_events(page=1, page_size=5)
        events = event_list.data
        print(f"   ✅ Found {len(events)} events (page 1)")

        for event in events[:3]:
            # Pydantic model — type-safe attribute access
            print(f"   • {event.name} (ID: {event.id})")
            if event.starts_at:
                print(f"     Starts: {event.starts_at}")
            if event.location_name:
                print(f"     Location: {event.location_name}")

    except EventyayConnectionError:
        print("   ❌ Connection error — check your internet")
        return
    except EventyayAPIError as e:
        print(f"   ❌ API Error: {e}")
        return

    # ── 2. Fetch Speakers for First Event ───────────────────
    if events:
        event_id = str(events[0].id)
        print(f"\n🎤 Speakers for '{events[0].name}'...")
        try:
            speakers = client.get_event_speakers(event_id)
            for speaker in speakers.data[:3]:
                bio = (speaker.short_biography or "")[:50]
                print(f"   • {speaker.name} — {bio}")
        except EventyayNotFoundError:
            print("   (no speakers found)")
        except EventyayAPIError:
            print("   (speakers endpoint unavailable)")

    # ── 3. Fetch Sessions for First Event ───────────────────
    if events:
        print(f"\n📋 Sessions for '{events[0].name}'...")
        try:
            sessions = client.get_event_sessions(event_id)
            for session in sessions.data[:3]:
                print(f"   • {session.title}")
                if session.starts_at:
                    print(f"     Time: {session.starts_at}")
        except EventyayNotFoundError:
            print("   (no sessions found)")
        except EventyayAPIError:
            print("   (sessions endpoint unavailable)")

    # ── 4. Fetch Tickets for First Event ────────────────────
    if events:
        identifier = events[0].identifier
        print(f"\n🎫 Tickets for '{events[0].name}'...")
        try:
            tickets = client.get_event_tickets(identifier)
            for ticket in tickets.data[:3]:
                price_str = f"${ticket.price}" if ticket.price else "Free"
                print(f"   • {ticket.name} — {price_str}")
        except EventyayNotFoundError:
            print("   (no tickets found)")
        except EventyayAPIError:
            print("   (tickets endpoint unavailable)")

    print("\n" + "=" * 60)
    print("  ✨ Demo complete! See README.md for more usage examples.")
    print("=" * 60)


if __name__ == "__main__":
    main()
