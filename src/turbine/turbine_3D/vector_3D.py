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
            radius_instance = sre_out.SimRadEquiOutput(
                row["r_p"],
                row["C_x1"],
                row["C_x2"],
                row["C_u1"],
                row["C_u2"],
                row["Rn_prim"],
                row["Rn"],
            )
            instances.append(radius_instance)
        return instances

    @staticmethod
    def ws_create_instances():
        sides = ["s", "r"]

        positions = co.radii_names_list()
        if "rmean" in positions:
            positions.remove("rmean")

        instances = {}

        for side in sides:
            for position in positions:
                instance_name = f"WS_{side}_{position}"
                instances[instance_name] = vector_of_state.VectorOfState()
        return instances

    @staticmethod
    def sre_initialise(turbine_assum, turbine_input):
        rp_list = co.radius_prim_list(turbine_assum, turbine_input)
        sre_input = sre_in.SimRadEquiInput()
        sre_input.calculate_data(turbine_assum, turbine_input)
        sre_output = sre_input.simple_radial_equi(rp_list, turbine_assum)
        sre_output.to_csv("./data/csv/sre_output.csv")

        return sre_output

    @staticmethod
    def sre_to_geom_data(turbine_assum, turbine_input, WS_stator, WS_rotor, plot):
        beta_in = list(np.zeros(dg.N_RAD))
        beta_out = list(np.zeros(dg.N_RAD))
        alfa2 = list(np.zeros(dg.N_RAD))
        alfa3 = list(np.zeros(dg.N_RAD))
        phi = list(np.zeros(dg.N_RAD))
        Rn = list(np.zeros(dg.N_RAD))
        Mach2 = list(np.zeros(dg.N_RAD))
        Mach_rel2 = list(np.zeros(dg.N_RAD))
        Mach3 = list(np.zeros(dg.N_RAD))
        Mach_rel3 = list(np.zeros(dg.N_RAD))

        ws_instances = Vector3D.ws_create_instances()
        instances_list = list(ws_instances.values())

        for instance_name in ws_instances.keys():
            instance = ws_instances[instance_name]
            instance.WS_get_data(turbine_assum, turbine_input, instance_name)

        sre_output = Vector3D.sre_initialise(turbine_assum, turbine_input)
        radii_inst = Vector3D.radius_instances(sre_output)

        # half_length = len(instances_list) // 2
        # stator_inst_list = instances_list[:half_length]
        # rotor_inst_list = instances_list[half_length:]

        # stator_inst_list.insert(half_length // 2, WS_stator)

        # rotor_inst_list.insert(half_length // 2, WS_rotor)

        stator_inst_list = [
            instances_list[0],
            instances_list[1],
            WS_stator,
            instances_list[2],
            instances_list[3],
        ]
        rotor_inst_list = [
            instances_list[4],
            instances_list[5],
            WS_rotor,
            instances_list[6],
            instances_list[7],
        ]

        for idx, (stator, rotor) in enumerate(zip(stator_inst_list, rotor_inst_list)):
            if idx == 2:
                beta_in[idx] = stator.find_beta(turbine_assum.phi)
                beta_out[idx] = rotor.find_beta(turbine_assum.phi)
                alfa2[idx] = stator.find_alfa()
                alfa3[idx] = rotor.find_alfa()
                phi[idx] = turbine_assum.phi
                Rn[idx] = radii_inst[idx].Rn
                # Mach2[idx] = stator.find_Mach()
                # Mach_rel2[idx] = stator.find_Mach_rel(turbine_assum.phi)
                # Mach3[idx] = rotor.find_Mach()
                # Mach_rel3[idx] = rotor.find_Mach_rel(turbine_assum.phi)
            else:
                alfa2[idx] = stator.find_alfa()
                alfa3[idx] = rotor.find_alfa()
                Rn[idx] = radii_inst[idx].Rn
                phi[idx] = (2 - 2 * Rn[idx]) / (
                    np.tan(th.rad(alfa2[idx])) + np.tan(th.rad(alfa3[idx]))
                )

                beta_in[idx] = stator.find_beta(phi[idx])
                beta_out[idx] = rotor.find_beta(phi[idx])

                # Mach2[idx] = stator.find_Mach()
                # Mach_rel2[idx] = stator.find_Mach_rel(phi[idx])
                # Mach3[idx] = rotor.find_Mach()
                # Mach_rel3[idx] = rotor.find_Mach_rel(phi[idx])
        if plot == True:
            return (
                beta_in,
                beta_out,
                radii_inst,
                alfa2,
                alfa3,
                phi,
                Rn,
                # Mach2,
                # Mach_rel2,
                # Mach3,
                # Mach_rel3,
            )
        return beta_in, beta_out, radii_inst, alfa2

    @staticmethod
    def create_geom_data_csv(turbine_assum, turbine_input, WS_stator, WS_rotor):
        beta_in_list, beta_out_list, radii_inst, alfa_in = Vector3D.sre_to_geom_data(
            turbine_assum, turbine_input, WS_stator, WS_rotor, plot=False
        )
        geo_input_df = pd.read_csv("./data/csv/geom_data_rotor.csv")

        rp_list = co.radius_prim_list(turbine_assum, turbine_input)
        rp_names = co.radii_names_list()
        r_list = co.radius_list(turbine_assum, turbine_input)
        for idx, rp in enumerate(rp_list):
            geo_input_df.loc[idx, "beta_in"] = beta_in_list[idx]
            geo_input_df.loc[idx, "beta_out"] = beta_out_list[idx]
            geo_input_df.loc[idx, "R"] = r_list[idx]
            geo_input_df.loc[idx, "chord_x"] = 0
            geo_input_df.loc[idx, "half_wedge_out"] = 0
            geo_input_df.loc[idx, "throat"] = 0
            geo_input_df.loc[idx, "chord_t"] = di.chord_t_intialization(
                dg.chord_init, beta_in_list[idx], beta_out_list[idx], idx
            )
            geo_input_df.loc[idx, "Nb"] = dg.NB_r
            pitch = (2 * np.pi * r_list[idx]) / dg.NB_r
            geo_input_df.loc[idx, "Rle"] = dg.RLE_MULTIPLIER * pitch
            # FIXME jak przyjdzie mi lepszy pomysł na oszacowanie solidity
            geo_input_df.loc[idx, "Rte"] = dg.RTE_MULTIPLIER * pitch * dg.SOLIDITY_ASSUM
            # FIXME wartości dla ugt i half_wedge_in
            geo_input_df.loc[idx, "ugt"] = dg.UGT[idx]
            geo_input_df.loc[idx, "half_wedge_in"] = dg.HALF_WEDGE_IN[idx]

        for idx, name in enumerate(rp_names):
            geo_input_df.loc[idx, "index"] = rp_names[idx]
        geo_input_df.set_index("index", inplace=True)
        print(geo_input_df)
        geo_input_df.to_csv("./data/csv/geom_data_rotor.csv")

    @staticmethod
    def create_geom_data_csv_stator(
        turbine_assum, turbine_input, WS_inlet, WS_stator, WS_rotor
    ):
        (
            beta_in_list,
            beta_out_list,
            radii_inst,
            alfa_out_list,
        ) = Vector3D.sre_to_geom_data(
            turbine_assum, turbine_input, WS_stator, WS_rotor, plot=False
        )
        alfa_in_list = list(np.zeros(dg.N_RAD))
        for i in range(len(alfa_in_list)):
            alfa_in_list[i] = WS_inlet.find_alfa()

        geo_input_df = pd.read_csv("./data/csv/geom_data_stator.csv")

        rp_list = co.radius_prim_list(turbine_assum, turbine_input)
        rp_names = co.radii_names_list()
        r_list = co.radius_list(turbine_assum, turbine_input)
        for idx, rp in enumerate(rp_list):
            geo_input_df.loc[idx, "beta_in"] = alfa_in_list[idx]
            geo_input_df.loc[idx, "beta_out"] = -alfa_out_list[idx]
            geo_input_df.loc[idx, "R"] = r_list[idx]
            geo_input_df.loc[idx, "chord_x"] = 0
            geo_input_df.loc[idx, "half_wedge_out"] = 0
            geo_input_df.loc[idx, "throat"] = 0
            geo_input_df.loc[idx, "chord_t"] = 0
            # geo_input_df.loc[idx, 'chord_t'] = di.chord_t_intialization(dg.chord_init, alfa_in_list[idx], alfa_out_list[idx], idx)
            geo_input_df.loc[idx, "Nb"] = dg.NB_s
            pitch = (2 * np.pi * r_list[idx]) / dg.NB_s
            geo_input_df.loc[idx, "Rle"] = dg.RLE_MULTIPLIER * pitch
            # FIXME jak przyjdzie mi lepszy pomysł na oszacowanie solidity
            geo_input_df.loc[idx, "Rte"] = dg.RTE_MULTIPLIER * pitch * dg.SOLIDITY_ASSUM
            # FIXME wartości dla ugt i half_wedge_in
            geo_input_df.loc[idx, "ugt"] = dg.UGT[idx]
            geo_input_df.loc[idx, "half_wedge_in"] = dg.HALF_WEDGE_IN[idx]
        for idx, name in enumerate(rp_names):
            geo_input_df.loc[idx, "index"] = rp_names[idx]
        geo_input_df.set_index("index", inplace=True)
        print(geo_input_df)
        geo_input_df.to_csv("./data/csv/geom_data_stator.csv")

    @staticmethod
    def geo_data_list(turbine_assum, turbine_input, WS_inlet, WS_stator, WS_rotor):
        Vector3D.create_geom_data_csv(turbine_assum, turbine_input, WS_stator, WS_rotor)
        Vector3D.create_geom_data_csv_stator(
            turbine_assum, turbine_input, WS_inlet, WS_stator, WS_rotor
        )

        geo_data_r = pd.read_csv("./data/csv/geom_data_rotor.csv", index_col=0)
        geo_data_s = pd.read_csv("./data/csv/geom_data_stator.csv", index_col=0)

        return [geo_data_r, geo_data_s]
