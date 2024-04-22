from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from services import (
    get_text, inverse_document_frequency, sort_idf, term_frequency
)


app = FastAPI()
# Указываем директорию, где хранятся шаблоны
templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse)
async def get_root(request: Request):
    """Обработчик для начальной страницы."""
    return templates.TemplateResponse(request=request, name="upload.html")


@app.post('/uploadfile', response_class=HTMLResponse)
async def handle_upload(request: Request, file: UploadFile = File()):
    """Обработчик кнопки 'Submit'."""
    text = await get_text(file)
    tf = await term_frequency(text)
    idf = await inverse_document_frequency(tf)
    sorted_idf = await sort_idf(idf)
    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "words": sorted_idf,
            "tf": tf,
            "idf": sorted_idf
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request, exc: HTTPException
) -> HTMLResponse:
    """Обработчик исключений."""
    return templates.TemplateResponse(request=request, name="400.html")
