"""
Задание 1
Напишите функцию, которая возвращает название валюты (поле ‘Name’) с максимальным значением курса с помощью сервиса www.cbr-xml-daily.ru...ly_json.js
"""

import requests


def get_currency_with_max_rate() -> str:
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    valutes = data["Valute"]

    # Находим валюту с максимальным курсом за 1 единицу
    max_valute = max(
        valutes.values(),
        key=lambda v: v["Value"] / v["Nominal"]
    )

    return max_valute["Name"]
if __name__ == "__main__":
    currency_name = get_currency_with_max_rate()
    print(f"Валюта с самым высоким курсом сегодня: {currency_name}")