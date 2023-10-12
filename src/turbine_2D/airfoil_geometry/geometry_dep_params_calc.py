import numpy as np

from . import geometry_parameters as gep
from . import geo_dep_params as gdp
from helpers.temp_helpers import TempHelpers as th
class GeometryDependentParametersCalculation:
    def __init__(self, geom_params: gep.GeometryParameters):
        self.gp = geom_params
    
    def find_pitch(self) -> float:
        return (2 * np.pi * self.gp.R) / self.gp.Nb
    
    def find_stagger_angle(self) -> float:
        return th.deg(np.arctan(self.gp.chord_t / self.gp.chord_x))
    
    def find_chord (self) -> float:
        return np.sqrt(self.gp.chord_x**2 + self.gp.chord_t**2)
    
    def find_zweifel_coefficient (self) -> float: #INCOMPRESSIBLE ZWEIFEL LOADING COEFFICIENT 
        return ((4*np.pi*self.gp.R)/(self.gp.Nb*self.gp.chord_x))*np.sin(th.rad(self.gp.beta_in - self.gp.beta_out))*(np.cos(th.rad(self.gp.beta_out))/np.cos(th.rad(self.gp.beta_in)))
    
    def find_solidity (self) -> float: 
        return self.find_chord()/self.find_pitch()
    
    def find_blockage_in (self) -> float:
        return (2*self.gp.Rle/(self.find_pitch()*np.cos(th.rad(self.gp.beta_in))))*100
    
    def find_blockage_out (self) -> float:
        return (2*self.gp.Rte/(self.find_pitch()*np.cos(th.rad(self.gp.beta_out))))*100
    
    def find_camber_angle (self) -> float:
        return self.gp.beta_in - self.gp.beta_out
    
    def find_lift_coefficient (self) -> float:
        return ((self.find_pitch())/self.find_chord()) * (np.cos(th.rad(self.gp.beta_in)) + np.cos(th.rad(self.gp.beta_out))) * (np.tan(th.rad(self.gp.beta_in)) - np.tan(th.rad(self.gp.beta_out)))
    
    
    def find_geometry_dependent_parameters(self) -> gdp.GeometryDependentParameters:
        pitch = self.find_pitch()
        stagger_angle = self.find_stagger_angle()
        chord = self.find_chord()
        zweifel_coefficient = self.find_zweifel_coefficient()
        solidity = self.find_solidity()
        blockage_in = self.find_blockage_in()
        blockage_out = self.find_blockage_out()
        camber_angle = self.find_camber_angle()
        lift_coefficient = self.find_lift_coefficient()
        return gdp.GeometryDependentParameters(pitch, stagger_angle, chord, zweifel_coefficient, solidity, blockage_in, blockage_out, camber_angle, lift_coefficient)

        

    