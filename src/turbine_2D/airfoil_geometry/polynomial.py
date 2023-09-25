import numpy as np
from . import surface_points as sp

class Polynomial:
    def __init__(self, a: float, b: float, c: float, d: float) -> None:
        self.a: float = a
        self.b: float = b
        self.c: float = c
        self.d: float = d
