# analysis.py
import csv
import random
import sys
import time

import matplotlib.pyplot as plt

from binary_search_tree import BinarySearchTree

sys.setrecursionlimit(20000)


def measure_search_time(tree: 'BinarySearchTree', queries: list[int]) -> float:
    """
    Измеряет время выполнения множественных операций поиска в дереве.

    Аргументы:
        tree (BinarySearchTree): Экземпляр бинарного дерева поиска.
        queries (list[int]): Список значений, которые нужно искать в дереве.

    Возвращает:
        float: Время выполнения всех операций поиска в секундах.
    """
    start = time.perf_counter()
    for q in queries:
        tree.search(q)
    end = time.perf_counter()
    return end - start


def build_balanced_by_shuffle(n: int) -> tuple['BinarySearchTree', list[int]]:
    """
    Создаёт сбалансированное BST, вставляя числа в случайном порядке.

    Аргументы:
        n (int): Количество элементов для вставки.

    Возвращает:
        tuple[BinarySearchTree, list[int]]: Пара из дерева и списка значений,
        вставленных в случайном порядке.
    """
    values = list(range(n))
    random.shuffle(values)

    bst = BinarySearchTree()
    for v in values:
        bst.insert(v)

    return bst, values


def build_degenerate(n: int) -> tuple['BinarySearchTree', list[int]]:
    """
    Создаёт вырожденное (линейное) BST, вставляя числа в отсортированном
    порядке.

    Аргументы:
        n (int): Количество элементов для вставки.

    Возвращает:
        tuple[BinarySearchTree, list[int]]: Пара из дерева и списка значений
        (в отсортированном порядке).
    """
    values = list(range(n))
    bst = BinarySearchTree()
    for v in values:
        bst.insert(v)
    return bst, values


def experiment(
    sizes: list[int] | None = None,
    repeats: int = 3,
    out_csv: str = "bst_times.csv",
    out_png: str = "bst_times.png",
) -> None:
    """
    Проводит эксперимент по сравнению времени поиска в сбалансированном
    и вырожденном BST.

    Для каждого размера дерева:
    - Создаётся сбалансированное дерево (вставка в случайном порядке).
    - Создаётся вырожденное дерево (вставка в отсортированном порядке).
    - Измеряется среднее время поиска ~1000 случайных элементов.
    - Результаты сохраняются в CSV и визуализируются на графике.

    Аргументы:
        sizes (list[int] | None): Список размеров деревьев для тестирования.
            По умолчанию [100, 500, 1000, 3000, 5000].
        repeats (int): Количество повторений для каждого размера (усреднение).
        out_csv (str): Имя выходного CSV-файла.
        out_png (str): Имя выходного PNG-файла с графиком.

    Эффекты:
        - Сохраняет результаты в файл CSV.
        - Сохраняет график в файл PNG.
        - Выводит сообщения о ходе выполнения в stdout.
    """
    if sizes is None:
        sizes = [100, 500, 1000, 3000, 5000]

    results = []

    for n in sizes:
        print(f"Running size {n} ...")

        balanced_times = []
        degenerate_times = []

        for _ in range(repeats):
            bst_bal, vals_bal = build_balanced_by_shuffle(n)
            bst_deg, vals_deg = build_degenerate(n)

            sample_bal = random.sample(vals_bal, min(n, 1000))
            sample_deg = random.sample(vals_deg, min(n, 1000))

            t_bal = measure_search_time(bst_bal, sample_bal)
            t_deg = measure_search_time(bst_deg, sample_deg)

            balanced_times.append(t_bal)
            degenerate_times.append(t_deg)

        avg_bal = sum(balanced_times) / repeats
        avg_deg = sum(degenerate_times) / repeats

        results.append((n, "balanced", avg_bal))
        results.append((n, "degenerate", avg_deg))

    # Save CSV
    with open(out_csv, "w", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerow(["n", "tree_type", "avg_search_time_s"])
        for row in results:
            writer.writerow(row)

    print(f"Saved results to {out_csv}")

    # Extract data for plotting
    sizes_unique = sorted(set(size for size, _, _ in results))

    balanced_plot = []
    degenerate_plot = []

    for s in sizes_unique:
        bal = next(
            val for size, typ, val in results
            if size == s and typ == "balanced"
        )
        deg = next(
            val for size, typ, val in results
            if size == s and typ == "degenerate"
        )
        balanced_plot.append(bal)
        degenerate_plot.append(deg)

    # Plot
    plt.figure(figsize=(8, 5))

    plt.plot(
        sizes_unique,
        balanced_plot,
        marker="o",
        label="Balanced (random insert)",
    )
    plt.plot(
        sizes_unique,
        degenerate_plot,
        marker="o",
        label="Degenerate (sorted insert)",
    )

    plt.xlabel("Number of elements (n)")
    plt.ylabel("Average time per ~1000 searches (s)")
    plt.title("Search time: balanced vs degenerate BST")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png)

    print(f"Saved plot to {out_png}")


if __name__ == "__main__":
    experiment()
