"""
Задание 5 (опционально)
Аналитик финансовой инвестиционной компании интересуется взаимосвязью между полом и склонностью к риску. Из базы данных была взята случайная выборка из 660 клиентов. Клиенты в выборке были классифицированы в соответствии с их полом и склонностью к риску. Результат приведен в следующей таблице.
Проверьте гипотезу о том, что склонность к риску клиентов этой компании не зависит от их пола. Используйте α = 0.01.
"""
# %matplotlib
# inline

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

contingency_table = pd.DataFrame(
    [
        [53, 23, 30, 36, 88],  # Женщины
        [71, 48, 51, 57, 203]  # Мужчины
    ],
    index=['Ж', 'М'],
    columns=[0, 1, 2, 3, 4]  # Уровни риска
)

print("Таблица сопряженности: Пол × Уровень риска")
print(contingency_table)
print(f"\nОбщий размер выборки: {contingency_table.values.sum()} клиентов")

print("ОПИСАТЕЛЬНАЯ СТАТИСТИКА")

# Маргинальные суммы
row_totals = contingency_table.sum(axis=1)
col_totals = contingency_table.sum(axis=0)
total = contingency_table.values.sum()

print("\nРаспределение по полу:")
for gender, count in row_totals.items():
    print(f"  {gender}: {count} ({count / total * 100:.1f}%)")

print("\nРаспределение по уровню риска:")
for risk, count in col_totals.items():
    print(f"  Уровень {risk}: {count} ({count / total * 100:.1f}%)")

# Тепловая карта и столбчатая диаграмма
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Тепловая карта наблюдаемых частот
sns.heatmap(contingency_table, annot=True, fmt='d', cmap='YlOrRd',
            ax=axes[0], cbar_kws={'label': 'Количество клиентов'})
axes[0].set_title('Наблюдаемые частоты')
axes[0].set_xlabel('Уровень риска')
axes[0].set_ylabel('Пол')

# Столбчатая диаграмма с группировкой
contingency_table.T.plot(kind='bar', ax=axes[1], color=['skyblue', 'lightcoral'])
axes[1].set_xlabel('Уровень риска')
axes[1].set_ylabel('Количество клиентов')
axes[1].set_title('Распределение по полу и уровню риска')
axes[1].legend(title='Пол')
axes[1].tick_params(axis='x', rotation=0)
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()

print("ПРОВЕРКА ПРЕДПОЛОЖЕНИЙ")
# Расчёт ожидаемых частот
expected = np.outer(row_totals, col_totals) / total
expected_df = pd.DataFrame(expected, index=contingency_table.index,
                           columns=contingency_table.columns)

print("\nОжидаемые частоты (при условии независимости):")
print(expected_df.round(2))

# Проверка: все ожидаемые частоты >= 5?
min_expected = expected.min()
print(f"\nМинимальная ожидаемая частота: {min_expected:.2f}")
if min_expected >= 5:
    print("Предположение выполнено: все ожидаемые частоты >= 5")
else:
    print("Внимание: некоторые ожидаемые частоты < 5")
    print("Необходимо рассмотреть объединение категорий или использование точного теста Фишера")

print("ХИ-КВАДРАТ ТЕСТ НЕЗАВИСИМОСТИ")

print("\nГипотезы:")
print("  H₀: Склонность к риску НЕ ЗАВИСИТ от пола (переменные независимы)")
print("  H₁: Склонность к риску ЗАВИСИТ от пола (переменные связаны)")

# Проведение теста
chi2_stat, p_value, dof, expected_freq = stats.chi2_contingency(contingency_table)

alpha = 0.01

print(f"\nРезультаты теста:")
print(f"Хи-квадрат статистика: {chi2_stat:.4f}")
print(f"Степени свободы: {dof}")
print(f"P-value: {p_value:.6f}")
print(f"Уровень значимости α: {alpha}")

# Критическое значение
critical_value = stats.chi2.ppf(1 - alpha, dof)
print(f"  Критическое значение χ²({dof}, α={alpha}): {critical_value:.4f}")

if p_value < alpha:
    print("РЕШЕНИЕ: Отклоняем нулевую гипотезу")
    print("ВЫВОД: Существует статистически значимая связь между полом и склонностью к риску")
else:
    print("РЕШЕНИЕ: Не отклоняем нулевую гипотезу")
    print("ВЫВОД: Склонность к риску не зависит от пола (на уровне значимости 0.01)")

print("РАЗМЕР ЭФФЕКТА (Коэффициент Крамера)")


def cramers_v(confusion_matrix):
    """Расчёт коэффициента Крамера для измерения силы связи"""
    chi2 = stats.chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.values.sum()
    r, k = confusion_matrix.shape
    return np.sqrt(chi2 / (n * min(r - 1, k - 1)))


cramers_v_value = cramers_v(contingency_table)

print(f"\nКоэффициент Крамера (V): {cramers_v_value:.4f}")
print("\nИнтерпретация (для таблиц 2×5):")
print("  V < 0.10  - очень слабая связь")
print("  0.10 ≤ V < 0.30 - слабая связь")
print("  0.30 ≤ V < 0.50 - умеренная связь")
print("  V ≥ 0.50  - сильная связь")

if cramers_v_value < 0.10:
    strength = "очень слабая"
elif cramers_v_value < 0.30:
    strength = "слабая"
elif cramers_v_value < 0.50:
    strength = "умеренная"
else:
    strength = "сильная"
print(f"\nВывод: {strength} связь между полом и склонностью к риску")

if p_value < alpha:
    print("АНАЛИЗ ВКЛАДА ОТДЕЛЬНЫХ КАТЕГОРИЙ")

    # Стандартизированные остатки
    standardized_residuals = (contingency_table.values - expected) / np.sqrt(expected)
    residuals_df = pd.DataFrame(standardized_residuals,
                                index=contingency_table.index,
                                columns=contingency_table.columns)

    print("\nСтандартизированные остатки (|z| > 2 указывает на значимый вклад):")
    print(residuals_df.round(3))

    print("\nИнтерпретация:")
    for gender in residuals_df.index:
        for risk in residuals_df.columns:
            resid = residuals_df.loc[gender, risk]
            if abs(resid) > 2:
                direction = "больше" if resid > 0 else "меньше"
                print(f"  • {gender}, уровень {risk}: наблюдаемое значение {direction} ожидаемого (z={resid:.2f})")

if p_value < alpha:
    plt.figure(figsize=(8, 4))
    sns.heatmap(residuals_df, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
                cbar_kws={'label': 'Стандартизированный остаток'})
    plt.title('Стандартизированные остатки')
    plt.xlabel('Уровень риска')
    plt.ylabel('Пол')
    plt.tight_layout()
    plt.show()

print("ИТОГОВЫЙ ВЫВОД")

print(f"""
1. Статистический результат:
   • χ²({dof}) = {chi2_stat:.2f}, p = {p_value:.6f}
   • При α = 0.01: {'отклоняем' if p_value < alpha else 'не отклоняем'} H₀

2. Практическая интерпретация:
   • Размер эффекта (Крамера V = {cramers_v_value:.3f}): {strength} связь
   • {'Пол влияет на склонность к риску' if p_value < alpha else 'Пол не является значимым фактором склонности к риску'}

3. Рекомендации:
   • При наличии связи: учитывать пол при сегментации клиентов по риску
   • При отсутствии связи: искать другие предикторы склонности к риску
   • Всегда дополнять статистический анализ предметной экспертизой
""")