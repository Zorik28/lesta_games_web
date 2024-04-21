from fastapi import FastAPI
from fastapi.responses import FileResponse


lesta_games = FastAPI()


@lesta_games.get('/', response_class=FileResponse)
async def get_root():
    return FileResponse("upload.html")
