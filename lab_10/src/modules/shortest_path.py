"""
Модуль для работы с графами: поиск компонент связности,
топологическая сортировка,
алгоритм Дейкстры для поиска кратчайших путей.

Функции:
- connected_components: находит все компоненты связности в
неориентированном/ориентированном графе.
- topological_sort: выполняет топологическую сортировку ориентированного
ациклического графа (DAG).
- dijkstra: находит кратчайшие расстояния от стартовой вершины до всех
остальных (для графов с неотрицательными весами).
"""

from typing import Dict, List, Tuple
import heapq


def connected_components(graph: Dict[int, List[int]]) -> List[List[int]]:
    """
    Находит все компоненты связности в графе.

    Использует обход в глубину (DFS) с помощью стека.

    Аргументы:
        graph (Dict[int, List[int]]): Граф в виде списка смежности.

    Возвращает:
        List[List[int]]: Список компонент связности,
        где каждая компонента — список вершин.
    """
    visited = set()
    components = []

    for vertex in graph:
        if vertex not in visited:
            stack = [vertex]
            comp = []

            while stack:
                v = stack.pop()
                if v not in visited:
                    visited.add(v)
                    comp.append(v)
                    stack.extend(graph.get(v, []))

            components.append(comp)

    return components


def topological_sort(graph: Dict[int, List[int]]) -> List[int]:
    """
    Выполняет топологическую сортировку
    ориентированного ациклического графа (DAG).

    Использует DFS: вершины добавляются в порядке
    завершения обхода, затем результат разворачивается.

    Аргументы:
        graph (Dict[int, List[int]]):
        Ориентированный граф в виде списка смежности.

    Возвращает:
        List[int]: Список вершин в топологическом порядке.
                   Для пустого графа возвращает пустой список.
    """
    visited = set()
    order = []

    def dfs(v: int) -> None:
        visited.add(v)
        for nbr in graph.get(v, []):
            if nbr not in visited:
                dfs(nbr)
        order.append(v)

    for v in graph:
        if v not in visited:
            dfs(v)

    return order[::-1]


def dijkstra(
    graph: Dict[int, List[Tuple[int, int]]],
    start: int
) -> Dict[int, float]:
    """
    Алгоритм Дейкстры для поиска кратчайших путей от
    стартовой вершины до всех остальных.

    Работает только с графами, имеющими неотрицательные веса рёбер.

    Аргументы:
        graph (Dict[int, List[Tuple[int, int]]]):
        Взвешенный граф в виде списка смежности.
            Ключ — вершина, значение — список кортежей (сосед, вес).
        start (int): Стартовая вершина.

    Возвращает:
        Dict[int, float]: Словарь, где ключ — вершина,
        значение — кратчайшее расстояние от start.
            Для недостижимых вершин значение — float('inf').
            Расстояние от start до себя — 0.0.
    """
    distances: Dict[int, float] = {v: float("inf") for v in graph}
    distances[start] = 0.0

    priority_queue: List[Tuple[float, int]] = [(0.0, start)]

    while priority_queue:
        dist, vertex = heapq.heappop(priority_queue)

        if dist > distances[vertex]:
            continue

        for nbr, weight in graph.get(vertex, []):
            new_dist = dist + weight
            if new_dist < distances[nbr]:
                distances[nbr] = new_dist
                heapq.heappush(priority_queue, (new_dist, nbr))

    return distances
