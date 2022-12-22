import os


def download_relative_way(name_class, number):
    return f"dataset/{name_class}/{str(number).zfill(4)}.jpg"


def changed_relative_way(name_class, number):
    return f"dataset/copy_elements/{name_class}_{str(number).zfill(4)}.jpg"


def random_relative_way(number):
    return f"dataset/random_copy/{str(number).zfill(4)}.jpg"


def get_absolute_way(name_class, number, mode):
    if mode == "download":
        return os.path.abspath(download_relative_way(name_class, number))
    if mode == "changed":
        return os.path.abspath(changed_relative_way(name_class, number))
    if mode == "random":
        return os.path.abspath(random_relative_way(number))