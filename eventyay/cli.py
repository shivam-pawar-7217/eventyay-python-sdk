"""
Eventyay CLI Tool

A rich, interactive command-line interface for the Eventyay API.
Supports all 16 resource domains with list/show operations,
CRUD for events and organizers, and machine-readable JSON output.
"""

import json
import os
from pathlib import Path
from typing import Optional, cast

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

app = typer.Typer(
    help="Eventyay CLI — manage events, organizers, and more from your terminal.",
    no_args_is_help=True,
)
console = Console()

CONFIG_DIR = Path.home() / ".config" / "eventyay"
CONFIG_FILE = CONFIG_DIR / "config.json"

# ── Lazy Client ──────────────────────────────────────────────

_client = None


def get_client():
    """Return a lazily-initialized EventyayClient, refreshing on each call
    so that ``login`` writes are picked up immediately."""
    global _client
    if _client is None:
        from eventyay.client import EventyayClient

        api_key = _resolve_api_key()
        _client = EventyayClient(api_key=api_key)
    return _client


def reset_client():
    """Force re-creation of the cached client (e.g. after login)."""
    global _client
    _client = None


def _resolve_api_key() -> Optional[str]:
    """Resolve the API key from env var → config file → None."""
    api_key = os.environ.get("EVENTYAY_API_KEY")
    if api_key:
        return api_key

    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                if isinstance(config, dict):
                    return cast(Optional[str], config.get("api_key"))
        except Exception:
            pass

    return None


def _print_json(data):
    """Print data as formatted JSON and exit."""
    console.print_json(json.dumps(data, default=str))


# ── Global Commands ──────────────────────────────────────────


@app.command()
def version():
    """Show the CLI version."""
    from eventyay import __version__

    console.print(Panel(f"Eventyay CLI v{__version__}", title="Version", style="bold green"))


@app.command()
def login():
    """Authenticate the CLI with an Eventyay API key."""
    api_key = typer.prompt("Enter your Eventyay API key", hide_input=True)

    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        config_data = {}
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r") as f:
                try:
                    config_data = json.load(f)
                except json.JSONDecodeError:
                    pass

        config_data["api_key"] = api_key

        with open(CONFIG_FILE, "w") as f:
            json.dump(config_data, f, indent=4)

        # Refresh the cached client so subsequent commands use the new key
        reset_client()

        console.print("[bold green]Successfully saved API key to config.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error saving config:[/bold red] {e}")


@app.command()
def logout():
    """Remove the stored API key."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                config_data = json.load(f)
            config_data.pop("api_key", None)
            with open(CONFIG_FILE, "w") as f:
                json.dump(config_data, f, indent=4)
            reset_client()
            console.print("[bold green]API key removed from config.[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
    else:
        console.print("[yellow]No config file found. Nothing to do.[/yellow]")


@app.command("config")
def show_config():
    """Show current CLI configuration."""
    env_key = os.environ.get("EVENTYAY_API_KEY")
    file_key = None
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                file_key = json.load(f).get("api_key")
        except Exception:
            pass

    active_key = env_key or file_key
    masked = f"{active_key[:4]}****" if active_key and len(active_key) > 4 else active_key

    content = f"""
[bold]Config file:[/bold] {CONFIG_FILE}
[bold]API Key (env):[/bold] {'Set' if env_key else 'Not set'}
[bold]API Key (file):[/bold] {'Set' if file_key else 'Not set'}
[bold]Active key:[/bold] {masked or 'None'}
    """
    console.print(Panel(content.strip(), title="Configuration", expand=False))


# ── Events ───────────────────────────────────────────────────

events_app = typer.Typer(help="Manage events")
app.add_typer(events_app, name="events")


@events_app.command("list")
def list_events(
    output: str = typer.Option("table", help="Output format: table or json"),
):
    """List all events."""
    try:
        client = get_client()
        with console.status("[bold green]Fetching events..."):
            events_list = client.get_events()
            events = events_list.data

        if output == "json":
            _print_json([e.model_dump() for e in events])
            return

        table = Table(title="Eventyay Events")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")
        table.add_column("Start Time", style="green")
        table.add_column("Privacy", style="yellow")

        for event in events:
            table.add_row(
                str(event.id),
                event.name,
                event.starts_at or "N/A",
                event.privacy or "N/A",
            )

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@events_app.command("show")
def show_event(
    event_id: int,
    output: str = typer.Option("panel", help="Output format: panel or json"),
):
    """Show detailed info for an event."""
    try:
        client = get_client()
        with console.status(f"[bold green]Fetching event {event_id}..."):
            event = client.get_event(event_id)

        if output == "json":
            _print_json(event.model_dump())
            return

        content = f"""
[bold]ID:[/bold] {event.id}
[bold]Identifier:[/bold] {event.identifier}
[bold]Start:[/bold] {event.starts_at}
[bold]End:[/bold] {event.ends_at}
[bold]Privacy:[/bold] {event.privacy}
[bold]Location:[/bold] {event.location_name or 'Online'}
        """
        console.print(Panel(content, title=f"Event: {event.name}", expand=False))

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@events_app.command("create")
def create_event(
    name: str = typer.Option(..., help="Event name"),
    identifier: str = typer.Option(..., help="Unique identifier (slug)"),
    starts_at: str = typer.Option(..., help="Start time (ISO 8601)"),
    ends_at: str = typer.Option(..., help="End time (ISO 8601)"),
    timezone: str = typer.Option(..., help="Timezone (e.g. UTC, Asia/Kolkata)"),
    privacy: str = typer.Option("public", help="Privacy setting"),
    location: str = typer.Option(None, help="Location name"),
    online: bool = typer.Option(False, help="Is the event online?"),
):
    """Create a new event."""
    try:
        client = get_client()
        with console.status("[bold green]Creating event..."):
            event = client.create_event(
                name=name,
                identifier=identifier,
                starts_at=starts_at,
                ends_at=ends_at,
                timezone=timezone,
                privacy=privacy,
                location_name=location,
                online=online,
            )

        console.print("[bold green]Event created successfully![/bold green]")

        content = f"""
[bold]ID:[/bold] {event.id}
[bold]Identifier:[/bold] {event.identifier}
[bold]Start:[/bold] {event.starts_at}
[bold]End:[/bold] {event.ends_at}
[bold]Privacy:[/bold] {event.privacy}
[bold]Location:[/bold] {event.location_name or 'Online'}
        """
        console.print(Panel(content, title=f"Event: {event.name}", expand=False))

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@events_app.command("delete")
def delete_event(
    event_id: int = typer.Argument(..., help="ID of the event to delete"),
    force: bool = typer.Option(False, "--force", "-f", help="Force delete without confirmation"),
):
    """Delete an event."""
    try:
        if not force:
            if not typer.confirm(f"Are you sure you want to delete event {event_id}?"):
                console.print("Aborted.")
                raise typer.Abort()

        client = get_client()
        with console.status(f"[bold red]Deleting event {event_id}..."):
            client.delete_event(event_id)

        console.print(f"[bold green]Event {event_id} deleted successfully![/bold green]")
    except typer.Abort:
        raise
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@events_app.command("update")
def update_event(
    event_id: int = typer.Argument(..., help="ID of the event to update"),
    name: str = typer.Option(None, help="New name"),
    starts_at: str = typer.Option(None, help="New start time"),
    ends_at: str = typer.Option(None, help="New end time"),
    timezone: str = typer.Option(None, help="New timezone"),
    privacy: str = typer.Option(None, help="New privacy setting"),
    location: str = typer.Option(None, help="New location name"),
):
    """Update an existing event."""
    try:
        client = get_client()
        with console.status(f"[bold green]Updating event {event_id}..."):
            event = client.update_event(
                event_id=event_id,
                name=name,
                starts_at=starts_at,
                ends_at=ends_at,
                timezone=timezone,
                privacy=privacy,
                location_name=location,
            )

        console.print("[bold green]Event updated successfully![/bold green]")

        content = f"""
[bold]ID:[/bold] {event.id}
[bold]Identifier:[/bold] {event.identifier}
[bold]Start:[/bold] {event.starts_at}
[bold]End:[/bold] {event.ends_at}
[bold]Privacy:[/bold] {event.privacy}
[bold]Location:[/bold] {event.location_name or 'Online'}
        """
        console.print(Panel(content, title=f"Event: {event.name}", expand=False))

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


# ── Organizers ───────────────────────────────────────────────

organizers_app = typer.Typer(help="Manage organizers")
app.add_typer(organizers_app, name="organizers")


@organizers_app.command("list")
def list_organizers(
    output: str = typer.Option("table", help="Output format: table or json"),
):
    """List all organizers."""
    try:
        client = get_client()
        with console.status("[bold green]Fetching organizers..."):
            organizers_list = client.get_organizers()
            organizers = organizers_list.data

        if output == "json":
            _print_json([o.model_dump() for o in organizers])
            return

        table = Table(title="Eventyay Organizers")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")
        table.add_column("Description", style="white")

        for org in organizers:
            desc = org.description or ""
            if len(desc) > 50:
                desc = desc[:47] + "..."
            table.add_row(str(org.id), org.name, desc)

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@organizers_app.command("show")
def show_organizer(
    organizer_id: str,
    output: str = typer.Option("panel", help="Output format: panel or json"),
):
    """Show detailed info for an organizer."""
    try:
        client = get_client()
        with console.status(f"[bold green]Fetching organizer {organizer_id}..."):
            org = client.get_organizer(organizer_id)

        if output == "json":
            _print_json(org.model_dump())
            return

        content = f"""
[bold]ID:[/bold] {org.id}
[bold]Name:[/bold] {org.name}
[bold]Description:[/bold] {org.description or 'N/A'}
[bold]URL:[/bold] {org.url or 'N/A'}
        """
        console.print(Panel(content, title=f"Organizer: {org.name}", expand=False))

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@organizers_app.command("create")
def create_organizer(
    name: str = typer.Option(..., help="Name of the organizer"),
    description: str = typer.Option(None, help="Description of the organizer"),
    url: str = typer.Option(None, help="Website URL"),
    logo_url: str = typer.Option(None, help="Logo URL"),
):
    """Create a new organizer."""
    try:
        client = get_client()
        with console.status("[bold green]Creating organizer..."):
            org = client.create_organizer(
                name=name, description=description, url=url, logo_url=logo_url
            )

        console.print("[bold green]Organizer created successfully![/bold green]")

        content = f"""
[bold]ID:[/bold] {org.id}
[bold]Name:[/bold] {org.name}
[bold]Description:[/bold] {org.description or 'N/A'}
[bold]URL:[/bold] {org.url or 'N/A'}
        """
        console.print(Panel(content, title=f"Organizer: {org.name}", expand=False))

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@organizers_app.command("update")
def update_organizer(
    organizer_id: str = typer.Argument(..., help="ID of the organizer to update"),
    name: str = typer.Option(None, help="New name"),
    description: str = typer.Option(None, help="New description"),
    url: str = typer.Option(None, help="New website URL"),
    logo_url: str = typer.Option(None, help="New logo URL"),
):
    """Update an existing organizer."""
    try:
        client = get_client()
        with console.status(f"[bold green]Updating organizer {organizer_id}..."):
            org = client.update_organizer(
                organizer_id=organizer_id,
                name=name,
                description=description,
                url=url,
                logo_url=logo_url,
            )

        console.print("[bold green]Organizer updated successfully![/bold green]")

        content = f"""
[bold]ID:[/bold] {org.id}
[bold]Name:[/bold] {org.name}
[bold]Description:[/bold] {org.description or 'N/A'}
[bold]URL:[/bold] {org.url or 'N/A'}
        """
        console.print(Panel(content, title=f"Organizer: {org.name}", expand=False))

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@organizers_app.command("delete")
def delete_organizer(
    organizer_id: str = typer.Argument(..., help="ID of the organizer to delete"),
    force: bool = typer.Option(False, "--force", "-f", help="Force delete without confirmation"),
):
    """Delete an organizer."""
    try:
        if not force:
            if not typer.confirm(f"Are you sure you want to delete organizer {organizer_id}?"):
                console.print("Aborted.")
                raise typer.Abort()

        client = get_client()
        with console.status(f"[bold red]Deleting organizer {organizer_id}..."):
            client.delete_organizer(organizer_id)

        console.print(f"[bold green]Organizer {organizer_id} deleted successfully![/bold green]")
    except typer.Abort:
        raise
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


# ── Speakers ─────────────────────────────────────────────────

speakers_app = typer.Typer(help="Browse event speakers")
app.add_typer(speakers_app, name="speakers")


@speakers_app.command("list")
def list_speakers(
    event_id: str = typer.Argument(..., help="Event ID or identifier"),
    output: str = typer.Option("table", help="Output format: table or json"),
):
    """List speakers for an event."""
    try:
        client = get_client()
        with console.status("[bold green]Fetching speakers..."):
            speakers_list = client.get_event_speakers(event_id)
            speakers = speakers_list.data

        if output == "json":
            _print_json([s.model_dump() for s in speakers])
            return

        table = Table(title=f"Speakers — Event {event_id}")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")
        table.add_column("Email", style="green")
        table.add_column("Bio", style="white", max_width=40)

        for s in speakers:
            bio = (s.short_biography or "")[:40]
            table.add_row(str(s.id), s.name, s.email or "N/A", bio)

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@speakers_app.command("show")
def show_speaker(
    event_id: str = typer.Argument(..., help="Event ID or identifier"),
    speaker_id: str = typer.Argument(..., help="Speaker ID"),
    output: str = typer.Option("panel", help="Output format: panel or json"),
):
    """Show detailed info for a speaker."""
    try:
        client = get_client()
        with console.status(f"[bold green]Fetching speaker {speaker_id}..."):
            speaker = client.get_speaker(event_id, speaker_id)

        if output == "json":
            _print_json(speaker.model_dump())
            return

        content = f"""
[bold]ID:[/bold] {speaker.id}
[bold]Name:[/bold] {speaker.name}
[bold]Email:[/bold] {speaker.email or 'N/A'}
[bold]Bio:[/bold] {speaker.short_biography or 'N/A'}
        """
        console.print(Panel(content, title=f"Speaker: {speaker.name}", expand=False))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


# ── Sessions ─────────────────────────────────────────────────

sessions_app = typer.Typer(help="Browse event sessions")
app.add_typer(sessions_app, name="sessions")


@sessions_app.command("list")
def list_sessions(
    event_id: str = typer.Argument(..., help="Event ID or identifier"),
    output: str = typer.Option("table", help="Output format: table or json"),
):
    """List sessions for an event."""
    try:
        client = get_client()
        with console.status("[bold green]Fetching sessions..."):
            sessions_list = client.get_event_sessions(event_id)
            sessions = sessions_list.data

        if output == "json":
            _print_json([s.model_dump() for s in sessions])
            return

        table = Table(title=f"Sessions — Event {event_id}")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="magenta")
        table.add_column("Starts At", style="green")
        table.add_column("Ends At", style="yellow")

        for sess in sessions:
            table.add_row(str(sess.id), sess.title, sess.starts_at or "TBD", sess.ends_at or "TBD")

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@sessions_app.command("show")
def show_session(
    event_id: str = typer.Argument(..., help="Event ID or identifier"),
    session_id: str = typer.Argument(..., help="Session ID"),
    output: str = typer.Option("panel", help="Output format: panel or json"),
):
    """Show detailed info for a session."""
    try:
        client = get_client()
        with console.status(f"[bold green]Fetching session {session_id}..."):
            session = client.get_session(event_id, session_id)

        if output == "json":
            _print_json(session.model_dump())
            return

        desc = (session.description or "N/A")[:200]
        content = f"""
[bold]ID:[/bold] {session.id}
[bold]Title:[/bold] {session.title}
[bold]Starts:[/bold] {session.starts_at or 'TBD'}
[bold]Ends:[/bold] {session.ends_at or 'TBD'}
[bold]Description:[/bold] {desc}
        """
        console.print(Panel(content, title=f"Session: {session.title}", expand=False))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


# ── Tickets ──────────────────────────────────────────────────

tickets_app = typer.Typer(help="Browse event tickets")
app.add_typer(tickets_app, name="tickets")


@tickets_app.command("list")
def list_tickets(
    event_id: str = typer.Argument(..., help="Event identifier (slug)"),
    output: str = typer.Option("table", help="Output format: table or json"),
):
    """List tickets for an event."""
    try:
        client = get_client()
        with console.status("[bold green]Fetching tickets..."):
            tickets_list = client.get_event_tickets(event_id)
            tickets = tickets_list.data

        if output == "json":
            _print_json([t.model_dump() for t in tickets])
            return

        table = Table(title=f"Tickets — Event {event_id}")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")
        table.add_column("Type", style="yellow")
        table.add_column("Price", style="green")
        table.add_column("Qty", style="white")

        for t in tickets:
            price = f"${t.price}" if t.price else "Free"
            qty = str(t.quantity) if t.quantity else "∞"
            table.add_row(str(t.id), t.name, t.type or "N/A", price, qty)

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@tickets_app.command("show")
def show_ticket(
    event_id: str = typer.Argument(..., help="Event identifier (slug)"),
    ticket_id: str = typer.Argument(..., help="Ticket ID"),
    output: str = typer.Option("panel", help="Output format: panel or json"),
):
    """Show detailed info for a ticket."""
    try:
        client = get_client()
        with console.status(f"[bold green]Fetching ticket {ticket_id}..."):
            ticket = client.get_ticket(event_id, ticket_id)

        if output == "json":
            _print_json(ticket.model_dump())
            return

        price = f"${ticket.price}" if ticket.price else "Free"
        content = f"""
[bold]ID:[/bold] {ticket.id}
[bold]Name:[/bold] {ticket.name}
[bold]Type:[/bold] {ticket.type or 'N/A'}
[bold]Price:[/bold] {price}
[bold]Quantity:[/bold] {ticket.quantity or '∞'}
[bold]Sales Start:[/bold] {ticket.sales_starts_at or 'N/A'}
[bold]Sales End:[/bold] {ticket.sales_ends_at or 'N/A'}
[bold]Hidden:[/bold] {ticket.is_hidden}
        """
        console.print(Panel(content, title=f"Ticket: {ticket.name}", expand=False))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


# ── Attendees ────────────────────────────────────────────────

attendees_app = typer.Typer(help="Browse event attendees")
app.add_typer(attendees_app, name="attendees")


@attendees_app.command("list")
def list_attendees(
    event_id: str = typer.Argument(..., help="Event identifier"),
    output: str = typer.Option("table", help="Output format: table or json"),
):
    """List attendees for an event."""
    try:
        client = get_client()
        with console.status("[bold green]Fetching attendees..."):
            attendees_list = client.get_event_attendees(event_id)
            attendees = attendees_list.data

        if output == "json":
            _print_json([a.model_dump() for a in attendees])
            return

        table = Table(title=f"Attendees — Event {event_id}")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("First Name", style="magenta")
        table.add_column("Last Name", style="magenta")
        table.add_column("Email", style="green")
        table.add_column("Checked In", style="yellow")

        for a in attendees:
            table.add_row(
                str(a.id),
                a.firstname or "N/A",
                a.lastname or "N/A",
                a.email or "N/A",
                "✓" if a.isCheckedIn else "✗",
            )

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@attendees_app.command("show")
def show_attendee(
    event_id: str = typer.Argument(..., help="Event identifier"),
    attendee_id: str = typer.Argument(..., help="Attendee ID"),
    output: str = typer.Option("panel", help="Output format: panel or json"),
):
    """Show detailed info for an attendee."""
    try:
        client = get_client()
        with console.status(f"[bold green]Fetching attendee {attendee_id}..."):
            attendee = client.get_attendee(event_id, attendee_id)

        if output == "json":
            _print_json(attendee.model_dump())
            return

        content = f"""
[bold]ID:[/bold] {attendee.id}
[bold]First Name:[/bold] {attendee.firstname or 'N/A'}
[bold]Last Name:[/bold] {attendee.lastname or 'N/A'}
[bold]Email:[/bold] {attendee.email or 'N/A'}
[bold]Checked In:[/bold] {'Yes' if attendee.isCheckedIn else 'No'}
        """
        console.print(Panel(content, title="Attendee Details", expand=False))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


# ── Tracks ───────────────────────────────────────────────────

tracks_app = typer.Typer(help="Browse event tracks")
app.add_typer(tracks_app, name="tracks")


@tracks_app.command("list")
def list_tracks(
    event_id: str = typer.Argument(..., help="Event identifier"),
    output: str = typer.Option("table", help="Output format: table or json"),
):
    """List tracks for an event."""
    try:
        client = get_client()
        with console.status("[bold green]Fetching tracks..."):
            tracks_list = client.get_event_tracks(event_id)
            tracks = tracks_list.data

        if output == "json":
            _print_json([t.model_dump() for t in tracks])
            return

        table = Table(title=f"Tracks — Event {event_id}")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")
        table.add_column("Color", style="green")
        table.add_column("Description", style="white", max_width=40)

        for t in tracks:
            desc = (t.description or "")[:40]
            table.add_row(str(t.id), t.name, t.color or "N/A", desc)

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@tracks_app.command("show")
def show_track(
    event_id: str = typer.Argument(..., help="Event identifier"),
    track_id: str = typer.Argument(..., help="Track ID"),
    output: str = typer.Option("panel", help="Output format: panel or json"),
):
    """Show detailed info for a track."""
    try:
        client = get_client()
        with console.status(f"[bold green]Fetching track {track_id}..."):
            track = client.get_track(event_id, track_id)

        if output == "json":
            _print_json(track.model_dump())
            return

        content = f"""
[bold]ID:[/bold] {track.id}
[bold]Name:[/bold] {track.name}
[bold]Color:[/bold] {track.color or 'N/A'}
[bold]Font Color:[/bold] {track.font_color or 'N/A'}
[bold]Description:[/bold] {track.description or 'N/A'}
        """
        console.print(Panel(content, title=f"Track: {track.name}", expand=False))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


# ── Microlocations ───────────────────────────────────────────

microlocations_app = typer.Typer(help="Browse event microlocations (rooms)")
app.add_typer(microlocations_app, name="microlocations")


@microlocations_app.command("list")
def list_microlocations(
    event_id: str = typer.Argument(..., help="Event identifier"),
    output: str = typer.Option("table", help="Output format: table or json"),
):
    """List microlocations for an event."""
    try:
        client = get_client()
        with console.status("[bold green]Fetching microlocations..."):
            ml_list = client.get_event_microlocations(event_id)
            mls = ml_list.data

        if output == "json":
            _print_json([m.model_dump() for m in mls])
            return

        table = Table(title=f"Microlocations — Event {event_id}")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")
        table.add_column("Floor", style="yellow")
        table.add_column("Room", style="green")

        for m in mls:
            table.add_row(
                str(m.id),
                m.name,
                str(m.floor) if m.floor is not None else "N/A",
                m.room or "N/A",
            )

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@microlocations_app.command("show")
def show_microlocation(
    event_id: str = typer.Argument(..., help="Event identifier"),
    microlocation_id: str = typer.Argument(..., help="Microlocation ID"),
    output: str = typer.Option("panel", help="Output format: panel or json"),
):
    """Show detailed info for a microlocation."""
    try:
        client = get_client()
        with console.status(f"[bold green]Fetching microlocation {microlocation_id}..."):
            ml = client.get_microlocation(event_id, microlocation_id)

        if output == "json":
            _print_json(ml.model_dump())
            return

        content = f"""
[bold]ID:[/bold] {ml.id}
[bold]Name:[/bold] {ml.name}
[bold]Floor:[/bold] {ml.floor if ml.floor is not None else 'N/A'}
[bold]Room:[/bold] {ml.room or 'N/A'}
[bold]Latitude:[/bold] {ml.latitude or 'N/A'}
[bold]Longitude:[/bold] {ml.longitude or 'N/A'}
        """
        console.print(Panel(content, title=f"Microlocation: {ml.name}", expand=False))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


# ── Sponsors ─────────────────────────────────────────────────

sponsors_app = typer.Typer(help="Browse event sponsors")
app.add_typer(sponsors_app, name="sponsors")


@sponsors_app.command("list")
def list_sponsors(
    event_id: str = typer.Argument(..., help="Event identifier"),
    output: str = typer.Option("table", help="Output format: table or json"),
):
    """List sponsors for an event."""
    try:
        client = get_client()
        with console.status("[bold green]Fetching sponsors..."):
            sponsors_list = client.get_event_sponsors(event_id)
            sponsors = sponsors_list.data

        if output == "json":
            _print_json([s.model_dump() for s in sponsors])
            return

        table = Table(title=f"Sponsors — Event {event_id}")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")
        table.add_column("Level", style="yellow")
        table.add_column("URL", style="green", max_width=30)

        for s in sponsors:
            table.add_row(str(s.id), s.name, s.level or "N/A", s.url or "N/A")

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@sponsors_app.command("show")
def show_sponsor(
    event_id: str = typer.Argument(..., help="Event identifier"),
    sponsor_id: str = typer.Argument(..., help="Sponsor ID"),
    output: str = typer.Option("panel", help="Output format: panel or json"),
):
    """Show detailed info for a sponsor."""
    try:
        client = get_client()
        with console.status(f"[bold green]Fetching sponsor {sponsor_id}..."):
            sponsor = client.get_sponsor(event_id, sponsor_id)

        if output == "json":
            _print_json(sponsor.model_dump())
            return

        content = f"""
[bold]ID:[/bold] {sponsor.id}
[bold]Name:[/bold] {sponsor.name}
[bold]Level:[/bold] {sponsor.level or 'N/A'}
[bold]URL:[/bold] {sponsor.url or 'N/A'}
[bold]Description:[/bold] {sponsor.description or 'N/A'}
        """
        console.print(Panel(content, title=f"Sponsor: {sponsor.name}", expand=False))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


# ── Discount Codes ───────────────────────────────────────────

discount_codes_app = typer.Typer(help="Browse event discount codes")
app.add_typer(discount_codes_app, name="discount-codes")


@discount_codes_app.command("list")
def list_discount_codes(
    event_id: str = typer.Argument(..., help="Event identifier"),
    output: str = typer.Option("table", help="Output format: table or json"),
):
    """List discount codes for an event."""
    try:
        client = get_client()
        with console.status("[bold green]Fetching discount codes..."):
            codes_list = client.get_event_discount_codes(event_id)
            codes = codes_list.data

        if output == "json":
            _print_json([c.model_dump() for c in codes])
            return

        table = Table(title=f"Discount Codes — Event {event_id}")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Code", style="magenta")
        table.add_column("Type", style="yellow")
        table.add_column("Value", style="green")
        table.add_column("Active", style="white")

        for c in codes:
            table.add_row(
                str(c.id),
                c.code,
                c.type or "N/A",
                str(c.value) if c.value else "N/A",
                "✓" if c.is_active else "✗",
            )

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@discount_codes_app.command("show")
def show_discount_code(
    event_id: str = typer.Argument(..., help="Event identifier"),
    code_id: str = typer.Argument(..., help="Discount code ID"),
    output: str = typer.Option("panel", help="Output format: panel or json"),
):
    """Show detailed info for a discount code."""
    try:
        client = get_client()
        with console.status(f"[bold green]Fetching discount code {code_id}..."):
            code = client.get_discount_code(event_id, code_id)

        if output == "json":
            _print_json(code.model_dump())
            return

        content = f"""
[bold]ID:[/bold] {code.id}
[bold]Code:[/bold] {code.code}
[bold]Type:[/bold] {code.type or 'N/A'}
[bold]Value:[/bold] {code.value or 'N/A'}
[bold]Active:[/bold] {'Yes' if code.is_active else 'No'}
[bold]Valid From:[/bold] {code.valid_from or 'N/A'}
[bold]Valid Till:[/bold] {code.valid_till or 'N/A'}
        """
        console.print(Panel(content, title=f"Discount Code: {code.code}", expand=False))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


# ── Orders ───────────────────────────────────────────────────

orders_app = typer.Typer(help="Browse event orders")
app.add_typer(orders_app, name="orders")


@orders_app.command("list")
def list_orders(
    event_id: str = typer.Argument(..., help="Event identifier"),
    output: str = typer.Option("table", help="Output format: table or json"),
):
    """List orders for an event."""
    try:
        client = get_client()
        with console.status("[bold green]Fetching orders..."):
            orders_list = client.get_event_orders(event_id)
            orders = orders_list.data

        if output == "json":
            _print_json([o.model_dump() for o in orders])
            return

        table = Table(title=f"Orders — Event {event_id}")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Identifier", style="magenta")
        table.add_column("Status", style="yellow")
        table.add_column("Amount", style="green")
        table.add_column("Paid Via", style="white")

        for o in orders:
            table.add_row(
                str(o.id),
                o.identifier or "N/A",
                o.status or "N/A",
                f"${o.amount}" if o.amount else "Free",
                o.paid_via or "N/A",
            )

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@orders_app.command("show")
def show_order(
    event_id: str = typer.Argument(..., help="Event identifier"),
    order_id: str = typer.Argument(..., help="Order identifier"),
    output: str = typer.Option("panel", help="Output format: panel or json"),
):
    """Show detailed info for an order."""
    try:
        client = get_client()
        with console.status(f"[bold green]Fetching order {order_id}..."):
            order = client.get_order(event_id, order_id)

        if output == "json":
            _print_json(order.model_dump())
            return

        content = f"""
[bold]ID:[/bold] {order.id}
[bold]Identifier:[/bold] {order.identifier or 'N/A'}
[bold]Status:[/bold] {order.status or 'N/A'}
[bold]Amount:[/bold] {'$' + str(order.amount) if order.amount else 'Free'}
[bold]Paid Via:[/bold] {order.paid_via or 'N/A'}
[bold]Created:[/bold] {order.created_at or 'N/A'}
[bold]Completed:[/bold] {order.completed_at or 'N/A'}
        """
        console.print(Panel(content, title=f"Order: {order.identifier}", expand=False))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


# ── Tax ──────────────────────────────────────────────────────

tax_app = typer.Typer(help="View event tax configuration")
app.add_typer(tax_app, name="tax")


@tax_app.command("show")
def show_tax(
    event_id: str = typer.Argument(..., help="Event identifier"),
    output: str = typer.Option("panel", help="Output format: panel or json"),
):
    """Show tax configuration for an event."""
    try:
        client = get_client()
        with console.status(f"[bold green]Fetching tax for event {event_id}..."):
            tax = client.get_event_tax(event_id)

        if output == "json":
            _print_json(tax.model_dump())
            return

        content = f"""
[bold]ID:[/bold] {tax.id}
[bold]Name:[/bold] {tax.name or 'N/A'}
[bold]Rate:[/bold] {tax.rate}%
[bold]Included in Price:[/bold] {'Yes' if tax.is_tax_included_in_price else 'No'}
[bold]Country:[/bold] {tax.country or 'N/A'}
        """
        console.print(Panel(content, title=f"Tax: {tax.name}", expand=False))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


# ── Users ────────────────────────────────────────────────────

users_app = typer.Typer(help="Manage users (admin)")
app.add_typer(users_app, name="users")


@users_app.command("list")
def list_users(
    output: str = typer.Option("table", help="Output format: table or json"),
):
    """List all users (requires admin)."""
    try:
        client = get_client()
        with console.status("[bold green]Fetching users..."):
            users_list = client.get_users()
            users = users_list.data

        if output == "json":
            _print_json([u.model_dump() for u in users])
            return

        table = Table(title="Eventyay Users")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Email", style="magenta")
        table.add_column("First Name", style="green")
        table.add_column("Last Name", style="green")

        for u in users:
            table.add_row(
                str(u.id),
                u.email or "N/A",
                u.first_name or "N/A",
                u.last_name or "N/A",
            )

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@users_app.command("show")
def show_user(
    user_id: str = typer.Argument(..., help="User ID (or 'me')"),
    output: str = typer.Option("panel", help="Output format: panel or json"),
):
    """Show detailed info for a user."""
    try:
        client = get_client()
        with console.status(f"[bold green]Fetching user {user_id}..."):
            user = client.get_user(user_id)

        if output == "json":
            _print_json(user.model_dump())
            return

        content = f"""
[bold]ID:[/bold] {user.id}
[bold]Email:[/bold] {user.email or 'N/A'}
[bold]First Name:[/bold] {user.first_name or 'N/A'}
[bold]Last Name:[/bold] {user.last_name or 'N/A'}
[bold]Contact:[/bold] {user.contact or 'N/A'}
        """
        console.print(Panel(content, title=f"User: {user.email}", expand=False))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


# ── Roles ────────────────────────────────────────────────────

roles_app = typer.Typer(help="Browse event roles")
app.add_typer(roles_app, name="roles")


@roles_app.command("list")
def list_roles(
    event_id: str = typer.Argument(..., help="Event identifier"),
    output: str = typer.Option("table", help="Output format: table or json"),
):
    """List roles for an event."""
    try:
        client = get_client()
        with console.status("[bold green]Fetching roles..."):
            roles_list = client.get_event_roles(event_id)
            roles = roles_list.data

        if output == "json":
            _print_json([r.model_dump() for r in roles])
            return

        table = Table(title=f"Roles — Event {event_id}")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")
        table.add_column("Title", style="green")

        for r in roles:
            table.add_row(str(r.id), r.name, r.title_name or "N/A")

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@roles_app.command("show")
def show_role(
    event_id: str = typer.Argument(..., help="Event identifier"),
    role_id: str = typer.Argument(..., help="Role ID"),
    output: str = typer.Option("panel", help="Output format: panel or json"),
):
    """Show detailed info for a role."""
    try:
        client = get_client()
        with console.status(f"[bold green]Fetching role {role_id}..."):
            role = client.get_role(event_id, role_id)

        if output == "json":
            _print_json(role.model_dump())
            return

        content = f"""
[bold]ID:[/bold] {role.id}
[bold]Name:[/bold] {role.name}
[bold]Title:[/bold] {role.title_name or 'N/A'}
        """
        console.print(Panel(content, title=f"Role: {role.name}", expand=False))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


# ── Feedbacks ────────────────────────────────────────────────

feedbacks_app = typer.Typer(help="Browse event feedbacks")
app.add_typer(feedbacks_app, name="feedbacks")


@feedbacks_app.command("list")
def list_feedbacks(
    event_id: str = typer.Argument(..., help="Event identifier"),
    output: str = typer.Option("table", help="Output format: table or json"),
):
    """List feedbacks for an event."""
    try:
        client = get_client()
        with console.status("[bold green]Fetching feedbacks..."):
            feedbacks_list = client.get_event_feedbacks(event_id)
            feedbacks = feedbacks_list.data

        if output == "json":
            _print_json([f.model_dump() for f in feedbacks])
            return

        table = Table(title=f"Feedbacks — Event {event_id}")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Rating", style="yellow")
        table.add_column("Comment", style="white", max_width=50)

        for fb in feedbacks:
            comment = (fb.comment or "")[:50]
            table.add_row(
                str(fb.id),
                str(fb.rating) if fb.rating is not None else "N/A",
                comment,
            )

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@feedbacks_app.command("show")
def show_feedback(
    event_id: str = typer.Argument(..., help="Event identifier"),
    feedback_id: str = typer.Argument(..., help="Feedback ID"),
    output: str = typer.Option("panel", help="Output format: panel or json"),
):
    """Show detailed info for a feedback entry."""
    try:
        client = get_client()
        with console.status(f"[bold green]Fetching feedback {feedback_id}..."):
            fb = client.get_feedback(event_id, feedback_id)

        if output == "json":
            _print_json(fb.model_dump())
            return

        content = f"""
[bold]ID:[/bold] {fb.id}
[bold]Rating:[/bold] {fb.rating or 'N/A'}
[bold]Comment:[/bold] {fb.comment or 'N/A'}
[bold]Session ID:[/bold] {fb.session_id or 'N/A'}
        """
        console.print(Panel(content, title="Feedback Details", expand=False))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


# ── Settings ─────────────────────────────────────────────────

settings_app = typer.Typer(help="View platform settings")
app.add_typer(settings_app, name="settings")


@settings_app.command("list")
def list_settings(
    output: str = typer.Option("table", help="Output format: table or json"),
):
    """List platform settings."""
    try:
        client = get_client()
        with console.status("[bold green]Fetching settings..."):
            settings_list = client.get_settings()
            settings = settings_list.data

        if output == "json":
            _print_json([s.model_dump() for s in settings])
            return

        table = Table(title="Eventyay Settings")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("App Name", style="magenta")
        table.add_column("Environment", style="yellow")
        table.add_column("Frontend URL", style="green")

        for s in settings:
            table.add_row(
                str(s.id),
                s.app_name or "N/A",
                s.app_environment or "N/A",
                s.frontend_url or "N/A",
            )

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@settings_app.command("show")
def show_setting(
    setting_id: str = typer.Argument(..., help="Setting ID"),
    output: str = typer.Option("panel", help="Output format: panel or json"),
):
    """Show detailed info for a setting."""
    try:
        client = get_client()
        with console.status(f"[bold green]Fetching setting {setting_id}..."):
            setting = client.get_setting(setting_id)

        if output == "json":
            _print_json(setting.model_dump())
            return

        content = f"""
[bold]ID:[/bold] {setting.id}
[bold]App Name:[/bold] {setting.app_name or 'N/A'}
[bold]Environment:[/bold] {setting.app_environment or 'N/A'}
[bold]Frontend URL:[/bold] {setting.frontend_url or 'N/A'}
        """
        console.print(Panel(content, title="Setting Details", expand=False))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


# ── Entry Point ──────────────────────────────────────────────

if __name__ == "__main__":
    app()
