"""
объединила три задания
"""

import requests
import argparse
import sys


SHOW_CURRENCY = True
SHOW_RATE = True
SHOW_DESIGNER = True



# Функция: валюта с максимальным курсом

def get_currency_with_max_rate() -> str:
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        valutes = data["Valute"]
        max_valute = max(
            valutes.values(),
            key=lambda v: v["Value"] / v["Nominal"]
        )
        return max_valute["Name"]
    except Exception as e:
        return f"Ошибка: {e}"

# Класс Rate
class Rate:
    def __init__(self, diff: bool = False):
        self.diff = diff
        self._data = self._fetch_data()
    def _fetch_data(self):
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    def _get_currency(self, char_code: str):
        valutes = self._data['Valute']
        if char_code not in valutes:
            raise ValueError(f"Валюта '{char_code}' не найдена")
        return valutes[char_code]
    def usd(self):
        return self._get_rate_or_diff('USD')
    def eur(self):
        return self._get_rate_or_diff('EUR')
    def jpy(self):
        return self._get_rate_or_diff('JPY')
    def _get_rate_or_diff(self, char_code: str):
        data = self._get_currency(char_code)
        current = data['Value'] / data['Nominal']
        if self.diff:
            previous = data['Previous'] / data['Nominal']
            return round(current - previous, 6)
        return round(current, 6)
    def get_info(self, char_code: str):
        return self._get_currency(char_code)


# Класс Designer
class Designer:
    def __init__(self, name: str, awards: int = 2):
        self.name = name
        self.awards = awards
    @property
    def points(self) -> int:
        return self.awards * 2
    @property
    def grade(self) -> int:
        return self.points // 7
    def add_award(self, count: int = 1):
        if count < 0:
            raise ValueError("Количество премий не может быть отрицательным")
        self.awards += count
    def __str__(self):
        return (f"Дизайнер {self.name}: "
                f"премий — {self.awards}, "
                f"баллов — {self.points}, "
                f"грейд — {self.grade}")


def main():
    global SHOW_CURRENCY, SHOW_RATE, SHOW_DESIGNER

    parser = argparse.ArgumentParser(
        description="Скрипт для работы с курсами валют и расчётом грейдов дизайнеров."
    )
    parser.add_argument("--currency", action="store_true", help="Показать валюту с максимальным курсом")
    parser.add_argument("--rate", action="store_true", help="Показать курсы валют и их изменения")
    parser.add_argument("--designer", action="store_true", help="Показать примеры работы с дизайнерами")
    parser.add_argument("--all", action="store_true", help="Запустить все части (по умолчанию)")
    args = parser.parse_args()

    # Устанавливаем глобальные флаги
    if not (args.currency or args.rate or args.designer or args.all):
        args.all = True

    SHOW_CURRENCY = args.all or args.currency
    SHOW_RATE = args.all or args.rate
    SHOW_DESIGNER = args.all or args.designer
    if SHOW_CURRENCY:
        print("\n🔹 Часть 1: Валюта с самым высоким курсом")
        print(f"Самая дорогая валюта: {get_currency_with_max_rate()}")
    if SHOW_RATE:
        print("\n🔹 Часть 2: Курсы и изменения")
        now = Rate(diff=False)
        diff = Rate(diff=True)
        print(f"USD: {now.usd()} руб. (Δ: {diff.usd():+})")
        print(f"EUR: {now.eur()} руб. (Δ: {diff.eur():+})")
    if SHOW_DESIGNER:
        print("\n🔹 Часть 3: Дизайнеры и грейды")
        d1 = Designer("Анна")
        d1.add_award(3)
        d2 = Designer("Карл", awards=6)
        print(d1)
        print(d2)

    print("\n✅ Выполнение завершено.")
if __name__ == "__main__":
    main()
