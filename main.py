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
