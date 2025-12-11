"""
Поиск подстроки с использованием Z-функции.
Сложность: O(n + m)
"""

from z_function import z_function


def z_search(text: str, pattern: str) -> list[int]:
    """Поиск подстроки с помощью Z-функции.

    Args:
        text (str): текст
        pattern (str): паттерн

    Returns:
        list[int]: позиции вхождений
    """
    if not pattern:
        return []

    s = pattern + "#" + text
    z = z_function(s)

    m = len(pattern)
    result = []

    for i in range(m + 1, len(s)):
        if z[i] == m:
            result.append(i - m - 1)

    return result
