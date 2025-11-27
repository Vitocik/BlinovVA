"""
priority_queue.py

Реализация простой приоритетной очереди на основе кучи.

API:
- enqueue(item, priority)
- dequeue() -> tuple(priority, item) или None, если очередь пуста

"""

from __future__ import annotations
from typing import Any, Optional, Tuple

from heap import Heap  # noqa: E402


class PriorityQueue:
    """
    Приоритетная очередь, где больший приоритет означает
    более раннее извлечение (max-priority).

    Внутри используется max-куча, в которую записываем кортежы:
    (priority, item). Поскольку кортежи сравнимы лексикографически,
    нужная сортировка достигается автоматически.
    """

    def __init__(self) -> None:
        self._heap = Heap(is_min=False)

    def enqueue(self, item: Any, priority: int) -> None:
        """
        O(log n).
        Помещает элемент с указанным приоритетом в очередь.
        """
        self._heap.insert((priority, item))

    def dequeue(self) -> Optional[Tuple[int, Any]]:
        """
        O(log n).
        Извлекает элемент с наибольшим приоритетом.
        Возвращает кортеж (priority, item) или None, если очередь пуста.
        """
        result = self._heap.extract()
        return result if result is not None else None

    def peek(self) -> Optional[Tuple[int, Any]]:
        """
        O(1).
        Просмотр элемента с наивысшим приоритетом без извлечения.
        """
        return self._heap.peek()
