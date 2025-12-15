"""
Домашнее задание к лекции «Функции»
"""
books = [
    {'genre': 'поэзия', 'number': '978-5-1000-1234-7', 'title': 'Евгений Онегин', 'author': 'Александр Пушкин'},
    {'genre': 'фэнтези', 'number': '88006', 'title': 'Властелин колец', 'author': 'Джон Р. Р. Толкин'},
    {'genre': 'детектив', 'number': 'D-1122', 'title': 'Безмолвный свидетель', 'author': 'Агата Кристи'}
]

directories = {
    '1': ['978-5-1000-1234-7', '88006'],
    '2': ['D-1122'],
    '3': []
}

def find_book_by_number(book_number):
    #Возвращает книгу по её уникальному номеру или None.
    for book in books:
        if book['number'] == book_number:
            return book
    return None
def find_book_by_title(title):
    #Возвращает книгу по названию или None.
    for book in books:
        if book['title'] == title:
            return book
    return None
def find_shelf_by_number(book_number):
    #Возвращает номер полки по номеру книги или None.
    for shelf, numbers in directories.items():
        if book_number in numbers:
            return shelf
    return None
def get_all_shelves():
    #Возвращает отсортированный список номеров полок как строку.
    return ", ".join(sorted(directories.keys(), key=lambda x: (len(x), x)))
def handle_book_info():
    book_number = input("Введите номер книги:\n").strip()
    book = find_book_by_number(book_number)
    if book:
        print(f"Название книги: {book['title']}")
        print(f"Автор: {book['author']}")
    else:
        print("Книга не найдена в базе")
def handle_shelf():
    title = input("Введите название книги:\n").strip()
    book = find_book_by_title(title)
    if book:
        shelf = find_shelf_by_number(book['number'])
        if shelf:
            print(f"Книга хранится на полке: {shelf}")
        else:
            # На случай, если книга есть в books, но не в directories (по условию не должно быть)
            print("Книга не найдена на полках")
    else:
        print("Книга не найдена в базе")
def handle_all():
    for book in books:
        shelf = find_shelf_by_number(book['number'])
        print(f"№: {book['number']}, жанр: {book['genre']}, название: {book['title']}, "
              f"автор: {book['author']}, полка хранения: {shelf}")
def handle_add_shelf():
    shelf_number = input("Введите номер полки:\n").strip()
    if shelf_number in directories:
        print(f"Такая полка уже существует. Текущий перечень полок: {get_all_shelves()}.")
    else:
        # Используем setdefault — по условию обязательно!
        directories.setdefault(shelf_number, [])
        print(f"Полка добавлена. Текущий перечень полок: {get_all_shelves()}.")
def handle_del_shelf():
    shelf_number = input("Введите номер полки:\n").strip()
    if shelf_number not in directories:
        print(f"Такой полки не существует. Текущий перечень полок: {get_all_shelves()}.")
    elif directories[shelf_number]:  # полка не пуста
        print(f"На полке есть книги, удалите их перед удалением полки. Текущий перечень полок: {get_all_shelves()}.")
    else:
        del directories[shelf_number]
        print(f"Полка удалена. Текущий перечень полок: {get_all_shelves()}.")
def main():
    while True:
        command = input("Введите команду:\n").strip().lower()
        match command:
            case "q":
                print("Программа завершена.")
                break
            case "book_info":
                handle_book_info()
            case "shelf":
                handle_shelf()
            case "all":
                handle_all()
            case "add_shelf":
                handle_add_shelf()
            case "del_shelf":
                handle_del_shelf()
            case _:
                print("Неизвестная команда. Доступные команды: book_info, shelf, all, add_shelf, del_shelf, q")

if __name__ == "__main__":
    main()