from fastapi import FastAPI
from src.api.v1.endpoints import repository

app = FastAPI(title="HubTrack")

app.include_router(repository.router, prefix="/repositories", tags=["Repositories"])

@app.get("/")
async def root():
    return {"message": "System is running. 🚀"}