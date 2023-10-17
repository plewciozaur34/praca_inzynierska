import numpy as np
from . import surface_points as sp

class Polynomial:
    def __init__(self, d: float, c: float, b: float, a: float) -> None:
        self.d: float = d
        self.c: float = c
        self.b: float = b
        self.a: float = a
