"""
Задание 3
Специалист по кадрам, работающий в технологической компании, интересуется сверхурочным временем разных команд. Чтобы выяснить, есть ли разница между сверхурочной работой команды разработчиков программного обеспечения и группы тестирования, она случайным образом выбрала 17 сотрудников в каждой из двух команд и записала их среднее сверхурочное время за неделю в пересчете на час. Данные ниже.
В соответствии с этой информацией проведите проверку гипотезы, чтобы проверить, есть ли разница между переутомлением двух команд, используя уровень значимости 0,05. Прежде чем приступать к проверке гипотез, проверьте предположение нормальности.
"""
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

plt.switch_backend('Agg')
test_team = [6.2, 7.1, 1.5, 2.3, 2, 1.5, 6.1, 2.4, 2.3, 12.4, 1.8, 5.3, 3.1, 9.4, 2.3, 4.1, 3.5]
developer_team = [2.3, 2.1, 1.4, 2.0, 8.7, 2.2, 3.1, 4.2, 3.6, 2.5, 3.1, 6.2, 12.1, 3.9, 2.2, 1.2, 3.4]

alpha = 0.05
print("ПРОВЕРКА НОРМАЛЬНОСТИ РАСПРЕДЕЛЕНИЯ")
# Проверка нормальности с помощью теста Шапиро-Уилка
stat_test, p_test = stats.shapiro(test_team)
stat_dev, p_dev = stats.shapiro(developer_team)

print(f"\nКоманда тестирования (n={len(test_team)}):")
print(f"Статистика Шапиро-Уилка: {stat_test:.4f}")
print(f"P-value: {p_test:.4f}")
print(f"Вывод: {'Нормальное распределение' if p_test > alpha else 'Не нормальное распределение'}")

print(f"\nКоманда разработчиков (n={len(developer_team)}):")
print(f"Статистика Шапиро-Уилка: {stat_dev:.4f}")
print(f"P-value: {p_dev:.4f}")
print(f"Вывод: {'Нормальное распределение' if p_dev > alpha else 'Не нормальное распределение'}")

# Визуализация распределений с сохранением в файл
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

sns.histplot(test_team, kde=True, ax=axes[0], color='skyblue')
axes[0].set_title('Команда тестирования')
axes[0].set_xlabel('Сверхурочные часы')

sns.histplot(developer_team, kde=True, ax=axes[1], color='lightgreen')
axes[1].set_title('Команда разработчиков')
axes[1].set_xlabel('Сверхурочные часы')

plt.tight_layout()
plt.savefig('histograms.png', dpi=300, bbox_inches='tight')
plt.close()

# Q-Q plots для визуальной проверки нормальности
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

stats.probplot(test_team, dist="norm", plot=axes[0])
axes[0].set_title('Q-Q plot: Команда тестирования')

stats.probplot(developer_team, dist="norm", plot=axes[1])
axes[1].set_title('Q-Q plot: Команда разработчиков')

plt.tight_layout()
plt.savefig('qq_plots.png', dpi=300, bbox_inches='tight')
plt.close()

print("ПРОВЕРКА РАВЕНСТВА ДИСПЕРСИЙ (Тест Левена)")
# Проверка равенства дисперсий
levene_stat, levene_p = stats.levene(test_team, developer_team)
print(f"Статистика Левена: {levene_stat:.4f}")
print(f"P-value: {levene_p:.4f}")

equal_var = levene_p > alpha
print(f"Вывод: Дисперсии {'равны' if equal_var else 'не равны'} (используем equal_var={equal_var})")

print("T-ТЕСТ СТЬЮДЕНТА ДЛЯ ДВУХ НЕЗАВИСИМЫХ ВЫБОРОК")
print("\nГипотезы:")
print("Среднее сверхурочное время в командах одинаково (μ₁ = μ₂)")
print("Среднее сверхурочное время в командах различается (μ₁ ≠ μ₂)")

# Проведение t-теста
t_stat, p_value = stats.ttest_ind(test_team, developer_team, equal_var=equal_var)

print(f"\nРезультаты теста:")
print(f"Среднее тест-команды:{np.mean(test_team):.2f} часов")
print(f"Среднее команды разработки: {np.mean(developer_team):.2f} часов")
print(f"Разница средних:{np.mean(test_team) - np.mean(developer_team):.2f} часов")
print(f"t-статистика:{t_stat:.4f}")
print(f"P-value:{p_value:.4f}")
print(f"Уровень значимости α:{alpha}")

# Принятие решения
if p_value < alpha:
    print("РЕШЕНИЕ: Отклоняем нулевую гипотезу")
    print("ВЫВОД: Существует статистически значимая разница в сверхурочном времени между командами")
else:
    print("РЕШЕНИЕ: Не отклоняем нулевую гипотезу")
    print("ВЫВОД: Разница в сверхурочном времени между командами статистически незначима")



print("ДОПОЛНИТЕЛЬНО: РАЗМЕР ЭФФЕКТА (Cohen's d)")

def cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    return (np.mean(group1) - np.mean(group2)) / pooled_std

d = cohens_d(test_team, developer_team)
print(f"Cohen's d: {d:.4f}")
print("Интерпретация:")
print("|d| < 0.2  - очень малый эффект")
print("0.2 <= |d| < 0.5 - малый эффект")
print("0.5 <= |d| < 0.8 - средний эффект")
print("|d| >= 0.8  - большой эффект")

plt.figure(figsize=(8, 5))
plt.boxplot([test_team, developer_team], tick_labels=['Тест-команда', 'Разработчики'], patch_artist=True)
plt.ylabel('Сверхурочные часы')
plt.title('Сравнение сверхурочного времени между командами')
plt.grid(axis='y', alpha=0.3)
plt.savefig('boxplot.png', dpi=300, bbox_inches='tight')
plt.close()
