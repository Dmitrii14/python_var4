import csv
import os
import get_path
import shutil
import logging
logging.basicConfig(level=logging.DEBUG, filename="changed_annotation.csv", filemode="w")


def copy_to_another(class_name: str):
    """
        Функция нужна для создания файла и копирования изображений в новый файл из файла annotation
    """
    logging.getLogger(__name__)
    with open("changed_annotation.csv", "a", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
        file_writer.writerow(["Абсолютный путь", "Относительный путь", "Класс"])
        for i in range(1000):
            if (os.path.isfile(get_path.get_absolute_path(class_name, i, "download")) == True):
                shutil.copyfile(get_path.get_absolute_path(class_name, i, "download"),
                                get_path.get_absolute_path(class_name, i, "changed"))
                file_writer.writerow(
                    [get_path.get_absolute_path(class_name, i, "download"), get_path.changed_relative_path(class_name, i),
                     class_name])


if __name__ == "__main__":
    print("The beginning of copying the annotation of images")
    if not os.path.isdir("dataset/changed_dataset"):
        os.mkdir("dataset/changed_dataset")
    class_name = "rose"
    copy_to_another(class_name)
    class_name = "tulip"
    copy_to_another(class_name)
    print("Successful copying of the annotation of images")
