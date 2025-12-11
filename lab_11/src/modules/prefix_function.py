"""
Модуль для вычисления префикс-функции строки.
Сложность: O(n) по времени, O(n) по памяти.
"""


def prefix_function(s: str) -> list[int]:
    """Вычисляет префикс-функцию для строки s.

    Args:
        s (str): исходная строка

    Returns:
        list[int]: массив π
    """
    pi = [0] * len(s)
    j = 0

    for i in range(1, len(s)):
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    return pi
