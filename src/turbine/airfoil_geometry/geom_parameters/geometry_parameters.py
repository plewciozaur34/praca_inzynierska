import numpy as np
import sys

from . import point as p
from . import point_no_beta as pnb
from . import throat_dicontinuity as td
from helpers.temp_helpers import TempHelpers as th

class GeometryParameters:
    def __init__(self, R: float = 0, chord_x: float =0 , chord_t: float = 0 , ugt: float = 0, beta_in: float = 0, 
                 half_wedge_in: float = 0, Rle: float = 0, beta_out: float = 0, Rte: float = 0, Nb: float = 0,
                throat: float = 0, half_wedge_out: float = 0) -> None:
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
        self.half_wedge_out: float = half_wedge_out

    def get_data(self, geo_data, index_name):
        attributes = ['R','chord_x','chord_t','ugt','beta_in','half_wedge_in','Rle','beta_out','Rte',
            'Nb','throat', 'half_wedge_out']
        for attribute in attributes:
            setattr(self, attribute, geo_data[attribute][index_name])

    def print_attributes(self):
        for attr, value in self.__dict__.items():
            print(f"{attr}: {value}")
    
    def def_values(self):
        if self.Rle >= 2:
            self.Rle = (self.Rle/100) * 2 * np.pi * (self.R / self.Nb) * np.cos(self.beta_in * np.pi / 180) / 2 
        if self.Rte >= 2:
            self.Rte = (self.Rte/100) * 2 * np.pi * (self.R / self.Nb) * np.cos(self.beta_out * np.pi / 180) / 2 
        if self.chord_x <= 0:
            self.chord_x = 4 * np.pi * self.R / self.Nb * np.sin((self.beta_in - self.beta_out) * np.pi / 180)
        if self.throat <= 0:
            self.throat = 2* np.pi * self.R / self.Nb * np.cos(self.beta_out * np.pi / 180) - 2 * self.Rte
        if self.ugt <= 0:
            self.ugt = 0.0001
        self.half_wedge_out = self.ugt/2
        if self.chord_t < 20:
#FIXME te założenia do chord_t tzreba poprawić - uwzględnić część kodu z fortrana, który jest w komentarzu
            #IF<CT.GE.4.l ITER=.TRUE.
            #IF<CT .GE.4.1 TTC=CT/100.
            if self.chord_t >= 4: 
                self.chord_t = 0
        else:
            self.chord_t = self.chord_x * np.tan(self.chord_t * np.pi / 180)

    def remove_throat_discontinuity(self, count=[0]) -> 'td.RemoveThroatDiscontinuity':
        count[0] += 1

        point1 = self.find_suction_surface_trailing_edge_tangency_point()
        point2 = self.find_suction_surface_throat_point()
        point3 = self.find_suction_surface_leading_edge_tangency_point()
        point4 = self.find_pressure_surface_leading_edge_tangency_point()
        point5 = self.find_pressure_surface_trailing_edge_tangency_point()
        point0 = point1.circle(point2) 

        yy2 = point0.y + np.sqrt(point0.r**2 - (point2.x - point0.x)**2)
        if np.abs(point2.y - yy2) < 0.00001:
            print('Throat discontinuity removed.')
            pressure_surf = point4.polynomial(point5)
            suction_surf = point2.polynomial(point3)
            return td.RemoveThroatDiscontinuity(pressure_surf, suction_surf, point0, point1, point2, point3, point4, point5)
        
        self.half_wedge_out = self.half_wedge_out * (point2.y / yy2)**4
        print(f"half wegde out={self.half_wedge_out}")
        if self.half_wedge_out > 0.001:
            print('Throat discontinuity NOT removed, calculating points again.')
            return self.remove_throat_discontinuity()
            
        print("THE EXIT WEDGE ANGLE ITERATION FAILED. THE EXIT WEDGE ANGLE WANTS TO GO NEGATIVE. REDUCE THE EXIT BLADE ANGLE OR DECREASE THE THROAT.")
        print(f"Remove throat discontinuity was iterated {self.remove_throat_discontinuity.__defaults__[0][0]} times.")
        sys.exit()
    
    def find_suction_surface_trailing_edge_tangency_point (self) -> p.Point:
        b1 = self.beta_out - self.half_wedge_out
        x1 = self.chord_x - self.Rte * (1 + np.sin(th.rad(b1)))
        y1 = self.Rte * np.cos(th.rad(b1))
            
        return p.Point(b1, x1, y1)
    
    def find_suction_surface_throat_point (self) -> p.Point:
        b2 = self.beta_out - self.half_wedge_out + self.ugt
        x2 = self.chord_x - self.Rte + (self.throat + self.Rte) * np.sin(th.rad(b2))
        y2 = ((2 * np.pi * self.R) / self.Nb) - (self.throat + self.Rte) * np.cos(th.rad(b2))
        
        return p.Point(b2, x2, y2)
    
    def find_suction_surface_leading_edge_tangency_point (self) -> p.Point:
        b3 = self.beta_in + self.half_wedge_in
        x3 = self.Rle * (1 - np.sin(th.rad(b3)))
        y3 = self.chord_t + self.Rle * np.cos(th.rad(b3))
        
        return p.Point(b3, x3, y3)
    
    def find_pressure_surface_leading_edge_tangency_point (self) -> p.Point:
        b4 = self.beta_in - self.half_wedge_in
        x4 = self.Rle * (1 + np.sin(th.rad(b4)))
        y4 = self.chord_t - self.Rle * np.cos(th.rad(b4))
        
        return p.Point(b4, x4, y4)
    
    def find_pressure_surface_trailing_edge_tangency_point (self) -> p.Point:
        b5 = self.beta_out + self.half_wedge_out
        x5 = self.chord_x - self.Rte * (1 - np.sin(th.rad(b5)))
        y5 = - self.Rte * np.cos(th.rad(b5))

        return p.Point(b5, x5, y5)

    def find_points_six_seven_eight_nine(self) -> pnb.PointNoBeta:
        x6 = self.chord_x
        y6 = 0
        x7 = self.chord_x - self.Rte
        y7 = 0
        x8 = 0
        y8 = self.chord_t
        x9 = self.Rle
        y9 = self.chord_t

        return pnb.PointNoBeta(x6, y6), pnb.PointNoBeta(x7, y7), pnb.PointNoBeta(x8, y8), pnb.PointNoBeta(x9, y9)
    
    
        


        
        
    
    
    
    
   
