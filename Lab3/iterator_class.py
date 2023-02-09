import next_element as next


class IteratorOfExemplar:
    """
        Класс нужен чтобы обойти объекты внутри собственного класса
    """
    def __init__(self, file_name: str, pointer: str):
        """
            Функция зписывает в файл абсолютный и относительный путь и название класса через ;
        """
        self.filename = file_name
        self.pointer = pointer

    def __next__(self) -> str:
        """
            возвращает следующий элемент
        """
        self.pointer = next.next_element(self.filename, self.pointer)
        return self.pointer
