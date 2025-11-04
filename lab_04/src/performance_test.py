"""
Модуль для тестирования производительности алгоритмов сортировки.

Замеряет время выполнения различных алгоритмов на разных типах массивов:
- случайный
- отсортированный
- обратный порядок
- почти отсортированный

Использует `timeit` для точного измерения времени.
"""
from timeit import timeit
from typing import Callable, Dict

from generate_data import generate_arrays
from sorts import (
    bubble_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
)


AlgorithmsType = Dict[str, Callable]
"""Словарь: название алгоритма -> функция сортировки"""

ResultType = Dict[int, Dict[str, Dict[str, float]]]
"""Вложенный словарь результатов:
   размер -> тип_данных -> алгоритм -> время (сек)
"""

# Словарь алгоритмов сортировки
algorithms: AlgorithmsType = {
    "Bubble": bubble_sort,
    "Selection": selection_sort,
    "Insertion": insertion_sort,
    "Merge": merge_sort,
    "Quick": quick_sort,
}

sizes = [100, 1000, 5000]

# Генерация тестовых данных
data = generate_arrays(sizes)

# Хранилище результатов
results: ResultType = {}

# Тестирование каждого размера массива
for size in sizes:
    print(f"\nArray size = {size}")
    results[size] = {}

    # Для каждого типа данных (random, sorted и т.д.)
    for dtype, array in data[size].items():
        results[size][dtype] = {}
        for name, func in algorithms.items():
            time_val = timeit(lambda: func(array.copy()), number=3)
            results[size][dtype][name] = time_val
            print(f"{name:9s} | {dtype:14s} = {time_val:.5f} sec")

print("\nDone.")
