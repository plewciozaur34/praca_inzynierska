import numpy as np

from turbine_input_data import vector_of_state
from helpers.calc_helpers import CalcOperations as co
from helpers.temp_helpers import TempHelpers as th
from . import sre_input as sre_in
from . import sre_output as sre_out

class Vector3D:
    def radius_instances(df):
        instances = []
        for _, row in df.iterrows():
            radius_instance = sre_out.SimRadEquiOutput(row['r_p'], row['C_x1'], row['C_x2'], row['C_u1'], row['C_u2'], row['Rn_prim'], row['Rn'])
            instances.append(radius_instance)
        return instances
    
    @staticmethod
    def ws_create_instances():
        sides = ["s", "r"]
        positions = ["rhub", "r2", "r4", "rtip"]
    
        instances = {}
        for side in sides:
            for position in positions:
                instance_name = f"WS_{side}_{position}"
                instances[instance_name] = vector_of_state.VectorOfState(instance_name)
        return instances
    
    @staticmethod
    def sre_initialise(turbine_assum, turbine_input):
        rp_list = co.radious_list(turbine_assum, turbine_input)
        sre_input = sre_in.SimRadEquiInput()
        sre_input.calculate_data(turbine_assum, turbine_input)
        sre_output = sre_input.simple_radial_equi(rp_list, turbine_assum)
        sre_output.to_csv('./data/csv/sre_output_check.csv')

        return sre_output
    
    @staticmethod
    def sre_to_geom_data(turbine_assum, turbine_input):
        beta_in = list(np.zeros(4))
        beta_out = list(np.zeros(4))
        ws_instances = Vector3D.ws_create_instances()
        WS_s_rhub, WS_s_r2, WS_s_r4, WS_s_rtip, WS_r_rhub, WS_r_r2, WS_r_r4, WS_r_rtip = ws_instances.values()
        instances_list = [WS_s_rhub, WS_s_r2, WS_s_r4, WS_s_rtip, WS_r_rhub, WS_r_r2, WS_r_r4, WS_r_rtip]
        for instance in instances_list:
            name = instance.get_instance_name()
            instance.WS_get_data(turbine_assum, turbine_input, name)

        sre_output = Vector3D.sre_initialise(turbine_assum, turbine_input)
        radii_inst = Vector3D.radius_instances(sre_output)

        stator_inst_list = [WS_s_rhub, WS_s_r2, WS_s_r4, WS_s_rtip]
        rotor_inst_list = [WS_r_rhub, WS_r_r2, WS_r_r4, WS_r_rtip]
        for idx, stator in enumerate(stator_inst_list):
            for rotor in rotor_inst_list:
                alfa2 = stator.find_alfa()
                alfa3 = rotor.find_alfa()
                Rn = radii_inst[idx].Rn

                phi = (2 - 2*Rn)/(np.tan(alfa2) + np.tan(alfa3))

                beta_in[idx] = th.deg(stator.find_beta(phi))
                beta_out[idx] = th.deg(rotor.find_beta(phi))

        return beta_in, beta_out

    @staticmethod
    def create_geom_data_csv(turbine_assum, turbine_input):
        beta_in_list, beta_out_list = Vector3D.sre_to_geom_data(turbine_assum, turbine_input)
#TODO zapis beta_in_list, beta_out_list do csv z danymi dla r_mean i zrobienie kolejnych wierszy dla 
#innych promieni; dobrze by było gdyby r_mean był pomiędzy - jak?? 

