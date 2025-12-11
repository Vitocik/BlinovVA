"""
Модуль реализует алгоритмы обхода графов:
поиск в ширину (BFS) и поиск в глубину (DFS).

Функции:
- bfs: находит кратчайшие расстояния от стартовой вершины
до всех достижимых (в рёбрах).
- dfs_recursive: обход в глубину с использованием рекурсии.
- dfs_iterative: итеративная версия DFS с явным использованием стека.

Граф предполагается неориентированным или ориентированным,
представленным в виде словаря
списков смежности. Вершины — целые числа.
"""

from collections import deque
from typing import Dict, List, Set


def bfs(graph: Dict[int, List[int]], start: int) -> Dict[int, int]:
    """
    Поиск в ширину (Breadth-First Search).

    Находит кратчайшие расстояния (в количестве рёбер)
    от стартовой вершины до всех достижимых.

    Аргументы:
        graph (Dict[int, List[int]]): Граф в виде списка смежности.
        start (int): Стартовая вершина для обхода.

    Возвращает:
        Dict[int, int]: Словарь, где ключ — вершина, значение —
        расстояние от start до этой вершины.
                        Для недостижимых вершин запись отсутствует.
                        Расстояние от start до себя — 0.

    Сложность: O(V + E), где V — количество вершин, E — количество рёбер.
    """
    visited = set()
    distance = {start: 0}
    queue = deque([start])

    while queue:
        vertex = queue.popleft()
        visited.add(vertex)

        for neighbor in graph[vertex]:
            if neighbor not in visited and neighbor not in queue:
                distance[neighbor] = distance[vertex] + 1
                queue.append(neighbor)

    return distance


def dfs_recursive(graph: Dict[int, List[int]], start: int) -> List[int]:
    """
    Рекурсивный поиск в глубину (Depth-First Search).

    Возвращает порядок обхода вершин.

    Аргументы:
        graph (Dict[int, List[int]]): Граф в виде списка смежности.
        start (int): Стартовая вершина для обхода.

    Возвращает:
        List[int]: Список вершин в порядке их первого
        посещения при обходе в глубину.

    Сложность: O(V + E)
    """
    visited: Set[int] = set()
    result: List[int] = []

    def dfs(v: int) -> None:
        visited.add(v)
        result.append(v)
        for nbr in graph[v]:
            if nbr not in visited:
                dfs(nbr)

    dfs(start)
    return result


def dfs_iterative(graph: Dict[int, List[int]], start: int) -> List[int]:
    """
    Итеративный поиск в глубину с использованием стека.

    Эквивалентен рекурсивному DFS, но избегает ограничений на глубину рекурсии.

    Аргументы:
        graph (Dict[int, List[int]]): Граф в виде списка смежности.
        start (int): Стартовая вершина для обхода.

    Возвращает:
        List[int]: Список вершин в порядке их посещения
        (аналогичен рекурсивному DFS).

    Сложность: O(V + E)
    """
    visited = set()
    stack = [start]
    result = []

    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            result.append(vertex)
            # Добавляем соседей в обратном порядке,
            # чтобы сохранить порядок обхода,
            # аналогичный рекурсивному DFS.
            stack.extend(reversed(graph[vertex]))

    return result
