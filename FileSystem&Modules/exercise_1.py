"""
Домашнее задание к лекции «Работа с файловой системой и модули»
"""
import json
import csv

# Шаг 1: Загрузка purchase_log.txt в словарь purchases
purchases = {}

with open('purchase_log.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line:
            record = json.loads(line)
            purchases[record['user_id']] = record['category']

print(f"Загружено {len(purchases)} записей о покупках.")

# Шаг 2: Обработка visit_log.csv и запись funnel.csv
with open('visit_log.csv', 'r', encoding='utf-8') as infile, \
     open('funnel.csv', 'w', encoding='utf-8', newline='') as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        if len(row) < 3:
            # Пропускаем некорректные строки
            writer.writerow(row)
            continue

        user_id = row[0]
        if user_id in purchases:
            row[2] = purchases[user_id]

        writer.writerow(row)

print("Файл funnel.csv успешно создан.")