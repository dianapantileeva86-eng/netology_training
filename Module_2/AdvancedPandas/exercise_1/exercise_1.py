"""
Задание 1
Для датафрейма log из материалов занятия создайте столбец source_type по правилам:

если источник traffic_source равен Yandex или Google, то в source_type ставится organic;
для источников paid и email из России ставим ad;
для источников paid и email не из России ставим other;
все остальные варианты берём из traffic_source без изменений.
"""

import pandas as pd
import numpy as np


log = pd.read_csv('visit_log.csv', sep=';')

# Приводим traffic_source к нижнему регистру для надёжного сравнения
log['traffic_source_lower'] = log['traffic_source'].str.lower().str.strip()

conditions = [

    log['traffic_source_lower'].isin(['yandex', 'google']),

    (log['traffic_source_lower'].isin(['paid', 'email'])) & (log['region'] == 'Russia'),

    (log['traffic_source_lower'].isin(['paid', 'email'])) & (log['region'] != 'Russia')
]

choices = ['organic', 'ad', 'other']

log['source_type'] = np.select(conditions, choices, default=log['traffic_source'])

log.drop('traffic_source_lower', axis=1, inplace=True)

log.to_csv('visit_log_updated.csv', sep=';', index=False, encoding='utf-8-sig')

print("Обработка завершена успешно!")
print(f"Обработано строк: {len(log)}")
print(f"Результат сохранён в файл: visit_log_updated.csv")
print("\nПример первых 10 строк с новым столбцом source_type:")
print(log[['traffic_source', 'region', 'source_type']].head(10))
print("\nРаспределение по source_type:")
print(log['source_type'].value_counts())