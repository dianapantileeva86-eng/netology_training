"""
Задание 1
Определите, какому фильму было выставлено больше всего оценок 5.0.
"""

import pandas as pd


movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')


five_star_ratings = ratings[ratings['rating'] == 5.0]

top_movie_id = five_star_ratings['movieId'].value_counts().idxmax()

top_movie_title = movies[movies['movieId'] == top_movie_id]['title'].iloc[0]

print(top_movie_title)