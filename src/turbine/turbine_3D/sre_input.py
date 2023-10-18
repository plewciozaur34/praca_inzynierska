import numpy as np
import pandas as pd

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
 
    def simple_radial_equi(self, rp_list) -> pd.DataFrame:
        radious_df = pd.DataFrame({'r_p':[],'Cp_x1':[], 'Cp_x2':[], 'Cp_u1':[], 'Cp_u2':[], 'Rn_prim':[], 'Rn':[]})
        a_p = 1- self.Rn_mean
        b_p = -self.psi_mean/2
        n = np.log((1-self.Rnp_hub)/a_p)/np.log(self.rp_hub) + 1
        for r_p in rp_list:
            z1 = 1+((n+1)/n)*(((1-self.Rn_mean)/self.phi_mean)**2)*((1-r_p**(2*n))+(n/(n-1))*(self.psi_mean/(1-self.Rn_mean))*(1-r_p**(n-1)))
            z2 = 1+((n+1)/n)*(((1-self.Rn_mean)/self.phi_mean)**2)*((1-r_p**(2*n))-(n/(n-1))*(self.psi_mean/(1-self.Rn_mean))*(1-r_p**(n-1)))
            Rn_prim = 1-a_p*(r_p)**(n-1)
            Rn = 1+(1-self.Rn_mean)*((2*r_p**(n-1)-n-1)/(n-1))
            Cp_x1 = np.sqrt(z1)*self.phi_mean
            Cp_x2 = np.sqrt(z2)*self.phi_mean
            Cp_u1 = a_p*r_p**n - b_p/r_p
            Cp_u2 = a_p*r_p**n + b_p/r_p
            rad_data = pd.DataFrame({'r_p':r_p,'Cp_x1':Cp_x1, 'Cp_x2':Cp_x2, 'Cp_u1':Cp_u1, 'Cp_u2':Cp_u2, 'Rn_prim':Rn_prim, 'Rn':Rn})
            radious_df = pd.concat([radious_df, rad_data])
        radious_df.set_index('r_p', inplace=True)

        return radious_df
            
       