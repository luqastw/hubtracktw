from fastapi import FastAPI
from src.api.v1.endpoints import repository
from src.core.config import settings

docs_url = "/docs" if settings.ENVIRONMENT == "development" else None
redoc_url = "/redoc" if settings.ENVIRONMENT == "development" else None

app = FastAPI(title="HubTrack", docs_url=docs_url, redoc_url=redoc_url)

app.include_router(repository.router, prefix="/repositories", tags=["Repositories"])

@app.get("/")
async def root():
    return {"message": "System is running. 🚀"}