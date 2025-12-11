"""
Алгоритм Рабина–Карпа.
Средняя сложность: O(n + m)
Худшая сложность: O(n * m)
"""


def rabin_karp(
    text: str,
    pattern: str,
    base: int = 257,
    mod: int = 10**9 + 7
) -> list[int]:
    """Поиск подстроки алгоритмом Рабина–Карпа."""
    n = len(text)
    m = len(pattern)

    if m == 0 or m > n:
        return []

    p_hash = 0
    t_hash = 0
    power = 1

    for _ in range(m - 1):
        power = (power * base) % mod

    for i in range(m):
        p_hash = (p_hash * base + ord(pattern[i])) % mod
        t_hash = (t_hash * base + ord(text[i])) % mod

    occurrences = []

    for i in range(n - m + 1):
        if p_hash == t_hash and text[i:i + m] == pattern:
            occurrences.append(i)

        if i < n - m:
            t_hash = (t_hash - ord(text[i]) * power) % mod
            t_hash = (t_hash * base + ord(text[i + m])) % mod
            t_hash = (t_hash + mod) % mod  # избегаем отрицательных значений

    return occurrences
