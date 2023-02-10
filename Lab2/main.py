import csv
import os
import get_path
import logging

logging.basicConfig(level='DEBUG', filename='mylog.log')
logger = logging.getLogger()


def create_annotation(class_name: str):
    """
        Функция создает файл аннотацию в который записывается абсолютный и относительный путь и класс
        :file_writer: - запись в файл
        :class_name: - имя класса
    """
    logger.debug(f'Create annotation file with absolute and relative way and class = {class_name}')
    with open("annotation.csv", "a", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
        file_writer.writerow(["Абсолютный путь", "Относительный путь", "Класс"])
        for i in range(1000):
            if (os.path.isfile(get_path.get_absolute_path(class_name, i, "download")) == True):
                file_writer.writerow([get_path.get_absolute_path(class_name, i, "download"),
                                      get_path.download_relative_path(class_name, i), class_name])


if __name__ == "__main__":
    print("Start creating an annotation of images")
    class_name = "rose"
    create_annotation(class_name)
    class_name = "tulip"
    create_annotation(class_name)
    print("Successful creation of an annotation of images")
