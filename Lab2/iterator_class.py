import csv


class IteratorOfExemplar:
    """
        Класс нужен чтобы обойти объекты внутри собственного класса
    """
    def __init__(self, file_name: str, class_name: str):
        """
            Функция зписывает в файл абсолютный и относительный путь и название класса через ;
            :file_name: - имя файла
            :class_name: - имя класса
            :reader: - считывает информацию из файла
        """
        self.limit = -1
        self.counter = -1
        self.file_name = file_name
        self.class_name = class_name
        self.rows = []
        with open(file_name, encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=";")
            for row in reader:
                if row[2] == class_name:
                    self.rows.append(row[0] + ';' + row[2])
                    self.limit += 1

    def __iter__(self) -> str:
        """
            Функция просто возвращает self
        """
        return self

    def __next__(self) -> str:
        """
            Функция перехода к следующему элементу
        """
        if self.counter < self.limit:
            self.counter += 1
            return self.rows[self.counter]
        else:
            raise StopIteration
            return None
