"""
Задание 2
Добавьте в класс Rate параметр diff (со значениями True или False), который в случае значения True в методах курсов валют (eur, usd итд) будет возвращать не курс валюты, а изменение по сравнению в прошлым значением.
Считайте, self.diff будет принимать значение True только при возврате значения курса. При отображении всей информации о валюте он не используется.
"""
import requests

class Rate:
    def __init__(self, diff: bool = False):
        self.diff = diff
        self._data = self._fetch_data()

    def _fetch_data(self):
        """Загружает актуальные данные от ЦБ РФ."""
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    def _get_currency(self, char_code: str):
        """Получает данные валюты по её коду (например, 'USD')."""
        valutes = self._data['Valute']
        if char_code not in valutes:
            raise ValueError(f"Валюта с кодом '{char_code}' не найдена.")
        return valutes[char_code]

    def usd(self):
        return self._get_rate_or_diff('USD')

    def eur(self):
        return self._get_rate_or_diff('EUR')

    def jpy(self):
        return self._get_rate_or_diff('JPY')

    def _get_rate_or_diff(self, char_code: str):
        """Возвращает курс или изменение в зависимости от self.diff."""
        data = self._get_currency(char_code)
        current_rate = data['Value'] / data['Nominal']
        if self.diff:
            previous_rate = data['Previous'] / data['Nominal']
            return round(current_rate - previous_rate, 6)
        return round(current_rate, 6)

    def get_info(self, char_code: str):
        """Возвращает полную информацию о валюте (без учёта diff)."""
        return self._get_currency(char_code)



if __name__ == "__main__":
    # 1. Получаем курсы (по умолчанию diff=False)
    rate = Rate()
    print(f"USD: {rate.usd()} руб.")
    print(f"EUR: {rate.eur()} руб.")
    print(f"JPY: {rate.jpy()} руб. (за 1 иену)")

    # 2. Получаем изменения по сравнению с предыдущим днём
    print("\n=== Изменения курсов за день ===")
    rate_diff = Rate(diff=True)
    print(f"USD Δ: {rate_diff.usd():+}")
    print(f"EUR Δ: {rate_diff.eur():+}")
    print(f"JPY Δ: {rate_diff.jpy():+}")

    # 3. Получаем полную информацию (diff игнорируется)
    print("\n=== Полная информация по USD ===")
    info = rate_diff.get_info('USD')  # даже если diff=True — данные полные!
    print(f"Название: {info['Name']}")
    print(f"Номинал: {info['Nominal']}")
    print(f"Текущий курс (за номинал): {info['Value']} руб.")
    print(f"Предыдущий курс: {info['Previous']} руб.")
    print(f"Курс за 1 единицу: {info['Value'] / info['Nominal']:.6f} руб.")