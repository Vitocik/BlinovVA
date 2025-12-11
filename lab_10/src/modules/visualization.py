"""
Модуль визуализации и анализа алгоритмов на графах.

Содержит функции для:
- Генерации случайных направленных и взвешенных графов.
- Реализации и замера времени выполнения алгоритмов: BFS, DFS, Dijkstra.
- Визуализации графов и путей с помощью matplotlib.

Автоматически при запуске:
- Проводит замеры производительности.
- Генерирует графики времени выполнения.
- Визуализирует примеры графов и путей.
"""

import math
import random
import time
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt


# ----------------------------------------
# Генерация случайных графов
# ----------------------------------------

def generate_graph(
    size: int,
    edge_prob: float = 0.02
) -> Dict[int, List[int]]:
    """
    Создаёт случайный ориентированный граф.

    Каждая пара вершин соединяется дугой с заданной вероятностью.
    Петли (самосвязи) исключены.

    Аргументы:
        size (int): Количество вершин в графе.
        edge_prob (float): Вероятность существования ребра (по умолчанию 0.02).

    Возвращает:
        Dict[int, List[int]]: Граф в виде списка смежности.
    """
    graph: Dict[int, List[int]] = {i: [] for i in range(size)}

    for i in range(size):
        for j in range(size):
            if i != j and random.random() < edge_prob:
                graph[i].append(j)

    return graph


def generate_weighted_graph(
    size: int,
    edge_prob: float = 0.02
) -> Dict[int, List[Tuple[int, int]]]:
    """
    Создаёт случайный взвешенный ориентированный граф.

    Каждое ребро имеет случайный вес от 1 до 10.

    Аргументы:
        size (int): Количество вершин.
        edge_prob (float): Вероятность существования ребра.

    Возвращает:
        Dict[int, List[Tuple[int, int]]]: Взвешенный граф в
        виде списка смежности,
        где каждое ребро представлено кортежем (сосед, вес).
    """
    graph: Dict[int, List[Tuple[int, int]]] = {
        i: [] for i in range(size)
    }

    for i in range(size):
        for j in range(size):
            if i != j and random.random() < edge_prob:
                weight = random.randint(1, 10)
                graph[i].append((j, weight))

    return graph


# ----------------------------------------
# Алгоритмы
# ----------------------------------------

def bfs(graph: Dict[int, List[int]], start: int) -> None:
    """
    Обход графа в ширину (Breadth-First Search).

    Использует очередь для посещения вершин уровня за уровнем.

    Аргументы:
        graph (Dict[int, List[int]]): Граф в виде списка смежности.
        start (int): Начальная вершина для обхода.
    """
    visited: set[int] = set()
    queue: List[int] = [start]

    while queue:
        v = queue.pop(0)
        visited.add(v)
        for nbr in graph[v]:
            if nbr not in visited:
                queue.append(nbr)


def dfs(graph: Dict[int, List[int]], start: int) -> None:
    """
    Обход графа в глубину (Depth-First Search).

    Использует стек для рекурсивного подобного обхода.

    Аргументы:
        graph (Dict[int, List[int]]): Граф в виде списка смежности.
        start (int): Начальная вершина для обхода.
    """
    visited: set[int] = set()
    stack: List[int] = [start]

    while stack:
        v = stack.pop()
        visited.add(v)
        for nbr in graph[v]:
            if nbr not in visited:
                stack.append(nbr)


def dijkstra(
    graph: Dict[int, List[Tuple[int, int]]],
    start: int
) -> None:
    """
    Алгоритм Дейкстры для поиска кратчайших путей в взвешенном графе.

    Использует приоритетную очередь (min-heap) для оптимизации.

    Аргументы:
        graph (Dict[int, List[Tuple[int, int]]]): Взвешенный граф.
        start (int): Стартовая вершина.
    """
    import heapq

    dist: Dict[int, float] = {v: float("inf") for v in graph}
    dist[start] = 0.0
    pq: List[Tuple[float, int]] = [(0.0, start)]

    while pq:
        d, v = heapq.heappop(pq)
        if d > dist[v]:
            continue
        for nbr, w in graph[v]:
            new_dist = d + w
            if new_dist < dist[nbr]:
                dist[nbr] = new_dist
                heapq.heappush(pq, (new_dist, nbr))


# ----------------------------------------
# Замер времени
# ----------------------------------------

def benchmark() -> None:
    """
    Проводит бенчмарк производительности алгоритмов: BFS, DFS, Dijkstra.

    Для каждого размера графа из списка:
    - Генерируются обычный и взвешенный графы.
    - Замеряется время выполнения каждого алгоритма.
    - Результаты строятся на графике и сохраняются в файл.

    Эффекты:
        - Сохраняет график времени выполнения в файл
        "benchmark_algorithms.png".
        - Выводит прогресс в stdout.
    """
    sizes: List[int] = [50, 100, 200, 400, 600, 800, 1000]

    bfs_times: List[float] = []
    dfs_times: List[float] = []
    dij_times: List[float] = []

    for size in sizes:
        graph: Dict[int, List[int]] = generate_graph(size)
        w_graph: Dict[int, List[Tuple[int, int]]] = (
            generate_weighted_graph(size)
        )

        t = time.perf_counter()
        bfs(graph, 0)
        bfs_times.append(time.perf_counter() - t)

        t = time.perf_counter()
        dfs(graph, 0)
        dfs_times.append(time.perf_counter() - t)

        t = time.perf_counter()
        dijkstra(w_graph, 0)
        dij_times.append(time.perf_counter() - t)

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, bfs_times, label="BFS")
    plt.plot(sizes, dfs_times, label="DFS")
    plt.plot(sizes, dij_times, label="Dijkstra")
    plt.xlabel("Размер графа (вершин)")
    plt.ylabel("Время (сек)")
    plt.title("Зависимость времени работы алгоритмов от размера графа")
    plt.grid(True)
    plt.legend()

    plt.savefig("benchmark_algorithms.png", dpi=150)
    plt.close()


# ----------------------------------------
# Визуализация графа
# ----------------------------------------

def draw_graph(
    graph: Dict[int, List[int]],
    filename: str = "graph_visual.png"
) -> None:
    """
    Визуализирует граф, размещая вершины на окружности.

    Аргументы:
        graph (Dict[int, List[int]]): Граф для отображения.
        filename (str): Имя выходного файла изображения.
    """
    n = len(graph)
    coords: Dict[int, Tuple[float, float]] = {}

    for i in range(n):
        angle = 2 * math.pi * i / n
        coords[i] = (math.cos(angle), math.sin(angle))

    plt.figure(figsize=(7, 7))

    for u in graph:
        for v in graph[u]:
            x1, y1 = coords[u]
            x2, y2 = coords[v]
            plt.plot([x1, x2], [y1, y2], linewidth=1)

    for v, (x, y) in coords.items():
        plt.scatter(x, y, s=80)
        plt.text(x, y, str(v), fontsize=10)

    plt.axis("off")
    plt.savefig(filename, dpi=150)
    plt.close()


# ----------------------------------------
# Визуализация пути
# ----------------------------------------

def draw_path(
    graph: Dict[int, List[int]],
    path: List[int],
    filename: str = "graph_path.png"
) -> None:
    """
    Визуализирует граф и выделяет заданный путь красной линией.

    Аргументы:
        graph (Dict[int, List[int]]): Граф для отображения.
        path (List[int]): Список вершин, образующих путь.
        filename (str): Имя выходного файла изображения.
    """
    n = len(graph)
    coords: Dict[int, Tuple[float, float]] = {}

    for i in range(n):
        angle = 2 * math.pi * i / n
        coords[i] = (math.cos(angle), math.sin(angle))

    plt.figure(figsize=(7, 7))

    for u in graph:
        for v in graph[u]:
            x1, y1 = coords[u]
            x2, y2 = coords[v]
            plt.plot([x1, x2], [y1, y2], "gray", linewidth=1)

    px = [coords[v][0] for v in path]
    py = [coords[v][1] for v in path]
    plt.plot(px, py, "red", linewidth=3)

    for v, (x, y) in coords.items():
        plt.scatter(x, y, s=80)
        plt.text(x, y, str(v), fontsize=10)

    plt.axis("off")
    plt.savefig(filename, dpi=150)
    plt.close()


# ----------------------------------------
# Автозапуск
# ----------------------------------------

if __name__ == "__main__":
    """
    Точка входа: автоматически запускает:
    - Бенчмарк алгоритмов.
    - Визуализацию случайного графа.
    - Визуализацию примера пути.
    """
    benchmark()
    print("✔ benchmark_algorithms.png создан")

    test_graph: Dict[int, List[int]] = generate_graph(10)
    draw_graph(test_graph)
    print("✔ graph_visual.png создан")

    example_path: List[int] = [0, 3, 6, 8]
    draw_path(test_graph, example_path)
    print("✔ graph_path.png создан")
