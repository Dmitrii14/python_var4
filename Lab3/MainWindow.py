import os
from enum import Enum
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QGridLayout
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
        self.s_p_rose = os.path.join("dataset", Type.ROSE.value, "0001.jpg")
        self.s_p_tulip = os.path.join("dataset", Type.TULIP.value, "0001.jpg")

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
