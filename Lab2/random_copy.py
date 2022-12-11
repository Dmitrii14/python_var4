import os
import random
import shutil
import copy_elements as ce
import main
from main import Data


def create_copy_dataset_with_random_number(obj: type(Data), path: str, class_name: str) -> None:
    later_dir = obj.dir_name
    ce.make_dir(obj)

    for i in range(1000):
        n = random.randint(0, 10000)
        os.rename(os.path.join(later_dir, class_name, f'{(i+1):04d}.jpg'),
                  os.path.join(later_dir, class_name, f'{n:05d}.jpg'))
        shutil.copy(os.path.join(later_dir, class_name, f'{n:05d}.jpg'), obj.dir_name)
        os.rename(os.path.join(later_dir, class_name, f"{n:05d}.jpg"),
                  os.path.join(later_dir, class_name, f'{(i+1):04d}.jpg'))
        obj.add(os.path.join(path, obj.dir_name, class_name), class_name, f'{n:05d}.jpg')


if __name__ == "__main__":
    create_copy_dataset_with_random_number(Data("dataset"), "C:\Users\User\Documents\GitHub\python_var4\Lab2",
                                           main.CLASS_DEFAULT[0])
