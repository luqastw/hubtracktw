import typer

from hubtracktw.client import GitHubClient

app = typer.Typer()


@app.command()
def ping():
    print("Pong.")


@app.command()
def analyze(repo: str):
    owner, name = repo.split("/")
    client = GitHubClient("https://api.github.com")

    data = client.get_repo(owner, name)
    print(f"{data['full_name']} {data['stargazers_count']}")
