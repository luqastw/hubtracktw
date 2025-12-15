from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select
from src.models.repository import RepositoryModel
from src.schemas.repository import RepositoryCreate, RepositoryResponse
from src.api.deps import SessionDep
from src.services.github_client import GitHubClient

router = APIRouter()

@router.post("/", response_model=RepositoryResponse, status_code=status.HTTP_201_CREATED)
async def create_repository(repo_in: RepositoryCreate, db: SessionDep):

    query = select(RepositoryModel).where(RepositoryModel.url == repo_in.url)
    existing = await db.execute(query)
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail='This repository has already registered.')
    
    gh_client = GitHubClient()
    owner, name = gh_client.extract_owner_and_name(repo_in.url)

    repo_data = await gh_client.get_repo_info(owner, name)

    new_repo = RepositoryModel(
        url = repo_in.url,
        name = name,
        owner = owner,
        description = repo_data.get('description'),
        stars = repo_data.get('stargazers_count', 0),
        language = repo_data.get('language')
    )

    db.add(new_repo)
    await db.commit()
    await db.refresh(new_repo)
    
    return new_repo