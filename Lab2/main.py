import csv
import os
import get_path
import logging
logging.basicConfig(level=logging.INFO, filename="annotation.csv", filemode="w")
logging.info("Creating an annotation of images")


def create_annotation(class_name: str):
    """
        Функция создает файл аннотацию в который записывается абсолютный и относительный путь и класс
    """
    with open("annotation.csv", "a", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
        file_writer.writerow(["Абсолютный путь", "Относительный путь", "Класс"])
        for i in range(1000):
            if (os.path.isfile(get_path.get_absolute_path(class_name, i, "download")) == True):
                file_writer.writerow([get_path.get_absolute_path(class_name, i, "download"),
                                      get_path.download_relative_path(class_name, i), class_name])


def main():
    """
        Главная функция выполнения программы и вывода в консоль начало и конец функции
    """
    print("Start creating an annotation of images")
    class_name = "rose"
    create_annotation(class_name)
    class_name = "tulip"
    create_annotation(class_name)
    print("Successful creation of an annotation of images")


if __name__ == "__main__":
    main()
