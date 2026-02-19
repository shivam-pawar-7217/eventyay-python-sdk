import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from eventyay.client import EventyayClient
import eventyay

app = typer.Typer(help="Eventyay CLI Tool")
console = Console()

# Initialize client (todo: add config for api key)
client = EventyayClient()

@app.command()
def version():
    """Show the CLI version."""
    console.print(Panel(f"Eventyay CLI v0.1.0", title="Version", style="bold green"))

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
                event.privacy or "N/A"
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
    online: bool = typer.Option(False, help="Is the event online?")
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
                online=online
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

@events_app.command("update")
def update_event(
    event_id: int = typer.Argument(..., help="ID of the event to update"),
    name: str = typer.Option(None, help="New name"),
    starts_at: str = typer.Option(None, help="New start time"),
    ends_at: str = typer.Option(None, help="New end time"),
    timezone: str = typer.Option(None, help="New timezone"),
    privacy: str = typer.Option(None, help="New privacy setting"),
    location: str = typer.Option(None, help="New location name")
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
                location_name=location
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
                
            table.add_row(
                str(org.id), 
                org.name, 
                desc
            )

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
    logo_url: str = typer.Option(None, help="Logo URL")
):
    """Create a new organizer."""
    try:
        with console.status("[bold green]Creating organizer..."):
            org = client.create_organizer(
                name=name,
                description=description,
                url=url,
                logo_url=logo_url
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
    logo_url: str = typer.Option(None, help="New logo URL")
):
    """Update an existing organizer."""
    try:
        with console.status(f"[bold green]Updating organizer {organizer_id}..."):
            org = client.update_organizer(
                organizer_id=organizer_id,
                name=name,
                description=description,
                url=url,
                logo_url=logo_url
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

if __name__ == "__main__":
    app()
