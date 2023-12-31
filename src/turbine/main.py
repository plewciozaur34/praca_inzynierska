# FIXME przejrzeć cały kod i poprawić typowanie zmiennych i wyjść z funkcji - jeśli wystarczy czasu

# TODO posprzątać kod - usunąć zbędne komentarze, usunąć zbędne funkcje, usunąć zbędne pliki

# TODO kod dla statora!!

# FIXME sre dla 50 promieni, pt 9.00, cgns dla turbiny i statora, np free vortex dla statora

import pandas as pd

from airfoil_geometry.geom_parameters import geometry_parameters as gp
from airfoil_geometry.dep_geom_parameters import geometry_dep_params_calc as gdpc
from turbine_input_data import vector_of_state
from turbine_input_data import turbine_input as ti
from turbine_input_data import turbine_assum as ta
from initial_turbine_settings import data_calc as dc
from initial_turbine_settings import data_geom as dg
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
turbine_assum = ta.TurbineAssum(dc.ALFA1, dc.ALFA2, dc.PHI, dc.C_X, dc.LAMBDA_N, dc.RH_RT)

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

    radii = co.radii_names_list()
    radius_list = co.radius_list(turbine_assum, turbine_input)
    part = ["rotor", "stator"]

    geo_data_list = v3d.geo_data_list(
        turbine_assum, turbine_input, WS_inlet, WS_stator, WS_rotor
    )

    Reynolds_number = co.find_reynolds(radius_list[4], dc.MU, turbine_assum, turbine_input)
    otf = OutputTextFile()

    for idx, geo_data in enumerate(geo_data_list):
        otf.data_text_file_one(
            turbine_assum,
            turbine_input,
            Reynolds_number,
            WS_inlet,
            WS_stator,
            WS_rotor,
            part[idx],
        )

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
            "airfoil_csa",
            "xcg",
            "ycg",
            "max_thickness"
            ]
        )
        for i in range(0, dg.N_RAD):
            print(f"RATD model for {radii[i]} on {part[idx]}: ")

            geo_params.get_data(geo_data_list[idx], radii[i])

            otf.data_text_file_two(radii[i], geo_params)

            itera, ttc = geo_params.def_values()
            rtd, pressure_and_suction_up = geo_params.chord_t_iteration(itera, ttc)
            print(
                f"Remove throat discontinuity was iterated {geo_params.remove_throat_discontinuity.__defaults__[0][0]} times."
            )

            otf.data_text_file_append_three(geo_params)

            fig.airfoil_figure(rtd, pressure_and_suction_up, radii[i], i, part[idx])

            otf.turbogrid_profile(pressure_and_suction_up, i, radius_list[i], part[idx])

            get_params = dep_params.find_geometry_dependent_parameters()
            params_dictionary = pd.DataFrame([get_params.to_dict()])

            mechanical_props = pressure_and_suction_up.mec_props()
            mechanical_props_dict = pd.DataFrame([mechanical_props.to_dict()])

            max_thickness = pressure_and_suction_up.find_thickness_max()
            max_thickness_dict = pd.DataFrame([max_thickness.to_dict()])

    # Create a temporary DataFrame for this iteration
            temp_df = pd.concat([params_dictionary, mechanical_props_dict, max_thickness_dict], axis=1)

    # Append the temporary DataFrame to geo_dep_params
            geo_dep_params = pd.concat([geo_dep_params, temp_df], ignore_index=True)
            
            print(geo_dep_params)

            calculated_parameters = pd.DataFrame(
                columns=["beta", "beta_deg", "alfa", "mach", "mach_rel"]
            )

        mean_chord = co.calculate_mean_chord(geo_dep_params, column_name="chord")
        Reynolds_chord = co.find_reynolds_chord(mean_chord, dc.MU, turbine_assum, turbine_input, part[idx])
        geo_dep_params.to_csv(f"./data/csv/geometry_dep_params_{part[idx]}.csv")

        tip_percentage_difference = co.is_rotor_rtip_change_needed(
            turbine_input, turbine_assum
        )
        print(f"Tip percentage difference: {tip_percentage_difference}%")
        otf.data_text_file_append_four(tip_percentage_difference, Reynolds_chord)

        otf.turbogrid_init(part[idx])
        otf.turbogrid_shroud(radius_list[4], part[idx])
        otf.turbogrid_hub(radius_list[0], part[idx])
        sft.save_text_blade(otf, part[idx])
        sft.save_turbogrid_profile(otf, part[idx])
        sft.save_turbogrid_shroud(otf, part[idx])
        sft.save_turbogrid_hub(otf, part[idx])
        sft.save_turbogrid_init(otf, part[idx])
        sft.save_dependent_params_csv(geo_dep_params, part[idx]) 
        otf.clear_output_text_file()

    plots.airfoil_plots(turbine_assum, turbine_input, WS_stator, WS_rotor)


if __name__ == "__main__":
    main()

