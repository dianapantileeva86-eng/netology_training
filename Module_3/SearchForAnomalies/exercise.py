"""
Задание 1. Загрузка данных
Изучить представленный набор данных на основе описания его столбцов в файле “horse_data.names” , загрузить его и оставить 8 столбцов для дальнейшего изучения: surgery?, Age, rectal temperature, pulse, respiratory rate, temperature of extremities, pain, outcome.

Задание 2. Первичное изучение данных
Проанализировать значения по столбцам, рассчитать базовые статистики, найти выбросы.

Задание 3. Работа с пропусками
Рассчитать количество пропусков для всех выбранных столбцов. Принять и обосновать решение о методе заполнения пропусков по каждому столбцу на основе рассчитанных статистик и возможной взаимосвязи значений в них. Сформировать датафрейм, в котором пропуски будут отсутствовать.

"""
import logging

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Задание 1
selected_columns = [0, 1, 3, 4, 5, 6, 10, 22]
column_names = ['surgery', 'age', 'rectal_temperature', 'pulse',
                'respiratory_rate', 'extremities_temp', 'pain', 'outcome']

df = pd.read_csv('horse_data.csv', header=None, usecols=selected_columns,
                 names=column_names, na_values='?')

# Преобразование типов
numeric_cols = ['rectal_temperature', 'pulse', 'respiratory_rate']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

categorical_cols = ['surgery', 'age', 'extremities_temp', 'pain', 'outcome']
for col in categorical_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
df['age'] = df['age'].replace(9, 2)

# Задание 2
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)

# Статистики (числовые)
stats_list = []
for col in numeric_cols:
    col_data = df[col].dropna()
    if len(col_data) > 0:
        q1 = col_data.quantile(0.25)
        q3 = col_data.quantile(0.75)
        stats_list.append({
            'Столбец': col,
            'Count': len(col_data),
            'Mean': round(col_data.mean(), 2),
            'Median': round(col_data.median(), 2),
            'Std': round(col_data.std(), 2),
            'Min': round(col_data.min(), 2),
            'Q1': round(q1, 2),
            'Q3': round(q3, 2),
            'Max': round(col_data.max(), 2),
            'IQR': round(q3 - q1, 2)
        })
stats_df = pd.DataFrame(stats_list)

# Выбросы (IQR)
outliers_report = []
for col in numeric_cols:
    col_data = df[col].dropna()
    if len(col_data) > 0:
        q1 = col_data.quantile(0.25)
        q3 = col_data.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outliers = df[(df[col] < lower) | (df[col] > upper)][col].dropna()
        outliers_report.append({
            'Столбец': col,
            'Нижняя граница': round(lower, 2),
            'Верхняя граница': round(upper, 2),
            'Выбросов': len(outliers),
            'Значения': list(outliers.values)
        })

# Задание 3
df_simple = df.copy()
for col in numeric_cols:
    df_simple[col] = df_simple[col].fillna(df_simple[col].median())
for col in categorical_cols:
    df_simple[col] = df_simple[col].fillna(df_simple[col].mode()[0])

df_grouped = df.copy()
for col in numeric_cols:
    df_grouped[col] = df_grouped[col].fillna(
        df_grouped.groupby(['surgery', 'age'])[col].transform('median')
    )
    df_grouped[col] = df_grouped[col].fillna(df_grouped[col].median())

for col in categorical_cols:
    df_grouped[col] = df_grouped[col].fillna(
        df_grouped.groupby(['surgery', 'age'])[col].transform(lambda x: x.mode()[0] if not x.mode().empty else None)
    )
    df_grouped[col] = df_grouped[col].fillna(df_grouped[col].mode()[0])

# Сравнение статистик до и после
comparison_stats = []
for col in numeric_cols:
    comparison_stats.append({
        'Столбец': col,
        'Медиана (до)': round(df[col].median(), 2),
        'Медиана (простое)': round(df_simple[col].median(), 2),
        'Медиана (группы)': round(df_grouped[col].median(), 2),
        'Пропусков': int(missing[col])
    })
comparison_df = pd.DataFrame(comparison_stats)

cat_analysis = {}
for col in categorical_cols:
    cat_analysis[col] = {
        'unique': df[col].unique().tolist(),
        'mode': int(df[col].mode()[0]) if not df[col].mode().empty else None,
        'distribution': df[col].value_counts().sort_index().to_dict()
    }

df_grouped.to_csv('horse_data_final.csv', index=False, encoding='utf-8')
stats_df.to_csv('horse_data_statistics.csv', index=False, encoding='utf-8')
comparison_df.to_csv('horse_data_comparison.csv', index=False, encoding='utf-8')

with open('horse_data_report.txt', 'w', encoding='utf-8') as f:
    f.write("ОТЧЁТ ПО АНАЛИЗУ ДАННЫХ HORSE COLIC\n\n")
    f.write(f"Записей: {df.shape[0]}, Столбцов: {df.shape[1]}\n\n")
    f.write("ВЫВОДЫ ПО КАТЕГОРИАЛЬНЫМ ПЕРЕМЕННЫМ\n")
    for col, info in cat_analysis.items():
        f.write(f"Уникальные значения: {info['unique']}\n")
        f.write(f"Мода: {info['mode']}\n")
        f.write(f"Распределение: {info['distribution']}\n")

    f.write("ПРОПУСКИ (до обработки)\n")
    for col, count, pct in zip(missing.index, missing.values, missing_pct.values):
        f.write(f"  {col}: {count} ({pct}%)\n")
    f.write(f"Всего пропущено: {missing.sum()}\n")

    f.write("БАЗОВЫЕ СТАТИСТИКИ\n")
    f.write(stats_df.to_string(index=False))

    f.write("\nВЫБРОСЫ (IQR)\n")
    for item in outliers_report:
        f.write(f"\n{item['Столбец']}:\n")
        f.write(f"Границы: [{item['Нижняя граница']}, {item['Верхняя граница']}]\n")
        f.write(f"Выбросов: {item['Выбросов']}\n")
        f.write(f"Значения: {item['Значения']}\n")

    f.write("ВЫВОДЫ\n")
    f.write("pulse (164, 150, 146...): Может быть реальным - при боли пульс значительно повышается.\n")
    f.write("rectal_temperature (35.4, 40.8): 40.8 - возможна лихорадка, 35.4 - гипотермия при шоке.\n")
    f.write("respiratory_rate (96, 90): При респираторном дистрессе частота дыхания растёт.\n")
    f.write("Вывод: Большинство выбросов - естественные значения при тяжёлых состояниях, не ошибки.\n")

    f.write("СРАВНЕНИЕ МЕТОДОВ ЗАПОЛНЕНИЯ\n")
    f.write(comparison_df.to_string(index=False))

    f.write("\nВЫВОДЫ ПО ЗАПОЛНЕНИЮ\n")
    f.write("Групповое заполнение учитывает взаимосвязи (например, температура может отличаться у лошадей с операцией и без)\n")
    f.write("Разница между методами небольшая, т.к. пропусков 30% и группы неоднородны.\n")

    f.write(f"Пропусков после обработки: {df_grouped.isnull().sum().sum()}\n")

print("Обработка завершена")
print(f"Записей: {df.shape[0]}, Столбцов: {df.shape[1]}")
print(f"Пропусков до: {missing.sum()}, после: {df_grouped.isnull().sum().sum()}")
print(f"Выбросов найдено: {sum(item['Выбросов'] for item in outliers_report)}")
print("Файлы: horse_data_final.csv, horse_data_statistics.csv, horse_data_comparison.csv, horse_data_report.txt")