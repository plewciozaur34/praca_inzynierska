# FIXME przejrzeć cały kod i poprawić typowanie zmiennych i wyjść z funkcji - jeśli wystarczy czasu

# TODO posprzątać kod - usunąć zbędne komentarze, usunąć zbędne funkcje, usunąć zbędne pliki

# TODO kod dla statora!!

import pandas as pd

from airfoil_geometry.geom_parameters import geometry_parameters as gp
from airfoil_geometry.dep_geom_parameters import geometry_dep_params_calc as gdpc
from turbine_input_data import vector_of_state
from turbine_input_data import turbine_input as ti
from turbine_input_data import turbine_assum as ta
from initial_turbine_settings import data_calc as dc
from helpers.figures import DrawFigures as fig
from helpers.plots import DrawPlots as plots
from helpers.calc_helpers import CalcOperations as co
from helpers.text_file import OutputTextFile
from helpers.saving import SaveFigText as sft
from turbine_3D.vector_3D import Vector3D as v3d

# część obliczeniowa

# WEKTOR STANU: [c_axial, c_radial, c_u, p, T, r]
# wektory stanu dla palisady płaskiej (r_mean)
WS_inlet = vector_of_state.VectorOfState()
WS_stator = vector_of_state.VectorOfState()
WS_rotor = vector_of_state.VectorOfState()

# turbine_input = [m_dot [kg/s], p01 [Pa], T01 [K], tpr [-], eta_is [-], omega [rpm]] for LP
turbine_input = ti.TurbineInput(dc.M_DOT, 0, dc.T_01, dc.TPR, dc.ETA_IS, dc.OMEGA)

# turbine_assum = [alfa1, alfa3, phi, c_x, lambda_n, r_hub/r_tip]
turbine_assum = ta.TurbineAssum(0, 0, dc.PHI, dc.C_X, dc.LAMBDA_N, dc.RH_RT)

turbine_input.p01 = co.turbine_input_stagnation_pressure(turbine_input, turbine_assum)


def main():
    # część obliczeniowa
    c_u2, c_u3 = co.find_cu2(turbine_assum, turbine_input)
    T_2, T_3 = co.find_temperature(turbine_input, turbine_assum)
    p_2, p_3 = co.find_pressure(turbine_input, turbine_assum)
    p_1 = co.turbine_input_static_pressure()
    T_1, c_1 = co.find_inlet_static_temp_and_velocity(turbine_input, turbine_assum)

    WS_inlet.cu = 0
    WS_stator.cu = c_u2
    WS_rotor.cu = c_u3

    WS_inlet.cx = turbine_assum.cx
    WS_stator.cx = turbine_assum.cx
    WS_rotor.cx = turbine_assum.cx

    WS_inlet.T = T_1
    WS_stator.T = T_2
    WS_rotor.T = T_3

    WS_inlet.p = p_1
    WS_stator.p = p_2
    WS_rotor.p = p_3

    WS_inlet.mean_calc(turbine_assum.phi)
    WS_rotor.mean_calc(turbine_assum.phi)
    # FIXME WS_rotor.find_work(WS_stator, turbine_input.omega)

    WS_stator.mean_calc(turbine_assum.phi)

    # ----------------------------------------------------------------------------------------------------
    # część geometria

    geo_params = gp.GeometryParameters()
    dep_params = gdpc.GeometryDependentParametersCalculation(geo_params)

    geo_data_list = v3d.geo_data_list(turbine_assum, turbine_input, WS_inlet, WS_stator, WS_rotor)
    radii = ["r_hub", "r_2", "r_mean", "r_4", "r_tip"]
    radius_list = co.stator_radius_list(turbine_assum, turbine_input)
    part = ["rotor", "stator"]

    Reynolds_number = co.find_reynolds(turbine_input.omega, radius_list[4], dc.MU)
    otf = OutputTextFile()
    
    for idx, geo_data in enumerate(geo_data_list): 
        otf.data_text_file_one(turbine_assum, turbine_input, Reynolds_number, part[idx])
        for i in range(0, 5):
            print(f"RATD model for {radii[i]}: ")

            geo_params.get_data(geo_data_list[idx], radii[i])

            otf.data_text_file_two(radii[i], geo_params)

            itera, ttc = geo_params.def_values()
            rtd, pressure_and_suction_up = geo_params.chord_t_iteration(itera, ttc)
            print(
                    f"Remove throat discontinuity was iterated {geo_params.remove_throat_discontinuity.__defaults__[0][0]} times."
                )

            otf.data_text_file_append_three(geo_params)

            fig.airfoil_figure(rtd, pressure_and_suction_up, radii[i], i , part[idx])

            otf.turbogrid_profile(pressure_and_suction_up, i, radius_list[i])

            get_params = dep_params.find_geometry_dependent_parameters()
            params_dictionary = pd.DataFrame([get_params.to_dict()])
            geo_dep_params = pd.DataFrame(
                columns=[
                    "pitch",
                    "stagger_angle",
                    "chord",
                    "zweifel_coefficient",
                    "solidity",
                    "blockage_in",
                    "blockage_out",
                    "camber_angle",
                    "lift_coefficient",
                    ]
                )
            geo_dep_params = pd.concat(
                    [geo_dep_params, params_dictionary], ignore_index=True
                )

            mechanical_props = pressure_and_suction_up.mec_props()
            mechanical_props_dict = pd.DataFrame([mechanical_props.to_dict()])
            mechanical_props_df = pd.DataFrame(columns=["airfoil_csa", "xcg", "ycg"])
            mechanical_props_df = pd.concat(
                    [mechanical_props_df, mechanical_props_dict], ignore_index=True
                )

            max_thickness = pressure_and_suction_up.find_thickness_max()
            max_thickness_dict = pd.DataFrame([max_thickness.to_dict()])
            max_thickness_df = pd.DataFrame(columns=["max_thickness"])
            max_thickness_df = pd.concat(
                    [max_thickness_df, max_thickness_dict], ignore_index=True
                )

            geo_dep_params = pd.concat([geo_dep_params, mechanical_props_df], axis=1)
            geo_dep_params = pd.concat([geo_dep_params, max_thickness_df], axis=1)
            geo_dep_params.to_csv(f"./data/csv/geometry_dep_params_{part[idx]}.csv")
            print(geo_dep_params)

            calculated_parameters = pd.DataFrame(
                    columns=["beta", "beta_deg", "alfa", "mach", "mach_rel"]
                )

        tip_percentage_difference = co.is_rotor_rtip_change_needed(
                turbine_input, turbine_assum
            )
        print(f"Tip percentage difference: {tip_percentage_difference}%")
        otf.data_text_file_append_four(tip_percentage_difference)

        otf.turbogrid_init(part[idx])
        otf.turbogrid_shroud(radius_list[4])
        otf.turbogrid_hub(radius_list[0])
        sft.save_text_blade(otf, part[idx])
        sft.save_turbogrid_profile(otf, part[idx])
        sft.save_turbogrid_shroud(otf, part[idx])
        sft.save_turbogrid_hub(otf, part[idx])
        sft.save_turbogrid_init(otf, part[idx])
        plots.airfoil_plots(turbine_assum, turbine_input, WS_stator, WS_rotor)
    
    #cg.run_geometry(geo_params, dep_params, geo_data_list, radii, radius_list, part)


if __name__ == "__main__":
    main()
