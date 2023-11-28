import numpy as np

from initial_turbine_settings import data_calc as dc
from initial_turbine_settings import data_geom as dg
from helpers.temp_helpers import TempHelpers as th


class CalcOperations:
    @staticmethod
    def turbine_input_static_pressure() -> float:
        M_h = 0.8
        pi_WL = 0.992
        pi_s = 26.6
        pi_KS = 0.94
        kappa = 1.4
        p_h = 101325 * (1 - (dc.H / 44300)) ** (5.256)
        p1 = pi_WL * p_h * (1 + ((kappa - 1) / 2) * M_h**2) ** (kappa / (kappa - 1))
        p2 = p1 * pi_s
        p3 = p2 * pi_KS
        return p3

    @staticmethod
    def find_inlet_static_temp_and_velocity(
        turbine_input, turbine_assum
    ) -> (float, float):
        c_x3 = turbine_assum.cx
        c_x1 = c_x3 / np.cos(th.rad(turbine_assum.alfa3))
        c_1 = c_x1
        T_1 = turbine_input.T01 - (c_1**2) / (2 * dc.CP)
        T1_T01 = T_1 / turbine_input.T01
        return T_1, c_1

    def turbine_input_stagnation_pressure(turbine_input, turbine_assum) -> float:
        p_1 = CalcOperations.turbine_input_static_pressure()
        T_1, c_1 = CalcOperations.find_inlet_static_temp_and_velocity(
            turbine_input, turbine_assum
        )
        M_1 = c_1 / np.sqrt(dc.KAPPA * dc.R_COMB * T_1)
        p_01 = p_1 * th.p_p0(M_1, dc.KAPPA)
        return p_01

    @staticmethod
    def find_tangential_velocity(turbine_assum) -> float:
        return turbine_assum.cx / turbine_assum.phi

    @staticmethod
    def find_temperature_drop(turbine_input) -> float:
        T_03 = turbine_input.T01 / (
            dc.ETA_IS * th.T2_T1_is(turbine_input.tpr, dc.KAPPA)
        )
        D_T0 = T_03 - turbine_input.T01
        # FIXME podział tmeperatury na stopnie ze względu na podział TPR na stopnie - znaleźć w literaturze
        d_T0 = D_T0 / 6  # 2HP+4LP, ale trzeba znaleźć ten podział procentowy na stopnie
        d_T0_prim = (
            -120
        )  # z danych literatrowych, 120 to tak typowo, ale i 150K tam widziałam chyba
        return d_T0

    @staticmethod
    def find_work_temperature(turbine_input) -> float:
        d_T0 = CalcOperations.find_temperature_drop(turbine_input)
        return dc.CP * d_T0

    @staticmethod
    def find_T03_for_one_stage(turbine_input, turbine_assum) -> float:
        T_01 = turbine_input.T01
        d_T0 = CalcOperations.find_temperature_drop(turbine_input)
        T_03_stage = T_01 + d_T0
        return T_03_stage

    def find_cu2(turbine_assum, turbine_input) -> (float, float):
        u = CalcOperations.find_tangential_velocity(turbine_assum)
        l = CalcOperations.find_work_temperature(turbine_input)
        d_c = l / u
        c_u3 = 0
        c_u2 = c_u3 - d_c
        return c_u2, c_u3

    @staticmethod
    def find_pressure(turbine_input, turbine_assum) -> float:
        T_2, T_3 = CalcOperations.find_temperature(turbine_input, turbine_assum)
        c_x2 = turbine_assum.cx
        c_u2, c_u3 = CalcOperations.find_cu2(turbine_assum, turbine_input)
        c_2 = np.sqrt(c_x2**2 + c_u2**2)
        # T2_T2_prim = T2 - T2_prim
        T2_T2_prim = turbine_assum.lambda_n * (c_2**2) / (2 * dc.CP)
        T2_prim = T_2 - T2_T2_prim
        p_2 = CalcOperations.turbine_input_stagnation_pressure(
            turbine_input, turbine_assum
        ) / th.p2_p1_is(turbine_input.T01 / T2_prim, dc.KAPPA)
        p_01 = CalcOperations.turbine_input_stagnation_pressure(
            turbine_input, turbine_assum
        )
        # FIXME T3, p3 są dla jednego stopnia, ale w werji delta T0/6
        T_03_stage = CalcOperations.find_T03_for_one_stage(turbine_input, turbine_assum)
        PR_stage = th.p2_p1_is(turbine_input.T01 / T_03_stage, dc.KAPPA)
        p_03 = p_01 / PR_stage
        # T_03 = turbine_input.T01/(dc.ETA_IS * th.T2_T1_is(turbine_input.tpr, dc.KAPPA))
        p_3 = p_03 * th.p2_p1_is(T_3 / T_03_stage, dc.KAPPA)
        return p_2, p_3

    @staticmethod
    def find_temperature(turbine_input, turbine_assum) -> float:
        c_x = turbine_assum.cx
        c_u2, c_u3 = CalcOperations.find_cu2(turbine_assum, turbine_input)
        c_2 = np.sqrt(c_x**2 + c_u2**2)
        c_3 = np.sqrt(c_x**2 + c_u3**2)
        # FIXME T3, p3 T3, p3 są dla jednego stopnia, ale w werji delta T0/6
        # T_03 = turbine_input.T01/(dc.ETA_IS * th.T2_T1_is(turbine_input.tpr, dc.KAPPA))
        T_03_stage = CalcOperations.find_T03_for_one_stage(turbine_input, turbine_assum)
        T_3 = T_03_stage - (c_3**2) / (2 * dc.CP)
        T_02 = turbine_input.T01
        T_2 = T_02 - (c_2**2) / (2 * dc.CP)
        return T_2, T_3

    @staticmethod
    def find_rotor_density(turbine_input, turbine_assum, outlet) -> float:
        p_2, p_3 = CalcOperations.find_pressure(turbine_input, turbine_assum)
        T_2, T_3 = CalcOperations.find_temperature(turbine_input, turbine_assum)
        if outlet == True:
            return p_3 / (dc.R_COMB * T_3)
        return p_2 / (dc.R_COMB * T_2)

    @staticmethod
    def find_stator_inlet_density(turbine_input, turbine_assum) -> float:
        p_1 = CalcOperations.turbine_input_static_pressure()
        T_1, c_1 = CalcOperations.find_inlet_static_temp_and_velocity(
            turbine_input, turbine_assum
        )
        return p_1 / (dc.R_COMB * T_1)

    @staticmethod
    def find_mean_radious(u: float, omega: float) -> float:
        return u / th.rpm_to_rad_s(omega)

    def find_rtip_rhub_rmean(turbine_assum, turbine_input) -> (float, float, float):
        rho = CalcOperations.find_rotor_density(
            turbine_input, turbine_assum, outlet=False
        )
        u = CalcOperations.find_tangential_velocity(turbine_assum)
        # FIXME jak policzyć r_mean dla statora???????
        r_mean = CalcOperations.find_mean_radious(u, turbine_input.omega)
        A = turbine_input.m_dot / (turbine_assum.cx * rho)
        r_tip = A / (np.pi * 4 * r_mean) + r_mean
        r_hub = 2 * r_mean - r_tip
        return r_tip, r_mean, r_hub

    @staticmethod
    def is_rotor_rtip_change_needed(turbine_input, turbine_assum):
        rho3 = CalcOperations.find_rotor_density(
            turbine_input, turbine_assum, outlet=True
        )
        r_tip2, r_mean, r_hub = CalcOperations.find_rtip_rhub_rmean(
            turbine_assum, turbine_input
        )
        A3 = turbine_input.m_dot / (turbine_assum.cx * rho3)
        r_tip3 = np.sqrt((A3 / np.pi) + r_hub**2)
        return round((abs(r_tip3 - r_tip2) / r_tip2) * 100, 2)

    @staticmethod
    def radius_prim_list(turbine_assum, turbine_input) -> list:
        r_tip, r_mean, r_hub = CalcOperations.find_rtip_rhub_rmean(turbine_assum, turbine_input)
        r_tip_p = r_tip / r_mean
        r_mean_p = r_mean / r_mean
        r_hub_p = r_hub / r_mean
        number_of_radii = dg.N_RAD

        if number_of_radii % 2 == 0:
            number_of_radii += 1

        first = np.linspace(r_hub_p, r_mean_p, number_of_radii // 2 + 1)
        second = np.linspace(r_mean_p, r_tip_p, number_of_radii // 2 + 1)[1:]
        combined = np.concatenate((first, second))
        return combined.tolist()

    @staticmethod
    def radius_list(turbine_assum, turbine_input) -> list:
        r_tip, r_mean, r_hub = CalcOperations.find_rtip_rhub_rmean(
            turbine_assum, turbine_input
        )
        radius_prim_list = CalcOperations.radius_prim_list(turbine_assum, turbine_input)
        for idx, radius in enumerate(radius_prim_list):
            radius_prim_list[idx] = radius * r_mean
        return radius_prim_list
    
    @staticmethod
    def radii_names_list() -> list:
        number_of_radii = dg.N_RAD
        if number_of_radii % 2 == 0:
            number_of_radii += 1

        radii_names = [""] * number_of_radii

        radii_names[number_of_radii // 2] = "rmean"
        radii_names[0] = "rhub"
        radii_names[-1] = "rtip"

        for i in range(1, number_of_radii // 2):
            radii_names[i] = f"r{i+1}"

        for i in range(number_of_radii // 2 + 1, number_of_radii -1):
            radii_names[i] = f"r{i+1}"

        return radii_names

    @staticmethod
    def find_psi_mean(turbine_assum, turbine_input) -> float:
        return (
            abs(CalcOperations.find_work_temperature(turbine_input))
            / CalcOperations.find_tangential_velocity(turbine_assum) ** 2
        )

    @staticmethod
    def find_reaction_mean(turbine_assum, turbine_input) -> float:
        c_u2, c_u3 = CalcOperations.find_cu2(turbine_assum, turbine_input)
        return 1 - (c_u2 + c_u3) / (
            2 * CalcOperations.find_tangential_velocity(turbine_assum)
        )

    @staticmethod
    def area_calc(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float):
        return np.abs(x1 * y2 + y1 * x3 + y3 * x2 - y2 * x3 - y1 * x2 - x1 * y3) / 2

    @staticmethod
    def find_reynolds(omega: float, radius: float, mu: float) -> float:
        return (th.rpm_to_rad_s(omega) * (2 * radius) ** 2) / mu
