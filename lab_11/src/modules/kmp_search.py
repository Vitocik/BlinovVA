"""
Алгоритм Кнута–Морриса–Пратта (KMP).
Сложность: O(n + m), где n — длина текста, m — длина паттерна.
"""

from prefix_function import prefix_function


def kmp_search(text: str, pattern: str) -> list[int]:
    """Ищет все вхождения pattern в text с помощью KMP.

    Args:
        text (str): текст
        pattern (str): подстрока

    Returns:
        list[int]: позиции вхождений
    """
    if not pattern:
        return []

    s = pattern + "#" + text
    pi = prefix_function(s)

    result = []
    m = len(pattern)

    for i in range(m + 1, len(s)):
        if pi[i] == m:
            result.append(i - 2 * m)
    return result
