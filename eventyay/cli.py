import typer
from rich.console import Console
from rich.panel import Panel
from eventyay.client import EventyayClient
import eventyay

app = typer.Typer(help="Eventyay CLI Tool")
console = Console()

@app.command()
def version():
    """Show the CLI version."""
    console.print(Panel(f"Eventyay CLI v0.1.0", title="Version", style="bold green"))

if __name__ == "__main__":
    app()
