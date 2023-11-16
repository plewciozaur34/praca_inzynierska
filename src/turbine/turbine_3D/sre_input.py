import numpy as np
import pandas as pd

from helpers.calc_helpers import CalcOperations as co
class SimRadEquiInput:
    def __init__(self, phi_mean: float = 0, psi_mean: float = 0, Rn_mean: float = 0,
                  Rnp_hub: float = 0, rp_hub: float = 0) -> None:
        self.phi_mean: float = phi_mean #współczynnik przepływu dla średniego promienia
        self.psi_mean: float = psi_mean #współczynnik pracy dla średniego promienia 
        self.Rn_mean: float = Rn_mean #reakcyjność
        self.Rnp_hub: float = Rnp_hub #reakcyjność_prim przy piaście (hub)
        self.rp_hub: float = rp_hub #promień_prim przy piaście (hub)

    def get_data(self, sre_data):
        attributes = ['phi_mean', 'psi_mean', 'Rn_mean', 'Rnp_hub', 'rp_hub']
        for attribute in attributes:
            setattr(self, attribute, sre_data[attribute])

    def print_attributes(self):
        for attr, value in self.__dict__.items():
            print(f"{attr}: {value}")
    
    #TODO: wzór na Rnp_hub?? czy po prostu zakładamy wartość?
    def calculate_data(self, turbine_assum, turbine_input) -> 'SimRadEquiInput':
        self.phi_mean = turbine_assum.phi
        r_tip, r_mean, r_hub = co.find_rtip_rhub_rmean(turbine_assum, turbine_input)
        self.rp_hub = r_hub/r_mean
        self.psi_mean = co.find_psi_mean(turbine_assum, turbine_input)
        self.Rn_mean = co.find_reaction_mean(turbine_assum, turbine_input)
        self.Rnp_hub = 0.25
 
    def simple_radial_equi(self, rp_list, turbine_assum) -> pd.DataFrame:
        radious_df = pd.DataFrame({'r_p':[],'C_x1':[], 'C_x2':[], 'C_u1':[], 'C_u2':[], 'Rn_prim':[], 'Rn':[]})
        u_mean = co.find_tangential_velocity(turbine_assum)
        a_p = 1- self.Rn_mean
        b_p = -self.psi_mean/2
        n = np.log((1-self.Rnp_hub)/a_p)/np.log(self.rp_hub) + 1
        for r_p in rp_list:
            z1 = 1+((n+1)/n)*(((1-self.Rn_mean)/self.phi_mean)**2)*((1-r_p**(2*n))+(n/(n-1))*(self.psi_mean/(1-self.Rn_mean))*(1-r_p**(n-1)))
            z2 = 1+((n+1)/n)*(((1-self.Rn_mean)/self.phi_mean)**2)*((1-r_p**(2*n))-(n/(n-1))*(self.psi_mean/(1-self.Rn_mean))*(1-r_p**(n-1)))
            Rn_prim = 1-a_p*(r_p)**(n-1)
            Rn = 1+(1-self.Rn_mean)*((2*r_p**(n-1)-n-1)/(n-1))
            Cp_x1 = np.sqrt(z1)*self.phi_mean
            C_x1 = Cp_x1*u_mean
            Cp_x2 = np.sqrt(z2)*self.phi_mean
            C_x2 = Cp_x2*u_mean
            Cp_u1 = a_p*r_p**n - b_p/r_p
            C_u1 = Cp_u1*u_mean
            Cp_u2 = a_p*r_p**n + b_p/r_p
            C_u2 = Cp_u2*u_mean
            rad_data = pd.DataFrame({'r_p':[r_p],'C_x1':[C_x1], 'C_x2':[C_x2], 'C_u1':[C_u1], 'C_u2':[C_u2], 'Rn_prim':[Rn_prim], 'Rn':[Rn]})
            radious_df = pd.concat([radious_df, rad_data])

        return radious_df
            
       