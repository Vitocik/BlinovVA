"""Хеш-таблица с методом цепочек (Chaining)."""

from typing import Any, Callable, List, Optional, Tuple

DEFAULT_INITIAL_CAPACITY = 53
DEFAULT_LOAD_FACTOR_THRESHOLD = 0.75


class ChainingHashTable:
    """Хеш-таблица с методом цепочек."""

    def __init__(
        self,
        capacity: int = DEFAULT_INITIAL_CAPACITY,
        hash_func: Optional[Callable[[str], int]] = None,
        load_factor_threshold: float = DEFAULT_LOAD_FACTOR_THRESHOLD,
    ) -> None:
        self._capacity: int = max(3, capacity)
        # each bucket: list of (key, value)
        self._buckets: List[List[Tuple[str, Any]]] = [
            [] for _ in range(self._capacity)
        ]
        self._size: int = 0
        self._hash_func: Callable[[str], int] = hash_func or hash
        self._load_factor_threshold: float = load_factor_threshold
        self.collisions: int = 0

    def _index(self, key: str) -> int:
        return self._hash_func(key) % self._capacity

    def insert(self, key: str, value: Any) -> None:
        """Insert or update key with value."""
        idx: int = self._index(key)
        bucket = self._buckets[idx]
        if bucket:
            # bucket not empty -> potential collision
            self.collisions += 1
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1
        if self.load_factor() > self._load_factor_threshold:
            self._rehash(self._capacity * 2 + 1)

    def get(self, key: str) -> Optional[Any]:
        """Return value or None if absent."""
        idx = self._index(key)
        for k, v in self._buckets[idx]:
            if k == key:
                return v
        return None

    def remove(self, key: str) -> bool:
        """Remove key if present. Return True if removed."""
        idx = self._index(key)
        bucket = self._buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self._size -= 1
                return True
        return False

    def contains(self, key: str) -> bool:
        """Return True if key in table."""
        return self.get(key) is not None

    def size(self) -> int:
        return self._size

    def capacity(self) -> int:
        return self._capacity

    def load_factor(self) -> float:
        return self._size / self._capacity

    def _rehash(self, new_capacity: int) -> None:
        """Rebuild table with new capacity."""
        old_items: List[Tuple[str, Any]] = [
            item for bucket in self._buckets for item in bucket
        ]
        self._capacity = max(3, new_capacity)
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0
        # collisions counter preserved for analysis
        for k, v in old_items:
            self.insert(k, v)
