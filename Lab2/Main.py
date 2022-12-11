import os
import csv

CLASS_DEFAULT = ["rose", "tulip"]  # базовые названия


class Data:
    def __init__(self, dir_name: str) -> None:
        self.number_lines = 0
        self.viewed_files = 1
        self.dir_name = dir_name