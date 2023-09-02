import numpy as np
import pandas as pd
phi_m = 0.4 #współczynnik przepływu dla średniego promienia (?)
psi_m = -0.25 #współczynnik pracy dla średniego promienia 
Rn_m = 0.5 #reakcyjność
Rnp_hub = 0.25 #reakcyjność_prim przy piaście (hub)
rp_hub = 0.75 #promień_prim przy piaście (hub)
rp_list = [0.75, 0.8, 0.9, 1.0, 1.1, 1.25] #rozkład promieni_prim (do rozbudowania)

def main():
    def simple_radial_equi(phi_m, psi_m, Rn_m, Rnp_hub, rp_list, rp_hub):
        rad_eqi = pd.DataFrame({'r_p':[],'Cp_x1':[], 'Cp_x2':[], 'Cp_u1':[], 'Cp_u2':[], 'Rn_prim':[], 'Rn':[]})
        a_p = 1- Rn_m 
        b_p = -psi_m/2
        #Rnp_hub = 1-a_p*(rp_hub)**(n-1)
        n = np.log((1-Rnp_hub)/a_p)/np.log(rp_hub) + 1
        print(f"n={round(n,2)}")
        for r_p in rp_list:
            z1 = 1+((n+1)/n)*(((1-Rn_m)/phi_m)**2)*((1-r_p**(2*n))+(n/(n-1))*(psi_m/(1-Rn_m))*(1-r_p**(n-1)))
            z2 = 1+((n+1)/n)*(((1-Rn_m)/phi_m)**2)*((1-r_p**(2*n))-(n/(n-1))*(psi_m/(1-Rn_m))*(1-r_p**(n-1)))
            Rn_prim = 1-a_p*(r_p)**(n-1)
            Rn = 1+(1-Rn_m)*((2*r_p**(n-1)-n-1)/(n-1))
            Cp_x1 = np.sqrt(z1)*phi_m
            Cp_x2 = np.sqrt(z2)*phi_m
            Cp_u1 = a_p*r_p**n - b_p/r_p
            Cp_u2 = a_p*r_p**n + b_p/r_p
            rad_data = pd.DataFrame({'r_p':[round(r_p,2)],'Cp_x1':[round(Cp_x1,3)], 'Cp_x2':[round(Cp_x2,3)], 'Cp_u1':[round(Cp_u1,3)], 'Cp_u2':[round(Cp_u2,3)], 'Rn_prim':[round(Rn_prim,3)], 'Rn':[round(Rn,3)]})
            rad_eqi = pd.concat([rad_eqi, rad_data])
        rad_eqi.set_index('r_p', inplace=True)
        print(rad_eqi)
        #print(rad_eqi['Cp_x1'])

        rad_eqi.to_csv('./praca_inzynierska/data/simple_radial_equilibrium.csv')
            
    simple_radial_equi(phi_m, psi_m, Rn_m, Rnp_hub, rp_list, rp_hub)

main()