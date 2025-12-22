"""
Задание 2
Дан поток дат в формате YYYY-MM-DD, в которых встречаются некорректные значения:
stream = [‘2018-04-02’, ‘2018-02-29’, ‘2018-19-02’]

Напишите функцию, которая проверяет эти даты на корректность. То есть для каждой даты возвращает True — дата корректна или False — некорректная.
"""
from datetime import datetime

def validate_dates(stream):
    results = []
    for date_str in stream:
        try:

            datetime.strptime(date_str, '%Y-%m-%d')
            results.append(True)
        except ValueError:
            # Если ошибка — дата некорректна
            results.append(False)
    return results



stream = ['2018-04-02', '2018-02-29', '2018-19-02']
print(validate_dates(stream))