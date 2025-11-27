"""
visualize.py

Скрипт строит три графика:

1) heap_build_vs_insert.png
   Сравнение времени последовательной insert() и build_heap().

2) sort_comparison.png
   Сравнение heapsort_inplace и встроенной sorted().

3) sort_compare_heap_quick_merge.png
   Сравнение HeapSort, QuickSort и MergeSort.

"""

from __future__ import annotations
import random
import time
from typing import Callable, List

import matplotlib.pyplot as plt

from heapsort import heapsort_inplace
from other_sorts import quicksort, mergesort
from heap import Heap


# ---------------------------------------------------------
#   Универсальная функция замера
# ---------------------------------------------------------
def measure(func: Callable[[], None]) -> float:
    """Замеряет время выполнения функции в секундах."""
    start = time.perf_counter()
    func()
    return time.perf_counter() - start


# ---------------------------------------------------------
#   ГРАФИК 1: insert() vs build_heap()
# ---------------------------------------------------------
def benchmark_heap_build_vs_insert(sizes: List[int]) -> None:
    """Сравнивает insert() и build_heap()."""

    insert_times: List[float] = []
    build_times: List[float] = []

    for n in sizes:
        arr = [random.randint(0, 1_000_000) for _ in range(n)]

        # последовательная вставка
        h = Heap(is_min=True)

        def do_insert() -> None:
            for x in arr:
                h.insert(x)

        t_insert = measure(do_insert)
        insert_times.append(t_insert)

        # build_heap
        h2 = Heap(is_min=True)

        def do_build() -> None:
            h2.build_heap(arr)

        t_build = measure(do_build)
        build_times.append(t_build)

        print(
            f"[BUILD] n={n}: insert={t_insert:.4f}s, "
            f"build_heap={t_build:.4f}s"
        )

    plt.figure()
    plt.plot(sizes, insert_times, marker="o")
    plt.plot(sizes, build_times, marker="o")
    plt.xlabel("Количество элементов")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение insert() и build_heap()")
    plt.legend(["insert()", "build_heap()"])
    plt.grid(True)
    plt.savefig("heap_build_vs_insert.png")
    plt.close()


# ---------------------------------------------------------
#   ГРАФИК 2: Heapsort vs встроенная sorted()
# ---------------------------------------------------------
def benchmark_sorting(sizes: List[int]) -> None:
    """Сравнивает heapsort_inplace и sorted()."""

    heap_times: List[float] = []
    python_times: List[float] = []

    for n in sizes:
        arr = [random.randint(0, 1_000_000) for _ in range(n)]

        # heapsort
        a1 = arr[:]

        def do_heapsort() -> None:
            heapsort_inplace(a1)

        t_heap = measure(do_heapsort)
        heap_times.append(t_heap)

        # встроенная sorted()
        a2 = arr[:]

        def do_sorted() -> None:
            sorted(a2)

        t_sorted = measure(do_sorted)
        python_times.append(t_sorted)

        print(
            f"[SORT] n={n}: heapsort={t_heap:.4f}s, "
            f"sorted={t_sorted:.4f}s"
        )

    plt.figure()
    plt.plot(sizes, heap_times, marker="o")
    plt.plot(sizes, python_times, marker="o")
    plt.xlabel("Количество элементов")
    plt.ylabel("Время (сек)")
    plt.title("Heapsort (in-place) vs sorted()")
    plt.legend(["Heapsort (in-place)", "sorted()"])
    plt.grid(True)
    plt.savefig("sort_comparison.png")
    plt.close()


# ---------------------------------------------------------
#   ГРАФИК 3: HeapSort vs QuickSort vs MergeSort
# ---------------------------------------------------------
def benchmark_full_sort_comparison(sizes: List[int]) -> None:
    """Полное сравнение трёх сортировок."""

    heap_times: List[float] = []
    quick_times: List[float] = []
    merge_times: List[float] = []

    for n in sizes:
        arr = [random.randint(0, 1_000_000) for _ in range(n)]

        # HeapSort (in-place)
        a1 = arr[:]

        def do_heap() -> None:
            heapsort_inplace(a1)

        t_heap = measure(do_heap)
        heap_times.append(t_heap)

        # QuickSort
        a2 = arr[:]

        def do_quick() -> None:
            quicksort(a2)

        t_quick = measure(do_quick)
        quick_times.append(t_quick)

        # MergeSort
        a3 = arr[:]

        def do_merge() -> None:
            mergesort(a3)

        t_merge = measure(do_merge)
        merge_times.append(t_merge)

        print(
            f"[COMPARE] n={n}: "
            f"heap={t_heap:.4f}s, "
            f"quick={t_quick:.4f}s, "
            f"merge={t_merge:.4f}s"
        )

    plt.figure()
    plt.plot(sizes, heap_times, marker="o")
    plt.plot(sizes, quick_times, marker="o")
    plt.plot(sizes, merge_times, marker="o")
    plt.xlabel("Количество элементов")
    plt.ylabel("Время (сек)")
    plt.title("Heapsort vs QuickSort vs MergeSort")
    plt.legend(["Heapsort", "QuickSort", "MergeSort"])
    plt.grid(True)
    plt.savefig("sort_compare_heap_quick_merge.png")
    plt.close()


# ---------------------------------------------------------
#   Точка входа
# ---------------------------------------------------------
def main() -> None:
    """Запускает все бенчмарки."""
    sizes = [1000, 2000, 3000, 4000, 5000]

    # График 1
    benchmark_heap_build_vs_insert(sizes)

    # График 2
    benchmark_sorting(sizes)

    # График 3
    benchmark_full_sort_comparison(sizes)


if __name__ == "__main__":
    main()
