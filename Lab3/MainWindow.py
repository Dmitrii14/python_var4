import copy_elements as cop
import random_copy as ran
from iterator_class import IteratorOfExemplar
import sys
import os
from enum import Enum
from main import create_annotation
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog
from PyQt6 import QtGui, QtWidgets
from typing import Type

CLASS_DEFAULT = ["rose", "tulip"]


class Type(Enum):
    ROSE = 0
    TULIP = 1


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        # параметры окна
        self.setWindowTitle("Pictures")
        self.dataset_path = QFileDialog.getExistingDirectory(self, 'Путь к папке базового датасет')
        self.setFixedSize(QSize(800, 600))
        src = QLabel(f'Базовый датасет:\n{self.dataset_path}', self)
        src.setFixedSize(QSize(800, 50))

        # стартовые значения
        self.count_r = 0
        self.count_t = 0
        self.s_p_rose = QFileDialog.getOpenFileName(self, 'Путь к первой розе')
        self.s_p_tulip = QFileDialog.getOpenFileName(self, 'Путь к первому тюльпану')
        self.s_p_rose = self.s_p_rose[0]
        self.s_p_tulip = self.s_p_tulip[0]

        # кнопки
        self.btn_create_of_annotation = self.add_button("Создать аннотацию", 140, 50, 630, 50)
        self.btn_copy_of_dataset = self.add_button("Копирование датасета", 140, 50, 630, 100)
        self.btn_random_of_dataset = self.add_button("Рандомный датасет", 140, 50, 630, 150)
        self.btn_next_rose = self.add_button("Следующая роза", 140, 50, 630, 200)
        self.btn_next_tulip = self.add_button("Следующий тюльпан", 140, 50, 630, 250)
        self.go_to_exit = self.add_button("Выйти", 140, 50, 630, 500)

        # картинка
        self.pic = QtWidgets.QLabel(self)
        self.pic.setPixmap(QtGui.QPixmap(self.s_p_rose))
        self.pic.resize(600, 500)
        self.pic.move(10, 50)

        if not os.path.exists(self.s_p_rose) or os.path.exists(self.s_p_tulip):
            self.pic.setText('Ошибка!\n' + 'В базовом датасете нету начальных картинок: "rose" или "tulip"')

        self.btn_next_rose.clicked.connect(
            lambda image_path=self.s_p_rose, index=Type.ROSE.value, count=self.count_r: self.next(self.s_p_rose,
                                                                                                  Type.ROSE.value,
                                                                                                  self.count_r))
        self.btn_next_tulip.clicked.connect(
            lambda image_path=self.s_p_tulip, index=Type.TULIP.value, count=self.count_t: self.next(self.s_p_tulip,
                                                                                                    Type.TULIP.value,
                                                                                                    self.count_t))

        # создание аннотации, копия + рандом
        self.btn_create_of_annotation.clicked.connect(self.create_annotation)
        self.btn_copy_of_dataset.clicked.connect(self.copy_of_dataset)
        self.btn_random_of_dataset.clicked.connect(self.random_of_dataset)

        # выход из программы
        self.go_to_exit.clicked.connect(self.exit)

        self.show()

    def add_button(self, name: str, size_x: int, size_y: int, pos_x: int, pos_y: int) -> type(QPushButton):
        """
            Создание кнопки
            :name: - название кнопки
            :size_x: - размер по x
            :size_y: - размер по y
            :pos_x: - позиция по x
            :pos_y: - позиция по y
        """
        button = QPushButton(name, self)
        button.setFixedSize(QSize(size_x, size_y))
        button.move(pos_x, pos_y)
        return button

    def next(self, image_path: str, index: int, count: int) -> None:
        """
            метод перехода к следующей картинке
            :image_path: - путь к первой розе
            :index: - индификатор картинки(роза или тюльпан)
            :count: - счетчик
        """
        try:
            if count >= 1000 or count < 1:
                image_path = QFileDialog.getOpenFileName(self, 'Путь к первой розе')
            else:
                annotation_path = QFileDialog.getOpenFileName(self, 'Путь к вашей аннотации')
                next = IteratorOfExemplar(annotation_path, image_path).__next__()
                next.replace("", '"')
                image_path = next.replace("/", "\\")
                count += 1
            self.pic.setPixmap(QtGui.QPixmap(image_path.replace('"', "")))
            if index == 0 and count != 0:
                self.s_p_rose = image_path
                self.count_r = count
            elif index == 1 and count != 0:
                self.s_p_tulip = image_path
                self.count_t = count
            else:
                self.pic.setText('Ошибка!\n' + 'Нет начальных картинок: "rose" или "tulip"')
        except OSError as error:
            print(f"{error}")

    def create_annotation(self) -> None:
        """
            метод создания файла аннотации
        """
        try:
            class_name = "rose"
            create_annotation(class_name)
            class_name = "tulip"
            create_annotation(class_name)
        except OSError as error:
            print(f"{error}")

    def copy_of_dataset(self) -> None:
        """
            метод создания копии dataset
        """
        try:
            class_name = "rose"
            cop.copy_to_another(class_name)
            class_name = "tulip"
            cop.copy_to_another(class_name)
        except OSError as error:
            print(f"{error}")

    def random_of_dataset(self) -> None:
        """
            метод создания рандомизации датасет
        """
        try:
            class_name = "rose"
            ran.random_copy(class_name)
            class_name = "tulip"
            ran.random_copy(class_name)
        except OSError as error:
            print(f"{error}")

    def exit(self) -> None:
        """
            метод выхода из программы
        """
        print("До свидания!")
        self.quit()


if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        app.exec()
