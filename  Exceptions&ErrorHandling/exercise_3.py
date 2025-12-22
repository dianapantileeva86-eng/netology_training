"""
Задание 3
Напишите функцию date_range, которая возвращает список дат за период от start_date до end_date.
Даты должны вводиться в формате YYYY-MM-DD. В случае неверного формата или при start_date > end_date должен возвращаться пустой список.
"""

from datetime import datetime, timedelta


def date_range(start_date, end_date):
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return []
    if start > end:
        return []

    dates = []
    current = start
    while current <= end:
        dates.append(current.strftime('%Y-%m-%d'))
        current += timedelta(days=1)
    return dates



print(date_range('2023-01-01', '2023-01-05'))
# ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05']

print(date_range('2023-01-05', '2023-01-01'))  # start > end
# []

print(date_range('2023-13-01', '2023-01-05'))  # неверный формат
# []