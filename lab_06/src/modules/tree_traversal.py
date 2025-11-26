# tree_traversal.py
from typing import List, Optional


class TreeNode:
    """Класс узла бинарного дерева."""
    def __init__(self, value: int, left: Optional['TreeNode'] = None,
                 right: Optional['TreeNode'] = None):
        self.value = value
        self.left = left
        self.right = right


def inorder_recursive(node: Optional[TreeNode]) -> List[int]:
    """
    Рекурсивный обход бинарного дерева в порядке "лево-узел-право" (in-order).

    Аргументы:
        node (Optional[TreeNode]): Корень бинарного дерева.

    Возвращает:
        List[int]: Список значений узлов в порядке in-order.
    """
    result: List[int] = []

    def _in(n: Optional[TreeNode]):
        if n is None:
            return
        _in(n.left)
        result.append(n.value)
        _in(n.right)

    _in(node)
    return result


def preorder_recursive(node: Optional[TreeNode]) -> List[int]:
    """
    Рекурсивный обход бинарного дерева в порядке "узел-лево-право" (pre-order).

    Аргументы:
        node (Optional[TreeNode]): Корень бинарного дерева.

    Возвращает:
        List[int]: Список значений узлов в порядке pre-order.
    """
    result: List[int] = []

    def _pre(n: Optional[TreeNode]):
        if n is None:
            return
        result.append(n.value)
        _pre(n.left)
        _pre(n.right)

    _pre(node)
    return result


def postorder_recursive(node: Optional[TreeNode]) -> List[int]:
    """
    Рекурсивный обход бинарного дерева в порядке "лево-право-узел"
    (post-order).

    Аргументы:
        node (Optional[TreeNode]): Корень бинарного дерева.

    Возвращает:
        List[int]: Список значений узлов в порядке post-order.
    """
    result: List[int] = []

    def _post(n: Optional[TreeNode]):
        if n is None:
            return
        _post(n.left)
        _post(n.right)
        result.append(n.value)

    _post(node)
    return result


def inorder_iterative(node: Optional[TreeNode]) -> List[int]:
    """
    Итеративный обход бинарного дерева в порядке "лево-узел-право"
    (in-order) с использованием стека.

    Аргументы:
        node (Optional[TreeNode]): Корень бинарного дерева.

    Возвращает:
        List[int]: Список значений узлов в порядке in-order.
    """
    result: List[int] = []
    stack: List[TreeNode] = []
    current = node

    while stack or current:
        while current:
            stack.append(current)
            current = current.left

        current = stack.pop()
        result.append(current.value)
        current = current.right

    return result
