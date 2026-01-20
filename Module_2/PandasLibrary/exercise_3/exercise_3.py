"""
Задание 3
Выберите страницу любого сайта с табличными данными. Импортируйте таблицы в pandas DataFrame. Вы можете взять любые страницы.
Примеры страниц:
https://pythonworld.ru/tipy-dannyx-v-python/stroki-funkcii-i-metody-strok.html
"""

import pandas as pd

# URL страницы
url = "https://pythonworld.ru/tipy-dannyx-v-python/stroki-funkcii-i-metody-strok.html"

# Импорт всех таблиц со страницы
tables = pd.read_html(url)

# На этой странице только одна таблица — заберём её
df = tables[0]

# Покажем результат
print(df.head())