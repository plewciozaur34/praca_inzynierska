import numpy as np

from . import polynomial as poly
from . import circle as cir
from helpers.temp_helpers import TempHelpers as th
 
class Point:
    def __init__(self, b: float, x: float, y: float) -> None:
        self.b: float = b
        self.x: float = x
        self.y: float = y

    def polynomial(self, second_point: 'Point') -> poly.Polynomial:
        d = ((np.tan(th.rad(self.b)) + np.tan(th.rad(second_point.b))) / ((second_point.x - self.x)**2))
        - ((2 * (self.y - second_point.y)) / (self.x - second_point.x)**3)
        c = ((self.y - second_point.y) / (self.x - second_point.x)**2) - (np.tan(th.rad(second_point.b)) / (self.x - second_point.x)) - (d * (self.x + 2 * second_point.x))
        b = np.tan(th.rad(second_point.b)) - 2 * c * second_point.x - 3 * d * second_point.x**2
        a = second_point.y - b * second_point.x - c * second_point.x**2 - d * second_point.x**3

        return poly.Polynomial(d, c, b, a)
    
    def circle(self, second_point: 'Point') -> cir.Circle:
        x = ((self.y - second_point.y) * np.tan(th.rad(self.b)) * np.tan(th.rad(second_point.b)) + 
             self.x * np.tan(th.rad(second_point.b)) - second_point.x * np.tan(th.rad(self.b)))/(np.tan(th.rad(second_point.b))
            - np.tan(th.rad(self.b)))
        y = - (x - self.x) / np.tan(th.rad(self.b)) + self.y
        r = np.sqrt((self.x - x)**2 + (self.y - y)**2)

        return cir.Circle(x, y, r)
