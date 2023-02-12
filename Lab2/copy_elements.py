import csv
import os
import get_path
import shutil
import logging
import tqdm

logging.basicConfig(level='DEBUG', filename='mylog.log')
logger = logging.getLogger()
file_log = tqdm.tqdm(total=1, position=1, bar_format='{desc}')
frame_log = tqdm.tqdm(total=0, position=2, bar_format='{desc}')


def copy_to_another(class_name: str):
    """
        Функция нужна для создания файла и копирования изображений в новый файл из файла annotation
        :class_name: - имя класса
        :file_writer: - запись в файл
    """
    file = os.path.join("changed_annotation.csv")
    logger.debug(f'Copying Elements')
    file_log.set_description_str(f'Current file: {file}')
    with open(file, "a", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
        logger.debug(f'The file opened successfully {w_file}')
        file_writer.writerow(["Абсолютный путь", "Относительный путь", "Класс"])
        for i in range(1000):
            if (os.path.isfile(get_path.get_absolute_path(class_name, i, "download")) == True):
                shutil.copyfile(get_path.get_absolute_path(class_name, i, "download"),
                                get_path.get_absolute_path(class_name, i, "changed"))
                file_writer.writerow(
                    [get_path.get_absolute_path(class_name, i, "download"), get_path.changed_relative_path(class_name, i),
                     class_name])
    logger.debug(f'The number of images recorded in the file: {i + 1}')
    frame_log.set_description_str(f'{i:3d} records are formed')


if __name__ == "__main__":
    print("The beginning of copying the annotation of images")
    if not os.path.isdir("dataset/changed_dataset"):
        os.mkdir("dataset/changed_dataset")
    class_name = "rose"
    copy_to_another(class_name)
    class_name = "tulip"
    copy_to_another(class_name)
    print("Successful copying of the annotation of images")
