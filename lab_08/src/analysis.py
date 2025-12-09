"""
Анализ времени работы алгоритма Хаффмана.

Измеряется зависимость времени выполнения
от размера входных данных. Результаты выводятся в терминал
и сохраняются в график time_vs_size.png.
"""

import random
import string
import time
from collections import Counter
from typing import List

from greedy_algorithms import build_huffman_tree
from visualization import plot_time_vs_size


def generate_random_string(length: int) -> str:
    """Генерирует случайную строку заданной длины."""
    return "".join(
        random.choice(string.ascii_lowercase)
        for _ in range(length)
    )


def measure_huffman_time(sizes: List[int]) -> List[float]:
    """
    Измеряет время работы алгоритма Хаффмана
    для различных размеров входных данных.
    """
    times: List[float] = []

    for size in sizes:
        text = generate_random_string(size)
        frequencies = dict(Counter(text))

        start_time = time.perf_counter()
        build_huffman_tree(frequencies)
        end_time = time.perf_counter()

        times.append(end_time - start_time)

    return times


def main() -> None:
    """Точка входа в программу анализа."""
    sizes = [100, 500, 1000, 2000, 5000, 10000]
    times = measure_huffman_time(sizes)

    print("=== Экспериментальное исследование времени работы Хаффмана ===")
    for size, t in zip(sizes, times):
        print(f"Размер {size:6d} → время {t:.6f} сек")

    plot_time_vs_size(
        sizes,
        times,
        filename="time_vs_size.png",
    )

    print("\nГрафик сохранён в файл time_vs_size.png")


if __name__ == "__main__":
    main()
