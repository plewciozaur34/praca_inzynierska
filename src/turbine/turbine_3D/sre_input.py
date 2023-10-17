import numpy as np

import sre_output as sre_out

class SimRadEqiInput:
    def __init__(self, phi_mean: float = 0, psi_mean: float = 0, Rn_mean: float = 0,
                  Rnp_hub: float = 0, rp_list: list = [], rp_hub: float = 0) -> None:
        self.phi_mean: float = phi_mean
        self.psi_mean: float = psi_mean
        self.Rn_mean: float = Rn_mean
        self.Rnp_hub: float = Rnp_hub
        self.rp_list: list = rp_list
        self.rp_hub: float = rp_hub

    def simple_radial_equi(self) -> sre_out.SimRadEqiOutput:
        a_p = 1- self.Rn_mean
        b_p = -self.psi_mean/2
        #Rnp_hub = 1-a_p*(rp_hub)**(n-1)
        n = np.log((1-self.Rnp_hub)/a_p)/np.log(self.rp_hub) + 1
        print(f"n={round(n,2)}")
        for r_p in self.rp_list:
            z1 = 1+((n+1)/n)*(((1-self.Rn_m)/self.phi_mean)**2)*((1-r_p**(2*n))+(n/(n-1))*(self.psi_mean/(1-self.Rn_mean))*(1-r_p**(n-1)))
            z2 = 1+((n+1)/n)*(((1-self.Rn_m)/self.phi_mean)**2)*((1-r_p**(2*n))-(n/(n-1))*(self.psi_mean/(1-self.Rn_mean))*(1-r_p**(n-1)))
            Rn_prim = 1-a_p*(r_p)**(n-1)
            Rn = 1+(1-self.Rn_m)*((2*r_p**(n-1)-n-1)/(n-1))
            Cp_x1 = np.sqrt(z1)*self.phi_mean
            Cp_x2 = np.sqrt(z2)*self.phi_mean
            Cp_u1 = a_p*r_p**n - b_p/r_p
            Cp_u2 = a_p*r_p**n + b_p/r_p

        #tzreba to pozamieniać na jakieś listy czy coś takiego bo będzie po kilka wartości, a;e 
        #w taki sposób, żeby łatwo się zapisało do macierzy (dataframe, 2D_array???)

        return sre_out.SimRadEqiOutput(r_p, Cp_x1, Cp_x2, Cp_u1, Cp_u2, Rn_prim, Rn)
           
            
       