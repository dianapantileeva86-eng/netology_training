"""
Задание 2
Даны две выборки роста мужчин и женщин.

Докажите, используя t-Тест Стьдента, что различие между выборками незначительно, если уровень значимости равен α= 0.001.
Покажите различия визуально
Является ли результат полезным с практической точки зрения? Почему да или нет?
"""
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Фиксация случайности и создание выборок
np.random.seed(42)

mens = stats.norm.rvs(loc=171, scale=10, size=150000)
womens = stats.norm.rvs(loc=170, scale=10, size=150000)

alpha = 0.001

t_statistic, p_value = stats.ttest_ind(mens, womens)

print("РЕЗУЛЬТАТЫ T-ТЕСТА СТЬЮДЕНТА")
print(f"Средний рост мужчин:  {mens.mean():.2f} см")
print(f"Средний рост женщин:  {womens.mean():.2f} см")
print(f"Разница средних:      {mens.mean() - womens.mean():.2f} см")
print(f"t-статистика:         {t_statistic:.4f}")
print(f"p-value:              {p_value:.6f}")
print(f"Уровень значимости α: {alpha}")

if p_value < alpha:
    print("Результат: Отклоняем нулевую гипотезу")
    print("Вывод: Различие между выборками статистически значимо")
else:
    print("Результат: Не отклоняем нулевую гипотезу")
    print("Вывод: Различие между выборками незначимо")


# Визуализация различий

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Гистограммы распределения
axes[0, 0].hist(mens, bins=50, alpha=0.6, label='Мужчины', color='blue', density=True)
axes[0, 0].hist(womens, bins=50, alpha=0.6, label='Женщины', color='red', density=True)
axes[0, 0].axvline(mens.mean(), color='blue', linestyle='--', linewidth=2, label=f'Среднее мужчин: {mens.mean():.1f}')
axes[0, 0].axvline(womens.mean(), color='red', linestyle='--', linewidth=2, label=f'Среднее женщин: {womens.mean():.1f}')
axes[0, 0].set_xlabel('Рост (см)')
axes[0, 0].set_ylabel('Плотность')
axes[0, 0].set_title('Распределение роста мужчин и женщин')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Box plot
axes[0, 1].boxplot([mens, womens], tick_labels=['Мужчины', 'Женщины'], patch_artist=True,
                   boxprops=dict(facecolor='lightblue'), medianprops=dict(color='red'))
axes[0, 1].set_ylabel('Рост (см)')
axes[0, 1].set_title('Сравнение распределений (Box Plot)')
axes[0, 1].grid(True, alpha=0.3, axis='y')

# KDE plot
sns.kdeplot(mens, ax=axes[1, 0], label='Мужчины', color='blue', linewidth=2)
sns.kdeplot(womens, ax=axes[1, 0], label='Женщины', color='red', linewidth=2)
axes[1, 0].axvline(mens.mean(), color='blue', linestyle='--', linewidth=1.5)
axes[1, 0].axvline(womens.mean(), color='red', linestyle='--', linewidth=1.5)
axes[1, 0].set_xlabel('Рост (см)')
axes[1, 0].set_ylabel('Плотность вероятности')
axes[1, 0].set_title('Плотность распределения (KDE)')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# Разница в распределениях
axes[1, 1].hist(mens - womens, bins=50, alpha=0.7, color='green', density=True)
axes[1, 1].axvline(np.mean(mens - womens), color='red', linestyle='--', linewidth=2,
                   label=f'Средняя разница: {np.mean(mens - womens):.2f} см')
axes[1, 1].set_xlabel('Разница в росте (см)')
axes[1, 1].set_ylabel('Плотность')
axes[1, 1].set_title('Распределение разницы между ростом мужчин и женщин')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

def cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    d = (np.mean(group1) - np.mean(group2)) / pooled_std
    return d

cohen_d = cohens_d(mens, womens)

print("\nАНАЛИЗ ПРАКТИЧЕСКОЙ ЗНАЧИМОСТИ")
print(f"Размер эффекта (Cohen's d): {cohen_d:.4f}")
print("Интерпретация Cohen's d:")
print("|d| < 0.2  - очень малый эффект")
print("0.2 <= |d| < 0.5 - малый эффект")
print("0.5 <= |d| < 0.8 - средний эффект")
print("|d| >= 0.8  - большой эффект")

plt.savefig('height_comparison.png', dpi=300, bbox_inches='tight')

print("\nВЫВОД О ПРАКТИЧЕСКОЙ ПОЛЬЗЕ РЕЗУЛЬТАТА")
print("""
Результат не является полезным с практической точки зрения по следующим причинам:

1. Статистическая значимость не равна практической значимости:
   - При очень больших выборках (n=150000 в каждой группе) 
     даже минимальные различия становятся статистически значимыми
   - Разница в 1 см статистически значима, но практически несущественна

2. Размер эффекта:
   - Cohen's d показывает очень малый эффект (d ≈ 0.1)
   - Это означает, что различие между группами пренебрежимо мало

3. Перекрытие распределений:
   - Распределения роста мужчин и женщин сильно перекрываются
   - Стандартное отклонение (10 см) в 10 раз больше разницы средних (1 см)
   - Невозможно надежно предсказать пол человека по росту

4. Практическое применение:
   - Разница в 1 см не имеет значения для:
     * Проектирования одежды
     * Эргономики рабочих мест
     * Медицинских рекомендаций
   - Такие малые различия находятся в пределах погрешности измерений

вывод: Статистическая значимость не равна практической значимости.
""")