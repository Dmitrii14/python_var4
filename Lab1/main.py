import os
import shutil
import requests
from bs4 import BeautifulSoup as BS

URL = "https://yandex.ru/images/"  # ссылка на страничку html


def save_image(image_url, name, i):
    """сохранение картинки в папку"""
    req = requests.get(f"https:{image_url}")
    with open(f"dataset/{name}/{i:04d}.jpg", "wb") as saver:
        saver.write(req.content)


def check_folder():
    """проверка существования папки"""
    try:
        os.mkdir("dataset")
    except:
        shutil.rmtree("dataset")
        os.mkdir("dataset")


def get_images_url(name):
    """
    Основная функция программы в которой с помощью цикла мы пробегаемся по searcher потом записываем ссылку с тега img
    потом в массив добавляем значение переменной потом проверяем строку на пустоту, если не пустая,
     то сохраняем картинку.
    """
    i = 1
    page = 0
    request = requests.get(f"{URL}search?p={page}&text={name}&lr=51&rpt=image", headers={"User-Agent": "Mozilla/5.0"})
    html = BS(request.content, "html.parser")
    data = []
    searcher = html.findAll("img")
    os.mkdir(f"dataset/{name}")
    if (i < 999):
        for event in searcher:
            image_url = event.get("src")
            data.append([image_url])
            if (i > 999):
                page = 0
                break
            if (image_url != ""):
                save_image(image_url, name, i)
                i += 1
        page += 1
    print("Images save: ")
    print(data)


if __name__ == "__main__":
    check_folder()
    get_images_url("rose")
    get_images_url("tulip")
