"""
Модуль для вычисления Z-функции строки.
Сложность: O(n) по времени, O(n) по памяти.
"""


def z_function(s: str) -> list[int]:
    """Вычисляет Z-функцию строки s.

    Args:
        s (str): строка

    Returns:
        list[int]: массив Z
    """
    n = len(s)
    z = [0] * n
    l, r = 0, 0

    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])

        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1

        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1

    return z
