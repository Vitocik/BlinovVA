"""Алгоритмы ДП (PEP8/flake8) с русской документацией."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple


def fib_naive(n: int) -> int:
    """Наивная рекурсия Фибоначчи (экспоненциальная сложность)."""
    if n < 0:
        raise ValueError("n должно быть неотрицательным")
    if n in (0, 1):
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


def fib_memo(n: int, memo: Optional[Dict[int, int]] = None) -> int:
    """Фибоначчи с мемоизацией (top-down), O(n) по времени."""
    if n < 0:
        raise ValueError("n должно быть неотрицательным")
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n in (0, 1):
        memo[n] = n
        return n
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


def fib_bottom_up(n: int) -> int:
    """Итеративный Фибоначчи (bottom-up), O(n) по времени и O(1) по памяти."""
    if n < 0:
        raise ValueError("n должно быть неотрицательным")
    if n in (0, 1):
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


@dataclass(frozen=True)
class Item:
    """Элемент задачи о рюкзаке (0-1)."""
    name: str
    weight: int
    value: int


def knapsack_01(
    items: Sequence[Item], capacity: int
) -> Tuple[int, List[Item]]:
    """Рюкзак 0-1: возвращает (макс. стоимость, выбранные предметы)."""
    if capacity < 0:
        raise ValueError("capacity должен быть неотрицательным")

    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        it = items[i - 1]
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if it.weight <= w:
                cand = dp[i - 1][w - it.weight] + it.value
                if cand > dp[i][w]:
                    dp[i][w] = cand

    chosen: List[Item] = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            it = items[i - 1]
            chosen.append(it)
            w -= it.weight
    chosen.reverse()
    return dp[n][capacity], chosen


def knapsack_01_1d(items: Sequence[Item], capacity: int) -> int:
    """Оптимизация памяти для 0-1 рюкзака (возвращает только стоимость)."""
    if capacity < 0:
        raise ValueError("capacity должен быть неотрицательным")

    dp = [0] * (capacity + 1)
    for it in items:
        for w in range(capacity, it.weight - 1, -1):
            dp[w] = max(dp[w], dp[w - it.weight] + it.value)
    return dp[capacity]


def lcs(a: str, b: str) -> Tuple[int, str]:
    """Наиб. общая подпоследовательность (LCS) с восстановлением строки."""
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    i, j = n, m
    out: List[str] = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return dp[n][m], "".join(reversed(out))


def levenshtein(a: str, b: str) -> int:
    """Расстояние Левенштейна (минимум вставок/удалений/замен)."""
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost,
            )
    return dp[n][m]


def coin_change(coins: Sequence[int], amount: int) -> Tuple[int, List[int]]:
    """Минимальное число монет для суммы amount (с восстановлением)."""
    if amount < 0:
        raise ValueError("amount должен быть неотрицательным")
    if any(c <= 0 for c in coins):
        raise ValueError("монеты должны быть положительными")

    inf = amount + 1
    dp = [inf] * (amount + 1)
    prev = [-1] * (amount + 1)
    dp[0] = 0

    for s in range(1, amount + 1):
        for c in coins:
            if c <= s and dp[s - c] + 1 < dp[s]:
                dp[s] = dp[s - c] + 1
                prev[s] = c

    if dp[amount] == inf:
        return -1, []

    res: List[int] = []
    cur = amount
    while cur > 0:
        coin = prev[cur]
        res.append(coin)
        cur -= coin
    return dp[amount], res


def lis(sequence: Sequence[int]) -> Tuple[int, List[int]]:
    """Наибольшая возрастающая подпоследовательность (O(n^2))."""
    n = len(sequence)
    if n == 0:
        return 0, []

    dp = [1] * n
    parent = [-1] * n
    best = 0

    for i in range(n):
        for j in range(i):
            if sequence[j] < sequence[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                parent[i] = j
        if dp[i] > dp[best]:
            best = i

    out: List[int] = []
    k = best
    while k != -1:
        out.append(sequence[k])
        k = parent[k]
    out.reverse()
    return dp[best], out


if __name__ == "__main__":
    print("\n=== Фибоначчи ===")
    print("fib_naive(10)      =", fib_naive(10))
    print("fib_memo(10)       =", fib_memo(10))
    print("fib_bottom_up(10)  =", fib_bottom_up(10))

    print("\n=== 0–1 рюкзак (DP) ===")
    items_demo = [
        Item("a", 1, 1),
        Item("b", 3, 4),
        Item("c", 4, 5),
    ]
    capacity_demo = 4
    best_value, chosen_items = knapsack_01(items_demo, capacity_demo)
    print("items:", [(it.name, it.weight, it.value) for it in items_demo])
    print("capacity =", capacity_demo)
    print("best value =", best_value)
    print(
        "chosen =",
        ["{} (w={}, v={})".format(it.name, it.weight, it.value)
            for it in chosen_items]
    )

    print("\n=== LCS (наибольшая общая подпоследовательность) ===")
    A = "ABCBDAB"
    B = "BDCAB"
    lcs_len, lcs_str = lcs(A, B)
    print(f"A = \"{A}\"")
    print(f"B = \"{B}\"")
    print("LCS length =", lcs_len)
    print("LCS string =", lcs_str)

    print("\n=== Расстояние Левенштейна ===")
    a = "kitten"
    b = "sitting"
    dist = levenshtein(a, b)
    print(f"a = \"{a}\"")
    print(f"b = \"{b}\"")
    print("distance =", dist)

    print("\n=== Размен монет (минимум монет) ===")
    coins_demo = [1, 2, 5]
    amount_demo = 11
    min_coins, coins_used = coin_change(coins_demo, amount_demo)
    print("coins =", coins_demo)
    print("amount =", amount_demo)
    print("min coins =", min_coins)
    print("coins used =", coins_used)

    print("\n=== LIS (наибольшая возрастающая подпоследовательность) ===")
    seq = [3, 1, 2, 5, 4]
    lis_len, lis_seq = lis(seq)
    print("sequence =", seq)
    print("length =", lis_len)
    print("subsequence =", lis_seq)

    print("\ndynamic_programming: OK\n")
