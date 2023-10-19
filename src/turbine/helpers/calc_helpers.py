import numpy as np

from turbine_input_data import data_calc as dc
from helpers.temp_helpers import TempHelpers as th

class CalcOperations:
    @staticmethod
    def turbine_input_pressure(tpr) -> float:
        p_comp_in = dc.P_INPUT #Pa 
        p_comp_out = tpr * p_comp_in
        p_1 = p_comp_out #baardzo proste założenie przemiany izobarycznej w komorze spalania, docelowo do zmiany
        return p_1 
    
    @staticmethod
    def find_cu2(turbine_assum: float, turbine_input: float) -> (float, float):
         u = th.find_tangential_velocity(turbine_assum)
         T_03 = turbine_input.T01/th.T2_T1_is(turbine_input.tpr, dc.KAPPA)
         D_T0 = T_03 - turbine_input.T01
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
    
    def find_inlet_density(self) -> float:
        p1 = self.turbine_input_pressure(dc.TPR)
        return p1/(dc.R_COMB*dc.T_01)
    
    #coś jest nie tak, promienie wychodzą na minusie
    def find_rtip_rhub_rmean(self, turbine_assum, turbine_input) -> (float, float, float):
        rho1 = self.find_inlet_density()
        u = th.find_tangential_velocity(turbine_assum)
        r_mean = th.find_mean_radious(u, turbine_input.omega)
        A = turbine_input.m_dot/(turbine_assum.cx*rho1)
        r_hub = A/(np.pi*4*r_mean) + r_mean
        r_tip = 2*r_mean - r_hub
        return r_tip, r_mean, r_hub
    
    def radious_list(self, turbine_assum, turbine_input) -> list:
        r_tip, r_mean, r_hub = self.find_rtip_rhub_rmean(turbine_assum, turbine_input)
        r_tip_p = r_tip / r_mean
        r_mean_p = r_mean / r_mean
        r_hub_p = r_hub / r_mean
        first = np.linspace(r_tip_p, r_mean_p, 3)
        second = np.linspace(r_mean_p, r_hub_p, 3)
        combined = np.concatenate((first, second[1:]))
        return combined.tolist()
    
