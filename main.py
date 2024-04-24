from http import HTTPStatus

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse


from config import db, IDF, templates, TF
from services import (
    get_text, inverse_document_frequency, paginator, term_frequency
)


app = FastAPI()


@app.get('/', response_class=HTMLResponse)
async def get_root(request: Request):
    """Обработчик для начальной страницы."""
    return templates.TemplateResponse(request=request, name="index.html")


@app.post('/uploadfile', response_class=RedirectResponse)
async def handle_upload(file: UploadFile = File()):
    """Обработчик файла, который клиент загрузил."""
    text = await get_text(file)
    tf = await term_frequency(text)
    idf = await inverse_document_frequency(tf)
    db.append(tf)   # записываем в БД
    db.append(idf)  # записываем в БД
    return RedirectResponse(url="/result", status_code=HTTPStatus.SEE_OTHER)


@app.get('/result', response_class=HTMLResponse)
async def get_result(request: Request, page: int = 1, size: int = 10):
    """Вывод таблицы с отсортированным IDF."""
    paginated_idf, total_pages = await paginator(page, size, db[IDF])
    context = {
        "words": paginated_idf,
        "tf": db[TF],
        "page": page,
        "size": size,
        "total_pages": total_pages
    }
    return templates.TemplateResponse(
        request=request, name="result.html", context=context
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request, exc: HTTPException
) -> HTMLResponse:
    """Обработчик исключений."""
    return templates.TemplateResponse(request=request, name="error.html")
