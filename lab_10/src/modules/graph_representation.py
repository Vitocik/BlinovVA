"""
Модуль реализует два способа представления графов:
- AdjacencyMatrixGraph: матрица смежности.
- AdjacencyListGraph: список смежности.

Оба класса поддерживают:
- Добавление вершин и рёбер.
- Удаление рёбер.
- Получение соседей вершины.

Графы ориентированные, могут быть взвешенными (вес по умолчанию 1).
"""


from typing import Dict, List, Tuple


class AdjacencyMatrixGraph:
    """
    Граф, реализованный с помощью матрицы смежности.

    Атрибуты:
        size (int): Текущее количество вершин.
        matrix (List[List[int]]): Квадратная матрица размера size x size,
            где matrix[u][v] — вес ребра из u в v
            (0 означает отсутствие ребра).

    Особенности:
        - Хорошо подходит для плотных графов.
        - Проверка наличия ребра — за O(1).
        - Использование памяти — O(V²).
    """

    def __init__(self, vertex_count: int = 0) -> None:
        """
        Инициализирует пустой граф с заданным количеством вершин.

        Аргументы:
            vertex_count (int): Начальное количество вершин (по умолчанию 0).
        """
        self.size = vertex_count
        self.matrix = [
            [0 for _ in range(self.size)]
            for _ in range(self.size)
        ]

    def add_vertex(self) -> None:
        """
        Добавляет новую вершину в граф.

        Матрица расширяется на одну строку и один столбец, заполняемые нулями.
        """
        self.size += 1
        for row in self.matrix:
            row.append(0)
        self.matrix.append([0] * self.size)

    def add_edge(self, u: int, v: int, weight: int = 1) -> None:
        """
        Добавляет направленное ребро из u в v с заданным весом.

        Если ребро уже существует, его вес будет перезаписан.

        Аргументы:
            u (int): Исходящая вершина.
            v (int): Входящая вершина.
            weight (int): Вес ребра (по умолчанию 1).
        """
        self.matrix[u][v] = weight

    def remove_edge(self, u: int, v: int) -> None:
        """
        Удаляет направленное ребро из u в v.

        Эквивалентно установке веса в 0.

        Аргументы:
            u (int): Исходящая вершина.
            v (int): Входящая вершина.
        """
        self.matrix[u][v] = 0

    def neighbors(self, vertex: int) -> List[int]:
        """
        Возвращает список соседей заданной вершины.

        Аргументы:
            vertex (int): Вершина, соседей которой нужно найти.

        Возвращает:
            List[int]: Список вершин, в которые ведут рёбра из vertex.
        """
        return [
            i for i, w in enumerate(self.matrix[vertex])
            if w != 0
        ]


class AdjacencyListGraph:
    """
    Граф, реализованный с помощью списка смежности.

    Атрибуты:
        graph (Dict[int, List[Tuple[int, int]]]): Словарь, где ключ — вершина,
            значение — список кортежей (сосед, вес).

    Особенности:
        - Эффективен для разреженных графов.
        - Использование памяти — O(V + E).
        - Быстрый доступ к соседям вершины.
    """

    def __init__(self, vertex_count: int = 0) -> None:
        """
        Инициализирует граф с заданным количеством вершин без рёбер.

        Аргументы:
            vertex_count (int): Начальное количество вершин (по умолчанию 0).
        """
        self.graph: Dict[int, List[Tuple[int, int]]] = {
            i: [] for i in range(vertex_count)
        }

    def add_vertex(self) -> None:
        """
        Добавляет новую вершину с наименьшим свободным индексом.

        Новая вершина не соединена ни с одной другой.
        """
        self.graph[len(self.graph)] = []

    def add_edge(self, u: int, v: int, weight: int = 1) -> None:
        """
        Добавляет направленное ребро из u в v с заданным весом.

        Если ребро уже существует, добавляется дубликат
        (мультграф не контролируется).

        Аргументы:
            u (int): Исходящая вершина.
            v (int): Входящая вершина.
            weight (int): Вес ребра (по умолчанию 1).
        """
        self.graph[u].append((v, weight))

    def remove_edge(self, u: int, v: int) -> None:
        """
        Удаляет все рёбра из u в v.

        Аргументы:
            u (int): Исходящая вершина.
            v (int): Входящая вершина.
        """
        self.graph[u] = [(x, w) for x, w in self.graph[u] if x != v]

    def neighbors(self, vertex: int) -> List[int]:
        """
        Возвращает список соседей заданной вершины.

        Аргументы:
            vertex (int): Вершина, соседей которой нужно найти.

        Возвращает:
            List[int]: Список вершин, в которые ведут рёбра из vertex.
        """
        return [v for v, _ in self.graph[vertex]]
