import numpy as np
import pandas as pd

from combustion_params import fuel_parameters as fp
from helpers.temp_helpers import TempHelpers as th
from turbine_input_data import vector_of_state
from turbine_input_data import turbine_input as ti
from turbine_input_data import turbine_assum as ta
from turbine_input_data import data_calc as dc
from turbine_input_data.calc_operations import CalcOperations as co

#ogólna idea: na początek wyliczamy wektor stanu dla statora i wirnika i korzystając z niego wyliczamy inne 
#parametry, które będą nam potrzebne
kappa = fp.CombustionHelpers.find_kappa_combust()
cp = fp.CombustionHelpers.find_cp_combust()
R = fp.CombustionHelpers.find_R_combust()

#WEKTOR STANU: [c_axial, c_radial, c_u, p, T, r]
WS_stator = vector_of_state.VectorOfState()
WS_rotor = vector_of_state.VectorOfState()

#crusing altitude = 10,700 m #silnik GE CF6, samolot A300
#temp=-54.3 C; p=23800 Pa; M=0.78
T_01 = th.celsius_to_kelvin(dc.TIT_celsius) #K
M_1 = dc.M_1

#turbine_input = [m_dot [kg/s], p01 [Pa], T01 [K], tpr [-], eta_is [-], omega [rpm]] for LP
turbine_input = ti.TurbineInput(dc.M_DOT, 0, T_01, dc.TPR, dc.ETA_IS, dc.OMEGA)

turbine_input.p01 = co.turbine_input_pressure() / th.p_p0(M_1, kappa)

#0.5<phi<1.0
#c_x - na podstawie danych z examples z principles of turbomachinery...

#turbine_assum = [alfa1, alfa3, phi, c_x ..]
turbine_assum = ta.TurbineAssum(0,0,dc.PHI, dc.C_X)

def main():

    u=turbine_assum.cx/turbine_assum.phi

    T_03 = turbine_input.T01/th.T2_T1_is(turbine_input.tpr, kappa)

    D_T0 = T_03 - T_01
    #print("D_T0="+str(round(D_T0, 2)))
    d_T0 = D_T0/6 #2HP+4LP, ale trzeba znaleźć ten podział procentowy na stopnie
    
    d_T0_prim=-120 #z danych literatrowych, 120 to tak typowo, ale i 150K tam widziałam chyba
    l=cp*d_T0
    d_c = l/u
    c_u3=0
    c_u2=c_u3-d_c

    WS_stator.cu = c_u2
    WS_rotor.cu = c_u3
    WS_stator.cx = turbine_assum.cx
    WS_rotor.cx = turbine_assum.cx
    
    WS_rotor.mean_calc()
    WS_stator.mean_calc()
    
    return c_u2, c_u3
    
   
    

    #zapisac zewnetrzny plik z danymi do profilu

    # dane2 = pd.DataFrame({'beta':[round(beta_3,2), round(beta_2,2), round(beta_3, 2)]})
    # dane = pd.concat([dane, dane2])
    # dane.index = range(1,)
    

if __name__ == "__main__":
    main()