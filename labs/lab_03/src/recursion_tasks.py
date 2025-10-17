# recursion_tasks.py
import os


# -----------------------------
# Функция 1: рекурсивный бинарный поиск
# -----------------------------
def binary_search_recursive(arr, target, left=0, right=None):
    """
    Рекурсивный бинарный поиск.

    Сложность:
    - Время: O(log n) — массив делится пополам на каждом шаге
    - Глубина рекурсии: log₂(n)
    - Память (стек вызовов): O(log n)
    """
    if right is None:
        right = len(arr) - 1  # задаём правую границу при первом вызове
    if left > right:
        return -1  # элемент не найден

    mid = (left + right) // 2  # индекс середины
    if arr[mid] == target:
        return mid  # элемент найден
    elif arr[mid] > target:
        # ищем в левой половине
        return binary_search_recursive(arr, target, left, mid - 1)
    else:
        # ищем в правой половине
        return binary_search_recursive(arr, target, mid + 1, right)


# -----------------------------
# Глобальная переменная для измерения глубины рекурсии при обходе каталогов
# -----------------------------
max_recursion_depth = 0


# -----------------------------
# Функция 2: обход файловой системы
# -----------------------------
def print_dir_tree(path, indent=0, max_depth=None, current_depth=1):
    """
    Рекурсивный обход файловой системы с измерением глубины.

    Сложность:
    - Время: O(N), где N — количество файлов и папок в обходимой части
    - Глубина рекурсии: ≤ max_depth (или глубина самой глубокой папки)
    - Память (стек вызовов): O(d), где d — глубина каталога
    """
    global max_recursion_depth
    max_recursion_depth = max(max_recursion_depth,
                              current_depth)  # обновляем макс глубину

    ignore_dirs = {'.git', '__pycache__', '.mypy_cache', '.idea',
                   '.vscode', 'venv', 'env'}  # папки, которые игнорируем

    # если достигли максимальной глубины, выходим
    if max_depth is not None and current_depth > max_depth:
        return

    try:
        # перебираем все элементы в текущей директории
        for item in os.listdir(path):
            full_path = os.path.join(path, item)  # полный путь к файлу/папке
            if item in ignore_dirs:
                continue  # пропускаем игнорируемые директории

            print(" " * indent + "|-- " + item)  # выводим элемент с отступом

            # если это папка — рекурсивно вызываем функцию
            if os.path.isdir(full_path):
                print_dir_tree(full_path, indent + 4, max_depth,
                               current_depth + 1)
    except PermissionError:
        print(" " * indent +
              "|-- [Доступ запрещен]")  # если нет прав на чтение


# -----------------------------
# Функция 3: измерение максимальной глубины рекурсии
# -----------------------------
def measure_dir_recursion_depth(path="."):
    """
    Измеряет максимальную глубину рекурсии при обходе каталога.

    Сложность:
    - Время: O(N)
    - Глубина рекурсии: ≤ max_depth
    - Память (стек вызовов): O(d)
    """
    global max_recursion_depth
    max_recursion_depth = 0  # сброс максимальной глубины
    print_dir_tree(path)  # обходим дерево каталогов
    print(f"\nМаксимальная глубина рекурсии: {max_recursion_depth}")


# -----------------------------
# Функция 4: Ханойские башни
# -----------------------------
def hanoi_tower(n, source, target, auxiliary):
    """
    Рекурсивное решение задачи Ханойских башен.

    Сложность:
    - Время: O(2^n) — экспоненциальная,
    - т.к. каждый диск вызывает два рекурсивных шага
    - Глубина рекурсии: n
    - Память (стек вызовов): O(n)
    """
    if n == 1:
        print(f"Переместить диск 1 с {source} → {target}")  # базовый случай
        return
    # рекурсивно переносим n-1 диск на вспомогательную башню
    hanoi_tower(n - 1, source, auxiliary, target)
    print(f"Переместить диск {n} с {source} → {target}")
    # рекурсивно переносим n-1 диск на целевую башню
    hanoi_tower(n - 1, auxiliary, target, source)


# -----------------------------
# Главная программа
# -----------------------------
if __name__ == "__main__":
    # --- Бинарный поиск ---
    arr = [1, 3, 5, 7, 9, 11]
    print("Бинарный поиск:")
    print("Элемент 7 имеет индекс:", binary_search_recursive(arr, 7))

    # --- Ханойские башни ---
    print("\nХанойские башни (3 диска):")
    hanoi_tower(3, "A", "C", "B")

    # --- Обход файловой системы ---
    print("\nОбход файловой системы (только до 2 уровней):")
    print_dir_tree(".", max_depth=2)

    # --- Измерение максимальной глубины ---
    print("\nИзмеряем максимальную глубину рекурсии для текущей структуры:")
    measure_dir_recursion_depth(".")
