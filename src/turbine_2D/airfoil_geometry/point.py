import numpy as np

from . import polynomial as poly
from . import circle as cir
class Point:
    def __init__(self, b: float, x: float, y: float) -> None:
        self.b: float = b
        self.x: float = x
        self.y: float = y

    def polynomial(self, second_point: 'Point') -> poly.Polynomial:
        d = ((np.tan(self.b) + np.tan(second_point.b)) / (self.x - second_point.x)**2) 
        - ((2 * (self.y - second_point.y)) / (self.x - second_point.x)**3)
        c = ((self.y - second_point.y) / (self.x - second_point.x)**2) - (np.tan(second_point.b) / (self.x - second_point.x)) - (d * (self.x + 2 * second_point.x))
        b = np.tan(second_point.b) - 2 * c * second_point.x - 3 * d * second_point.x**2
        a = second_point.y - b * second_point.x - c * second_point.x**2 - d * second_point.x**3

        return poly.Polynomial(a, b, c, d)
    
    def circle(self, second_point: 'Point') -> cir.Circle:
        r = (second_point.x - self.x) / (np.sin(second_point.b) + np.sin(self.b))
        x_0 = self.x - r * np.sin(self.b)
        y_0 = self.y + r * np.cos(self.b)

        return cir.Circle(x_0, y_0, r)
    
    def bezier(self, second_point: 'Point'):    
        return 0