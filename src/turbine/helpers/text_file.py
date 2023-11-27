import numpy as np

from initial_turbine_settings import data_geom as dg


class OutputTextFile:
    def __init__(self):
        self.buffer = ""
        self.profile = ""
        self.shroud = ""
        self.hub = ""
        self.init = ""

    def data_text_file_one(self, turbine_assum, turbine_input, Reynolds_number, part, stage=dg.stage):
        self.buffer += "Blade_Data_Sheet\n"
        self.buffer += f"Reynolds number for the turbine: {Reynolds_number}\n"
        self.buffer += f"File for stage {stage} of {part}.\n"
        self.buffer += f"Selected initialization method for chord_t: {dg.chord_init} \n"
        if dg.chord_init == "chord_t_value":
            self.buffer += (
                f"   initial chord_t values = {dg.CHORD_T} (from r_hub to r_tip)\n"
            )
        self.buffer += f"turbine_input = [m_dot: {turbine_input.m_dot}, p01: {round(turbine_input.p01,1)}, T01: {turbine_input.T01}, tpr: {turbine_input.tpr}, eta_is: {turbine_input.eta_is}, omega: {turbine_input.omega}]\n"
        self.buffer += f"turbine_assum = [alfa1: {turbine_assum.alfa1}, alfa3: {turbine_assum.alfa3}, phi: {turbine_assum.phi}, c_x: {turbine_assum.cx}, lambda_n: {turbine_assum.lambda_n}, r_hub/r_tip: {turbine_assum.rhub_rtip}] \n"
        self.buffer += f"Number of elements: {dg.N_EL} (for one side of the airfoil)\n"
        self.buffer += f"data_geom input values => solidity: {dg.SOLIDITY_ASSUM}, ugt: {dg.UGT}, half_wedge_in: {dg.HALF_WEDGE_IN}, rte_multiplier: {dg.RTE_MULTIPLIER}, rle_multiplier: {dg.RLE_MULTIPLIER}\n"

    def data_text_file_two(self, radii, geo_params):
        self.buffer += f"   \n"
        self.buffer += f"Input independent parameters for RATD model for {radii}: \n"
        self.buffer += f"R= {round(geo_params.R,3)} \n"
        self.buffer += f"beta_in= {round(geo_params.beta_in,2)} \n"
        self.buffer += f"beta_out= {round(geo_params.beta_out,2)} \n"
        self.buffer += f"chord_x= {round(geo_params.chord_x,4)} \n"
        self.buffer += f"chord_t= {round(geo_params.chord_t,4)} \n"
        self.buffer += f"ugt= {round(geo_params.ugt,2)} \n"
        self.buffer += f"Rle= {round(geo_params.Rle,5)} \n"
        self.buffer += f"Rte= {round(geo_params.Rte,5)} \n"
        self.buffer += f"Nb= {geo_params.Nb} \n"
        self.buffer += f"throat= {round(geo_params.throat,4)} \n"
        self.buffer += f"half_wedge_in= {round(geo_params.half_wedge_in,2)} \n"

    def data_text_file_append_three(self, geo_params):
        self.buffer += f"   \n"
        self.buffer += f"Independent parameters after def_values, remove_throat_discontinuity and chord_t_intialization: \n"
        self.buffer += f"chord_x= {round(geo_params.chord_x,4)} \n"
        self.buffer += f"chord_t= {round(geo_params.chord_t,4)} \n"
        self.buffer += f"ugt= {round(geo_params.ugt,2)} \n"
        self.buffer += f"Rle= {round(geo_params.Rle,5)} \n"
        self.buffer += f"Rte= {round(geo_params.Rte,5)} \n"
        self.buffer += f"throat= {round(geo_params.throat,4)} \n"
        self.buffer += f"half_wedge_out= {round(geo_params.half_wedge_out,4)} \n"
        self.buffer += f"   \n"

    def data_text_file_append_four(self, tip_percentage_difference):
        self.buffer += f"Tip percentage difference: {tip_percentage_difference}%"

    def turbogrid_profile(self, ps, idx, radius):
        number = idx + 1
        if idx == 0:
            self.profile += f"##\tMain\tblade\n"
        self.profile += f"#Profile\t{number}\n"
        for i in range(0, dg.N_EL):
            self.profile += f"{radius:.{6}f}\t{ps.ys[i]:.{6}f}\t{ps.xs[i]:.{6}f}\n"
        for i in range(0, dg.N_EL - 1):
            self.profile += f"{radius:.{6}f}\t{ps.yp[dg.N_EL - i -1]:.{6}f}\t{ps.xp[dg.N_EL - i -1]:.{6}f}\n"

    def turbogrid_init(self, part):
        self.init += f"Axis of Rotation: Z \n"
        if part == "rotor":
            self.init += f"Number of Blade Sets: {dg.NB_r} \n"
        else:
            self.init += f"Number of Blade Sets: {dg.NB_s} \n"
        self.init += f"Number of Blades Per Set: 1 \n"
        self.init += f"Blade Loft Direction: Streamwise \n"
        self.init += f"Geometry Units: M \n"
        self.init += f"Blade 0 TE: EllipseEnd \n"
        self.init += f"Hub Data File: turbine_design_blade_{part}_hub.curve \n"
        self.init += f"Shroud Data File: turbine_design_blade_{part}_shroud.curve \n"
        self.init += f"Profile Data File: turbine_design_blade_{part}_profile.curve \n"

    def turbogrid_shroud(self, radius):
        x = 0.0
        y = np.linspace(-0.07, 0.20, dg.N_EL)
        tip_radius = radius  # - 0.001
        for i in range(0, dg.N_EL):
            self.shroud += f"{x:.{6}f}\t{tip_radius:.{6}f}\t{y[i]:.{6}f}\n"

    def turbogrid_hub(self, radius):
        x = 0.0
        y = np.linspace(-0.07, 0.20, dg.N_EL)
        hub_radius = radius  # + 0.001
        for i in range(0, dg.N_EL):
            self.hub += f"{x:.{6}f}\t{hub_radius:.{6}f}\t{y[i]:.{6}f}\n"
