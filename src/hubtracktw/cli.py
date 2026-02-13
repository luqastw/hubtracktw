from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
import typer
import httpx

from hubtracktw.client import GitHubClient

app = typer.Typer()
console = Console()

FILLED = "▓"
EMPTY = "░"
BAR_WIDTH = 10


def _parse_repo(repo: str) -> tuple[str, str]:
    if "/" in repo:
        if repo.startswith("http"):
            repo = repo.rstrip("/")
            parses = repo.rsplit("/", 2)
            owner = parses[1]
            name = parses[2]
            return owner, name
        else:
            owner, name = repo.split("/")
            return owner, name
    else:
        raise ValueError(f"Invalid format: {repo}. Use 'owner/name' or a GitHub URL.")


def _format_number(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}k"
    return str(n)


def _progress_bar(percentage: float) -> str:
    filled = round(percentage / 100 * BAR_WIDTH)
    return f"{FILLED * filled}{EMPTY * (BAR_WIDTH - filled)} {percentage:.0f}%"


def _time_ago(iso_date: str) -> str:
    from datetime import datetime, timezone

    dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    delta = datetime.now(timezone.utc) - dt
    if delta.days > 365:
        return f"{delta.days // 365}y ago"
    if delta.days > 30:
        return f"{delta.days // 30}mo ago"
    if delta.days > 0:
        return f"{delta.days}d ago"
    return "today"


@app.command()
def ping():
    print("Pong.")


@app.command()
def analyze(repo: str):
    owner, name = _parse_repo(repo)
    client = GitHubClient("https://api.github.com")

    with console.status("[bold green]Fetching data from GitHub..."):
        try:
            repo_data = client.get_repo(owner, name)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                console.print("[red]Repository not found.[/red]")
                raise typer.Exit(1)

    title = Text()
    title.append(f"  {repo_data.full_name.upper()}", style="bold cyan")
    if repo_data.archived:
        title.append("  [ARCHIVED]", style="bold red")

    sections = []
    if repo_data.description:
        sections.append(f"  [dim]{repo_data.description}[/dim]\n")

    if repo_data.languages:
        total_bytes = sum(repo_data.languages.values())
        lang_table = Table(
            box=box.SIMPLE_HEAVY,
            show_header=True,
            header_style="bold white",
            padding=(0, 2),
        )
        lang_table.add_column("Language", style="bold")
        lang_table.add_column("Bytes", justify="right")
        lang_table.add_column("Distribution", min_width=18)

        for lang, bytes_count in sorted(
            repo_data.languages.items(), key=lambda x: x[1], reverse=True
        )[:6]:
            pct = (bytes_count / total_bytes) * 100
            lang_table.add_row(
                lang,
                _format_number(bytes_count),
                _progress_bar(pct),
            )

        sections.append("  [bold white]CODEBASE[/bold white]")

    activity_line = (
        f"  [bold white]ACTIVITY[/bold white]\n"
        f"  Last push: [cyan]{_time_ago(repo_data.pushed_at)}[/cyan]  │  "
        f"Created: [cyan]{_time_ago(repo_data.created_at)}[/cyan]  │  "
        f"Branch: [cyan]{repo_data.default_branch}[/cyan]"
    )

    release_tag = repo_data.latest_release or "N/A"
    footer = (
        f"  👥 Contributors: [bold]{repo_data.contributors_count}[/bold]  │  "
        f"⭐ [bold]{_format_number(repo_data.stars)}[/bold]  │  "
        f"🔱 [bold]{_format_number(repo_data.forks)}[/bold]  │  "
        f"🐛 Issues: [bold]{_format_number(repo_data.open_issues)}[/bold]  │  "
        f"📦 [bold]{release_tag}[/bold]"
    )

    output = Text()
    panel_content = "\n".join(sections)
    panel_content += "\n"

    console.print()
    console.print(Panel(title, box=box.DOUBLE, style="cyan", expand=True))

    for section in sections:
        console.print(section)
    if repo_data.languages:
        console.print(lang_table)
        console.print()

    console.print(activity_line)
    console.print()
    console.print(Panel(footer, box=box.HEAVY, style="dim", expand=True))
    console.print()
