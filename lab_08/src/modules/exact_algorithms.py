"""Точные алгоритмы для сравнения с жадными."""

from typing import List, Tuple


def knapsack_01(
    items: List[Tuple[int, int]],
    capacity: int,
) -> Tuple[int, List[int]]:
    """Точная задача о рюкзаке (0-1)."""
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        value, weight = items[i - 1]
        for w in range(capacity + 1):
            if weight <= w:
                dp[i][w] = max(
                    dp[i - 1][w],
                    dp[i - 1][w - weight] + value,
                )
            else:
                dp[i][w] = dp[i - 1][w]

    w = capacity
    selected: List[int] = []

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i - 1)
            w -= items[i - 1][1]

    selected.reverse()
    return dp[n][capacity], selected
