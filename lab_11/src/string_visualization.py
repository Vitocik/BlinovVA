"""
Визуализация алгоритмов поиска подстроки.
Создаёт графики и выводит примеры работы алгоритмов в консоль.
"""

import random
import statistics
import string
import time
from pathlib import Path
from typing import Callable

import matplotlib.pyplot as plt
import pandas as pd

from kmp_search import kmp_search
from prefix_function import prefix_function
from rabin_karp import rabin_karp
from string_matching import z_search
from z_function import z_function

# Папка для графиков
OUTPUT_DIR = Path("visualization_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


# ===============================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ===============================================================

def time_function(func: Callable, *args, repeats: int = 3) -> float:
    """Возвращает медианное время работы функции."""
    results = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        func(*args)
        t1 = time.perf_counter()
        results.append(t1 - t0)
    return statistics.median(results)


def random_string(n: int) -> str:
    """Генерирует случайную строку."""
    return "".join(random.choices(string.ascii_lowercase, k=n))


# ===============================================================
# БЕНЧМАРКИ
# ===============================================================

def benchmark(
    text_lengths: list[int],
    pattern_lengths: list[int]
) -> pd.DataFrame:
    """Замеряет время работы алгоритмов поиска подстроки."""
    rows = []

    for n in text_lengths:
        for m in pattern_lengths:
            if m > n:
                continue

            text = random_string(n)
            pattern = random_string(m)

            t_kmp = time_function(kmp_search, text, pattern)
            t_z = time_function(z_search, text, pattern)
            t_rk = time_function(rabin_karp, text, pattern)

            rows.append({
                "n": n,
                "m": m,
                "kmp": t_kmp,
                "z": t_z,
                "rk": t_rk,
            })

    return pd.DataFrame(rows)


# ===============================================================
# ПОСТРОЕНИЕ ГРАФИКОВ
# ===============================================================

def plot_time_vs_text(df: pd.DataFrame) -> str:
    plt.figure(figsize=(8, 5))

    for alg in ("kmp", "z", "rk"):
        grouped = df.groupby("n")[alg].median().reset_index()
        plt.plot(grouped["n"], grouped[alg], label=alg)

    plt.xlabel("Длина текста n")
    plt.ylabel("Время (с)")
    plt.title("Зависимость времени от длины текста")
    plt.legend()

    path = OUTPUT_DIR / "time_vs_text.png"
    plt.savefig(path)
    plt.close()
    return str(path)


def plot_time_vs_pattern(df: pd.DataFrame, text_length: int) -> str:
    df_fixed = df[df["n"] == text_length]

    plt.figure(figsize=(8, 5))

    for alg in ("kmp", "z", "rk"):
        grouped = df_fixed.groupby("m")[alg].median().reset_index()
        plt.plot(grouped["m"], grouped[alg], label=alg)

    plt.xlabel("Длина паттерна m")
    plt.ylabel("Время (с)")
    plt.title(f"Время поиска при фиксированном тексте n={text_length}")
    plt.legend()

    path = OUTPUT_DIR / "time_vs_pattern.png"
    plt.savefig(path)
    plt.close()
    return str(path)


def plot_array(arr: list[int], title: str, filename: str) -> str:
    plt.figure(figsize=(8, 4))
    plt.plot(range(len(arr)), arr)
    plt.xlabel("Индекс")
    plt.ylabel("Значение")
    plt.title(title)

    path = OUTPUT_DIR / filename
    plt.savefig(path)
    plt.close()
    return str(path)


# ===============================================================
# ОСНОВНОЙ БЛОК (запускается при старте файла)
# ===============================================================

if __name__ == "__main__":
    print("=== Пример работы алгоритмов ===\n")

    text = "ababcabcababc"
    pattern = "abc"

    print(f"Текст: {text}")
    print(f"Паттерн: {pattern}")
    print("KMP:", kmp_search(text, pattern))
    print("Z-search:", z_search(text, pattern))
    print("Rabin–Karp:", rabin_karp(text, pattern))

    print("\nСтрока: abababab")
    print("Период:", prefix_function("abababab")[-1])
    print()

    a = "abcdef"
    b = "defabc"
    print(f"a = '{a}'")
    print(f"b = '{b}'")
    print("b является циклическим сдвигом a:",
          b in (a + a))

    # Бенчмарки
    text_lengths = [2000, 4000, 8000]
    pattern_lengths = [3, 5, 10, 50]

    df = benchmark(text_lengths, pattern_lengths)

    p1 = plot_time_vs_text(df)
    p2 = plot_time_vs_pattern(df, text_length=8000)

    pi = prefix_function("ababcababababc")
    p3 = plot_array(pi, "Префикс-функция", "prefix_demo.png")

    z = z_function("ababcababababc")
    p4 = plot_array(z, "Z-функция", "z_demo.png")

    print("\nГрафики успешно созданы:")
    print(p1)
    print(p2)
    print(p3)
    print(p4)
