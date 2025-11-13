"""Набор хеш-функций для строковых ключей.

Функции:
- simple_hash: сумма кодов символов
- polynomial_hash: полиномиальная (rolling) хеш-функция
- djb2: классическая функция DJB2
"""
from typing import Optional


def simple_hash(s: str) -> int:
    """Простая хеш-функция: сумма кодов символов."""
    h: int = 0
    for ch in s:
        h += ord(ch)
    return h & 0x7FFFFFFF


def polynomial_hash(s: str,
                    base: int = 257,
                    mod: Optional[int] = None) -> int:
    """Полиномиальная (rolling) хеш-функция.

    Если mod не задан, возвращаем неограниченное целое.
    """
    h: int = 0
    if mod is None:
        for ch in s:
            h = h * base + ord(ch)
    else:
        for ch in s:
            h = (h * base + ord(ch)) % mod
    return h & 0x7FFFFFFF


def djb2(s: str) -> int:
    """Хеш-функция DJB2 (Dan Bernstein)."""
    h: int = 5381
    for ch in s:
        # h * 33 + ord(ch)
        h = (h * 33) + ord(ch)
    return h & 0x7FFFFFFF
