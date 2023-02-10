import csv
import logging

logging.basicConfig(level='DEBUG', filename='mylog.log')
logger = logging.getLogger()


class IteratorOfExemplar:
    """
        Класс нужен чтобы обойти объекты внутри собственного класса
    """
    logger = logging.getLogger()

    def __init__(self, file_name: str, class_name: str):
        """
            Функция зписывает в файл абсолютный и относительный путь и название класса через ;
            :file_name: - имя файла
            :class_name: - имя класса
            :reader: - считывает информацию из файла
        """
        self.logger.debug(f'Function writer in file')
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
        self.logger.debug(f'iterator of class')
        return self

    def __next__(self) -> str:
        """
            Функция перехода к следующему элементу
        """
        self.logger.debug(f'Function of moving to the next element')
        if self.counter < self.limit:
            self.counter += 1
            return self.rows[self.counter]
        else:
            raise StopIteration
            return None
