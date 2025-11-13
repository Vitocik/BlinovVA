"""Main script: тестирование хеш-таблиц и построение графиков."""

import random
import string
import time

import matplotlib.pyplot as plt

from hash_functions import djb2, polynomial_hash, simple_hash
from hash_table_chaining import ChainingHashTable
from hash_table_open_addressing import OpenAddressingHashTable


def random_string(length: int = 8) -> str:
    """Генерирует случайную строку."""
    return ''.join(random.choices(string.ascii_letters, k=length))


def measure_insert_performance(
    table_class,
    hash_func,
    mode: str | None = None,
    num_elements: int = 2000,
):
    """Замеряет время вставки для разных коэффициентов заполнения."""
    load_factors = [0.1, 0.3, 0.5, 0.7, 0.9]
    times = []
    collisions = []

    for lf in load_factors:
        capacity = 101
        if mode is None:
            table = table_class(capacity=capacity, hash_func=hash_func)
        else:
            table = table_class(
                capacity=capacity, hash_func=hash_func, mode=mode
            )

        n = int(capacity * lf)
        keys = [random_string() for _ in range(n)]

        start = time.perf_counter()
        for key in keys:
            table.insert(key, random.randint(0, 1000))
        elapsed = time.perf_counter() - start

        times.append(elapsed)
        collisions.append(table.collisions)

    return load_factors, times, collisions


def main() -> None:
    """Основная функция: тесты и построение графиков."""
    random.seed(42)

    # --- Проверка корректности работы ---
    print("=== Проверка корректности ===")
    ht = ChainingHashTable(hash_func=simple_hash)
    ht.insert("apple", 10)
    ht.insert("banana", 20)
    print("apple:", ht.get("apple"))
    print("banana:", ht.get("banana"))
    print("contains apple:", ht.contains("apple"))
    ht.remove("apple")
    print("после удаления apple:", ht.get("apple"))

    oa = OpenAddressingHashTable(hash_func=djb2, mode="linear")
    oa.insert("cat", 5)
    oa.insert("dog", 15)
    print("cat:", oa.get("cat"))
    print("dog:", oa.get("dog"))
    print("collisions:", oa.collisions)

    # --- Эксперимент ---
    print("\n=== Измерения ===")

    results = {}
    funcs = [
        ("simple_hash", simple_hash),
        ("polynomial_hash", polynomial_hash),
        ("djb2", djb2),
    ]

    for name, func in funcs:
        print(f"\nТест хеш-функции: {name}")
        lf, t_chain, c_chain = measure_insert_performance(
            ChainingHashTable, func
        )
        lf, t_linear, c_linear = measure_insert_performance(
            OpenAddressingHashTable, func, mode="linear"
        )
        lf, t_double, c_double = measure_insert_performance(
            OpenAddressingHashTable, func, mode="double"
        )

        results[name] = {
            "load": lf,
            "chaining": (t_chain, c_chain),
            "linear": (t_linear, c_linear),
            "double": (t_double, c_double),
        }

        # Печать таблицы времени и коллизий
        print("Коэфф. заполнения | chaining (с) | linear (с) | double (с)")
        print("-" * 60)
        for i, lf_val in enumerate(lf):
            print(
                f"{lf_val:>7.1f}              "
                f"{t_chain[i]:.6f}       "
                f"{t_linear[i]:.6f}       "
                f"{t_double[i]:.6f}"
            )
        print("\nКоллизии:")
        print("Метод цепочек:", c_chain)
        print("Линейное пробирование:", c_linear)
        print("Двойное хеширование:", c_double)

    # --- График 1: время вставки ---
    plt.figure(figsize=(8, 5))
    for name, data in results.items():
        lf = data["load"]
        plt.plot(
            lf, data["chaining"][0],
            marker='o', label=f"{name} - chaining"
        )
        plt.plot(
            lf, data["linear"][0],
            marker='x', label=f"{name} - linear"
        )
        plt.plot(
            lf, data["double"][0],
            marker='s', label=f"{name} - double"
        )
    plt.title("Время вставки в зависимости от коэффициента заполнения")
    plt.xlabel("Коэффициент заполнения")
    plt.ylabel("Время (сек)")
    plt.legend()
    plt.grid(True)
    plt.savefig("insertion_time.png", dpi=200)
    plt.close()

    # --- График 2: количество коллизий ---
    plt.figure(figsize=(8, 5))
    for name, data in results.items():
        lf = data["load"]
        plt.plot(
            lf, data["chaining"][1],
            marker='o', label=f"{name} - chaining"
        )
        plt.plot(
            lf, data["linear"][1],
            marker='x', label=f"{name} - linear"
        )
        plt.plot(
            lf, data["double"][1],
            marker='s', label=f"{name} - double"
        )
    plt.title("Количество коллизий при разных коэффициентах заполнения")
    plt.xlabel("Коэффициент заполнения")
    plt.ylabel("Число коллизий")
    plt.legend()
    plt.grid(True)
    plt.savefig("collisions.png", dpi=200)
    plt.close()

    # --- График 3: гистограмма распределения коллизий ---
    lf_index = 3  # для коэффициента заполнения 0.7
    funcs_names = []
    collisions_values = []

    for name, data in results.items():
        total_collisions = (
            data["chaining"][1][lf_index]
            + data["linear"][1][lf_index]
            + data["double"][1][lf_index]
        ) / 3
        funcs_names.append(name)
        collisions_values.append(total_collisions)

    plt.figure(figsize=(7, 5))
    plt.bar(
        funcs_names,
        collisions_values,
        color=["#4CAF50", "#2196F3", "#FFC107"],
    )
    plt.title("Среднее количество коллизий при коэффициенте заполнения 0.7")
    plt.xlabel("Хеш-функция")
    plt.ylabel("Среднее число коллизий")
    plt.grid(axis="y")
    plt.savefig("collisions_hist.png", dpi=200)
    plt.close()

    print(
        "\nГрафики сохранены как:\n"
        "  • insertion_time.png\n"
        "  • collisions.png\n"
        "  • collisions_hist.png"
    )


if __name__ == "__main__":
    main()
