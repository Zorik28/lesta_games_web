from fastapi.templating import Jinja2Templates


# Указываем директорию, где хранятся шаблоны
templates = Jinja2Templates(directory="templates")

db = []  # Имитация базы данных
TF = 0    # term-frequency dict
IDF = 1   # sorted inverse_document_frequency list
