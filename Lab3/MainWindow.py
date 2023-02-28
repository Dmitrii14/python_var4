import copy_elements as cop
import random_copy as ran
from iterator_class import IteratorOfExemplar
import sys
import os
from enum import Enum
from main import create_annotation
from PyQt6.QtCore import QSize, Qt
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
        self.text_directory = None
        self.dirname = None
        self.rose_index = 0
        self.tulip_index = 0
        self.tiger_path = None
        self.text = None
        self.image_tulip = None
        self.image_rose = None

        # параметры окна
        self.setWindowTitle("Pictures")
        self.dataset_path = QFileDialog.getExistingDirectory(self, 'Путь к папке базового датасет')
        self.setFixedSize(QSize(800, 600))
        src = QLabel(f'Базовый датасет:\n{self.dataset_path}', self)
        src.setFixedSize(QSize(800, 50))

        # стартовые значения
        self.count_r = 0
        self.count_t = 0
        self.s_p_rose = os.path.join(self.dataset_path, CLASS_DEFAULT[0], "0001.jpg")
        self.s_p_tulip = os.path.join(self.dataset_path, CLASS_DEFAULT[1], "0001.jpg")

        # кнопки
        self.btn_get_directory = self.add_button("Выбрать директорию", 140, 50, 630, 50)
        self.btn_create_of_annotation = self.add_button("Создать аннотацию", 140, 50, 630, 100)
        self.btn_copy_of_dataset = self.add_button("Копирование датасета", 140, 50, 630, 150)
        self.btn_random_of_dataset = self.add_button("Рандомный датасет", 140, 50, 630, 200)
        self.btn_next_rose = self.add_button("Следующая роза", 140, 50, 630, 250)
        self.btn_next_tulip = self.add_button("Следующий тюльпан", 140, 50, 630, 300)
        self.go_to_exit = self.add_button("Выйти", 140, 50, 630, 500)

        # картинка
        self.pic = QtWidgets.QLabel(self)
        self.pic.setPixmap(QtGui.QPixmap(self.s_p_rose))
        self.pic.resize(600, 500)
        self.pic.move(10, 50)

        if not os.path.exists(self.s_p_rose) or os.path.exists(self.s_p_tulip):
            self.pic.setText('Ошибка!\n' + 'В базовом датасете нету начальных картинок: "rose" или "tulip"')
        self.btn_get_directory.clicked.connect(self.get_directory)
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

    def get_directory(self) -> None:
        """
        Выбор директории для работы.
        """
        self.rose_index = 0
        self.tulip_index = 0
        self.dataset_path = QFileDialog.getExistingDirectory(self)
        self.text_directory.setText(f"Текущая папка: {self.dataset_path}")
        self.dirname = os.path.dirname(self.dataset_path)
        if os.path.isdir(os.path.join(self.dataset_path, "rose")) & os.path.isdir(os.path.join(self.dataset_path, 
                                                                                               "tulip")):
            rosefiles = []
            for (dirpath, dirnames, filenames) in os.walk(os.path.join(self.dataset_path, CLASS_DEFAULT[0])):
                rosefiles.extend(filenames)
                self.rose_path = os.path.join(self.dataset_path, CLASS_DEFAULT[0], rosefiles[0])
                self.image_rose.setPixmap(QtGui.QPixmap(self.rose_path).scaled(self.image_rose.height(),
                                                                                self.image_rose.width(), 
                                                                                aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))
            tulipfiles = []
            for (dirpath, dirnames, filenames) in os.walk(os.path.join(self.dataset_path, CLASS_DEFAULT[1])):
                tulipfiles.extend(filenames)
                self.tulip_path = os.path.join(self.dataset_path, CLASS_DEFAULT[1], tulipfiles[0])
                self.image_tulip.setPixmap(QtGui.QPixmap(self.tulip_path).scaled(self.image_tulip.height(), 
                                                                                 self.image_tulip.width(), 
                                                                                 aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))
                self.text.setText("Папка выбрана!")
        else:
            self.text.setText("Здесь нет папок rose и tulip!")
            
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
