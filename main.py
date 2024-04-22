from http import HTTPStatus
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates


# Создание объекта приложения.
lesta_games = FastAPI()
# Указываем директорию, где хранятся шаблоны
templates = Jinja2Templates(directory="templates")


# Декоратор, определяющий, что GET-запросы к основному URL приложения
# должны обрабатываться этой функцией.
@lesta_games.get('/') ________________________________________Response class o model?
async def get_root(request: Request): ________________________Возвращает что?
    # Возвращаем шаблон
    return templates.TemplateResponse(request=request, name="upload.html")


@lesta_games.post('/uploadfile')
async def handle_upload(file: UploadFile = File(...)): ___________фильтрация по файлу
    try:
        # Пытаемся декодировать содержимое файла как текст в UTF-8
        content = await file.read()
        content.decode()
    except UnicodeDecodeError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
    return content


@lesta_games.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse(request=request, name="400.html")
