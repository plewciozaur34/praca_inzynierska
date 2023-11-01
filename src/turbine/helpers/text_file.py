from initial_turbine_settings import data_geom as dg

class OutputTextFile:
    
    @staticmethod
    def data_text_file_create(turbine_assum, turbine_input):
        with open("blade_data_sheet.txt", "w") as file:
            file.write("Blade_Data_Sheet\n")
            file.write(f"File for stage {dg.stage} of {dg.part}.\n")
            file.write(f"Selected initialization method for chord_t: {dg.chord_init} \n")
            file.write(f"turbine_input = [m_dot: {turbine_input.m_dot}, p01: {round(turbine_input.p01,1)}, T01: {turbine_input.T01}, tpr: {turbine_input.tpr}, eta_is: {turbine_input.eta_is}, omega: {turbine_input.omega}]\n")
            file.write(f"turbine_assum = [alfa1: {turbine_assum.alfa1}, alfa3: {turbine_assum.alfa3}, phi: {turbine_assum.phi}, c_x: {turbine_assum.cx}, r_hub/r_tip: {turbine_assum.rhub_rtip}] \n")
            file.write(f"Number of elements: {dg.N_EL} (for one side of the airfoil)\n")

    def data_text_file_append(radii, geo_params):
        with open("blade_data_sheet.txt", "a") as file:
            file.write(f"   \n")
            file.write(f"Input independent parameters for RATD model for {radii}: \n")
            file.write(f"R= {round(geo_params.R,3)} \n")
            file.write(f"beta_in= {round(geo_params.beta_in,2)} \n")
            file.write(f"beta_out= {round(geo_params.beta_out,2)} \n")
            file.write(f"chord_x= {geo_params.chord_x} \n")
            file.write(f"chord_t= {geo_params.chord_t} \n")
            file.write(f"ugt= {round(geo_params.ugt,2)} \n") 
            file.write(f"Rle= {round(geo_params.Rle,5)} \n")
            file.write(f"Rte= {round(geo_params.Rte,5)} \n")
            file.write(f"Nb= {geo_params.Nb} \n")
            file.write(f"throat= {geo_params.throat} \n")
            file.write(f"half_wedge_in= {round(geo_params.half_wedge_in,2)} \n")


