from initial_turbine_settings import data_geom as dg

class OutputTextFile:
    def __init__(self):
        self.buffer = ""
        self.empty = ""

    def data_text_file_one(self, turbine_assum, turbine_input):
        self.buffer += "Blade_Data_Sheet\n"
        self.buffer += f"File for stage {dg.stage} of {dg.part}.\n"
        self.buffer += f"Selected initialization method for chord_t: {dg.chord_init} \n"
        if dg.chord_init == 'chord_t_value':
            self.buffer += f"   initial chord_t values = {dg.CHORD_T} (from r_hub to r_tip)\n"
        self.buffer += f"turbine_input = [m_dot: {turbine_input.m_dot}, p01: {round(turbine_input.p01,1)}, T01: {turbine_input.T01}, tpr: {turbine_input.tpr}, eta_is: {turbine_input.eta_is}, omega: {turbine_input.omega}]\n"
        self.buffer += f"turbine_assum = [alfa1: {turbine_assum.alfa1}, alfa3: {turbine_assum.alfa3}, phi: {turbine_assum.phi}, c_x: {turbine_assum.cx}, r_hub/r_tip: {turbine_assum.rhub_rtip}] \n"
        self.buffer += f"Number of elements: {dg.N_EL} (for one side of the airfoil)\n"

    def data_text_file_two(self,radii, geo_params):
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

    def data_text_file_append_three(self, radii, geo_params):
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

    def turbogrid_file(self, ps, idx, radius):
        number = idx + 1
        if idx == 0:
            self.empty += f"##\tMain\tblade\n"
        self.empty += f"#Profile\t{number}\n"
        for i in range(0, dg.N_EL):
            self.empty += f'{ps.xs[i]}\t{ps.ys[i]}\t{radius}\n'
        for i in range(0, dg.N_EL):
            self.empty += f'{ps.xp[i]}\t{ps.yp[i]}\t{radius}\n'

