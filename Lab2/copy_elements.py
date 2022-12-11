import os
import shutil
import Main
from Main import Data
from typing import Type


def make_dir(obj: type(Data)) -> None:
    try:
        os.mkdir("new_dataset")
        obj.dir_name = "new_dataset"
    except OSError:
        shutil.rmtree("new_dataset")
        os.mkdir("new_dataset")
        obj.dir_name = "new_dataset"
