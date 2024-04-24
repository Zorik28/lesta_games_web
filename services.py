import math
import random
import re
from collections import Counter
from http import HTTPStatus
from typing import Iterable

from fastapi import UploadFile, HTTPException


async def get_text(file: UploadFile) -> str:
    """Проверяем является ли документ текстовым и возвращаем текст."""
    try:
        # Пытаемся декодировать содержимое файла как текст в UTF-8
        content = await file.read()
        text = content.decode()
    except UnicodeDecodeError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
    finally:
        await file.close()

    return text


async def term_frequency(text: str) -> Counter:
    """Считет кол-во слов и частоту вхождения каждого слова(TF)."""
    # находим в тексте все слова
    split_text = re.findall(r'\b[^\d\W]+\b', text)
    if len(split_text) < 1:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
    # считаем кол-во уникальных вхождений записывая в словарь
    word_tf = Counter(split_text)
    total = word_tf.total()

    # находим TF для каждого слова
    for word in word_tf:
        word_tf[word] /= total

    return word_tf


async def inverse_document_frequency(words: Counter) -> list[tuple[str, int]]:
    """Вычисляем обратную частоту документов(IDF)."""
    dict_idf = {}             # Словарь для idf
    total_docs = 100_000_000  # Для демонстрации количество документов 100млн
    for word in words:
        # docs_with_word - якобы кол-во документов с конкретным словом.
        # Переменная должна содержать запись из БД,
        # к которой прибавляем дополнительное вхождение
        docs_with_word = random.randint(0, 3000) + 1
        idf = math.log10(total_docs/docs_with_word)
        dict_idf[word] = idf  # записываем в словарь idf

    # Сортировка словаря c idf по значениям в обратном порядке
    sorted_idf = sorted(
        dict_idf.items(), key=lambda item: item[1], reverse=True
    )
    return sorted_idf[:50]  # Возвращаем первые 50 элементов


async def paginator(
    page: int, size: int, data: Iterable
) -> tuple[Iterable, int]:
    """Постраничный вывод данных."""
    start = (page - 1) * size
    end = start + size
    items = data[start:end]
    total_pages = math.ceil(len(data) / size)  # округляем до страницы
    # Проверка на выход за пределы диапазона страниц
    if page < 1 or page > total_pages:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return items, total_pages
