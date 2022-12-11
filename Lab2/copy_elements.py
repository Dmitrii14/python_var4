import os
import shutil
import Main
from Main import Data


def make_dir(obj: type(Data)) -> None:
    try:
        os.mkdir("new_dataset")
        obj.dir_name = "new_dataset"
    except OSError:
        shutil.rmtree("new_dataset")
        os.mkdir("new_dataset")
        obj.dir_name = "new_dataset"


def teleport_dir(obj: type(Data), path: str, class_name: str) -> None:
    later_dir = obj.dir_name
    make_dir(obj)
    for i in range(1000):
        os.rename(os.path.join(later_dir, class_name, f'{(i+1):04d}.jpg'),
                  os.path.join(later_dir, class_name, f'{class_name}_{(i+1):04d}.jpg'))
        shutil.copy(os.path.join(later_dir, class_name, f'{class_name}_{(i+1):04d}.jpg'), obj.dir_name)
        os.rename(os.path.join(later_dir, class_name, f"{class_name}_{(i+1):04d}.jpg"),
                  os.path.join(later_dir, class_name, f'{(i+1):04d}.jpg'))
        obj.add(os.path.join(path, obj.dir_name, class_name), class_name, f'{class_name}_{(i+1):04d}.jpg')


if __name__ == "__main__":
    teleport_dir(Data("dataset"), "C:\Users\User\Documents\GitHub\python_var4\Lab2", Main.CLASS_DEFAULT[0])