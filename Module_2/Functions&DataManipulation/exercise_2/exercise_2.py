"""
Задание 2
Используйте файл keywords.csv.
Нужно написать гео-классификатор, который каждой строке сможет выставить географическую принадлежность определённому региону. Т. е. если поисковый запрос содержит название города региона, то в столбце ‘region’ пишется название этого региона. Если поисковый запрос не содержит названия города, то ставим ‘undefined’.
Правила распределения по регионам Центр, Северо-Запад и Дальний Восток:
geo_data = {
'Центр': ['москва', 'тула', 'ярославль'],
'Северо-Запад': ['петербург', 'псков', 'мурманск'],
'Дальний Восток': ['владивосток', 'сахалин', 'хабаровск']
}
Результат классификации запишите в отдельный столбец region.
"""
import pandas as pd

# Геоданные
geo_data = {
    'Центр': ['москва', 'тула', 'ярославль'],
    'Северо-Запад': ['петербург', 'псков', 'мурманск'],
    'Дальний Восток': ['владивосток', 'сахалин', 'хабаровск']
}
city_to_region = {}
for region, cities in geo_data.items():
    for city in cities:
        city_to_region[city] = region

df = pd.read_csv('keywords.csv')
df['keyword_lower'] = df['keyword'].str.lower()

def classify_region(query):
    if pd.isna(query):
        return 'undefined'
    for city, region in city_to_region.items():
        if city in query:
            return region
    return 'undefined'

df['region'] = df['keyword_lower'].apply(classify_region)
df.drop(columns=['keyword_lower'], inplace=True)
df.to_csv('keywords_with_region.csv', index=False)
print("Классификация завершена. Результат сохранён в 'keywords_with_region.csv'.")