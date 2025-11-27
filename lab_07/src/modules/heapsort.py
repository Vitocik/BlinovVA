"""
heapsort.py

Реализация пирамидальной сортировки (heapsort).
Функции:
- heapsort(array) -> List: сортировка с использованием внешней кучи.
- heapsort_inplace(array) -> None: in-place версия (не требует доп. памяти).

"""

from __future__ import annotations
from typing import List, Any


from heap import Heap  # noqa: E402  (импорт локального модуля)


def heapsort(array: List[Any]) -> List[Any]:
    """
    Сортировка с использованием внешней min-кучи.
    Возвращает новый отсортированный список (по возрастанию).
    Сложность O(n log n).
    """
    if not array:
        return []

    h = Heap(is_min=True)
    h.build_heap(array)
    result: List[Any] = []
    while h.data:
        result.append(h.extract())
    return result


def heapsort_inplace(array: List[Any]) -> None:
    """
    In-place реализация heapsort.
    Алгоритм:
    1) Построить max-кучу (вместо min).
    2) Поочерёдно переставлять корень в конец и уменьшать границу.
    В результате массив будет отсортирован по возрастанию.

    Сложность: O(n log n). Память: O(1) дополнительная.
    """
    n = len(array)

    def sift_down(a: List[Any], n_val: int, i: int) -> None:
        """Вспомогательная процедура sift_down для max-кучи."""
        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            largest = i

            if left < n_val and a[left] > a[largest]:
                largest = left
            if right < n_val and a[right] > a[largest]:
                largest = right

            if largest != i:
                a[i], a[largest] = a[largest], a[i]
                i = largest
            else:
                break

    # Построение max-кучи
    for idx in range(n // 2 - 1, -1, -1):
        sift_down(array, n, idx)

    # Извлечение максимума в конец и уменьшение границы
    for end in range(n - 1, 0, -1):
        array[0], array[end] = array[end], array[0]
        sift_down(array, end, 0)
