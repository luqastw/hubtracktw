import httpx
from fastapi import HTTPException, status

class GitHubClient:
    BASE_URL = 'https://api.github.com/repos'

    async def get_repo_info(self, owner: str, repo_name: str) -> dict:
        async with httpx.AsyncClient() as client:
            url = f'{self.BASE_URL}/{owner}/{repo_name}'

            try:
                response = await client.get(url, timeout=10.0)
            except httpx.RequestError:
                raise HTTPException(status_code=503, detail='Conection with GitHub failed.')
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail='Repository not found.')
            if response.status_code != 200:
                raise HTTPException(status_code=502, detail='Failed to connect with API.')
            
            return response.json()
        
    @staticmethod
    def extract_owner_and_name(url: str) -> tuple[str, str]:
        clean_url = url.rstrip('/').replace('.git', '')
        parts = clean_url.split('/')

        if len(parts) < 2:
            raise HTTPException(status_code=400, detail='Invalid URL. Use the model: https://github.com/owner/repo')
            
        repo_name = parts[-1]
        owner = parts[-2]

        return owner, repo_name