"""
heap.py

Реализация универсальной бинарной кучи (min-heap / max-heap) на основе массива.
Все комментарии и документация — на русском языке.

Класс Heap поддерживает:
- insert(value)  — вставка O(log n)
- extract()      — извлечение корня O(log n)
- peek()         — просмотр корня O(1)
- build_heap(arr) — построение кучи из массива O(n)
- print_tree()   — текстовая визуализация кучи (для небольших размеров)

"""

from __future__ import annotations
from typing import Any, List, Optional


class Heap:
    """
    Универсальная бинарная куча, реализованная на массиве.

    Параметры:
        is_min: bool
            True  — min-куча (корень — минимальный элемент),
            False — max-куча (корень — максимальный элемент).

    Примечание:
        Куча хранит произвольные объекты, которые поддерживают
        операции сравнения между собой (например, числа, кортежи).
        При использовании кортежей сравнение будет лексикографическим,
        что полезно для хранения (priority, item).
    """

    def __init__(self, is_min: bool = True) -> None:
        self.data: List[Any] = []
        self.is_min = is_min

    # -------------------------
    # Внутренние вспомогательные методы
    # -------------------------
    def _compare(self, a: Any, b: Any) -> bool:
        """
        Сравнение в зависимости от типа кучи.
        Возвращает True, если элемент a должен располагаться
        выше (ближе к корню), чем элемент b.
        """
        return a < b if self.is_min else a > b

    def _sift_up(self, index: int) -> None:
        """
        O(log n).
        "Всплытие" элемента: поднимаем элемент с позиции index вверх,
        пока не восстановим свойство кучи.
        """
        while index > 0:
            parent = (index - 1) // 2
            if self._compare(self.data[index], self.data[parent]):
                self.data[index], self.data[parent] = (
                    self.data[parent],
                    self.data[index],
                )
                index = parent
            else:
                break

    def _sift_down(self, index: int) -> None:
        """
        O(log n).
        "Погружение" элемента: опускаем элемент с позиции index вниз,
        пока не будет выполнено свойство кучи.
        """
        size = len(self.data)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            candidate = index

            if (
                left < size
                and self._compare(self.data[left], self.data[candidate])
            ):
                candidate = left

            if (
                right < size
                and self._compare(self.data[right], self.data[candidate])
            ):
                candidate = right

            if candidate != index:
                self.data[index], self.data[candidate] = (
                    self.data[candidate],
                    self.data[index],
                )
                index = candidate
            else:
                break

    # -------------------------
    # Публичный API
    # -------------------------
    def insert(self, value: Any) -> None:
        """
        O(log n).
        Вставляет значение в кучу.
        """
        self.data.append(value)
        self._sift_up(len(self.data) - 1)

    def extract(self) -> Optional[Any]:
        """
        O(log n).
        Извлекает и возвращает корень кучи.
        Если куча пустая — возвращает None.
        """
        if not self.data:
            return None

        root = self.data[0]
        last = self.data.pop()
        if self.data:
            self.data[0] = last
            self._sift_down(0)
        return root

    def peek(self) -> Optional[Any]:
        """
        O(1).
        Возвращает корень кучи без извлечения.
        """
        return self.data[0] if self.data else None

    def build_heap(self, array: List[Any]) -> None:
        """
        O(n).
        Построение кучи из произвольного массива (in-place копия массива).
        Алгоритм: выполняем sift_down для всех узлов от len//2 - 1 до 0.
        """
        self.data = array[:]
        # начинаем с последнего внутреннего узла
        for i in range(len(self.data) // 2 - 1, -1, -1):
            self._sift_down(i)

    # -------------------------
    # Визуализация
    # -------------------------
    def print_tree(self) -> None:
        """
        Текстовая печать кучи в виде уровней (для небольших размеров).
        Формат: элементы уровня выводятся в одну строку.
        """
        if not self.data:
            print("<пустая куча>")
            return

        level = 0
        count = 0
        next_level = 1

        for value in self.data:
            print(value, end=" ")
            count += 1
            if count == next_level:
                print()
                level += 1
                next_level += 2 ** level
        print()
