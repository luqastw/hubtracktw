from rich.table import Table
from rich.console import Console
import typer

from hubtracktw.client import GitHubClient

app = typer.Typer()
console = Console()


@app.command()
def ping():
    print("Pong.")


@app.command()
def analyze(repo: str):
    owner, name = repo.split("/")
    client = GitHubClient("https://api.github.com")

    repo = client.get_repo(owner, name)

    table = Table(title="hubtracktw")
    table.add_column("Metric")
    table.add_column("Value")
    table.add_row("Name", repo.full_name)
    table.add_row("Stars", str(repo.stars))
    table.add_row("Forks", str(repo.forks))
    table.add_row("Issues", str(repo.open_issues))
    table.add_row("Language", repo.language or "N/A")
    console.print(table)
