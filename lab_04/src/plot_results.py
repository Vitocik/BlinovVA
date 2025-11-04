import os
import pandas as pd
import matplotlib.pyplot as plt

from performance_test import results


def plot_results():
    """Строит и сохраняет графики по результатам тестов."""

    # Создать папку для сохранения графиков
    os.makedirs("plots", exist_ok=True)

    for size, data in results.items():
        df = pd.DataFrame(data)

        # Создать график
        ax = df.plot(kind="bar", figsize=(10, 6))
        ax.set_title(f"Сравнение алгоритмов сортировки (n = {size})")
        ax.set_ylabel("Время (сек)")
        ax.set_xlabel("Тип входных данных")
        ax.grid(True)

        plt.xticks(rotation=0)
        plt.tight_layout()

        filename = f"plots/sort_compare_{size}.png"
        plt.savefig(filename)
        plt.close()

        print(f"[+] Сохранено: {filename}")


if __name__ == "__main__":
    plot_results()
