import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
from PIL import Image


class DataAnalysis:
    def __init__(self) -> None:
        self.df = None
        self.forming_data_frame()

    def image_form(self, all_path: pd.Series) -> None:
        """
            функция для изображения в столбце находит ширину, высоту и каналы.
            :df: - это dataframe
            :all_path: - это список путей
        """
        height_image = []
        width_image = []
        channels_image = []
        numerical = []
        label_n = 0
        counter = 0
        for path_image in all_path:
            with Image.open(path_image) as img:
                width, height = img.size
                height_image.append(height)
                width_image.append(width)
                channels_image.append(3)
                numerical.append(label_n)
            if counter == 998:
                label_n += 1
            counter += 1
        self.df['numerical'] = numerical
        self.df['width'] = width_image
        self.df['height'] = height_image
        self.df['channel'] = channels_image

    def change_columns_dataframe(self) -> pd.DataFrame:
        """
            данная функция предназначена для изменения столбцов dataframe, добавления
            столбцов высоты, ширины, глубины изображения и вычисления статистической информации для столбцов.
        """
        self.image_forms(self.df["related_path"])
        self.saving_in_csv_file("property.csv")

    def forming_data_frame(self, filename: str = 'annotation.csv'):
        """
            данная функция с помощью pandas формирует DataFrame, происходит изменение названия колонок
            :df: - это dataframe
        """
        self.df = pd.read_csv(filename)
        self.df.drop(['абсолютный путь'], axis=1, inplace=True)
        self.df = self.df.rename(columns={'относительный путь': 'related_path', 'класс': 'name_class'})
        self.change_columns_dataframe()

    def filter_label_class(self, mark_class: str) -> pd.DataFrame:
        """
            функция вернет отфильтрованный по метке класса dataframe. \
            :mark_class: метка класса
        """
        return self.df[self.df.name_class == mark_class]

    def multifunctional_filter(self, width_max: int, height_max: int,
                               mark_class: str) -> pd.DataFrame:
        """
            данная функция вернет отфильтрованный по переданной максимальной высоте и ширине + метке класса dataframe.
            :width_max: максимально возможная ширина
            :height_max: максимально возможная высота
            :mark_class: метка класса
        """
        return self.df[
            ((self.df.name_class == mark_class) & (self.df.width <= width_max) & (self.df.height <= height_max))]

    def grouping(self) -> tuple:
        """
            данная функция делает группировку dataframe, вычисляя min и max + cред.знач по пикселям.
            min() - получение минимального
            max() - получение максимального
            mean() - сред.знач
        """
        self.df['pixels'] = self.df['height'] * self.df['width'] * self.df['channel']
        return self.df.groupby('name_class').min(), self.df.groupby('name_class').max(), self.df.groupby(
            'name_class').mean()

    def histogram_build(self, mark_class: str) -> list:
        """
        данная функция выполняет построение гистограммы. На вход функция принимает dataframe и метку класса,
        на выходе - три массива.
        :mark_class: метка класса
        """
        img = cv2.imread(np.random.choice(self.filter_mark_class(mark_class).related_path.to_numpy()))
        height, width, channel = img.shape
        return [cv2.calcHist([img], [0], None, [256], [0, 256]) / (height * width),
                cv2.calcHist([img], [1], None, [256], [0, 256]) / (height * width),
                cv2.calcHist([img], [2], None, [256], [0, 256]) / (height * width)]
