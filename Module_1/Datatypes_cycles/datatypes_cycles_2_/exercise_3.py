"""
Задание 3
Дана переменная, в которой хранится информация о затратах и доходе рекламных кампаний
по различным источникам. Необходимо дополнить исходную структуру показателем ROI,
который рассчитаем по формуле: ((revenue / cost) - 1) * 100

Пример работы программы:

results = {
‘vk’: {‘revenue’: 103, ‘cost’: 98},
‘yandex’: {‘revenue’: 179, ‘cost’: 153},
‘facebook’: {‘revenue’: 103, ‘cost’: 110},
‘adwords’: {‘revenue’: 35, ‘cost’: 34},
‘twitter’: {‘revenue’: 11, ‘cost’: 24},
}
Результат:

{‘adwords’: {‘revenue’: 35, ‘cost’: 34, ‘ROI’: 2.94},
‘facebook’: {‘revenue’: 103, ‘cost’: 110, ‘ROI’: -6.36},
‘twitter’: {‘revenue’: 11, ‘cost’: 24, ‘ROI’: -54.17},
‘vk’: {‘revenue’: 103, ‘cost’: 98, ‘ROI’: 5.1},
‘yandex’: {‘revenue’: 179, ‘cost’: 153, ‘ROI’: 16.99}}
"""

import json


results = {
    'vk': {'revenue': 103, 'cost': 98},
    'yandex': {'revenue': 179, 'cost': 153},
    'facebook': {'revenue': 103, 'cost': 110},
    'adwords': {'revenue': 35, 'cost': 34},
    'twitter': {'revenue': 11, 'cost': 24},
}

for source in results.values():
    roi = ((source['revenue'] / source['cost']) - 1) * 100
    source['ROI'] = round(roi, 2)

sorted_results = {k: results[k] for k in sorted(results)}
print(json.dumps(sorted_results, indent=4, ensure_ascii=False))