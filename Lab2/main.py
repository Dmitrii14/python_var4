import csv
import os
import get_path
import logging
import tqdm
from enum import Enum
from get_path import Mode


logging.basicConfig(level='DEBUG', filename='mylog.log')
logger = logging.getLogger()
file_log = tqdm.tqdm(total=1, position=1, bar_format='{desc}')
frame_log = tqdm.tqdm(total=0, position=2, bar_format='{desc}')


def create_annotation(class_name: str):
    """
        Функция создает файл аннотацию в который записывается абсолютный и относительный путь и класс
        :file_writer: - запись в файл
        :class_name: - имя класса
    """
    file = os.path.join("annotation.csv")
    logger.debug(f'Creating data')
    file_log.set_description_str(f'Current file: {file}')
    with open(file, "a", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
        file_writer.writerow(["Абсолютный путь", "Относительный путь", "Класс"])
        for i in range(1000):
            if (os.path.isfile(get_path.get_absolute_path(class_name, i, Enum(Mode.download.name))) == True):
                file_writer.writerow([get_path.get_absolute_path(class_name, i, Enum(Mode.download.name)),
                                      get_path.download_relative_path(class_name, i), class_name])
    logger.debug(f'The number of images recorded in the file: {i+1}')
    frame_log.set_description_str(f'{i:3d} records are formed')


if __name__ == "__main__":
    print("Start creating an annotation of images")
    class_name = "rose"
    create_annotation(class_name)
    class_name = "tulip"
    create_annotation(class_name)
    print("Successful creation of an annotation of images")
