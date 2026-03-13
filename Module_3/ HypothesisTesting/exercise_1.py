"""
Задание 1
Разработайте функцию для проверки нормальности распределения выборки данных,
используя шаблон в материалах к домашнему заданию. Вы можете использовать один из известных Вам статистических тестов.
"""
from scipy import stats
import numpy as np


def check_normality(data, alpha=0.05):
    """
    Функция для проверки нормальности распределения выборки данных.
    Использует тест Шапиро-Уилка.
    """

    stat, p_value = stats.shapiro(data)
    if p_value < alpha:
        print("Отклоняем нулевую гипотезу >> Данные распределены не нормально")
    else:
        print("Не отклоняем нулевую гипотезу >> Данные распределены нормально")

    # Дополнительная информация (опционально)
    print(f"Статистика теста: {stat:.4f}")
    print(f"P-value: {p_value:.4f}")
    print(f"Уровень значимости (alpha): {alpha}")

    return p_value
# Пример 1: Нормально распределённые данные
np.random.seed(42)
normal_data = np.random.normal(loc=0, scale=1, size=100)
print("=== Проверка нормальных данных ===")
check_normality(normal_data)

print("\n")
# Пример 2: Данные с экспоненциальным распределением (не нормальные)
exponential_data = np.random.exponential(scale=1, size=100)
print("Проверка экспоненциальных данных ===")
check_normality(exponential_data)