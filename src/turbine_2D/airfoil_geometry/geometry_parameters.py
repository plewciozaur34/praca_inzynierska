import numpy as np
from . import point as p
from . import circle as c
from . import polynomial as poly

class GeometryParameters:
    def __init__(self, R: float = 0, chord_x: float =0 , chord_t: float = 0 , ugt: float = 0, beta_in: float = 0, 
                 half_wedge_in: float = 0, Rle: float = 0, beta_out: float = 0, Rte: float = 0, Nb: float = 0, throat: float = 0) -> None:
        self.R: float = R
        self.chord_x: float = chord_x
        self.chord_t: float = chord_t
        self.ugt: float = ugt
        self.beta_in: float = beta_in
        self.half_wedge_in: float = half_wedge_in
        self.Rle: float = Rle
        self.beta_out: float = beta_out
        self.Rte: float = Rte
        self.Nb: float = Nb
        self.throat: float = throat

    def get_data(self, geo_data, index_name):
        attributes = ['R','chord_x','chord_t','ugt','beta_in','half_wedge_in','Rle','beta_out','Rte',
            'Nb','throat']

        for attribute in attributes:
            setattr(self, attribute, geo_data[attribute][index_name])

    def find_half_wedge_out(self) -> float: #first guess, trzeba go jeszcze wcześniej iterować? do doczytania w artykule
        return self.ugt/2 
    
    def find_suction_surface_trailing_edge_tangency_point (self) -> p.Point:
        b1 = self.beta_out - self.find_half_wedge_out()
        x1 = self.chord_x - self.Rte * (1+np.sin(b1))
        y1 = self.Rte * np.cos(b1)
            
        return p.Point(b1, x1, y1)
    
    def find_suction_surface_throat_point (self) -> p.Point:
        b2 = self.beta_out - self.find_half_wedge_out() + self.ugt
        x2 = self.chord_x - self.Rte + (self.throat + self.Rte) * np.sin(b2)
        y2 = ((2*np.pi*self.R) / self.Nb) - (self.throat + self.Rte) * np.cos(b2)
        
        return p.Point(b2, x2, y2)
    
    def find_suction_surface_leading_edge_tangency_point (self) -> p.Point:
        b3 = self.beta_in + self.half_wedge_in
        x3 = self.Rle*(1-np.sin(b3))
        y3 = self.chord_t + self.Rle*np.cos(b3)
        
        return p.Point(b3, x3, y3)
    
    def find_pressure_surface_leading_edge_tangency_point (self) -> p.Point:
        b4 = self.beta_in - self.half_wedge_in
        x4 = self.Rle*(1+np.sin(b4))
        y4 = self.chord_t - self.Rle*np.cos(b4)
        
        return p.Point(b4, x4, y4)
    
    def find_pressure_surface_trailing_edge_tangency_point (self) -> p.Point:
        b5 = self.beta_out + self.find_half_wedge_out()
        x5 = self.chord_x - self.Rte * (1-np.sin(b5))
        y5 = -self.Rte * np.cos(b5)

        return p.Point(b5, x5, y5)
    
    @staticmethod
    def circle(x_a: float, x_b: float, y_a: float, b_a: float, b_b: float) -> c.Circle:
        r = (x_b - x_a) / (np.sin(b_b) + np.sin(b_a))
        x_0 = x_a - r * np.sin(b_a)
        y_0 = y_a + r * np.cos(b_a)

        return c.Circle(x_0, y_0, r)
    
    @staticmethod
    def polynomial(x_a: float, x_b: float, y_a: float, y_b: float, b_a: float, b_b: float) -> poly.Polynomial:
        d = ((np.tan(b_a) + np.tan(b_b)) / (x_a - x_b)**2) - ((2 * (y_a - y_b)) / (x_a - x_b)**3)
        c = ((y_a - y_b) / (x_a - x_b)**2) - (np.tan(b_b) / (x_a - x_b)) - (d * (x_a + 2 * x_b))
        b = np.tan(b_b) - 2 * c * x_b - 3 * d * x_b**2
        a = y_b - b * x_b - c * x_b**2 - d * x_b**3

        return poly.Polynomial(a, b, c, d)
        


        
        
    
    
    
    
   
