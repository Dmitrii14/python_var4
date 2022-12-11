import os
import shutil
import requests
from bs4 import BeautifulSoup as BS
HEADERS = {"User-Agent": "Mozilla/5.0"}

URL = "https://yandex.ru/images/"  # ссылка на страничку html


def save_image(image_url, name, i):
    """сохранение картинки в папку"""
    req = requests.get(f"https:{image_url}")
    file = os.path.join(f"../Lab2/dataset/{name}/{i:04d}.jpg")
    with open(file, "wb") as saver:
        saver.write(req.content)


def check_folder():
    """проверка существования папки"""
    try:
        if not os.path.isdir("../Lab2/dataset"):
            os.mkdir("../Lab2/dataset")
        else:
            shutil.rmtree("../Lab2/dataset")
            os.mkdir("../Lab2/dataset")
    except OSError as err:
        print(f"Возникла ошибка!!{err}")


def get_images_url(name):
    """
    Основная функция программы в которой с помощью цикла мы пробегаемся по searcher потом записываем ссылку с тега img
    потом в массив добавляем значение переменной потом проверяем строку на пустоту, если не пустая,
     то сохраняем картинку.
    """
    i = 1
    page = 0
    request = requests.get(f"{URL}search?p={page}&text={name}&lr=51&rpt=image", HEADERS)
    html = BS(request.content, "html.parser")
    data = []
    searcher = html.findAll("img")
    try:
        os.mkdir(f"../Lab2/dataset/{name}")
    except PermissionError:
        print("Unable to create a directory")
    for event in searcher:
        image_url = event.get("src")
        data.append([image_url])
        if (image_url != ""):
            save_image(image_url, name, i)
            i += 1
        if (i > 999):
            page = 0
            break
        page += 1
    print("Images save: ")
    print(data)


if __name__ == "__main__":
    check_folder()
    get_images_url("rose")
    get_images_url("tulip")
