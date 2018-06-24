from cube_utils import *
from random import uniform, randint

class Generator:
    """Genarator Base Class"""
    def __init__(self):
        self.controlArg_1 = 0
        self.controlArg_2 = 0
        self.controlArg_3 = 0

    def control(arg1, arg2, arg3):
        self.controlArg_1 = arg1
        self.controlArg_2 = arg2
        self.controlArg_3 = arg3

    def generate(world, step):
        return world
