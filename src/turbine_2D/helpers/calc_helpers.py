from turbine_input_data import data_calc as dc
from turbine_input_data import turbine_input as turbine_input
from helpers.temp_helpers import TempHelpers as th

class CalcOperations:
    @staticmethod
    def turbine_input_pressure(tpr) -> float:
        p_comp_in = dc.P_INPUT #Pa 
        p_comp_out = tpr * p_comp_in
        p_1 = p_comp_out #baardzo proste założenie przemiany izobarycznej w komorze spalania, docelowo do zmiany
        return p_1 
    
    @staticmethod
    def find_cu2(cx: float, phi: float, tpr: float, T01: float) -> (float, float):
         u=cx/phi
         T_03 = T01/th.T2_T1_is(tpr, dc.KAPPA)
         D_T0 = T_03 - T01
         d_T0 = D_T0/6 #2HP+4LP, ale trzeba znaleźć ten podział procentowy na stopnie
         d_T0_prim=-120 #z danych literatrowych, 120 to tak typowo, ale i 150K tam widziałam chyba
         l=dc.CP*d_T0 
         d_c = l/u
         c_u3=0
         c_u2=c_u3-d_c
         return c_u2, c_u3
    
    @staticmethod
    def find_pressure() -> float:
        return 0
    
    @staticmethod
    def find_temperature() -> float:
        return 0
    
