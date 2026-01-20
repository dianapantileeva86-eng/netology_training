"""
Задание 1
Печатные газеты использовали свой формат дат для каждого выпуска. Для каждой газеты из списка напишите формат указанной даты для перевода в объект datetime:
The Moscow Times — Wednesday, October 2, 2002
The Guardian — Friday, 11.10.13
Daily News — Thursday, 18 August 1977
"""

from datetime import datetime

moscow_times_str = "Wednesday, October 2, 2002"
guardian_str = "Friday, 11.10.13"
daily_news_str = "Thursday, 18 August 1977"

format_moscow = "%A, %B %d, %Y"
format_guardian = "%A, %d.%m.%y"
format_daily = "%A, %d %B %Y"

moscow_dt = datetime.strptime(moscow_times_str, format_moscow)
guardian_dt = datetime.strptime(guardian_str, format_guardian)
daily_dt = datetime.strptime(daily_news_str, format_daily)

print("The Moscow Times:", moscow_dt)
print("The Guardian    :", guardian_dt)
print("Daily News      :", daily_dt)