import os, shutil, requests
from bs4 import BeautifulSoup as BS

URL = "https://yandex.ru/images/" # ссылка на страничку html
def save_image(image_url, name, i):
    """сохранение картинки в папку"""
    req = requests.get(f"https:{image_url}")
    saver = open(f"dataset/{name}/{i:04d}.jpg", "wb")
    saver.write(req.content)
    saver.close()