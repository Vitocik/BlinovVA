# memoization.py
import time

import matplotlib.pyplot as plt


# -----------------------------
# Функция 1: наивная рекурсивная Фибоначчи
# -----------------------------
def fib_naive(n: int) -> int:
    """
    Наивное рекурсивное вычисление числа Фибоначчи.

    Сложность:
    - Время: O(2^n) — экспоненциальная,
    - т.к. каждая функция вызывает две подфункции
    - Глубина рекурсии: n
    - Память (стек вызовов): O(n)
    """
    if n <= 1:
        return n  # базовые случаи: F(0)=0, F(1)=1
    # рекурсивный шаг: F(n) = F(n-1) + F(n-2)
    return fib_naive(n - 1) + fib_naive(n - 2)


# -----------------------------
# Функция 2: мемоизированная Фибоначчи
# -----------------------------
def fib_memo(n: int, cache=None) -> int:
    """
    Мемоизированная версия функции Фибоначчи.

    Сложность:
    - Время: O(n) — каждое значение вычисляется один раз и сохраняется в кэше
    - Глубина рекурсии: n
    - Память: O(n) — кэш хранит n значений
    """
    if cache is None:
        cache = {}  # создаём пустой кэш при первом вызове

    if n in cache:
        return cache[n]  # если значение уже есть, возвращаем его без рекурсии

    if n <= 1:
        cache[n] = n  # базовые случаи
    else:
        # рекурсивное вычисление с сохранением результата в кэше
        cache[n] = fib_memo(n - 1, cache) + fib_memo(n - 2, cache)

    return cache[n]  # возвращаем результат


# -----------------------------
# Функция 3: сравнение производительности
# -----------------------------
def compare_fib_performance():
    """
    Сравнивает производительность наивной и мемоизированной рекурсии,
    строит график и сохраняет его в PNG-файл.
    """

    pc_info = """
    Характеристики ПК для тестирования:
    - Процессор: 12th Gen Intel(R) Core(TM) i5-12450H 2.00 GHz
    - Оперативная память: 16 GB DDR4
    - ОС: Windows 11 Pro
    - Python: 3.10.10
    """
    print(pc_info)

    print("Сравнение времени выполнения рекурсии с мемоизацией и без:")

    n = 35  # число Фибоначчи для быстрого сравнения

    # --- Наивная рекурсия ---
    start = time.time()
    fib_naive(n)
    naive_time = time.time() - start
    print(f"Наивная рекурсия ({n}): {naive_time:.4f} сек")

    # --- С мемоизацией ---
    start = time.time()
    fib_memo(n)
    memo_time = time.time() - start
    print(f"С мемоизацией ({n}): {memo_time:.4f} сек")

    # --- Построение графика ---
    values = range(5, 36)  # диапазон n для графика
    times_naive = []  # список времени для наивной функции
    times_memo = []   # список времени для мемоизированной функции

    for i in values:
        # время наивной функции
        start = time.time()
        fib_naive(i)
        times_naive.append(time.time() - start)

        # время мемоизированной функции
        start = time.time()
        fib_memo(i)
        times_memo.append(time.time() - start)

    plt.figure(figsize=(8, 5))
    plt.plot(values, times_naive, label="Наивная рекурсия", marker="o")
    plt.plot(values, times_memo, label="С мемоизацией", marker="o")

    # подписи оси X через каждые 5 единиц
    tick_values = [5, 10, 15, 20, 25, 30, 35]
    plt.xticks(tick_values)

    plt.title("Сравнение времени вычисления чисел Фибоначчи")
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # сохраняем график в файл
    output_file = "fibonacci_plot.png"
    plt.savefig(output_file, dpi=300)
    plt.close()

    print(f"\nГрафик сохранён в файл: {output_file}")


# -----------------------------
# Главная программа
# -----------------------------
if __name__ == "__main__":
    compare_fib_performance()
