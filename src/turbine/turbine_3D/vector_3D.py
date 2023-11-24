import numpy as np
import pandas as pd

from turbine_input_data import vector_of_state
from helpers.calc_helpers import CalcOperations as co
from helpers.temp_helpers import TempHelpers as th
from helpers.data_interpolation import DataInterpolation as di
from . import sre_input as sre_in
from . import sre_output as sre_out
from initial_turbine_settings import data_geom as dg

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
        rp_list = co.radious_prim_list(turbine_assum, turbine_input)
        sre_input = sre_in.SimRadEquiInput()
        sre_input.calculate_data(turbine_assum, turbine_input)
        sre_output = sre_input.simple_radial_equi(rp_list, turbine_assum)
        sre_output.to_csv('./data/csv/sre_output.csv')

        return sre_output
    
    @staticmethod
    def sre_to_geom_data(turbine_assum, turbine_input, WS_stator, WS_rotor, plot):
        beta_in = list(np.zeros(5))
        beta_out = list(np.zeros(5))
        alfa2 = list(np.zeros(5))
        alfa3 = list(np.zeros(5))
        phi = list(np.zeros(5))
        Rn = list(np.zeros(5))
        Mach2 = list(np.zeros(5))
        Mach_rel2 = list(np.zeros(5))
        Mach3 = list(np.zeros(5))
        Mach_rel3 = list(np.zeros(5))
        ws_instances = Vector3D.ws_create_instances()
        WS_s_rhub, WS_s_r2, WS_s_r4, WS_s_rtip, WS_r_rhub, WS_r_r2, WS_r_r4, WS_r_rtip = ws_instances.values()
        instances_list = [WS_s_rhub, WS_s_r2, WS_s_r4, WS_s_rtip, WS_r_rhub, WS_r_r2, WS_r_r4, WS_r_rtip]
        for instance in instances_list:
            name = instance.get_instance_name()
            instance.WS_get_data(turbine_assum, turbine_input, name)

        sre_output = Vector3D.sre_initialise(turbine_assum, turbine_input)
        radii_inst = Vector3D.radius_instances(sre_output)

        stator_inst_list = [WS_s_rhub, WS_s_r2, WS_stator, WS_s_r4, WS_s_rtip]
        rotor_inst_list = [WS_r_rhub, WS_r_r2, WS_rotor, WS_r_r4, WS_r_rtip]
        for idx, stator in enumerate(stator_inst_list):
            for rotor in rotor_inst_list:
                if idx == 2:
                    beta_in[idx] = stator.find_beta(turbine_assum.phi)
                    beta_out[idx] = rotor.find_beta(turbine_assum.phi)
                    alfa2[idx] = stator.find_alfa()
                    alfa3[idx] = rotor.find_alfa()
                    phi[idx] = turbine_assum.phi
                    Rn[idx] = radii_inst[idx].Rn
                    Mach2[idx] = stator.find_Mach()
                    Mach_rel2[idx] = stator.find_Mach_rel(turbine_assum.phi)
                    Mach3[idx] = rotor.find_Mach()
                    Mach_rel3[idx] = rotor.find_Mach_rel(turbine_assum.phi)
                else:
                    alfa2[idx] = stator.find_alfa()
                    alfa3[idx] = rotor.find_alfa()
                    Rn[idx] = radii_inst[idx].Rn
                    phi[idx] = (2 - 2*Rn[idx])/(np.tan(th.rad(alfa2[idx])) + np.tan(th.rad(alfa3[idx])))

                    beta_in[idx] = stator.find_beta(phi[idx])
                    beta_out[idx] = rotor.find_beta(phi[idx])

                    Mach2[idx] = stator.find_Mach()
                    Mach_rel2[idx] = stator.find_Mach_rel(phi[idx])
                    Mach3[idx] = rotor.find_Mach()
                    Mach_rel3[idx] = rotor.find_Mach_rel(phi[idx])
        if plot == True:
            return beta_in, beta_out, radii_inst, alfa2, alfa3, phi, Rn, Mach2, Mach_rel2, Mach3, Mach_rel3
        return beta_in, beta_out, radii_inst

    @staticmethod
    def create_geom_data_csv(turbine_assum, turbine_input, WS_stator, WS_rotor):
        beta_in_list, beta_out_list, radii_inst = Vector3D.sre_to_geom_data(turbine_assum, turbine_input, WS_stator, WS_rotor, plot=False)
        geo_input_df = pd.read_csv('./data/csv/geom_data_rotor.csv')
        
        rp_list = co.radious_prim_list(turbine_assum, turbine_input)
        rp_names = ["r_hub", "r_2","r_mean", "r_4", "r_tip"]
        r_list = co.radious_list(radii_inst, turbine_assum, turbine_input)
        for idx, rp in enumerate(rp_list):
            geo_input_df.loc[idx, 'beta_in'] = beta_in_list[idx]
            geo_input_df.loc[idx, 'beta_out'] = beta_out_list[idx]
            geo_input_df.loc[idx, 'R'] = r_list[idx]
            geo_input_df.loc[idx, 'chord_x'] = 0
            geo_input_df.loc[idx, 'half_wedge_out'] = 0
            geo_input_df.loc[idx, 'throat'] = 0
            geo_input_df.loc[idx, 'chord_t'] = di.chord_t_intialization(dg.chord_init, beta_in_list[idx], beta_out_list[idx], idx)
            geo_input_df.loc[idx, 'Nb'] = dg.NB
            pitch = (2 * np.pi * r_list[idx]) / dg.NB
            geo_input_df.loc[idx, 'Rle'] = dg.RLE_MULTIPLIER * pitch
#FIXME jak przyjdzie mi lepszy pomysł na oszacowanie solidity
            geo_input_df.loc[idx, 'Rte'] = dg.RTE_MULTIPLIER * pitch * dg.SOLIDITY_ASSUM
#FIXME wartości dla ugt i half_wedge_in
            geo_input_df.loc[idx, 'ugt'] = dg.UGT[idx]
            geo_input_df.loc[idx, 'half_wedge_in'] = dg.HALF_WEDGE_IN[idx]
        for idx, name in enumerate(rp_names):
            geo_input_df.loc[idx, 'index'] = rp_names[idx]
        geo_input_df.set_index('index', inplace=True)
        print(geo_input_df)
        geo_input_df.to_csv('./data/csv/geom_data_rotor.csv')

