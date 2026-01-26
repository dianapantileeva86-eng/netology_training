"""
Задание 1
Напишите функцию, которая классифицирует фильмы из материалов занятия по правилам:

оценка 2 и ниже — низкий рейтинг;
оценка 4 и ниже — средний рейтинг;
оценка 4.5 и 5 — высокий рейтинг.
"""

import pandas as pd
import os

def classify_movies(df):
    def classify_rating(rating):
        if rating <= 2:
            return 'низкий рейтинг'
        elif rating <= 4:
            return 'средний рейтинг'
        else:
            return 'высокий рейтинг'

    df['class'] = df['rating'].apply(classify_rating)
    return df

input_filename = 'ratings.csv'
output_filename = 'ratings_classified.csv'

if os.path.exists(input_filename):
    df = pd.read_csv(input_filename)
else:
    raise FileNotFoundError(f"Файл '{input_filename}' не найден в текущей директории.")

df = classify_movies(df)

df.to_csv(output_filename, index=False)
print(f"Результат сохранён в '{output_filename}'.")
