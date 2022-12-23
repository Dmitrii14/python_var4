import os


def download_relative_path(name_class: str, number: int):
    """
        Функция возвращает путь к файлу аннотации
    """
    return os.path.join(f"dataset/{name_class}/{str(number).zfill(4)}.jpg")


def changed_relative_path(name_class: str, number: int):
    """
        Функция возвращает путь к файлу копирования
    """
    return os.path.join(f"dataset/copy_elements/{name_class}_{str(number).zfill(4)}.jpg")


def random_relative_path(number: int):
    """
        Функция возвращает путь к файлу рандомного копирования
    """
    return os.path.join(f"dataset/random_copy/{str(number).zfill(4)}.jpg")


def get_absolute_path(name_class: str, number: int, mode: str):
    """
        Функция возвращает абсолютный путь к фалам аннотации
    """
    if mode == "download":
        return os.path.abspath(download_relative_path(name_class, number))
    if mode == "changed":
        return os.path.abspath(changed_relative_path(name_class, number))
    if mode == "random":
        return os.path.abspath(random_relative_path(number))