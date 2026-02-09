from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Repo:
    full_name: str
    description: str
    stars: int
    forks: int
    open_issues: int
    watchers: int
    created_at: str
    pushed_at: str
    default_branch: str
    language: Optional[str] = None
    archived: bool = False
    languages: dict[str, int] = field(default_factory=dict)
    contributors_count: int = 0
    latest_release: Optional[str] = None
