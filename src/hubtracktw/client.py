import httpx

from hubtracktw.models import Repo


class GitHubClient:
    def __init__(self, base_url: str, token: str | None = None):
        self.base_url = base_url
        self.token = token
        self.headers = {}
        if token:
            self.headers["Authorization"] = f"token {token}"

    def _get(self, endpoint: str) -> dict | list:
        response = httpx.get(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    def get_repo(self, owner: str, name: str) -> Repo:
        data = self._get(f"/repos/{owner}/{name}")
        languages = self._get(f"/repos/{owner}/{name}/languages")

        contributors_count = 0
        try:
            contributors = self._get(
                f"/repos/{owner}/{name}/contributors?per_page=1&anon=true"
            )
            contributors_count = len(contributors)
        except httpx.HTTPStatusError:
            pass

        latest_release = None
        try:
            release_data = self._get(f"/repos/{owner}/{name}/releases/latest")
            latest_release = release_data.get("tag_name")
        except httpx.HTTPStatusError:
            pass

        return Repo(
            full_name=data["full_name"],
            description=data.get("description") or "",
            stars=data["stargazers_count"],
            forks=data["forks_count"],
            open_issues=data["open_issues_count"],
            watchers=data["watchers_count"],
            created_at=data["created_at"],
            pushed_at=data["pushed_at"],
            default_branch=data["default_branch"],
            language=data.get("language"),
            archived=data.get("archived", False),
            languages=languages,
            contributors_count=contributors_count,
            latest_release=latest_release,
        )
