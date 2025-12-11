"""
Unit-тесты для всех алгоритмов.
"""

import unittest

from kmp_search import kmp_search
from prefix_function import prefix_function
from rabin_karp import rabin_karp
from string_matching import z_search
from z_function import z_function


class TestStringAlgorithms(unittest.TestCase):

    def test_prefix_function(self):
        self.assertEqual(
            prefix_function("ababc"),
            [0, 0, 1, 2, 0]
        )

    def test_kmp(self):
        self.assertEqual(
            kmp_search("ababcabcababc", "abc"),
            [2, 5, 10]
        )

    def test_z_function(self):
        self.assertEqual(
            z_function("aaaaa"),
            [0, 4, 3, 2, 1]
        )

    def test_z_search(self):
        self.assertEqual(
            z_search("aaaaa", "aa"),
            [0, 1, 2, 3]
        )

    def test_rabin_karp(self):
        self.assertEqual(
            rabin_karp("abracadabra", "abra"),
            [0, 7]
        )


if __name__ == "__main__":
    unittest.main()
