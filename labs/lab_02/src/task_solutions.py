# === task_solutions.py ===
"""
Решения практических задач:
1) Проверка сбалансированности скобок (используется list как стек)
2) Симуляция очереди печати (collections.deque)
3) Проверка палиндрома (collections.deque)
"""

from __future__ import annotations
from collections import deque
from typing import Iterable


def is_balanced_brackets(s: str) -> bool:
    """Проверка сбалансированности скобок. Временная сложность: O(n)."""
    pairs = {'(': ')', '[': ']', '{': '}'}
    stack = []  # используем list как стек: push=append, pop=pop()
    for ch in s:
        if ch in pairs:
            stack.append(ch)
        elif ch in pairs.values():
            if not stack:
                return False
            opening = stack.pop()
            if pairs[opening] != ch:
                return False
    return not stack


def simulate_print_queue(jobs: Iterable[str]) -> None:
    """Простая симуляция очереди печати. Каждый job — строка с именем задания.

    Для демонстрации используем deque, /
    т.к. он эффективен для операций слева (popleft())
    """
    q = deque(jobs)
    while q:
        job = q.popleft()
        print(f'Printing job: {job}')


def is_palindrome(seq: Iterable) -> bool:
    """Проверка палиндрома с использованием deque. Временная сложность: O(n)"""
    d = deque(seq)
    while len(d) > 1:
        if d.popleft() != d.pop():
            return False
    return True


if __name__ == '__main__':
    # Простые тесты
    tests = ['{[()]}', '{[(])}', '((()))', '([)]']
    for t in tests:
        print(t, '->', is_balanced_brackets(t))

    print('\nSimulate print queue:')
    simulate_print_queue(['doc1.pdf', 'photo.png', 'report.docx'])

    print('\nPalindrome tests:')
    print('radar ->', is_palindrome('radar'))
    print('[1,2,3,2,1] ->', is_palindrome([1, 2, 3, 2, 1]))
    print('[1,2,3] ->', is_palindrome([1, 2, 3]))
