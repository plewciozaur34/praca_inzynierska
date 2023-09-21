import numpy as np
from . import geometry_parameters as gep
from . import geo_dep_params as gdp
class GeometryDependentParametersCalculation:
    def __init__(self, geom_params: gep.GeometryParameters):
        self.gp = geom_params

    #czy ona tu powinna zostać, skoro jest w geometry_parameters? z termodynamicznego punktu widzenia
    def find_half_wedge_out(self) -> float: #first guess, trzeba go jeszcze wcześniej iterować? do doczytania w artykule
        return self.gp.ugt / 2
    
    def find_pitch(self) -> float:
        return (2 * np.pi * self.gp.R) / self.gp.Nb
    
    def find_stagger_angle(self) -> float:
        return np.arctan(self.gp.chord_t / self.gp.chord_x)
    
    #trzeba najpierw wyliczyć te trójkąty powierzchni appendix D
    def find_airfoil_csa (self) -> float: #cross sectional area
        return 0
    
    def find_chord (self) -> float:
        return np.sqrt(self.gp.chord_x**2 + self.gp.chord_t**2)
    
    def find_zweifel_coefficient (self) -> float: #INCOMPRESSIBLE ZWEIFEL LOADING COEFFICIENT 
        return ((4*np.pi*self.gp.R)/(self.gp.Nb*self.gp.chord_x))*np.sin(self.gp.beta_in-self.gp.beta_out)*(np.cos(self.gp.beta_in)/np.cos(self.gp.beta_out))
    
    def find_solidity (self) -> float: 
        return self.find_chord()/self.find_pitch()
    
    #trzeba najpierw ogarnąć airfoil_csa
    def find_xcg (self) -> float:
        return 0
    
    def find_ycg (self) -> float:
        return 0 

    def find_blockage_in (self) -> float:
        return (2*self.gp.Rle/(self.find_pitch()*np.cos(self.gp.beta_in)))*100
    
    def find_blockage_out (self) -> float:
        return (2*self.gp.Rte/(self.find_pitch()*np.cos(self.gp.beta_out)))*100
    
    def find_camber_angle (self) -> float:
        return self.gp.beta_in - self.gp.beta_out
    
    def find_lift_coefficient (self) -> float:
        return ((2*self.find_pitch())/self.find_chord()) * (np.cos(self.gp.beta_in) + np.cos(self.gp.beta_out)) * (np.tan(self.gp.beta_in) - np.tan(self.gp.beta_out))
    
    def find_geometry_dependent_parameters(self) -> gdp.GeometryDependentParameters:
        half_wedge_out = self.find_half_wedge_out()
        pitch = self.find_pitch()
        stagger_angle = self.find_stagger_angle()
        airfoil_csa = self.find_airfoil_csa()
        chord = self.find_chord()
        zweifel_coefficient = self.find_zweifel_coefficient()
        solidity = self.find_solidity()
        xcg = self.find_xcg()
        ycg = self.find_ycg()
        blockage_in = self.find_blockage_in()
        blockage_out = self.find_blockage_out()
        camber_angle = self.find_camber_angle()
        lift_coefficient = self.find_lift_coefficient()
        return gdp.GeometryDependentParameters(half_wedge_out, pitch, stagger_angle, airfoil_csa, chord, zweifel_coefficient, solidity, xcg, ycg, blockage_in, blockage_out, camber_angle, lift_coefficient)

        

    