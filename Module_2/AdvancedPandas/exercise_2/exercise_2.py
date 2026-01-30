"""
Задание 2
В файле URLs.txt содержатся URL страниц новостного сайта. Вам нужно отфильтровать его по адресам страниц с текстами новостей. Известно, что шаблон страницы новостей имеет внутри URL конструкцию: /, затем 8 цифр, затем дефис. Выполните действия:

Прочитайте содержимое файла с датафрейм.
Отфильтруйте страницы с текстом новостей, используя метод str.contains и регулярное выражение в соответствие с заданным шаблоном.
"""
import pandas as pd

urls_df = pd.read_csv('URLs.txt', header=None, names=['url'])

news_urls = urls_df[urls_df['url'].str.contains(r'/\d{8}-', regex=True)]

print(f"Всего URL: {len(urls_df)}")
print(f"URL новостей: {len(news_urls)}")
print("\nПримеры отфильтрованных URL:")
print(news_urls.head(10))

news_urls.to_csv('news_urls.csv', index=False, header=False)
print("\n Отфильтрованные URL сохранены в файл news_urls.csv")