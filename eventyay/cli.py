import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from eventyay.client import EventyayClient

app = typer.Typer(help="Eventyay CLI Tool")
console = Console()

# Initialize client (todo: add config for api key)
client = EventyayClient()


@app.command()
def version():
    """Show the CLI version."""
    console.print(Panel("Eventyay CLI v0.1.0", title="Version", style="bold green"))


events_app = typer.Typer(help="Manage events")
app.add_typer(events_app, name="events")


@events_app.command("list")
def list_events(public: bool = True):
    """List all events."""
    try:
        with console.status("[bold green]Fetching events..."):
            # We use get_events() which returns EventList object
            events_list = client.get_events()
            events = events_list.data

        table = Table(title="Eventyay Events")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")
        table.add_column("Start Time", style="green")
        table.add_column("Privacy", style="yellow")

        for event in events:
            # Pydantic models in action!
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
def show_event(event_id: int):
    """Show detailed info for an event."""
    try:
        with console.status(f"[bold green]Fetching event {event_id}..."):
            event = client.get_event(event_id)

        # Create a detailed view using Rich Panel
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

        console.print(f"[bold green]Event created successfully![/bold green]")

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
    force: bool = typer.Option(
        False, "--force", "-f", help="Force delete without confirmation"
    ),
):
    """Delete an event."""
    try:
        if not force:
            if not typer.confirm(f"Are you sure you want to delete event {event_id}?"):
                console.print("Aborted.")
                raise typer.Abort()

        with console.status(f"[bold red]Deleting event {event_id}..."):
            client.delete_event(event_id)

        console.print(
            f"[bold green]Event {event_id} deleted successfully![/bold green]"
        )
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

        console.print(f"[bold green]Event updated successfully![/bold green]")

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


organizers_app = typer.Typer(help="Manage organizers")
app.add_typer(organizers_app, name="organizers")


@organizers_app.command("list")
def list_organizers():
    """List all organizers."""
    try:
        with console.status("[bold green]Fetching organizers..."):
            organizers_list = client.get_organizers()
            organizers = organizers_list.data

        table = Table(title="Eventyay Organizers")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")
        table.add_column("Description", style="white")

        for org in organizers:
            desc = org.description or ""
            # Truncate description if too long
            if len(desc) > 50:
                desc = desc[:47] + "..."

            table.add_row(str(org.id), org.name, desc)

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@organizers_app.command("show")
def show_organizer(organizer_id: str):
    """Show detailed info for an organizer."""
    try:
        with console.status(f"[bold green]Fetching organizer {organizer_id}..."):
            org = client.get_organizer(organizer_id)

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
        with console.status("[bold green]Creating organizer..."):
            org = client.create_organizer(
                name=name, description=description, url=url, logo_url=logo_url
            )

        console.print(f"[bold green]Organizer created successfully![/bold green]")

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
        with console.status(f"[bold green]Updating organizer {organizer_id}..."):
            org = client.update_organizer(
                organizer_id=organizer_id,
                name=name,
                description=description,
                url=url,
                logo_url=logo_url,
            )

        console.print(f"[bold green]Organizer updated successfully![/bold green]")

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
    force: bool = typer.Option(
        False, "--force", "-f", help="Force delete without confirmation"
    ),
):
    """Delete an organizer."""
    try:
        if not force:
            if not typer.confirm(
                f"Are you sure you want to delete organizer {organizer_id}?"
            ):
                console.print("Aborted.")
                raise typer.Abort()

        with console.status(f"[bold red]Deleting organizer {organizer_id}..."):
            client.delete_organizer(organizer_id)

        console.print(
            f"[bold green]Organizer {organizer_id} deleted successfully![/bold green]"
        )
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


# ── Speakers ─────────────────────────────────────────────────
speakers_app = typer.Typer(help="Browse event speakers")
app.add_typer(speakers_app, name="speakers")


@speakers_app.command("list")
def list_speakers(event_id: str = typer.Argument(..., help="Event ID or identifier")):
    """List speakers for an event."""
    try:
        with console.status("[bold green]Fetching speakers..."):
            speakers_list = client.get_event_speakers(event_id)
            speakers = speakers_list.data

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
):
    """Show detailed info for a speaker."""
    try:
        with console.status(f"[bold green]Fetching speaker {speaker_id}..."):
            speaker = client.get_speaker(event_id, speaker_id)

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
def list_sessions(event_id: str = typer.Argument(..., help="Event ID or identifier")):
    """List sessions for an event."""
    try:
        with console.status("[bold green]Fetching sessions..."):
            sessions_list = client.get_event_sessions(event_id)
            sessions = sessions_list.data

        table = Table(title=f"Sessions — Event {event_id}")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="magenta")
        table.add_column("Starts At", style="green")
        table.add_column("Ends At", style="yellow")

        for sess in sessions:
            table.add_row(
                str(sess.id), sess.title, sess.starts_at or "TBD", sess.ends_at or "TBD"
            )

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@sessions_app.command("show")
def show_session(
    event_id: str = typer.Argument(..., help="Event ID or identifier"),
    session_id: str = typer.Argument(..., help="Session ID"),
):
    """Show detailed info for a session."""
    try:
        with console.status(f"[bold green]Fetching session {session_id}..."):
            session = client.get_session(event_id, session_id)

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
def list_tickets(event_id: str = typer.Argument(..., help="Event identifier (slug)")):
    """List tickets for an event."""
    try:
        with console.status("[bold green]Fetching tickets..."):
            tickets_list = client.get_event_tickets(event_id)
            tickets = tickets_list.data

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
):
    """Show detailed info for a ticket."""
    try:
        with console.status(f"[bold green]Fetching ticket {ticket_id}..."):
            ticket = client.get_ticket(event_id, ticket_id)

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


if __name__ == "__main__":
    app()
