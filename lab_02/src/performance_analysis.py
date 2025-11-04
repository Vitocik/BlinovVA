# === performance_analysis.py ===
"""
Сценарии измерений:
1) Вставка в начало: list.insert(0, x) vs LinkedList.insert_at_start
2) Очередь: list.pop(0) vs collections.deque.popleft

"""

from __future__ import annotations
import os
import time
from collections import deque
from typing import Callable, List

import matplotlib.pyplot as plt

from linked_list import LinkedList


def time_function(fn: Callable[[], None], repeats: int = 3) -> float:
    """Возвращает среднее время выполнения fn при repeats запусках."""
    times: List[float] = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        t1 = time.perf_counter()
        times.append(t1 - t0)
    return sum(times) / len(times)


def measure_insert_start_list(n: int) -> float:
    """Измерить n вставок в начало для Python list: O(n) на вставк в среднем"""
    def work():
        lst = []
        for i in range(n):
            lst.insert(0, i)
    return time_function(work)


def measure_insert_start_linkedlist(n: int) -> float:
    """Измерить n вставок в начало для LinkedList: O(1) на вставку."""
    def work():
        ll = LinkedList()
        for i in range(n):
            ll.insert_at_start(i)
    return time_function(work)


def measure_dequeue_list_pop0(n: int) -> float:
    """Заполнить список n элементами, затем делать pop(0) n раз."""
    def work():
        lst = list(range(n))
        for _ in range(n):
            lst.pop(0)
    return time_function(work)


def measure_deque_popleft(n: int) -> float:
    def work():
        d = deque(range(n))
        for _ in range(n):
            d.popleft()
    return time_function(work)


def ensure_plots_dir() -> str:
    out = 'plots'
    os.makedirs(out, exist_ok=True)
    return out


def run_all_measurements(sizes: List[int]) -> None:
    outdir = ensure_plots_dir()

    list_times = []
    linked_times = []
    pop0_times = []
    popleft_times = []

    pc_info = """
    Характеристики ПК для тестирования:
    - Процессор: 12th Gen Intel(R) Core(TM) i5-12450H 2.00 GHz
    - Оперативная память: 16 GB DDR4
    - ОС: Windows 11 Pro
    - Python: 3.10.10
    """
    print(pc_info)

    for n in sizes:
        print(f'Measuring n={n}...')
        lt = measure_insert_start_list(n)
        llt = measure_insert_start_linkedlist(n)
        pt = measure_dequeue_list_pop0(n)
        dpt = measure_deque_popleft(n)

        list_times.append(lt)
        linked_times.append(llt)
        pop0_times.append(pt)
        popleft_times.append(dpt)

    # Построим графики
    plt.figure()
    plt.plot(sizes, list_times, marker='o', label='list.insert(0, x)')
    plt.plot(sizes,
             linked_times, marker='o',
             label='LinkedList.insert_at_start')
    plt.xlabel('n (количество вставок)')
    plt.ylabel('время (секунд)')
    plt.title('Вставка в начало: list vs LinkedList')
    plt.legend()
    plt.grid(True)
    fname1 = os.path.join(outdir, 'insert_start_list_vs_linkedlist.png')
    plt.savefig(fname1)
    print('Saved', fname1)

    plt.figure()
    plt.plot(sizes, pop0_times, marker='o', label='list.pop(0)')
    plt.plot(sizes, popleft_times, marker='o', label='deque.popleft()')
    plt.xlabel('n (количество операций dequeue)')
    plt.ylabel('время (секунд)')
    plt.title('Очередь: list.pop(0) vs deque.popleft()')
    plt.legend()
    plt.grid(True)
    fname2 = os.path.join(outdir, 'queue_list_vs_deque.png')
    plt.savefig(fname2)
    print('Saved', fname2)

    print("\nSummary (first/last values):")
    print(
        f"insert_start list: {list_times[0]:.10f} ... "
        f"{list_times[-1]:.10f}"
    )
    print(
        f"insert_start linked: {linked_times[0]:.10f} ... "
        f"{linked_times[-1]:.10f}"
    )
    print(
        f"pop(0): {pop0_times[0]:.10f} ... "
        f"{pop0_times[-1]:.10f}"
    )
    print(
        f"popleft: {popleft_times[0]:.10f} ... "
        f"{popleft_times[-1]:.10f}"
    )


if __name__ == '__main__':
    # Подбираем набор размеров. Для интерактивной отладки можно уменьшить.
    sizes = [100, 500, 1000, 2000]
    run_all_measurements(sizes)
