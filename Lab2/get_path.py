import os
import logging

logging.basicConfig(level='DEBUG', filename='mylog.log')
logger = logging.getLogger()


def download_relative_path(name_class: str, number: int) -> str:
    """
        Функция возвращает путь к файлу аннотации
        :name_class: - название класса
        :number: - номер картинки
    """
    logger.debug(f'Return download path in file annotation')
    return os.path.join(f"dataset/{name_class}/{str(number).zfill(4)}.jpg")


def changed_relative_path(name_class: str, number: int) -> str:
    """
        Функция возвращает путь к файлу копирования
        :name_class: - название класса
        :number: - номер картинки
    """
    logger.debug(f'Return path in file changed_annotation')
    return os.path.join(f"dataset/copy_elements/{name_class}_{str(number).zfill(4)}.jpg")


def random_relative_path(number: int) -> str:
    """
        Функция возвращает путь к файлу рандомного копирования
        :name_class: - название класса
        :number: - номер картинки
    """
    logger.debug(f'Return path in file random_annotation')
    return os.path.join(f"dataset/random_copy/{str(number).zfill(4)}.jpg")


def get_absolute_path(name_class: str, number: int, mode: str) -> str:
    """
        Функция возвращает абсолютный путь к фалам аннотации
        :name_class: - название класса
        :number: - номер картинки
        :mode: - выбор действия в функции
    """
    logger.debug(f'Return absolute path in file annotation')
    if mode == "download":
        return os.path.abspath(download_relative_path(name_class, number))
    if mode == "changed":
        return os.path.abspath(changed_relative_path(name_class, number))
    if mode == "random":
        return os.path.abspath(random_relative_path(number))
