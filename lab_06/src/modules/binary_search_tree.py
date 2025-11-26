# binary_search_tree.py
from __future__ import annotations

from typing import Optional, Generator, List


class TreeNode:
    """
    Класс, представляющий узел бинарного дерева поиска (BST).

    Атрибуты:
        value (int): Значение узла.
        left (TreeNode | None): Левый потомок.
        right (TreeNode | None): Правый потомок.
    """

    def __init__(self, value: int) -> None:
        """
        Инициализирует узел с заданным значением.

        Аргументы:
            value (int): Значение, которое будет храниться в узле.
        """
        self.value: int = value
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None

    def __repr__(self) -> str:
        """Возвращает строковое представление узла."""
        return f"TreeNode({self.value})"


class BinarySearchTree:
    """
    Класс бинарного дерева поиска (BST).

    Атрибуты:
        root (TreeNode | None): Корневой элемент дерева.
    """

    def __init__(self) -> None:
        """Создаёт пустое бинарное дерево поиска."""
        self.root: Optional[TreeNode] = None

    # -------------------------------------------------------------
    # INSERT (ITERATIVE)
    # -------------------------------------------------------------
    def insert(self, value: int) -> None:
        """
        Итеративно вставляет новое значение в BST.

        Аргументы:
            value (int): Значение для вставки.

        Сложность:
            Средняя: O(log n)
            Худшая: O(n)
        """
        if self.root is None:
            self.root = TreeNode(value)
            return

        current = self.root
        while True:
            if value < current.value:
                if current.left is None:
                    current.left = TreeNode(value)
                    return
                current = current.left

            elif value > current.value:
                if current.right is None:
                    current.right = TreeNode(value)
                    return
                current = current.right

            else:
                # Дубликаты не вставляем.
                return

    # -------------------------------------------------------------
    # SEARCH (ITERATIVE)
    # -------------------------------------------------------------
    def search(self, value: int) -> Optional[TreeNode]:
        """
        Ищет значение в BST.

        Аргументы:
            value (int): Искомое значение.

        Возвращает:
            TreeNode | None: Узел, если найден; иначе None.
        """
        current = self.root
        while current:
            if value == current.value:
                return current

            if value < current.value:
                current = current.left
            else:
                current = current.right

        return None

    # -------------------------------------------------------------
    # DELETE (ITERATIVE)
    # -------------------------------------------------------------
    def delete(self, value: int) -> None:
        """
        Удаляет узел с указанным значением из дерева.

        Обрабатывает все 3 случая:
            1) Узел — лист
            2) Узел имеет одного потомка
            3) Узел имеет двух потомков (замена inorder successor)

        Аргументы:
            value (int): Значение, подлежащее удалению.
        """
        parent: Optional[TreeNode] = None
        node: Optional[TreeNode] = self.root

        # Ищем удаляемый узел
        while node and node.value != value:
            parent = node
            if value < node.value:
                node = node.left
            else:
                node = node.right

        if node is None:
            return  # Нет такого значения

        # Случай 1 и 2: узел имеет 0 или 1 потомка
        if node.left is None or node.right is None:
            new_child = node.left if node.left else node.right

            if parent is None:
                self.root = new_child
            else:
                if parent.left is node:
                    parent.left = new_child
                else:
                    parent.right = new_child

            return

        # Случай 3: узел имеет двух потомков
        succ_parent = node
        succ = node.right

        # Ищем inorder successor (минимум справа)
        while succ.left:
            succ_parent = succ
            succ = succ.left

        # Копируем значение
        node.value = succ.value

        # Удаляем successor
        child = succ.right
        if succ_parent.left is succ:
            succ_parent.left = child
        else:
            succ_parent.right = child

    # -------------------------------------------------------------
    # FIND MIN / MAX
    # -------------------------------------------------------------
    def find_min(self, node: Optional[TreeNode] = None) -> Optional[TreeNode]:
        """
        Возвращает узел с минимальным значением (самый левый элемент).

        Аргументы:
            node (TreeNode | None): Начальный узел.

        Возвращает:
            TreeNode | None
        """
        if node is None:
            node = self.root
        if node is None:
            return None

        while node.left:
            node = node.left
        return node

    def find_max(self, node: Optional[TreeNode] = None) -> Optional[TreeNode]:
        """
        Возвращает узел с максимальным значением (самый правый элемент).

        Аргументы:
            node (TreeNode | None): Начальный узел.

        Возвращает:
            TreeNode | None
        """
        if node is None:
            node = self.root
        if node is None:
            return None

        while node.right:
            node = node.right
        return node

    # -------------------------------------------------------------
    # HEIGHT
    # -------------------------------------------------------------
    def height(self, node: Optional[TreeNode] = None) -> int:
        """
        Рекурсивно вычисляет высоту дерева.

        Высота пустого дерева равна 0.

        Сложность:
            O(n) – требуется посетить все узлы.
        """
        if node is None:
            node = self.root
        if node is None:
            return 0

        left_h = self.height(node.left) if node.left else 0
        right_h = self.height(node.right) if node.right else 0
        return 1 + max(left_h, right_h)

    # -------------------------------------------------------------
    # VALID BST CHECK
    # -------------------------------------------------------------
    def is_valid_bst(self) -> bool:
        """
        Проверяет корректность BST по диапазонам значений.

        Возвращает:
            bool: True, если дерево корректно.
        """
        stack: List[
            tuple[Optional[TreeNode], float, float]
        ] = [(self.root, float("-inf"), float("inf"))]

        while stack:
            node, low, high = stack.pop()
            if node is None:
                continue

            if not low < node.value < high:
                return False

            stack.append((node.right, node.value, high))
            stack.append((node.left, low, node.value))

        return True

    # -------------------------------------------------------------
    # TEXT VISUALIZATION
    # -------------------------------------------------------------
    def visualize(
        self,
        node: Optional[TreeNode] = None,
        indent: str = ""
    ) -> str:
        """
        Возвращает дерево в виде многострочного текста с отступами.

        Аргументы:
            node (TreeNode | None): Начальный узел.
            indent (str): Текущий отступ.

        Возвращает:
            str: Текстовое представление дерева.
        """
        if node is None:
            node = self.root
        if node is None:
            return "<empty tree>\n"

        lines: List[str] = []

        def _viz(n: Optional[TreeNode], pref: str) -> None:
            if n is None:
                lines.append(pref + "·")
                return
            lines.append(pref + str(n.value))
            _viz(n.left, pref + "  ")
            _viz(n.right, pref + "  ")

        _viz(node, indent)
        return "\n".join(lines) + "\n"

    # -------------------------------------------------------------
    # BRACKET REPRESENTATION
    # -------------------------------------------------------------
    def bracket_repr(self, node: Optional[TreeNode] = None) -> str:
        """
        Возвращает дерево в виде скобочной последовательности:

        Формат: value(left_subtree)(right_subtree)

        Пример:
            10(5(3()())(8()()))(15()())

        Аргументы:
            node (TreeNode | None): Узел для печати.

        Возвращает:
            str: Скобочное представление дерева.
        """
        if node is None:
            node = self.root
        if node is None:
            return ""

        def _br(n: Optional[TreeNode]) -> str:
            if n is None:
                return "()"
            return f"{n.value}{_br(n.left)}{_br(n.right)}"

        return _br(node)

    # -------------------------------------------------------------
    # INORDER VALUES GENERATOR
    # -------------------------------------------------------------
    def inorder_values(self) -> Generator[int, None, None]:
        """
        Генератор, возвращающий значения в порядке in-order.

        Возвращает:
            Generator[int]: Последовательность значений.
        """
        stack: List[TreeNode] = []
        current = self.root

        while stack or current:
            while current:
                stack.append(current)
                current = current.left

            current = stack.pop()
            yield current.value
            current = current.right
