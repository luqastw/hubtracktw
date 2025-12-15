from pydantic import BaseModel, ConfigDict
from datetime import datetime

class RepositoryBase(BaseModel):
    name: str
    owner: str
    url: str

class RepositoryCreate(RepositoryBase):
    pass

class RepositoryResponse(RepositoryBase):
    id: int
    description: str | None = None
    stars: int = 0
    language: str | None = None
    created_at: datetime | None
    last_analyzed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)