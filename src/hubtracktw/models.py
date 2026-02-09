from dataclasses import dataclass
from typing import Optional


@dataclass
class Repo:
    full_name: str
    stars: int
    forks: int
    open_issues: int
    language: Optional[str] = None
