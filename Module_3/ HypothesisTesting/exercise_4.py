"""
Задание 4
Педиатр хочет увидеть влияние потребления смеси на среднемесячную прибавку в весе у новорожденных. По этой причине она собрала данные из трех разных групп. Первая группа – дети исключительно грудного вскармливания, вторая группа – дети, которых кормят только смесью, и последняя группа – это дети, находящиеся на искусственном вскармливании и на грудном вскармливании. Эти данные приведены ниже.
В соответствии с этой информацией проведите проверку гипотезы, чтобы проверить, есть ли разница между среднемесячным приростом этих трех групп, используя уровень значимости 0,05. Если есть значительная разница, выполните дальнейший анализ, чтобы найти причину разницы.
"""
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.multicomp import pairwise_tukeyhsd

only_breast = [794.1, 716.9, 993.0, 724.7, 760.9, 908.2, 659.3, 690.8, 768.7, 717.3, 630.7, 729.5, 714.1, 810.3, 583.5,
               679.9, 865.1]
only_formula = [898.8, 881.2, 940.2, 966.2, 957.5, 1061.7, 1046.2, 980.4, 895.6, 919.7, 1074.1, 952.5, 796.3, 859.6,
                871.1, 1047.5, 919.1, 1160.5, 996.9]
both = [976.4, 656.4, 861.2, 706.8, 718.5, 717.1, 759.8, 894.6, 867.6, 805.6, 765.4, 800.3, 789.9, 875.3, 740.0, 799.4,
        790.3, 795.2, 823.6, 818.7, 926.8, 791.7, 948.3]

alpha = 0.05

groups = [only_breast, only_formula, both]
group_names = ['Только грудное', 'Только смесь', 'Смешанное']

print("ОПИСАТЕЛЬНАЯ СТАТИСТИКА")
for name, data in zip(group_names, groups):
    print(f"\n{name} (n={len(data)}):")
    print(f"Среднее: {np.mean(data):.2f} г")
    print(f"Стандартное отклонение: {np.std(data, ddof=1):.2f} г")
    print(f"Минимум: {np.min(data):.2f} г")
    print(f"Максимум: {np.max(data):.2f} г")

# Визуализация распределений
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Boxplot
axes[0].boxplot(groups, tick_labels=group_names, patch_artist=True,
                boxprops=dict(facecolor='lightblue'), medianprops=dict(color='red'))
axes[0].set_ylabel('Прибавка в весе (г)')
axes[0].set_title('Сравнение распределений (Box Plot)')
axes[0].grid(axis='y', alpha=0.3)

# Гистограммы с KDE
for name, data, color in zip(group_names, groups, ['skyblue', 'lightgreen', 'plum']):
    sns.kdeplot(data, ax=axes[1], label=name, fill=True, alpha=0.4, color=color)
axes[1].set_xlabel('Прибавка в весе (г)')
axes[1].set_ylabel('Плотность')
axes[1].set_title('Плотность распределения по группам')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('anova_distributions.png', dpi=300, bbox_inches='tight')
plt.close()

print("ПРОВЕРКА ПРЕДПОЛОЖЕНИЙ")
# Проверка нормальности (тест Шапиро-Уилка)
print("\nПроверка нормальности распределения (Шапиро-Уилк):")
normality_results = []
for name, data in zip(group_names, groups):
    stat, p_val = stats.shapiro(data)
    is_normal = p_val > alpha
    normality_results.append(is_normal)
    print(f"  {name}: W={stat:.4f}, p={p_val:.4f} → {'Нормальное' if is_normal else 'Не нормальное'}")

# Проверка гомогенности дисперсий (тест Левена)
print("\nПроверка равенства дисперсий (тест Левена):")
levene_stat, levene_p = stats.levene(*groups)
equal_var = levene_p > alpha
print(f"Статистика Левена: {levene_stat:.4f}")
print(f"P-value: {levene_p:.4f}")
print(f"Вывод: Дисперсии {'равны' if equal_var else 'не равны'}")

print("ОДНОФАКТОРНЫЙ ДИСПЕРСИОННЫЙ АНАЛИЗ (ANOVA)")
# Формулировка гипотез
print("\nГипотезы:")
print("  H₀: μ₁ = μ₂ = μ₃ (средние прибавки во всех группах равны)")
print("  H₁: Хотя бы одно среднее отличается от остальных")

# Проведение ANOVA
f_stat, p_value = stats.f_oneway(*groups)

print(f"\nРезультаты ANOVA:")
print(f"F-статистика: {f_stat:.4f}")
print(f"P-value: {p_value:.4f}")
print(f"Уровень значимости α: {alpha}")

if p_value < alpha:
    print("РЕШЕНИЕ: Отклоняем нулевую гипотезу")
    print("ВЫВОД: Существует статистически значимая разница в прибавке веса между группами")
    anova_significant = True
else:
    print("РЕШЕНИЕ: Не отклоняем нулевую гипотезу")
    print("ВЫВОД: Разница в прибавке веса между группами статистически незначима")
    anova_significant = False

# Пост-хок анализ (если ANOVA значим)
if anova_significant:
    print("ШАГ 4: ПОСТ-ХОК АНАЛИЗ (Тест Тьюки)")


    # Подготовка данных для Tukey HSD
    all_data = np.concatenate(groups)
    group_labels = np.repeat(group_names, [len(g) for g in groups])

    # Проведение теста Тьюки
    tukey = pairwise_tukeyhsd(all_data, group_labels, alpha=alpha)

    print("\nПолные результаты Tukey HSD:")
    print(tukey.summary())

    fig, ax = plt.subplots(figsize=(8, 6))
    tukey.plot_simultaneous(ax=ax)
    ax.set_title('Попарные сравнения (95% доверительные интервалы)')
    plt.tight_layout()
    plt.savefig('tukey_results.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Простая интерпретация через атрибуты
    print("\nКраткая интерпретация:")


    # Используем только публичные атрибуты
    print(f"Уникальные группы: {tukey.groupsunique}")
    print(f"Количество сравнений: {len(tukey.pvalues)}")
    print(f"P-values: {tukey.pvalues}")
    print(f"Отклонение H₀: {tukey.reject}")
    print(f"Разницы средних: {tukey.meandiffs}")

    # Вывод в читаемом формате
    print("\nПопарные сравнения:")
    comparison_idx = 0
    for i in range(len(tukey.groupsunique)):
        for j in range(i + 1, len(tukey.groupsunique)):
            if comparison_idx < len(tukey.pvalues):
                g1 = tukey.groupsunique[i]
                g2 = tukey.groupsunique[j]
                diff = tukey.meandiffs[comparison_idx]
                pval = tukey.pvalues[comparison_idx]
                rej = tukey.reject[comparison_idx]

                sig = "★ ЗНАЧИМО" if rej else "не значимо"
                print(f"{g1} vs {g2}: разница={diff:.2f}г, p={pval:.4f} → {sig}")
                comparison_idx += 1


# Дополнительные метрики: размер эффекта (eta-squared)
print("ДОПОЛНИТЕЛЬНО: РАЗМЕР ЭФФЕКТА (Eta-squared)")
def eta_squared(f_stat, df_between, df_within):
    """Расчёт размера эффекта η² для ANOVA"""
    return (f_stat * df_between) / (f_stat * df_between + df_within)


# Степени свободы
n_total = sum(len(g) for g in groups)
k = len(groups)
df_between = k - 1
df_within = n_total - k

eta_sq = eta_squared(f_stat, df_between, df_within)
print(f"\nEta-squared (η²): {eta_sq:.4f}")
print("Интерпретация η²:")
print("0.01 - малый эффект")
print("0.06 - средний эффект")
print("0.14 - большой эффект")

if eta_sq < 0.01:
    effect_size = "очень малый"
elif eta_sq < 0.06:
    effect_size = "малый"
elif eta_sq < 0.14:
    effect_size = "средний"
else:
    effect_size = "большой"
print(f"\nВывод: Размер эффекта — {effect_size}")

# Итоговый вывод
print("\n" + "=" * 70)
print("ИТОГОВЫЙ ВЫВОД")
print("=" * 70)
print(f"""
1. Статистический результат:
   - Прибавка в весе достоверно различается между группами (p = {p_value:.4f})

2. Практическая интерпретация:
   - Группа 'Только смесь' показывает наибольшую среднюю прибавку ({np.mean(only_formula):.0f} г)
   - Группа 'Только грудное' — наименьшую ({np.mean(only_breast):.0f} г)
   - Группа 'Смешанное' занимает промежуточное положение ({np.mean(both):.0f} г)

3. Размер эффекта:
   - η² = {eta_sq:.3f} ({effect_size} эффект)

4. Рекомендации:
   - При принятии решений учитывать не только статистическую значимость,
     но и клиническую/практическую важность различий
   - Для подтверждения причинно-следственных связей необходимы
     контролируемые исследования с учётом дополнительных факторов
""")