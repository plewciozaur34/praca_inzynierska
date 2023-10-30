import numpy as np

from . import data_calc as dc 
from helpers.temp_helpers import TempHelpers as th

class CalcOperations:
    @staticmethod
    def turbine_input_pressure(tpr) -> float:
        p_comp_in = dc.P_INPUT #Pa 
        p_comp_out = tpr * p_comp_in
        p_1 = p_comp_out #FIXME baardzo proste założenie przemiany izobarycznej w komorze spalania, docelowo do zmiany
        return p_1 
    
    @staticmethod
    def area_calc(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float):
        return np.abs(x1 * y2 + y1 * x3 + y3 * x2 - y2 * x3 - y1 * x2 - x1 * y3)/2

    @staticmethod
    def find_tangential_velocity(turbine_assum) -> float:
        return turbine_assum.cx/turbine_assum.phi
    
    @staticmethod
    def find_work_temperature(turbine_input) -> float:
         T_03 = turbine_input.T01/th.T2_T1_is(turbine_input.tpr, dc.KAPPA)
         D_T0 = T_03 - turbine_input.T01
    #FIXME podział tmeperatury na stopnie ze względu na podział TPR na stopnie - znaleźć w literaturze
         d_T0 = D_T0/6 #2HP+4LP, ale trzeba znaleźć ten podział procentowy na stopnie
         d_T0_prim=-120 #z danych literatrowych, 120 to tak typowo, ale i 150K tam widziałam chyba
         return dc.CP*d_T0
    
    def find_cu2(turbine_assum, turbine_input) -> (float, float):
         u = CalcOperations.find_tangential_velocity(turbine_assum)
         l = CalcOperations.find_work_temperature(turbine_input)
         d_c = l/u
         c_u3=0
         c_u2=c_u3-d_c
         return c_u2, c_u3
    
    #TODO napisać funkcję zwracającą wartości ciśnienia p2, brak pewności co do p3
    #(czy tu na pewno powinny być statyczne z tego TPR?)
    @staticmethod
    def find_pressure() -> float:
        p_1 = CalcOperations.turbine_input_pressure(dc.TPR)
        p_2 = 0
        p_3 = p_1 / dc.TPR
        return p_2, p_3
    
    @staticmethod
    def find_temperature(turbine_input, turbine_assum) -> float:
        c_x = turbine_assum.cx
        c_u2, c_u3 = CalcOperations.find_cu2(turbine_assum, turbine_input)
        c_2 = np.sqrt(c_x**2 + c_u2**2)
        c_3 = np.sqrt(c_x**2 + c_u3**2)
        T_03 = turbine_input.T01/th.T2_T1_is(turbine_input.tpr, dc.KAPPA)
        T_3 = T_03 - (c_3**2)/(2*dc.CP)
        T_02 = turbine_input.T01
        T_2 = T_02 - (c_2**2)/(2*dc.CP)
        return T_2, T_3
    
    @staticmethod
    def find_inlet_density() -> float:
        p1 = CalcOperations.turbine_input_pressure(dc.TPR)
        return p1/(dc.R_COMB*dc.T_01)
    
    @staticmethod
    def find_mean_radious(u: float, omega: float) -> float:
        return u/th.rpm_to_rad_s(omega)
    
    def find_rtip_rhub_rmean(turbine_assum, turbine_input) -> (float, float, float):
        rho1 = CalcOperations.find_inlet_density()
        u = CalcOperations.find_tangential_velocity(turbine_assum)
        r_mean = CalcOperations.find_mean_radious(u, turbine_input.omega)
        A = turbine_input.m_dot/(turbine_assum.cx*rho1)
        r_tip = A/(np.pi*4*r_mean) + r_mean
        r_hub = 2*r_mean - r_tip
        return r_tip, r_mean, r_hub
    
    @staticmethod
    def radious_prim_list(turbine_assum, turbine_input) -> list:
        r_tip, r_mean, r_hub = CalcOperations.find_rtip_rhub_rmean(turbine_assum, turbine_input)
        r_tip_p = r_tip / r_mean
        r_mean_p = r_mean / r_mean
        r_hub_p = r_hub / r_mean
        first = np.linspace(r_hub_p, r_mean_p, 3)
        second = np.linspace(r_mean_p, r_tip_p, 3)
        combined = np.concatenate((first, second[1:]))
        return combined.tolist()
    
    @staticmethod
    def radious_list(radious_instance_df, turbine_assum, turbine_input) -> list:
        r_tip, r_mean, r_hub = CalcOperations.find_rtip_rhub_rmean(turbine_assum, turbine_input)
        radious_list = list(np.zeros(5))
        for idx in range(5):
            radious_list[idx] = radious_instance_df[idx].r_p * r_mean
        return radious_list
    
    @staticmethod
    def find_psi_mean(turbine_assum, turbine_input) -> float:
        return abs(CalcOperations.find_work_temperature(turbine_input))/CalcOperations.find_tangential_velocity(turbine_assum)**2
    
    @staticmethod
    def find_reaction_mean(turbine_assum, turbine_input) -> float:
        c_u2, c_u3 = CalcOperations.find_cu2(turbine_assum, turbine_input)
        return 1 - (c_u2 + c_u3)/(2*CalcOperations.find_tangential_velocity(turbine_assum))

