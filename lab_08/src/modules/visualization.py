"""
Модуль визуализации для алгоритма Хаффмана.

Содержит функции:
- отрисовка дерева Хаффмана;
- построение графика зависимости времени работы от размера входных данных.
"""

from typing import List

import matplotlib.pyplot as plt


class HuffmanNode:
    """
    Узел дерева Хаффмана.
    """

    def __init__(
        self,
        symbol: str | None,
        freq: int,
        left: "HuffmanNode | None" = None,
        right: "HuffmanNode | None" = None,
    ) -> None:
        self.symbol = symbol
        self.freq = freq
        self.left = left
        self.right = right


def _draw_node(
    ax: plt.Axes,
    node: HuffmanNode,
    x: float,
    y: float,
    dx: float,
) -> None:
    """
    Рекурсивная отрисовка узлов дерева.
    """
    label = f"{node.symbol}:{node.freq}" if node.symbol else str(node.freq)
    ax.text(x, y, label, ha="center", va="center")

    if node.left:
        ax.plot([x, x - dx], [y, y - 1])
        _draw_node(ax, node.left, x - dx, y - 1, dx / 2)

    if node.right:
        ax.plot([x, x + dx], [y, y - 1])
        _draw_node(ax, node.right, x + dx, y - 1, dx / 2)


def draw_huffman_tree(root: HuffmanNode, filename: str) -> None:
    """
    Сохраняет изображение дерева Хаффмана в PNG-файл.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis("off")

    _draw_node(ax, root, 0.5, 1.0, 0.25)

    plt.savefig(filename)
    plt.close()


def plot_time_vs_size(
    sizes: List[int],
    times: List[float],
    filename: str,
) -> None:
    """
    Строит график зависимости времени работы от размера входных данных.
    """
    plt.figure()
    plt.plot(sizes, times, marker="o")
    plt.xlabel("Размер входных данных")
    plt.ylabel("Время выполнения (сек)")
    plt.grid(True)
    plt.savefig(filename)
    plt.close()
