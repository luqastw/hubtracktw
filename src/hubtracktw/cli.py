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

    data = client.get_repo(owner, name)
    print(f"{data['full_name']} {data['stargazers_count']}")

    table = Table(title="hubtracktw")
    table.add_column("Metric")
    table.add_column("Value")
    table.add_row("Name", data["full_name"])
    table.add_row("Stars", str(data["stargazers_count"]))
    table.add_row("Forks", str(data["forks_count"]))
    table.add_row("Issues", str(data["open_issues_count"]))
    table.add_row("Language", data["language"])
    console.print(table)
