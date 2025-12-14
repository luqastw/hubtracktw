from fastapi import APIRouter, status
from sqlalchemy import select
from src.models.repository import RepositoryModel
from src.schemas.repository import RepositoryCreate, RepositoryResponse
from src.api.deps import SessionDep

router = APIRouter()

@router.post("/", response_model=RepositoryResponse, status_code=status.HTTP_201_CREATED)
async def create_repository(repo_in: RepositoryCreate, db: SessionDep):
    new_repo = RepositoryModel(**repo_in.model_dump())
    db.add(new_repo)
    await db.commit()
    await db.refresh(new_repo)
    return new_repo