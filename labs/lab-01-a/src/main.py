import time
import matplotlib.pyplot as plt


# Линейный поиск O(n)
def linear_search(arr, target):
    """
    Выполняет линейный поиск элемента в списке.

    :param arr: Список, в котором производится поиск.
    :param target: Элемент, который необходимо найти.
    :return: Индекс первого вхождения элемента `target` в списке `arr`,
             если элемент найден; иначе `None`.
    """
    for i in range(len(arr)):  # O(n) - цикл по всем элементам массива
        if arr[i] == target:  # O(1) - сравнение элемента с target
            return i  # O(1) - возврат индекса при совпадении
    return None  # O(1) - возврат None, если не найден


# Бинарный поиск O(log n)
def binary_search(arr, target):
    """
    Выполняет бинарный поиск элемента в отсортированном списке.

    :param arr: Отсортированный список, в котором производится поиск.
    :param target: Элемент, который необходимо найти.
    :return: Индекс первого вхождения элемента `target` в списке `arr`,
             если элемент найден; иначе `None`.
    """
    left, right = 0, len(arr) - 1  # O(1) - инициализация границ
    while left <= right:  # O(log n) - цикл, делящий массив пополам
        mid = (left + right) // 2  # O(1) - вычисление середины
        if arr[mid] == target:  # O(1) - сравнение с элементом в середине
            return mid  # O(1) - возврат индекса при совпадении
        elif arr[mid] < target:  # O(1) - проверка, куда сместить границу
            left = mid + 1  # O(1) - смещение левой границы
        else:
            right = mid - 1  # O(1) - смещение правой границы
    return None  # O(1) - возврат None, если не найден


# Замер времени выполнения функции
def measure_time(func, arr, target, repeats=5):
    """
    Замеряет среднее время выполнения функции поиска.

    :param func: Функция поиска (например, linear_search или binary_search).
    :param arr: Список для поиска.
    :param target: Целевой элемент для поиска.
    :param repeats: Количество повторений для усреднения времени.
    :return: Среднее время выполнения функции в секундах.
    """
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        func(arr, target)
        t1 = time.perf_counter()
        times.append(t1 - t0)
    return sum(times) / len(times)


pc_info = """
Характеристики ПК для тестирования:
- Процессор: 12th Gen Intel(R) Core(TM) i5-12450H 2.00 GHz
- Оперативная память: 16 GB DDR4
- ОС: Windows 11 Pro
- Python: 3.10.10
"""
print(pc_info)


if __name__ == "__main__":
    # Определяем размеры массивов для тестирования
    sizes = [1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000]
    linear_times = []  # Время для линейного поиска
    binary_times = []  # Время для бинарного поиска

    with open("results.txt", "w", encoding="utf-8") as f:
        f.write("Размер массива | Linear (ms) | Binary (ms)\n")
        f.write("----------------------------------------\n")

        for n in sizes:
            # Создаем отсортированный массив размером n
            arr = list(range(n))
            # Тестируемые цели: начало, середина, конец, несуществующий элемент
            targets = [arr[0], arr[n // 2], arr[-1], -1]

            lin_total = 0
            bin_total = 0
            for t in targets:
                lin_total += measure_time(linear_search, arr, t)
                bin_total += measure_time(binary_search, arr, t)

            # Среднее время на цель
            lin_avg = lin_total / len(targets)
            bin_avg = bin_total / len(targets)

            linear_times.append(lin_avg)
            binary_times.append(bin_avg)

            # Выводим результаты в миллисекундах
            line = (
                f"n={n:6d} | linear={lin_avg*1000:.5f} ms | "
                f"binary={bin_avg*1000:.5f} ms"
            )
            print(line)
            f.write(line + "\n")
        f.write(pc_info)

    # График (обычная шкала)
    plt.figure(figsize=(8, 5))
    plt.plot(sizes, [t * 1000 for t in linear_times],
             marker="o", label="Linear search")
    plt.plot(sizes, [t * 1000 for t in binary_times],
             marker="o", label="Binary search")
    plt.xlabel("Array size (n)")
    plt.ylabel("Time (ms)")
    plt.title("Search time vs array size (linear scale)")
    plt.legend()
    plt.grid(True)
    plt.savefig("time_vs_n_linear.png", bbox_inches="tight")

    # График (логарифмическая шкала)
    plt.figure(figsize=(8, 5))
    plt.plot(sizes, [t * 1000 for t in linear_times],
             marker="o", label="Linear search")
    plt.plot(sizes, [t * 1000 for t in binary_times],
             marker="o", label="Binary search")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Array size (n) [log]")
    plt.ylabel("Time (ms) [log]")
    plt.title("Search time vs array size (log-log scale)")
    plt.legend()
    plt.grid(True, which="both", ls="--")
    plt.savefig("time_vs_n_loglog.png", bbox_inches="tight")

    print("Графики сохранены: time_vs_n_linear.png, time_vs_n_loglog.png")
