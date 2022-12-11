import Main
from Main import Data
import next_element as ne
import os


class IteratorOfExemplar:
    """
        класс итератор - чтобы обойти элементы внутри объекта вашего собственного класса
    """

    def __init__(self, obj: type(Data), pointer: str):
        self.obj = obj
        self.pointer = pointer
        self.counter = 0
