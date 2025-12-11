from collections import deque
import random
from shortest_path import connected_components, topological_sort

# ----------------------------
# 1) Кратчайший путь в лабиринте
# ----------------------------


def build_maze(rows, cols, wall_prob=0.25, seed=0):
    random.seed(seed)
    maze = [[1 if random.random() < wall_prob else 0 for _ in range(cols)]
            for _ in range(rows)]
    maze[0][0] = 0
    maze[rows - 1][cols - 1] = 0
    return maze


def maze_to_graph(maze):
    rows, cols = len(maze), len(maze[0])
    g = {}
    d = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 0:
                idx = i * cols + j
                g[idx] = []
                for di, dj in d:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols and maze[ni][nj] == 0:
                        g[idx].append(ni * cols + nj)
    return g


def shortest_path_in_maze(maze):
    graph = maze_to_graph(maze)
    start = 0
    goal = len(maze) * len(maze[0]) - 1

    queue = deque([start])
    prev = {start: None}

    while queue:
        v = queue.popleft()
        if v == goal:
            break
        for nbr in graph.get(v, []):
            if nbr not in prev:
                prev[nbr] = v
                queue.append(nbr)

    if goal not in prev:
        return None

    # восстановление пути
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    return path[::-1]


# ----------------------------
# 2) Определить связность сети
# ----------------------------

def build_random_network(n, p=0.03, seed=0):
    random.seed(seed)
    g = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                g[i].append(j)
                g[j].append(i)
    return g


def is_network_connected(graph):
    """
    Используем поиск компонент связности.
    Если компонент ровно одна — сеть связна.
    """
    comps = connected_components(graph)
    return len(comps) == 1


# ----------------------------
# 3) Топологическая сортировка
# ----------------------------

def sample_dag():
    return {
        0: [1, 2],
        1: [3],
        2: [3],
        3: []
    }


if __name__ == "__main__":
    # 1) Лабиринт
    maze = build_maze(10, 10, wall_prob=0.3)
    path = shortest_path_in_maze(maze)
    print("Maze shortest path length:", len(path) if path else None)

    # 2) Сеть
    net = build_random_network(50, p=0.05)
    print("Network connected:", is_network_connected(net))

    # 3) Топологическая сортировка
    dag = sample_dag()
    print("Topological order:", topological_sort(dag))
