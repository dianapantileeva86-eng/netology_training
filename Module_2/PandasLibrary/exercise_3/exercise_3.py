"""
Задание 3
Выберите страницу любого сайта с табличными данными. Импортируйте таблицы в pandas DataFrame. Вы можете взять любые страницы.
Примеры страниц:
https://pythonworld.ru/tipy-dannyx-v-python/stroki-funkcii-i-metody-strok.html
"""

import pandas as pd

url = "https://pythonworld.ru/tipy-dannyx-v-python/stroki-funkcii-i-metody-strok.html"

tables = pd.read_html(url)


df = tables[0]
print(df.head())