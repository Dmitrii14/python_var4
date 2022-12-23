import os
import get_path
import shutil
import csv
import random
import logging
logging.basicConfig(level=logging.INFO, filename="random_annotation.csv", filemode="w")
logging.info("Random copying of the annotation of images")


def random_copy(class_name: str):
    """
        Функция нужна для создания файла и рандомного копирования изображений в новый файл из файла annotation
    """
    with open("random_annotation.csv", "a", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
        file_writer.writerow(["Абсолютный путь", "Относительный путь", "Класс"])
        for i in range(1000):
            rand_number = random.randint(0, 10000)
            if (os.path.isfile(get_path.get_absolute_path(class_name, i, "download")) == True):
                while (os.path.isfile(get_path.get_absolute_path(class_name, rand_number, "random")) == True):
                    rand_number = random.randint(0, 10000)
                shutil.copyfile(get_path.get_absolute_path(class_name, i, "download"),
                                get_path.get_absolute_path(class_name, rand_number, "random"))
                file_writer.writerow(
                    [get_path.get_absolute_path(class_name, i, "download"), get_path.random_relative_path(rand_number),
                     class_name])


def main():
    """
        Главная функция выполнения программы и вывода в консоль начало и конец функции
    """
    print("The beginning of random copying of the annotation of images")
    if not os.path.isdir("dataset/random_dataset"):
        os.mkdir("dataset/random_dataset")
    class_name = "rose"
    random_copy(class_name)
    class_name = "tulip"
    random_copy(class_name)
    print("Successful random copying of the annotation of images")


if __name__ == "__main__":
    main()
