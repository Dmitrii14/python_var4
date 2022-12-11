import os
import csv

CLASS_DEFAULT = ["rose", "tulip"]  # базовые названия


class Data:
    def __init__(self, dir_name: str) -> None:
        self.number_lines = 0
        self.viewed_files = 1
        self.dir_name = dir_name

    def add(self, path: str, class_name: str, name_image: str) -> None:
        with open("annotation.csv", "a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            if self.number_lines == 0:  # если кол-во строк = 0, то это заголовки файла аннотация
                writer.writerow([
                    "абсолютный путь",
                    "относительный путь",
                    "класс"
                ])
                self.number_lines += 1
            writer.writerow([os.path.join(path, self.dir_name, class_name, name_image),
                             os.path.join(self.dir_name, class_name, name_image), class_name])
            self.number_lines += 1
