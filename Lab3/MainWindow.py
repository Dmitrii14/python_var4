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


class Type(Enum):
    ROSE = 0
    TULIP = 1


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        # параметры окна
        self.setWindowTitle("Main window")
        self.dataset_path = QFileDialog.getExistingDirectory(self, 'Путь к папке базового датасет')
        src = QLabel(f'Базовый датасет:\n{self.dataset_path}', self)
        src.setFixedSize(QSize(800, 50))

        # стартовые значения
        self.count_r = 1
        self.count_t = 1
        self.s_p_rose = os.path.join("dataset", "rose", "0001.jpg")
        self.s_p_tulip = os.path.join("dataset", "tulip", "0001.jpg")

        # кнопки
        self.btn_create_of_annotation = self.add_button("Создать аннотацию", 150, 50, 630, 50)
        self.btn_copy_of_dataset = self.add_button("Копирование датасет", 150, 50, 630, 100)
        self.btn_random_of_dataset = self.add_button("Рандомное датасет", 150, 50, 630, 150)
        self.btn_next_rose = self.add_button("Следующая роза", 150, 50, 630, 250)
        self.btn_back_rose = self.add_button("Предыдущая роза", 150, 50, 630, 300)
        self.btn_next_tulip = self.add_button("Следующий тюльпан", 150, 50, 630, 350)
        self.btn_back_tulip = self.add_button("Предыдущий тюльпан", 150, 50, 630, 400)
        self.go_to_exit = self.add_button("Выйти", 150, 50, 630, 500)

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
        self.btn_back_rose.clicked.connect(
            lambda image_path=self.s_p_rose, index=Type.ROSE.value, count=self.count_r: self.back(self.s_p_rose,
                                                                                                  Type.ROSE.value,
                                                                                                  self.count_r))
        self.btn_next_tulip.clicked.connect(
            lambda image_path=self.s_p_tulip, index=Type.TULIP.value, count=self.count_t: self.next(self.s_p_tulip,
                                                                                                    Type.TULIP.value,
                                                                                                    self.count_t))
        self.btn_back_tulip.clicked.connect(
            lambda image_path=self.s_p_tulip, index=Type.TULIP.value, count=self.count_t: self.back(self.s_p_tulip,
                                                                                                    Type.TULIP.value,
                                                                                                    self.count_t))

        # создание аннотации, копия + рандом
        self.btn_create_of_annotation.clicked.connect(self.create_annotation)
        self.btn_copy_of_dataset.clicked.connect(self.copy_of_dataset)
        self.btn_random_of_dataset.clicked.connect(self.random_of_dataset)

        # выход из программы
        self.go_to_exit.clicked.connect(self.exit)

        self.show()

    def add_button(self, name: str, size_x: int, size_y: int, pos_x: int, pos_y: int):
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

    def next(self, image_path: str, index: int, count: int):
        """
            метод перехода к следующей картинки
        """
        try:
            if count >= 1000 or count < 1:
                image_path = os.path.join("dataset", index, "0001.jpg")
            else:
                next = IteratorOfExemplar("annotation.csv", image_path).__next__()
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
        except OSError:
            print("error")

    def back(self, image_path: str, index: int, count: int):
        """
            метод перехода к предыдущей картинки
        """
        try:
            if count >= 1000 or count < 1:
                image_path = os.path.join("dataset", index, "0001.jpg")
            else:
                next = IteratorOfExemplar("annotation.csv", image_path).__back__()
                next.replace("", '"')
                image_path = next.replace("/", "\\")
                count -= 1
            self.pic.setPixmap(QtGui.QPixmap(image_path.replace('"', "")))
            if index == 0 and count != 0:
                self.s_p_rose = image_path
                self.count_r = count
            elif index == 1 and count != 0:
                self.s_p_tulip = image_path
                self.count_t = count
            else:
                self.pic.setText('Ошибка!\n' + 'Нет начальных картинок: "rose" или "tulip"')
        except OSError:
            print("error")

    def create_annotation(self):
        """
            метод создания файла аннотации
        """
        try:
            class_name = "rose"
            create_annotation(class_name)
            class_name = "tulip"
            create_annotation(class_name)
        except OSError:
            print("error")

    def copy_of_dataset(self):
        """
            метод создания копии dataset
        """
        try:
            class_name = "rose"
            cop.copy_to_another(class_name)
            class_name = "tulip"
            cop.copy_to_another(class_name)
        except OSError:
            print("error")

    def random_of_dataset(self):
        """
            метод создания рандомизации датасет
        """
        try:
            class_name = "rose"
            ran.random_copy(class_name)
            class_name = "tulip"
            ran.random_copy(class_name)
        except OSError:
            print("error")

    def exit(self):
        """
            метод выхода из программы
        """
        print("До свидания!")
        self.quit()


if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        app.exec()
