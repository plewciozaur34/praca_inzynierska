import numpy as np

from turbine_2D.airfoil_geometry.point import Point

class GeometryParameters:
    def __init__(self, R: float, chord_x: float, chord_t: float, ugt: float, beta_in: float, half_wedge_in: float,
                  Rle: float, beta_out: float, Rte: float, Nb: float, throat: float) -> None:
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


    def find_half_wedge_out(self) -> float:
        return self.ugt/2
    
    def find_pitch(self) -> float:
        return (2*np.pi*self.R)/self.Nb
    
    def find_stagger_angle(self) -> float:
        return np.arctan(self.chord_t/self.chord_x)
    
    #trzeba najpierw wyliczyć te trójkąty powierzchni appendix D
    def find_airfoil_csa (self) -> float: #cross sectional area
        return 0
    
    def find_chord (self) -> float:
        return np.sqrt(self.chord_x**2 + self.chord_t**2)
    
    def find_zweifel_coefficient (self) -> float: #INCOMPRESSIBLE ZWEIFEL LOADING COEFFICIENT 
        return ((4*np.pi*self.R)/(self.Nb*self.chord_x))*np.sin(self.beta_in-self.beta_out)*(np.cos(self.beta_in)/np.cos(self.beta_out))
    
    def find_solidity (self) -> float: 
        return self.find_chord()/self.find_pitch()
    
    # def find_xcg / ycg #trzeba najpierw ogarnąć airfoil_csa

    def find_blockage_in (self) -> float:
        return (2*self.Rle/(self.find_pitch()*np.cos(self.beta_in)))*100
    
    def find_blockage_out (self) -> float:
        return (2*self.Rte/(self.find_pitch()*np.cos(self.beta_out)))*100
    
    def find_camber_angle (self) -> float:
        return self.beta_in - self.beta_out
    
    def find_lift_coefficient (self) -> float:
        return ((2*self.find_pitch())/self.find_chord()) * (np.cos(self.beta_in) + np.cos(self.beta_out)) * (np.tan(self.beta_in) - np.tan(self.beta_out))
    
    def find_suction_surface_trailing_edge_tangency_point (self) -> Point:
            b1 = self.beta_out - self.half_wedge_in
            x1 = self.chord_x - self.Rte * (1+np.sin(b1))
            y1 = self.Rte * np.cos(b1)
            
            return Point(b1, x1, y1)
    
