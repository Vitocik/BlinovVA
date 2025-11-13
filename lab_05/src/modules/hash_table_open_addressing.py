from typing import Any, Callable, Iterator, List, Optional, Union

DEFAULT_INITIAL_CAPACITY = 53
DEFAULT_LOAD_FACTOR_THRESHOLD = 0.6

_DELETED = object()


class OpenAddressingHashTable:
    """Open addressing hash table supporting linear and double probing."""

    def __init__(
        self,
        capacity: int = DEFAULT_INITIAL_CAPACITY,
        hash_func: Optional[Callable[[str], int]] = None,
        second_hash_func: Optional[Callable[[str], int]] = None,
        mode: str = "linear",
        load_factor_threshold: float = DEFAULT_LOAD_FACTOR_THRESHOLD,
    ) -> None:
        assert mode in ("linear", "double")
        self._capacity: int = max(3, capacity)
        # ключи могут быть строкой, None или _DELETED (object)
        self._keys: List[Optional[Union[str,
                                        object]]] = [None] * self._capacity
        self._values: List[Optional[Any]] = [None] * self._capacity
        self._size: int = 0
        self._hash_func: Callable[[str], int] = hash_func or hash
        self._second_hash: Callable[[str], int]
        if second_hash_func is not None:
            self._second_hash = second_hash_func
        else:
            self._second_hash = lambda s: 1 + (hash(s) % (self._capacity - 1))
        self._mode: str = mode
        self._load_factor_threshold: float = load_factor_threshold
        self.collisions: int = 0

    def _probe_sequence(self, key: str) -> Iterator[int]:
        """Generator yielding probe indices."""
        h1 = self._hash_func(key) % self._capacity
        if self._mode == "linear":
            i = 0
            while True:
                yield (h1 + i) % self._capacity
                i += 1
        # double hashing
        step = self._second_hash(key) % self._capacity
        if step == 0:
            step = 1
        i = 0
        while True:
            yield (h1 + i * step) % self._capacity
            i += 1

    def insert(self, key: str, value: Any) -> None:
        """Insert or update key with value."""
        if self.load_factor() >= self._load_factor_threshold:
            new_cap = self._capacity * 2 + 1
            self._rehash(new_cap)
        first_del: Optional[int] = None
        for idx in self._probe_sequence(key):
            if self._keys[idx] is None:
                # empty slot
                target_idx = first_del if first_del is not None else idx
                self._keys[target_idx] = key
                self._values[target_idx] = value
                self._size += 1
                if target_idx != idx:
                    self.collisions += 1
                return
            if self._keys[idx] is _DELETED:
                if first_del is None:
                    first_del = idx
                # continue probing
                continue
            if self._keys[idx] == key:
                # update existing
                self._values[idx] = value
                return
            # occupied by another key -> collision
            self.collisions += 1
            continue

    def get(self, key: str) -> Optional[Any]:
        """Return value or None if absent."""
        for idx in self._probe_sequence(key):
            if self._keys[idx] is None:
                return None
            if self._keys[idx] is _DELETED:
                continue
            if self._keys[idx] == key:
                return self._values[idx]
        return None

    def remove(self, key: str) -> bool:
        """Remove key if present. Return True if removed."""
        for idx in self._probe_sequence(key):
            if self._keys[idx] is None:
                return False
            if self._keys[idx] is _DELETED:
                continue
            if self._keys[idx] == key:
                self._keys[idx] = _DELETED  # type: ignore[assignment]
                self._values[idx] = None
                self._size -= 1
                return True
        return False

    def contains(self, key: str) -> bool:
        return self.get(key) is not None

    def size(self) -> int:
        return self._size

    def capacity(self) -> int:
        return self._capacity

    def load_factor(self) -> float:
        return self._size / self._capacity

    def _rehash(self, new_capacity: int) -> None:
        """Rebuild table with new capacity."""
        old_items: list[tuple[str, Any]] = []
        for k, v in zip(self._keys, self._values):
            # фильтруем только реальные строковые ключи
            if isinstance(k, str):
                old_items.append((k, v))
        self._capacity = max(3, new_capacity)
        self._keys = [None] * self._capacity
        self._values = [None] * self._capacity
        self._size = 0
        for k, v in old_items:
            self.insert(k, v)
