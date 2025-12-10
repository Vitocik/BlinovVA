"""Автоматические эксперименты по 0-1 рюкзаку."""

from __future__ import annotations

import csv
import os
import random
import time
from dataclasses import dataclass
from typing import List, Sequence

import matplotlib.pyplot as plt


@dataclass(frozen=True)
class Item:
    """Предмет рюкзака (0-1)."""
    name: str
    weight: int
    value: int


def knapsack_table(items: Sequence[Item], capacity: int) -> List[List[int]]:
    """Строит DP-таблицу (n+1) x (capacity+1) и возвращает её."""
    if capacity < 0:
        raise ValueError("capacity должен быть неотрицательным")

    n = len(items)
    dp: List[List[int]] = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        it = items[i - 1]
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if it.weight <= w:
                cand = dp[i - 1][w - it.weight] + it.value
                if cand > dp[i][w]:
                    dp[i][w] = cand
    return dp


def knapsack_value(items: Sequence[Item], capacity: int) -> int:
    """Возвращает только оптим. стоимость (быстрый вариант для замеров)."""
    return knapsack_table(items, capacity)[len(items)][capacity]


def generate_items(n: int, seed: int = 42) -> List[Item]:
    """Детерминированная генерация n предметов (для повторяемых замеров)."""
    rng = random.Random(seed)
    res: List[Item] = []
    for i in range(n):
        w = rng.randint(1, 10)
        v = rng.randint(1, 20)
        res.append(Item(name=f"it{i}", weight=w, value=v))
    return res


def format_table(dp: Sequence[Sequence[int]]) -> str:
    """Текстовый вывод таблицы DP (удобен для отчёта и консоли)."""
    if not dp:
        return "<пустая таблица>"

    widths = [
        max(len(str(dp[r][c])) for r in range(len(dp)))
        for c in range(len(dp[0]))
    ]
    rows = []
    for r in range(len(dp)):
        parts = [str(dp[r][c]).rjust(widths[c]) for c in range(len(dp[0]))]
        rows.append(" | ".join(parts))
    return "\n".join(rows)


def show_dp_trace() -> None:
    """Визуализация заполнения таблицы DP на маленьком примере."""
    n = 4
    capacity = 10
    items = generate_items(n, seed=7)

    print("=== ВИЗУАЛИЗАЦИЯ ===")
    print("Входные данные:")
    for it in items:
        print(f"  {it.name}: weight={it.weight}, value={it.value}")
    print(f"capacity = {capacity}\n")

    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        it = items[i - 1]
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if it.weight <= w:
                cand = dp[i - 1][w - it.weight] + it.value
                if cand > dp[i][w]:
                    dp[i][w] = cand

        print(f"--- после предмета i={i} ({it.name}) ---")
        print(format_table(dp[: i + 1]))
        print()

    print("=== Итоговая таблица ===")
    print(format_table(dp))
    print("Оптимальная стоимость:", dp[n][capacity])
    print("=== КОНЕЦ ВИЗУАЛИЗАЦИИ ===\n")


def time_once(func, *args) -> float:
    start = time.perf_counter()
    func(*args)
    return time.perf_counter() - start


def run_scalability(
    n_list: Sequence[int],
    capacity_factor: int,
    repeats: int,
    out_dir: str = "results",
) -> str:
    """Пункт 6: замеры времени на одной машине и запись в CSV."""
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, "knapsack_scalability.csv")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["n", "capacity", "repeats", "median_time_sec",
                    "mean_time_sec"])

        for n in n_list:
            capacity = max(1, n * capacity_factor)
            times: List[float] = []
            for r in range(repeats):
                items = generate_items(n, seed=42 + r)
                times.append(time_once(knapsack_value, items, capacity))

            times_sorted = sorted(times)
            median = times_sorted[len(times_sorted) // 2]
            mean = sum(times) / len(times)
            w.writerow([n, capacity, repeats, f"{median:.9f}", f"{mean:.9f}"])

    return csv_path


def plot_time_curve(csv_path: str, out_dir: str = "results") -> str:
    """Построение графика зависимости времени от n (п. 7, график)."""
    ns: List[int] = []
    meds: List[float] = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ns.append(int(row["n"]))
            meds.append(float(row["median_time_sec"]))

    plt.figure()
    plt.plot(ns, meds, marker="o")
    plt.title("Время (медиана) vs размер задачи n (0-1 рюкзак)")
    plt.xlabel("n (кол-во предметов)")
    plt.ylabel("время, сек (медиана)")
    plt.grid(True)

    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "knapsack_time_vs_n.png")
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close()
    return out_path


def main() -> None:
    show_dp_trace()

    n_list = [5, 8, 10, 12, 15, 18, 20]
    capacity_factor = 8
    repeats = 5

    print("=== МАСШТАБИРУЕМОСТЬ ===")
    csv_path = run_scalability(n_list, capacity_factor, repeats)
    png_path = plot_time_curve(csv_path)

    print("Готово. Результаты сохранены:")
    print("  CSV:", csv_path)
    print("  PNG:", png_path)


if __name__ == "__main__":
    main()
