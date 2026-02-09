from typing import Optional
import httpx

from hubtracktw.models import Repo


class GitHubClient:
    def __init__(self, base_url: str, token: Optional[str] = None):
        self.base_url = base_url
        self.token = token

    def get_repo(self, owner: str, name: str):
        response = httpx.get(f"{self.base_url}/repos/{owner}/{name}")
        response.raise_for_status()
        data = response.json()
        repo = Repo(
            full_name=data["full_name"],
            stars=data["stargazers_count"],
            forks=data["forks_count"],
            open_issues=data["open_issues_count"],
            language=data["language"],
        )
        return repo
