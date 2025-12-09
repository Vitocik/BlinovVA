"""
Жадные алгоритмы.

Содержит реализации:
- выбор заявок (Interval Scheduling)
- дробный рюкзак (Fractional Knapsack)
- кодирование Хаффмана (Huffman Algorithm)
- размен монет
- алгоритм Краскала (Minimum Spanning Tree)

Каждый алгоритм снабжен:
- временной сложностью;
- объяснением корректности жадного выбора.
"""

import heapq
from typing import Dict, Iterable, List, Optional, Tuple

Interval = Tuple[int, int]
Item = Tuple[float, float]
Edge = Tuple[float, int, int]


def interval_scheduling(intervals: Iterable[Interval]) -> List[Interval]:
    """
    Выбор максимального числа непересекающихся интервалов.

    Жадная стратегия:
        Выбирать интервалы с наименьшим временем окончания.

    Корректность жадного выбора:
        Если интервал заканчивается раньше других, то он оставляет
        максимальное пространство для последующих интервалов.
        Доказано методом "обмена": любое оптимальное решение можно
        преобразовать в решение жадного алгоритма, не ухудшая его.

    Временная сложность:
        O(n log n) — сортировка интервалов.

    :param intervals: iterable из пар (start, end)
    :return: список выбранных интервалов
    """
    sorted_intervals = sorted(intervals, key=lambda x: x[1])
    result: List[Interval] = []
    last_end: Optional[int] = None

    for start, end in sorted_intervals:
        if last_end is None or start >= last_end:
            result.append((start, end))
            last_end = end

    return result


def fractional_knapsack(
    items: List[Item],
    capacity: float,
) -> Tuple[float, List[Tuple[int, float]]]:
    """
    Дробная задача о рюкзаке.

    Жадная стратегия:
        Выбирать предметы в порядке убывания удельной стоимости (value/weight).

    Корректность:
        Для дробной версии оптимальное решение достигается сортировкой
        по удельной стоимости.
        Доказано с помощью метода обмена: любую стратегию всегда можно
        улучшить,
        заменив менее выгодный фрагмент более выгодным.

    Временная сложность:
        O(n log n) — сортировка предметов.

    :param items: список (value, weight)
    :param capacity: вместимость рюкзака
    :return: (максимальная стоимость, [(индекс, доля предмета)...])
    """
    indexed = []
    for index, (value, weight) in enumerate(items):
        ratio = value / weight if weight else float("inf")
        indexed.append((index, value, weight, ratio))

    indexed.sort(key=lambda x: x[3], reverse=True)

    total_value = 0.0
    remaining = capacity
    taken: List[Tuple[int, float]] = []

    for index, value, weight, _ in indexed:
        if remaining <= 0:
            break

        if weight <= remaining:
            taken.append((index, 1.0))
            total_value += value
            remaining -= weight
        else:
            fraction = remaining / weight
            taken.append((index, fraction))
            total_value += value * fraction
            remaining = 0

    return total_value, taken


class HuffmanNode:
    """Узел дерева Хаффмана."""

    def __init__(
        self,
        freq: int,
        symbol: Optional[str] = None,
        left: Optional["HuffmanNode"] = None,
        right: Optional["HuffmanNode"] = None,
    ) -> None:
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right

    def __lt__(self, other: "HuffmanNode") -> bool:
        return self.freq < other.freq


def build_huffman_tree(frequencies: Dict[str, int]) -> HuffmanNode:
    """
    Построение дерева Хаффмана.

    Жадный выбор:
        На каждом шаге объединяются два наименее частотных узла.

    Корректность:
        Алгоритм Хаффмана доказан как оптимальный:
        объединение двух минимальных частот гарантирует минимизацию
        суммарной длины закодированного сообщения.
        Это следует из "Свободного выбора" и "Оптимальной подструктуры".

    Временная сложность:
        O(n log n) — операции с приоритетной очередью.

    :param frequencies: частоты символов
    :return: корень дерева
    """
    heap = [HuffmanNode(freq, symbol) for symbol, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(left.freq + right.freq, None, left, right)
        heapq.heappush(heap, merged)

    return heap[0]


def huffman_codes(frequencies: Dict[str, int]) -> Dict[str, str]:
    """
    Генерация кодов Хаффмана.

    Временная сложность:
        O(n) — обход дерева.

    :param frequencies: частоты символов
    :return: словарь {символ: код}
    """
    root = build_huffman_tree(frequencies)
    codes: Dict[str, str] = {}

    def traverse(node: HuffmanNode, prefix: str) -> None:
        if node.symbol is not None:
            codes[node.symbol] = prefix or "0"
            return
        if node.left:
            traverse(node.left, prefix + "0")
        if node.right:
            traverse(node.right, prefix + "1")

    traverse(root, "")
    return codes


def greedy_coin_change(
    amount: int,
    coins: Iterable[int],
) -> List[Tuple[int, int]]:
    """
    Жадный алгоритм размена монет.

    Жадная стратегия:
        Всегда брать монету с максимальным номиналом.

    Корректность:
        Для стандартной системы монет (1,5,10,25,...)
        жадное решение оптимально.
        Но встречаются контрпримеры (например монеты 1,3,4 → размен 6).

    Временная сложность:
        O(n log n) — сортировка номиналов.

    :param amount: сумма
    :param coins: доступные номиналы
    :return: список (монета, количество)
    """
    remaining = amount
    result: List[Tuple[int, int]] = []

    for coin in sorted(coins, reverse=True):
        count = remaining // coin
        if count:
            result.append((coin, count))
            remaining -= coin * count

    return result


class DisjointSet:
    """Система непересекающихся множеств для алгоритма Краскала."""

    def __init__(self, size: int) -> None:
        self.parent = list(range(size))

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False
        self.parent[root_y] = root_x
        return True


def kruskal_mst(nodes: int, edges: Iterable[Edge]) -> List[Edge]:
    """
    Алгоритм Краскала — построение минимального остовного дерева.

    Жадная стратегия:
        Выбирать ребро минимального веса, которое не создаёт цикл.

    Корректность:
        Базируется на "Свойстве безопасного выбора":
        минимальное ребро, пересекающее разрез, всегда принадлежит МОД.

    Временная сложность:
        O(E log E) — сортировка рёбер

    :param nodes: количество вершин
    :param edges: список рёбер (вес, u, v)
    :return: рёбра МОД
    """
    result: List[Edge] = []
    ds = DisjointSet(nodes)

    for weight, u, v in sorted(edges, key=lambda e: e[0]):
        if ds.union(u, v):
            result.append((weight, u, v))
        if len(result) == nodes - 1:
            break

    return result
