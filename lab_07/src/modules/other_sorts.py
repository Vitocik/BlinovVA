"""
other_sorts.py

Здесь находятся две классические сортировки:
1) Быстрая сортировка (QuickSort)
2) Сортировка слиянием (MergeSort)

Обе реализованы в простейшем, учебном, рекурсивном виде.

Сложности:
    QuickSort:
        Средняя: O(n log n)
        Худшая:  O(n^2)
    MergeSort:
        Всегда: O(n log n)
"""

# ---------------------------------------------------------
#   QUICK SORT (классический, рекурсивный)
# ---------------------------------------------------------


def quicksort(arr):
    """
    Рекурсивная быстрая сортировка.
    Пивот — первый элемент массива.

    Возвращает новый отсортированный список.
    Не является in-place версией.

    Пример:
        quicksort([3, 1, 2]) -> [1, 2, 3]
    """
    if len(arr) <= 1:
        return arr

    pivot = arr[0]

    left = [x for x in arr[1:] if x < pivot]
    right = [x for x in arr[1:] if x >= pivot]

    return quicksort(left) + [pivot] + quicksort(right)


# ---------------------------------------------------------
#   MERGE SORT (классический, рекурсивный)
# ---------------------------------------------------------


def mergesort(arr):
    """
    Рекурсивная сортировка слиянием.

    Возвращает новый отсортированный список.
    Сложность O(n log n) в любом случае.

    Пример:
        mergesort([4, 3, 1]) -> [1, 3, 4]
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = mergesort(arr[:mid])
    right = mergesort(arr[mid:])

    return merge(left, right)


def merge(a, b):
    """
    Сливает два отсортированных массива a и b
    в один отсортированный массив.

    Используется в mergesort().
    """
    result = []
    i = 0
    j = 0

    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1

    result.extend(a[i:])
    result.extend(b[j:])
    return result
