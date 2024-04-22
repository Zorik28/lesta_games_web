import math
import random
import re
from collections import Counter
from http import HTTPStatus

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


async def inverse_document_frequency(word_tf: Counter) -> dict[str, int]:
    """Вычисляем обратную частоту документа(IDF)."""
    word_idf = {}             # Словарь для idf
    total_docs = 100_000_000  # Для демонстрации количество документов 100млн
    for word in word_tf:
        # docs_with_word - якобы кол-во документов с конкретным словом.
        # Переменная должна содержать запись из БД,
        # к которой прибавляем дополнительное вхождение
        docs_with_word = random.randint(0, 3000) + 1
        idf = math.log10(total_docs/docs_with_word)
        word_idf[word] = idf  # записываем в словарь idf
    return word_idf


async def sort_idf(word_idf: dict[str, int]) -> dict[str, int]:
    """Сортировка словаря c idf по значениям в обратном порядке."""
    sorted_word_idf = sorted(
        word_idf.items(), key=lambda item: item[1], reverse=True
    )[:50]
    return dict(sorted_word_idf)
