"""
Задание 3
Напишите класс Designer, который учитывает количество международных премий.
"""


class Designer:
    def __init__(self, name: str, awards: int = 2):
        """
        Инициализация дизайнера.
        :param name: Имя дизайнера
        :param awards: Количество международных премий (по умолчанию 2)
        """
        self.name = name
        self.awards = awards

    @property
    def points(self) -> int:
        """Возвращает общее количество баллов: 2 балла за каждую премию."""
        return self.awards * 2

    @property
    def grade(self) -> int:
        """Возвращает текущий грейд: 1 грейд за каждые 7 баллов (целочисленное деление)."""
        return self.points // 7

    def add_award(self, count: int = 1):
        """
        Добавляет указанное количество международных премий.
        :param count: Сколько премий добавить (по умолчанию 1)
        """
        if count < 0:
            raise ValueError("Количество премий не может быть отрицательным")
        self.awards += count

    def __str__(self):
        return (f"Дизайнер {self.name}: "
                f"премий — {self.awards}, "
                f"баллов — {self.points}, "
                f"грейд — {self.grade}")


if __name__ == "__main__":

    # 1. Создаём дизайнера с двумя премиями (по умолчанию)
    anna = Designer("Анна")
    print(anna)

    # 2. Добавляем премию — например, выиграла новый конкурс
    anna.add_award()
    print("После получения новой премии:")
    print(anna)

    # 3. Создаём опытного дизайнера с 5 премиями
    mark = Designer("Марк", awards=5)
    print("\nНовый дизайнер:")
    print(mark)

    # 4. Марк получает сразу 3 премии
    mark.add_award(3)
    print("После победы в трёх конкурсах:")
    print(mark)

    # 5. Проверим крайний случай: 0 премий
    newbie = Designer("Лиза", awards=0)
    print("\nНовичок без премий:")
    print(newbie)

    # 6. А теперь дадим ей 4 премии → 8 баллов → грейд 1
    newbie.add_award(4)
    print("После успеха на международной арене:")
    print(newbie)

    print("\n✅ Работа завершена.")