import csv
import os
import get_path
import shutil


def copy_to_another(class_name):
    with open("changed_annotation.csv", mode="a", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
        file_writer.writerow(["Абсолютный путь", "Относительный путь", "Класс"])
        for i in range(1050):
            if (os.path.isfile(get_path.get_absolute_way(class_name, i, "download")) == True):
                shutil.copyfile(get_path.get_absolute_way(class_name, i, "download"),
                                get_path.get_absolute_way(class_name, i, "changed"))
                file_writer.writerow(
                    [get_path.get_absolute_way(class_name, i, "download"), get_path.changed_relative_way(class_name, i),
                     class_name])


def main():
    print("Start changing")
    if not os.path.isdir("dataset/changed_dataset"):
        os.mkdir("dataset/changed_dataset")
    class_name = "rose"
    copy_to_another(class_name)
    class_name = "tulip"
    copy_to_another(class_name)
    print("The end of changing")


if __name__ == "__main__":
    main()
