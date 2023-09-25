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
        x = ((self.y - second_point.y) * np.tan(self.b * np.pi / 180) * np.tan(second_point.b * np.pi /180) + 
             self.x * np.tan(second_point.b * np.pi /180) - second_point.x * np.tan(self.b * np.pi / 180))/(np.tan(second_point.b * np.pi /180)
            - np.tan(self.b * np.pi / 180))
        y = - (x - self.x) / np.tan(self.b * np.pi / 180) + self.y
        r = np.sqrt((self.x - x)**2 + (self.y - y)**2)

        return cir.Circle(x, y, r)
    
    def bezier(self, second_point: 'Point'):    
        return 0