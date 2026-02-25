"""
Задание 1. Загрузка данных
Изучить представленный набор данных на основе описания его столбцов в файле “horse_data.names” , загрузить его и оставить 8 столбцов для дальнейшего изучения: surgery?, Age, rectal temperature, pulse, respiratory rate, temperature of extremities, pain, outcome.

Задание 2. Первичное изучение данных
Проанализировать значения по столбцам, рассчитать базовые статистики, найти выбросы.

Задание 3. Работа с пропусками
Рассчитать количество пропусков для всех выбранных столбцов. Принять и обосновать решение о методе заполнения пропусков по каждому столбцу на основе рассчитанных статистик и возможной взаимосвязи значений в них. Сформировать датафрейм, в котором пропуски будут отсутствовать.

"""
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Задание 1
df_raw = pd.read_csv('horse_data.csv', header=None)

selected_columns = [0, 1, 3, 4, 5, 6, 10, 22]
column_names = ['surgery', 'age', 'rectal_temperature', 'pulse',
                'respiratory_rate', 'extremities_temp', 'pain', 'outcome']

df = df_raw[selected_columns].copy()
df.columns = column_names
df = df.replace('?', np.nan)

numeric_cols = ['rectal_temperature', 'pulse', 'respiratory_rate']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

categorical_cols = ['surgery', 'age', 'extremities_temp', 'pain', 'outcome']
for col in categorical_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
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
df_filled = df.copy()
filling_strategy = {}

col = 'surgery'
mode_val = int(df[col].mode()[0])
df_filled[col] = df_filled[col].fillna(mode_val)
filling_strategy[col] = {'method': 'mode', 'value': mode_val}

col = 'age'
mode_val = int(df[col].mode()[0])
df_filled[col] = df_filled[col].fillna(mode_val)
filling_strategy[col] = {'method': 'mode', 'value': mode_val}

col = 'rectal_temperature'
median_val = round(df[col].median(), 2)
df_filled[col] = df_filled[col].fillna(median_val)
filling_strategy[col] = {'method': 'median', 'value': median_val}

col = 'pulse'
median_val = round(df[col].median(), 2)
df_filled[col] = df_filled[col].fillna(median_val)
filling_strategy[col] = {'method': 'median', 'value': median_val}

col = 'respiratory_rate'
median_val = round(df[col].median(), 2)
df_filled[col] = df_filled[col].fillna(median_val)
filling_strategy[col] = {'method': 'median', 'value': median_val}

col = 'extremities_temp'
mode_val = int(df[col].mode()[0])
df_filled[col] = df_filled[col].fillna(mode_val)
filling_strategy[col] = {'method': 'mode', 'value': mode_val}

col = 'pain'
mode_val = int(df[col].mode()[0])
df_filled[col] = df_filled[col].fillna(mode_val)
filling_strategy[col] = {'method': 'mode', 'value': mode_val}

col = 'outcome'
mode_val = int(df[col].mode()[0])
df_filled[col] = df_filled[col].fillna(mode_val)
filling_strategy[col] = {'method': 'mode', 'value': mode_val}

remaining_missing = df_filled.isnull().sum()
# Обработанные данные
df_filled.to_csv('horse_data_final.csv', index=False, encoding='utf-8')

# Статистики
stats_df.to_csv('horse_data_statistics.csv', index=False, encoding='utf-8')

with open('horse_data_report.txt', 'w', encoding='utf-8') as f:
    f.write("ОТЧЁТ ПО АНАЛИЗУ ДАННЫХ HORSE COLIC\n\n")
    f.write(f"Записей: {df.shape[0]}, Столбцов: {df.shape[1]}\n\n")
    f.write("ПРОПУСКИ (до обработки):\n")
    for col, count, pct in zip(missing.index, missing.values, missing_pct.values):
        f.write(f"  {col}: {count} ({pct}%)\n")
    f.write(f"Всего пропущено: {missing.sum()}\n\n")
    f.write("БАЗОВЫЕ СТАТИСТИКИ:\n")
    f.write(stats_df.to_string(index=False))
    f.write("ВЫБРОСЫ (IQR):\n")
    for item in outliers_report:
        f.write(f"  {item['Столбец']}: {item['Выбросов']} выбросов\n")
    f.write("ЗАПОЛНЕНИЕ ПРОПУСКОВ:\n")
    for col, info in filling_strategy.items():
        f.write(f"  {col}: {info['method']} = {info['value']}\n")
    f.write(f"Пропусков после обработки: {remaining_missing.sum()}\n")

# Стратегия заполнения
import json
with open('filling_strategy.json', 'w', encoding='utf-8') as f:
    json.dump(filling_strategy, f, ensure_ascii=False, indent=2)

print(f"Записей: {df.shape[0]}, Столбцов: {df.shape[1]}")
print(f"Пропусков до: {missing.sum()}, после: {remaining_missing.sum()}")
print(f"Выбросов найдено: {sum(item['Выбросов'] for item in outliers_report)}")
print("Созданные файлы: horse_data_final.csv, horse_data_statistics.csv, horse_data_report.txt, filling_strategy.json")