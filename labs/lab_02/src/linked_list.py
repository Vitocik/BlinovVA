# === linked_list.py ===

from __future__ import annotations
from typing import Any, Iterator, Optional


class Node:
    """Узел связного списка."""

    def __init__(self, data: Any, next: Optional['Node'] = None) -> None:
        self.data = data
        self.next = next

    def __repr__(self) -> str:  # pragma: no cover
        return f"Node({self.data!r})"


class LinkedList:
    """Простой односвязный список с хвостовым указателем.

    Методы и их временная сложность (в комментариях рядом с методом):
    - insert_at_start: O(1)
    - insert_at_end: O(1) с tail
    - delete_from_start: O(1)
    - traversal: O(n)
    - __len__: O(n) (можно сделать O(1), поддерживая счётчик)
    """

    def __init__(self) -> None:
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._size: int = 0  # поддерживаем размер для O(1) len

    def insert_at_start(self, value: Any) -> None:
        """Вставка в начало — O(1)."""
        new_node = Node(value, self.head)
        self.head = new_node
        if self.tail is None:
            self.tail = new_node
        self._size += 1

    def insert_at_end(self, value: Any) -> None:
        """Вставка в конец — O(1) благодаря tail."""
        new_node = Node(value)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            assert self.tail is not None
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def delete_from_start(self) -> Any:
        """Удаление из начала — O(1).

        Возвращает удалённое значение или вызывает IndexError, если список пуст
        """
        if self.head is None:
            raise IndexError("delete_from_start from empty LinkedList")
        node = self.head
        self.head = node.next
        if self.head is None:
            self.tail = None
        self._size -= 1
        return node.data

    def traversal(self) -> Iterator[Any]:
        """Обход списка — O(n)."""
        current = self.head
        while current is not None:
            yield current.data
            current = current.next

    def to_list(self) -> list:
        """Конвертировать в Python list — O(n)."""
        return list(self.traversal())

    def __len__(self) -> int:
        """Возвращает размер — O(1) (так как мы поддерживаем _size)."""
        return self._size

    def __iter__(self) -> Iterator[Any]:
        return self.traversal()


# Простой самотест
if __name__ == '__main__':
    ll = LinkedList()
    ll.insert_at_start(1)
    ll.insert_at_start(2)
    ll.insert_at_end(3)
    print('LinkedList ->', ll.to_list())
    print('Delete:', ll.delete_from_start())
    print('After delete ->', ll.to_list())
