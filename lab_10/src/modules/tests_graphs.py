import unittest

from graph_representation import AdjacencyListGraph, AdjacencyMatrixGraph
from graph_traversal import bfs, dfs_iterative, dfs_recursive
from shortest_path import connected_components, topological_sort, dijkstra


class TestGraphs(unittest.TestCase):
    def setUp(self):
        # Маленький граф 0→1→2→3→0
        self.al = AdjacencyListGraph(4)
        self.al.add_edge(0, 1)
        self.al.add_edge(1, 2)
        self.al.add_edge(2, 3)
        self.al.add_edge(3, 0)

        self.am = AdjacencyMatrixGraph(4)
        self.am.add_edge(0, 1)
        self.am.add_edge(1, 2)
        self.am.add_edge(2, 3)
        self.am.add_edge(3, 0)

    def test_neighbors(self):
        self.assertEqual(sorted(self.al.neighbors(0)), [1])
        self.assertEqual(sorted(self.am.neighbors(3)), [0])

    def test_bfs(self):
        g = {i: [x for x, _ in self.al.graph[i]] for i in self.al.graph}
        dist = bfs(g, 0)
        self.assertEqual(dist[3], 3)

    def test_dfs(self):
        g = {i: [x for x, _ in self.al.graph[i]] for i in self.al.graph}
        rec = dfs_recursive(g, 0)
        it = dfs_iterative(g, 0)
        self.assertIn(0, rec)
        self.assertIn(0, it)

    def test_components(self):
        g = {0: [1], 1: [], 2: [3], 3: []}
        comps = connected_components(g)
        self.assertEqual(len(comps), 2)

    def test_topological_sort(self):
        dag = {0: [1], 1: [2], 2: []}
        order = topological_sort(dag)
        self.assertEqual(order, [0, 1, 2])

    def test_dijkstra(self):
        g = {0: [(1, 4)], 1: [(2, 5)], 2: []}
        dist = dijkstra(g, 0)
        self.assertEqual(dist[2], 9)


if __name__ == "__main__":
    unittest.main()
