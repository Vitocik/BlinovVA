# Лабораторная работа: анализ сложности алгоритмов (O(1) и O(N))
# Примеры: проверка чётности числа и поиск максимума в массиве

import timeit
import random
import matplotlib.pyplot as plt


# ----------------------------
# Функции
# ----------------------------

def is_even(n: int) -> bool:  # O(1) – определение функции
    """Пример функции O(1): проверка чётности числа"""
    return n % 2 == 0  # O(1) – операция деления по модулю и сравнение
# Общая сложность: O(1)


def find_max(arr):  # O(1) – определение функции
    """Пример функции O(N): поиск максимального элемента"""
    maximum = arr[0]  # O(1) доступ к элементу по индексу и присваивание 
    for num in arr:  # O(N) – цикл по всем элементам массива
        if num > maximum:  # O(1) – сравнение
            maximum = num  # O(1) – присваивание
    return maximum  # O(1) – возврат результата
    # Общая сложность: O(1) + O(N) * (O(1) + O(1)) + O(1) = O(N)


# ----------------------------
# Ваша функция замера времени
# ----------------------------

def measure_time(func, data):
    """Измеряет время выполнения функции в миллисекундах."""
    start_time = timeit.default_timer()
    func(data)
    end_time = timeit.default_timer()
    return (end_time - start_time) * 1000  # мс


# ----------------------------
# Эксперименты
# ----------------------------

pc_info = """
Характеристики ПК для тестирования:
- Процессор: 12th Gen Intel(R) Core(TM) i5-12450H 2.00 GHz
- Оперативная память: 16 GB DDR4
- ОС: Windows 11 Pro
- Python: 3.10.10
"""
print(pc_info)

sizes_linear = [1000, 5000, 10000, 20000, 50000, 100000]  # Размеры массивов
random.seed(123)

results = []

# O(N) — поиск максимума
for n in sizes_linear:
    data = [random.randint(1, 1000) for _ in range(n)]
    time_ms = measure_time(find_max, data)
    results.append(('O(N) find_max', n, time_ms))

# O(1) — проверка чётности числа
time_const = measure_time(lambda d=None: is_even(123456), None)
results.append(('O(1) is_even', 1, time_const))


# ----------------------------
# Вывод результатов в консоль и файл
# ----------------------------

output_lines = []
output_lines.append(pc_info + "\n")
output_lines.append("Результаты замеров (мс):\n")
for algo, n, t in results:
    line = f"{algo:20s} N={n:<7d} time={t:.6f} мс"
    print(line)
    output_lines.append(line + "\n")

output_lines.append("\nВыводы:\n")
output_lines.append("- Функция is_even имеет константную сложность O(1).\n")
output_lines.append("- Функция find_max имеет линейную сложность O(N).\n")

with open("sum_analysis.txt", "w", encoding="utf-8") as f:
    f.writelines(output_lines)


# ----------------------------
# Построение графика
# ----------------------------

plt.figure(figsize=(8, 5))
for algo in set(r[0] for r in results):
    sub = [(n, t) for a, n, t in results if a == algo]
    Ns, times = zip(*sub)
    plt.plot(Ns, times, marker='o', label=algo)

plt.xlabel("Размер входа N")
plt.ylabel("Время (мс)")
plt.title("Эмпирическая сложность: O(1) vs O(N)")
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

# Сохраняем график в файл PNG
plt.savefig("performance.png", dpi=300, bbox_inches="tight")

plt.show()
