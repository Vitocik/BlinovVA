"""Unit tests для проекта."""

import unittest

from hash_functions import djb2, polynomial_hash, simple_hash
from hash_table_chaining import ChainingHashTable
from hash_table_open_addressing import OpenAddressingHashTable


class TestHashFunctions(unittest.TestCase):
    def test_simple_hash_consistent(self) -> None:
        self.assertEqual(simple_hash("abc"), simple_hash("abc"))

    def test_polynomial_hash_distinct(self) -> None:
        self.assertNotEqual(polynomial_hash("abc"), polynomial_hash("acb"))

    def test_djb2_consistent(self) -> None:
        self.assertEqual(djb2("hello"), djb2("hello"))


class TestChainingHashTable(unittest.TestCase):
    def test_insert_get(self) -> None:
        t = ChainingHashTable(capacity=7)
        t.insert("a", 1)
        t.insert("b", 2)
        self.assertEqual(t.get("a"), 1)
        self.assertEqual(t.get("b"), 2)
        self.assertTrue(t.contains("a"))
        self.assertTrue(t.remove("a"))
        self.assertFalse(t.contains("a"))

    def test_overwrite(self) -> None:
        t = ChainingHashTable(capacity=7)
        t.insert("k", 1)
        t.insert("k", 2)
        self.assertEqual(t.get("k"), 2)


class TestOpenAddressingHashTable(unittest.TestCase):
    def test_linear_insert_get(self) -> None:
        t = OpenAddressingHashTable(capacity=7, mode="linear")
        t.insert("a", 1)
        t.insert("b", 2)
        self.assertEqual(t.get("a"), 1)
        self.assertEqual(t.get("b"), 2)
        self.assertTrue(t.remove("a"))
        self.assertFalse(t.contains("a"))

    def test_double_insert_get(self) -> None:
        t = OpenAddressingHashTable(capacity=7, mode="double")
        t.insert("a", 1)
        t.insert("b", 2)
        self.assertEqual(t.get("a"), 1)
        self.assertEqual(t.get("b"), 2)


if __name__ == "__main__":
    unittest.main()
