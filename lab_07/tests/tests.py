"""
Простые unit-тесты для проверки корректности реализации.
Запуск:
python -m unittest tests.py
"""

import unittest
from heap import Heap  # noqa: E402
from heapsort import heapsort, heapsort_inplace  # noqa: E402
from priority_queue import PriorityQueue  # noqa: E402


class TestHeap(unittest.TestCase):
    def test_insert_extract_min(self):
        h = Heap(is_min=True)
        data = [5, 3, 8, 1, 2]
        for x in data:
            h.insert(x)
        sorted_out = [h.extract() for _ in range(len(data))]
        self.assertEqual(sorted_out, sorted(data))

    def test_build_heap(self):
        arr = [9, 4, 7, 1, 3, 6]
        h = Heap(is_min=True)
        h.build_heap(arr)
        out = [h.extract() for _ in range(len(arr))]
        self.assertEqual(out, sorted(arr))

    def test_max_heap(self):
        arr = [2, 9, 1, 7]
        h = Heap(is_min=False)
        for x in arr:
            h.insert(x)
        out = [h.extract() for _ in range(len(arr))]
        self.assertEqual(out, sorted(arr, reverse=True))


class TestHeapsort(unittest.TestCase):
    def test_heapsort(self):
        arr = [3, 1, 4, 1, 5, 9, 2]
        out = heapsort(arr)
        self.assertEqual(out, sorted(arr))

    def test_heapsort_inplace(self):
        arr = [7, 3, 5, 2, 9]
        arr_copy = arr[:]
        heapsort_inplace(arr_copy)
        self.assertEqual(arr_copy, sorted(arr))


class TestPriorityQueue(unittest.TestCase):
    def test_pq(self):
        pq = PriorityQueue()
        pq.enqueue("a", priority=2)
        pq.enqueue("b", priority=5)
        pq.enqueue("c", priority=3)
        top = pq.dequeue()
        # ожидаем наибольший приоритет 5
        self.assertEqual(top[0], 5)
        self.assertEqual(top[1], "b")


if __name__ == "__main__":
    unittest.main()
