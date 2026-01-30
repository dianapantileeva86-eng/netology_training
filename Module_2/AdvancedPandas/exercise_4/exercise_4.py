"""
Задание 4
Дана статистика услуг перевозок клиентов компании по типам (см. файл “Python_13_join.ipynb” в разделе «Материалы для лекции “Продвинутый pandas”» ---- Ноутбуки к лекции «Продвинутый pandas»).
Нужно сформировать две таблицы:

таблицу с тремя типами выручки для каждого client_id без указания адреса клиента;
аналогичную таблицу по типам выручки с указанием адреса клиента.
Обратите внимание, что в процессе объединения таблиц данные не должны теряться.
"""

import pandas as pd


rzd = pd.DataFrame({
    'client_id': [111, 112, 113, 114, 115],
    'rzd_revenue': [1093, 2810, 10283, 5774, 981]
})

auto = pd.DataFrame({
    'client_id': [113, 114, 115, 116, 117],
    'auto_revenue': [57483, 83, 912, 4834, 98]
})

air = pd.DataFrame({
    'client_id': [115, 116, 117, 118],
    'air_revenue': [81, 4, 13, 173]
})

client_base = pd.DataFrame({
    'client_id': [111, 112, 113, 114, 115, 116, 117, 118],
    'address': ['Комсомольская 4', 'Энтузиастов 8а', 'Левобережная 1а', 'Мира 14',
                'ЗЖБИиДК 1', 'Строителей 18', 'Панфиловская 33', 'Мастеркова 4']
})

result = client_base.merge(rzd, on='client_id', how='left') \
                    .merge(auto, on='client_id', how='left') \
                    .merge(air, on='client_id', how='left')

result = result.fillna(0)

result['total_revenue'] = result['rzd_revenue'] + result['auto_revenue'] + result['air_revenue']

result = result.sort_values('total_revenue', ascending=False).reset_index(drop=True)

print("Объединённая таблица доходов клиентов:")
print(result)

print("\nСводная статистика по видам перевозок:")
print(f"ЖД перевозки (rzd):   {result['rzd_revenue'].sum():>10.0f} руб.")
print(f"Авто перевозки (auto): {result['auto_revenue'].sum():>10.0f} руб.")
print(f"Авиа перевозки (air):  {result['air_revenue'].sum():>10.0f} руб.")
print(f"ИТОГО:                 {result['total_revenue'].sum():>10.0f} руб.")