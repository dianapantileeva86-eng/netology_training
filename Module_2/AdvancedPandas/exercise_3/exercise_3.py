"""
Задание 3
Используйте файл с оценками фильмов ml-latest-small/ratings.csv. Посчитайте среднее время жизни пользователей,
которые выставили более 100 оценок. Под временем жизни понимается разница между максимальным и минимальным значениями столбца timestamp для данного значения userId.
"""

import pandas as pd

ratings = pd.read_csv('ratings.csv')

user_stats = ratings.groupby('userId').agg(
    num_ratings=('rating', 'count'),
    min_timestamp=('timestamp', 'min'),
    max_timestamp=('timestamp', 'max')
)

user_stats['lifetime'] = user_stats['max_timestamp'] - user_stats['min_timestamp']

active_users = user_stats[user_stats['num_ratings'] > 100]

avg_lifetime = active_users['lifetime'].mean()

print(f"Всего пользователей: {len(user_stats)}")
print(f"Пользователей с >100 оценок: {len(active_users)}")
print(f"Среднее время жизни активных пользователей: {avg_lifetime:.2f} секунд")
print(f"В днях: {avg_lifetime / 86400:.2f} дней")
print(f"В месяцах (≈30 дней): {avg_lifetime / (86400 * 30):.2f} месяцев")

print("\nТоп-5 пользователей по продолжительности активности:")
top_users = active_users.nlargest(5, 'lifetime')[['num_ratings', 'lifetime']]
top_users['days'] = top_users['lifetime'] / 86400
print(top_users[['num_ratings', 'days']].rename(columns={'days': 'lifetime_days'}))