"""
Задание 2
По данным файла power.csv посчитайте суммарное потребление стран Прибалтики (Латвия, Литва и Эстония) категорий 4, 12 и 21 за период с 2005 по 2010 год. Не учитывайте в расчётах отрицательные значения quantity.
"""

import pandas as pd

df = pd.read_csv('power.csv')

baltic = ['Latvia', 'Lithuania', 'Estonia']
filtered = df[
    (df['country'].isin(baltic)) &
    (df['year'].between(2005, 2010)) &
    (df['category'].isin([4, 12, 21])) &
    (df['quantity'] > 0)
]

result = filtered['quantity'].sum()
print("Суммарное потребление:", result)