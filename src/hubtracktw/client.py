from typing import Optional
import httpx


class GitHubClient:
    def __init__(self, base_url: str, token: Optional[str] = None):
        self.base_url = base_url
        self.token = token

    def get_repo(self, owner: str, name: str):
        response = httpx.get(f"{self.base_url}/repos/{owner}/{name}")
        response.raise_for_status()
        data = response.json()
        return data
