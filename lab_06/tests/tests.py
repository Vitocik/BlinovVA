# tests.py
import unittest

from binary_search_tree import BinarySearchTree
import tree_traversal as trav


class TestBST(unittest.TestCase):
    """
    Набор unit-тестов для проверки корректности реализации
    бинарного дерева поиска (BinarySearchTree).

    Проверяются:
        • вставка элементов
        • поиск значений
        • корректность обходов дерева
        • удаление узлов в разных случаях
        • свойства корректного BST
        • высота дерева, минимум, максимум
    """

    def setUp(self):
        """
        Создаёт тестовое дерево перед каждым тестом.

        Дерево:
                     50
                  /      /
                30        70
               /  /      /  /
             20  40    60  80
        """

        self.bst = BinarySearchTree()
        for v in [50, 30, 70, 20, 40, 60, 80]:
            self.bst.insert(v)

    def test_search(self):
        """Тест: поиск существующих и несуществующего значений."""
        self.assertIsNotNone(self.bst.search(50))
        self.assertIsNotNone(self.bst.search(20))
        self.assertIsNone(self.bst.search(999))

    def test_inorder(self):
        """Тест: корректность рекурсивного in-order обхода."""
        inorder = trav.inorder_recursive(self.bst.root)
        self.assertEqual(inorder, sorted(inorder))
        self.assertEqual(inorder, [20, 30, 40, 50, 60, 70, 80])

    def test_pre_and_post_order(self):
        """Тест: pre-order и post-order обходы возвращают 7 элементов."""
        pre = trav.preorder_recursive(self.bst.root)
        post = trav.postorder_recursive(self.bst.root)
        self.assertEqual(len(pre), 7)
        self.assertEqual(len(post), 7)

    def test_iterative_inorder(self):
        """Тест: итеративный in-order должен совпадать с рекурсивным."""
        result = trav.inorder_iterative(self.bst.root)
        self.assertEqual(result, [20, 30, 40, 50, 60, 70, 80])

    def test_delete_leaf(self):
        """Тест: удаление листа (20) не нарушает свойств BST."""
        self.bst.delete(20)
        self.assertIsNone(self.bst.search(20))
        self.assertTrue(self.bst.is_valid_bst())

    def test_delete_node_one_child(self):
        """
        Тест: удаление узла с одним потомком.
        Узел 30 имеет левого потомка 25.
        """
        self.bst.insert(25)
        self.bst.delete(30)
        self.assertTrue(self.bst.is_valid_bst())

    def test_delete_node_two_children(self):
        """Тест: удаление узла с двумя потомками (50)."""
        self.bst.delete(50)
        self.assertIsNone(self.bst.search(50))
        self.assertTrue(self.bst.is_valid_bst())

    def test_min_max_height(self):
        """Тест: корректность find_min, find_max и вычисления высоты."""
        self.assertEqual(self.bst.find_min().value, 20)
        self.assertEqual(self.bst.find_max().value, 80)
        self.assertIsInstance(self.bst.height(), int)


if __name__ == "__main__":
    unittest.main()
