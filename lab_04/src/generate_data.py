import random
from typing import Dict, List


def generate_arrays(sizes: List[int]) -> Dict[int, Dict[str, List[int]]]:
    """
    Генерирует набор тестовых массивов для каждого указанного размера.
    Для каждого размера создает 4 типа массивов:
    - случайный порядок
    - отсортированный
    - обратный порядок
    - почти отсортированный (небольшое количество перестановок)

    :param sizes: Список размеров массивов для генерации.
    :return: Словарь, где:
             - ключ — размер массива (int),
             - значение — словарь с 4 типами массивов:
               * "random" — перемешанный массив
               * "sorted" — отсортированный по возрастанию
               * "reversed" — отсортированный по убыванию
               * "almost_sorted" — почти отсортированный
               (1 из 20 элементов переставлен)

    Пример:
        generate_arrays([3, 5]) -> {
            3: {
                "random": [2, 0, 1],
                "sorted": [0, 1, 2],
                "reversed": [2, 1, 0],
                "almost_sorted": [0, 2, 1]
            },
            ...
        }
    """
    data: Dict[int, Dict[str, List[int]]] = {}

    for size in sizes:
        # Базовый отсортированный массив [0, 1, 2, ..., size-1]
        base = list(range(size))

        # Случайный порядок
        random_data = base.copy()
        random.shuffle(random_data)

        # Обратный порядок
        reversed_data = list(reversed(base))

        # Почти отсортированный: делаем несколько случайных перестановок
        almost_sorted = base.copy()
        swaps = max(1, size // 20)  # минимум 1 перестановка, максимум ~5%
        for _ in range(swaps):
            i = random.randrange(size)
            j = random.randrange(size)
            tmp = almost_sorted[i]
            almost_sorted[i] = almost_sorted[j]
            almost_sorted[j] = tmp

        # Сохраняем все типы массивов для данного размера
        data[size] = {
            "random": random_data,
            "sorted": base,
            "reversed": reversed_data,
            "almost_sorted": almost_sorted,
        }

    return data
