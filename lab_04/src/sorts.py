"""
Алгоритмы сортировки
Все функции возвращают новый отсортированный список (не меняют исходный).
"""

from typing import List, TypeVar

T = TypeVar('T', bound=int)  # Ограничение: работаем с целыми числами


# ---------------- Bubble Sort ----------------
def bubble_sort(arr: List[T]) -> List[T]:
    """
    Сортировка пузырьком (Bubble Sort) — простой алгоритм,
    который многократно проходит по списку,
    сравнивая соседние элементы и меняя их местами,
    если они в неправильном порядке.

    :param arr: Список для сортировки.
    :return: Новый отсортированный список.

    Сложность по времени:
        - Лучшее: O(n) — если массив уже отсортирован.
        - Среднее: O(n²)
        - Худшее: O(n²)

    Сложность по памяти: O(1) — сортирует "на месте" (но мы возвращаем копию).
    """
    a = arr.copy()
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break  # Массив уже отсортирован
    return a


# ---------------- Selection Sort ----------------
def selection_sort(arr: List[T]) -> List[T]:
    """
    Сортировка выбором (Selection Sort) — на каждом шаге
    находит минимальный элемент
    из неотсортированной части и помещает его в начало.

    :param arr: Список для сортировки.
    :return: Новый отсортированный список.

    Сложность по времени: O(n²) — всегда, независимо от входа.
    Сложность по памяти: O(1) — сортирует "на месте" (но мы возвращаем копию).
    """
    a = arr.copy()
    n = len(a)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if a[j] < a[min_index]:
                min_index = j
        a[i], a[min_index] = a[min_index], a[i]
    return a


# ---------------- Insertion Sort ----------------
def insertion_sort(arr: List[T]) -> List[T]:
    """
    Сортировка вставками (Insertion Sort) — строит отсортированный
    массив по одному элементу за раз,
    вставляя каждый новый элемент на правильную позицию.

    :param arr: Список для сортировки.
    :return: Новый отсортированный список.

    Сложность по времени:
        - Лучшее: O(n) — если массив уже отсортирован.
        - Среднее: O(n²)
        - Худшее: O(n²)

    Сложность по памяти: O(1) — сортирует "на месте" (но мы возвращаем копию).
    """
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


# ---------------- Merge Sort ----------------
def merge_sort(arr: List[T]) -> List[T]:
    """
    Сортировка слиянием (Merge Sort) — рекурсивный алгоритм
    "разделяй и властвуй".
    Разбивает массив на половинки, рекурсивно сортирует их и сливает.

    :param arr: Список для сортировки.
    :return: Новый отсортированный список.

    Сложность по времени: O(n log n) — всегда.
    Сложность по памяти: O(n) — требуется дополнительная память для слияния.
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    result = []
    i = j = 0

    # Слияние двух отсортированных частей
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Добавляем остатки
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ---------------- Quick Sort ----------------
def quick_sort(arr: List[T]) -> List[T]:
    """
    Быстрая сортировка (Quick Sort) — ещё один алгоритм "разделяй и властвуй".
    Выбирает опорный элемент, разделяет массив на меньшие и большие,
    рекурсивно сортирует.

    :param arr: Список для сортировки.
    :return: Новый отсортированный список.

    Сложность по времени:
        - Лучшее/среднее: O(n log n)
        - Худшее: O(n²) — при плохом выборе опорного элемента (например,
        - в уже отсортированном массиве).

    Сложность по памяти: O(log n) — из-за глубины рекурсии.
    """
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]  # Опорный элемент (можно выбирать иначе)
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)
