"""Сравнительный анализ (Фибоначчи и рюкзак) с замером времени и памяти.

Запуск (просто):
    python comparison.py
"""

from __future__ import annotations

import argparse
import random
import time
import tracemalloc
from typing import Callable, Dict, List, Sequence, Tuple, TypeVar

from dynamic_programming import Item, fib_bottom_up, knapsack_01

T = TypeVar("T")


def measure_time_memory(func: Callable[..., T], *args) -> Tuple[float, int, T]:
    """Возвращает (время_сек, пик_памяти_байт, результат) для одного вызова."""
    tracemalloc.start()
    start = time.perf_counter()
    result = func(*args)
    dt = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return dt, peak, result


def fib_memo_stack(n: int) -> int:
    """Топ-даун Фибоначчи с мемоизацией без рекурсии (через явный стек)."""
    if n < 0:
        raise ValueError("n должно быть неотрицательным")

    memo: Dict[int, int] = {0: 0, 1: 1}
    stack: List[int] = [n]

    while stack:
        k = stack.pop()
        if k in memo:
            continue
        stack.append(k)
        stack.append(k - 1)
        stack.append(k - 2)

        # Если оба подзначения уже посчитаны — можно заполнить memo[k].
        if (k - 1) in memo and (k - 2) in memo:
            memo[k] = memo[k - 1] + memo[k - 2]

    for i in range(2, n + 1):
        memo[i] = memo[i - 1] + memo[i - 2]

    return memo[n]


def compare_fibonacci(n: int) -> None:
    """Сравнение: memo (без рекурсии) vs bottom-up (итеративно)."""
    print("\n=== Сравнение Фибоначчи (мемоизация без рекурсии vs "
          "итеративный) ===")
    print(f"Параметр n = {n}\n")

    t_memo, m_memo, _ = measure_time_memory(fib_memo_stack, n)
    t_iter, m_iter, _ = measure_time_memory(fib_bottom_up, n)

    print("Мемоизация (stack-based):")
    print(f"  время  = {t_memo:.6f} с")
    print(f"  память = {m_memo} байт")

    print("\nИтеративно (bottom-up):")
    print(f"  время  = {t_iter:.6f} с")
    print(f"  память = {m_iter} байт")


def continuous_knapsack_greedy(items: Sequence[Item], capacity: int) -> float:
    """Жадный алгоритм для непрерывного (дробного) рюкзака."""
    if capacity <= 0:
        return 0.0

    items_sorted = sorted(items, key=lambda it: it.value /
                          it.weight, reverse=True)

    remaining = capacity
    total = 0.0
    for it in items_sorted:
        if remaining == 0:
            break
        take = min(it.weight, remaining)
        total += take * (it.value / it.weight)
        remaining -= take
    return total


def make_random_items(n: int, seed: int = 42) -> List[Item]:
    """Детерминированная генерация набора предметов (чтобы
    сравнение было честным)."""
    rng = random.Random(seed)
    res: List[Item] = []
    for i in range(n):
        w = rng.randint(1, 10)
        v = rng.randint(1, 20)
        res.append(Item(name=f"it{i}", weight=w, value=v))
    return res


def compare_knapsack(n: int, capacity: int) -> None:
    """Сравнение: дробный рюкзак (жадный) vs 0–1 рюкзак (ДП)."""
    print("\n=== Сравнение рюкзака: дробный (жадный) vs 0–1 (ДП) ===")
    print(f"Параметры: n = {n}, capacity = {capacity}\n")

    items = make_random_items(n, seed=42)

    t_frac, m_frac, best_frac = measure_time_memory(
        continuous_knapsack_greedy, items, capacity
    )
    dp_call = measure_time_memory(knapsack_01, items, capacity)
    t_dp, m_dp, dp_result = dp_call
    best_dp, chosen = dp_result

    print("Дробный рюкзак (жадный):")
    print(f"  значение = {best_frac}")
    print(f"  время    = {t_frac:.6f} с")
    print(f"  память   = {m_frac} байт")

    print("\n0–1 рюкзак (ДП):")
    print(f"  значение = {best_dp}")
    print(f"  время    = {t_dp:.6f} с")
    print(f"  память   = {m_dp} байт")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Сравнительный анализ (Фибоначчи и рюкзак)"
        "с замером времени и памяти."
    )
    parser.add_argument("--fib-n", type=int, default=2000)
    parser.add_argument("--knap-n", type=int, default=12)
    parser.add_argument("--knap-cap", type=int, default=80)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    compare_fibonacci(args.fib_n)
    compare_knapsack(args.knap_n, args.knap_cap)


if __name__ == "__main__":
    main()
