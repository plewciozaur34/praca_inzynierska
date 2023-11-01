#FIXME przejrzeć cały kod i poprawić typowanie zmiennych i wyjść z funkcji - jeśli wystarczy czasu
#TODO zapisywanie do i z csv - zrobić poprządek z danymi check i faktycznymi danymi do obliczeń
#TODO do sprawdzenia - w jakiej formie zwracać dane o geometrii do TurboGrida


import pandas as pd
import os

from airfoil_geometry.geom_parameters import geometry_parameters as gp
from airfoil_geometry.dep_geom_parameters import geometry_dep_params_calc as gdpc 
from helpers.temp_helpers import TempHelpers as th
from turbine_input_data import vector_of_state
from turbine_input_data import turbine_input as ti
from turbine_input_data import turbine_assum as ta
from initial_turbine_settings import data_calc as dc
from initial_turbine_settings import data_geom as dg
from helpers.figures import DrawFigures as fig
from helpers.calc_helpers import CalcOperations as co
from helpers.text_file import OutputTextFile as otf
from turbine_3D.vector_3D import Vector3D as v3d

# część obliczeniowa

#WEKTOR STANU: [c_axial, c_radial, c_u, p, T, r]
#wektory stanu dla palisady płaskiej (r_mean)
WS_stator = vector_of_state.VectorOfState()
WS_rotor = vector_of_state.VectorOfState()

#turbine_input = [m_dot [kg/s], p01 [Pa], T01 [K], tpr [-], eta_is [-], omega [rpm]] for LP
turbine_input = ti.TurbineInput(dc.M_DOT, 0, dc.T_01, dc.TPR, dc.ETA_IS, dc.OMEGA)
turbine_input.p01 = co.turbine_input_pressure(turbine_input.tpr) / th.p_p0(dc.M_1, dc.KAPPA)

#turbine_assum = [alfa1, alfa3, phi, c_x, r_hub/r_tip]
turbine_assum = ta.TurbineAssum(0,0,dc.PHI, dc.C_X, dc.RH_RT)

#-----------------------------------------------------------------------------------------
# część geometria

#geo_params = gp.GeometryParameters()
#dep_params = gdpc.GeometryDependentParametersCalculation(geo_params)

#TODO reasearch - dane prawdziwe do projektu (obliczenia plus literatura)
#geo_data_r = pd.read_csv('./data/csv/geometry_data_rotor_check.csv', index_col=0)

#geo_params.get_data(geo_data_r, 'check2')


def main():

    #część obliczeniowa 
    c_u2, c_u3 = co.find_cu2(turbine_assum, turbine_input)
    T_2, T_3 = co.find_temperature(turbine_input, turbine_assum)
    p_2, p_3 = co.find_pressure()
    
    WS_stator.cu = c_u2
    WS_rotor.cu = c_u3
    WS_stator.cx = turbine_assum.cx
    WS_rotor.cx = turbine_assum.cx
    WS_stator.T = T_2
    WS_rotor.T = T_3
    WS_stator.p = p_2
    WS_rotor.p = p_3
    
    WS_rotor.mean_calc(turbine_assum.phi)
    #WS_rotor.find_work(WS_stator, turbine_input.omega)

    WS_stator.mean_calc(turbine_assum.phi)

    #----------------------------------------------------------------------------------------------------
    #część geometria
    v3d.sre_to_geom_data(turbine_assum, turbine_input, WS_stator, WS_rotor)
    v3d.create_geom_data_csv(turbine_assum, turbine_input, WS_stator, WS_rotor)

    geo_params = gp.GeometryParameters()
    dep_params = gdpc.GeometryDependentParametersCalculation(geo_params)

    geo_data_r = pd.read_csv('./data/csv/geom_data_rotor.csv', index_col=0)

    radii = ['r_hub', 'r_2', 'r_mean', 'r_4', 'r_tip']

    otf.data_text_file_create(turbine_assum, turbine_input)

    for i in range(0,5):

        geo_params.get_data(geo_data_r, radii[i])
        otf.data_text_file_append(radii[i], geo_params)
        itera, ttc = geo_params.def_values()
        geo_params.print_attributes()
        rtd, pressure_and_suction_up = geo_params.chord_t_iteration(itera, ttc)
        print(f"Remove throat discontinuity was iterated {geo_params.remove_throat_discontinuity.__defaults__[0][0]} times.")
        geo_params.print_attributes()

        timestamp = fig.airfoil_figure(rtd, pressure_and_suction_up, radii[i], i)

        get_params = dep_params.find_geometry_dependent_parameters()
        params_dictionary = pd.DataFrame([get_params.to_dict()])
        geo_dep_params = pd.DataFrame(columns=['pitch', 'stagger_angle', 'chord', 
            'zweifel_coefficient', 'solidity', 'blockage_in', 
            'blockage_out', 'camber_angle', 'lift_coefficient'])
        geo_dep_params = pd.concat([geo_dep_params, params_dictionary], ignore_index=True)

        mechanical_props = pressure_and_suction_up.mec_props()
        mechanical_props_dict = pd.DataFrame([mechanical_props.to_dict()])
        mechanical_props_df = pd.DataFrame(columns=['airfoil_csa', 'xcg', 'ycg'])
        mechanical_props_df = pd.concat([mechanical_props_df, mechanical_props_dict], ignore_index=True)

        max_thickness = pressure_and_suction_up.find_thickness_max()
        max_thickness_dict = pd.DataFrame([max_thickness.to_dict()])
        max_thickness_df = pd.DataFrame(columns=['max_thickness'])
        max_thickness_df = pd.concat([max_thickness_df, max_thickness_dict], ignore_index=True)

        geo_dep_params = pd.concat([geo_dep_params, mechanical_props_df], axis=1)
        geo_dep_params = pd.concat([geo_dep_params, max_thickness_df], axis=1)
        geo_dep_params.to_csv('./data/csv/geometry_dep_params.csv')
        print(geo_dep_params)

        calculated_parameters = pd.DataFrame(columns=['beta','beta_deg','alfa','work'])


    source_file = "./blade_data_sheet.txt"
    destination_path = f"./data/airfoils/{dg.stage_part}_{timestamp}/"
    os.makedirs(destination_path, exist_ok=True)

    os.rename(source_file, os.path.join(destination_path, "blade_data_sheet.txt"))

if __name__ == "__main__":
    main()