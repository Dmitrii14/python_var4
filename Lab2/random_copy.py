import os
import get_path
import shutil
import csv
import random
import logging
import tqdm

logging.basicConfig(level='DEBUG', filename='mylog.log')
logger = logging.getLogger()
file_log = tqdm.tqdm(total=1, position=1, bar_format='{desc}')
frame_log = tqdm.tqdm(total=0, position=2, bar_format='{desc}')


def random_copy(class_name: str):
    """
        Функция нужна для создания файла и рандомного копирования изображений в новый файл из файла annotation
        :class_name: - имя класса
        :rand_number: - находит случайное число от 0 до 1000
    """
    file = os.path.join("random_annotation.csv")
    logger.debug(f'Creating data')
    file_log.set_description_str(f'Current file: {file}')
    with open(file, "a", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
        file_writer.writerow(["Абсолютный путь", "Относительный путь", "Класс"])
        for i in range(1000):
            rand_number = random.randint(0, 1000)
            if (os.path.isfile(get_path.get_absolute_path(class_name, i, "download")) == True):
                while (os.path.isfile(get_path.get_absolute_path(class_name, rand_number, "random")) == True):
                    rand_number = random.randint(0, 1000)
                shutil.copyfile(get_path.get_absolute_path(class_name, i, "download"),
                                get_path.get_absolute_path(class_name, rand_number, "random"))
                file_writer.writerow(
                    [get_path.get_absolute_path(class_name, i, "download"), get_path.random_relative_path(rand_number),
                     class_name])
    logger.debug(f'The number of images recorded in the file: {i + 1}')
    frame_log.set_description_str(f'{i:3d} records are formed')


if __name__ == "__main__":
    print("The beginning of random copying of the annotation of images")
    if not os.path.isdir("dataset/random_dataset"):
        os.mkdir("dataset/random_dataset")
    class_name = "rose"
    random_copy(class_name)
    class_name = "tulip"
    random_copy(class_name)
    print("Successful random copying of the annotation of images")
