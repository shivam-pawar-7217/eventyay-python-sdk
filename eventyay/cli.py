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

if __name__ == "__main__":
    app()
