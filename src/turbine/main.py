#FIXME przejrzeć cały kod i poprawić typowanie zmiennych i wyjść z funkcji - jeśli wystarczy czasu
#TODO zapisywanie do i z csv - zrobić poprządek z danymi check i faktycznymi danymi do obliczeń
#TODO do sprawdzenia - w jakiej formie zwracać dane o geometrii do TurboGrida

import pandas as pd
import matplotlib.pyplot as plt

from airfoil_geometry.geom_parameters import geometry_parameters as gp
from airfoil_geometry.dep_geom_parameters import geometry_dep_params_calc as gdpc
from airfoil_geometry.dep_geom_parameters import surface_points  as sp
from helpers.temp_helpers import TempHelpers as th
from turbine_input_data import vector_of_state
from turbine_input_data import turbine_input as ti
from turbine_input_data import turbine_assum as ta
from helpers import data_calc as dc
from helpers.calc_helpers import CalcOperations as co
from turbine_3D import sre_input as sre_in

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

geo_params = gp.GeometryParameters()
dep_params = gdpc.GeometryDependentParametersCalculation(geo_params)

#TODO reasearch - dane prawdziwe do projektu (obliczenia plus literatura)
geo_data_r = pd.read_csv('./data/csv/geometry_data_rotor.csv', index_col=0)

geo_params.get_data(geo_data_r, 'check2')


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
#FIXME czy ta pętla jest tu potzrebna - albo usunąć albo dac mozliwość zmiany danych pomiędzy iteracjami
    N = 1
    for i in range(0,N):
        
        geo_params.def_values()
        geo_params.print_attributes()

        rtd = geo_params.remove_throat_discontinuity()
        print(f"Remove throat discontinuity was iterated {geo_params.remove_throat_discontinuity.__defaults__[0][0]} times.")

        pressure_and_suction_up = sp.SurfacePoints()
        pressure_and_suction_up.surface_points(geo_params, rtd)

        exes = [rtd.point1.x, rtd.point2.x, rtd.point3.x, rtd.point4.x, rtd.point5.x]
        whys = [rtd.point1.y, rtd.point2.y, rtd.point3.y, rtd.point4.y, rtd.point5.y]
        colors = ['red', 'blue', 'green', 'grey', 'pink']
        legend = ['point1', 'point2', 'point3', 'point4', 'point5']

        fig, axs = plt.subplots(1,1, figsize = (6,5))
        for x, y, color, legend in zip(exes, whys, colors, legend):
            axs.scatter(x, y, color=color, s=10, label=legend)

        #th.plot_line_through_point(axs, [rtd.point3.x, rtd.point3.y], rtd.point3.b, length=0.1, color='green', linestyle='--')
        #th.plot_line_through_point(axs, [rtd.point4.x, rtd.point4.y], rtd.point4.b, length=0.1, color='grey', linestyle='--')
        
#TODO zapis do png - tworzący nowe pliki a nie nadpisujący stare iteracje
        axs.plot(pressure_and_suction_up.xp, pressure_and_suction_up.yp, color = 'blue')
        axs.plot(pressure_and_suction_up.xs, pressure_and_suction_up.ys, color = 'black')
        axs.set_title('Airfoil geometry')
        axs.legend()
        plt.show()

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

        rp_list_check = [0.75, 0.9, 1.0, 1.1, 1.25]
        rp_list = co.radious_list(turbine_assum, turbine_input)
        print(f"rp_list = {rp_list}")
        sre_input = sre_in.SimRadEquiInput()
        #sre_data = pd.read_csv('./data/csv/sre_check_data.csv')
        sre_input.calculate_data(turbine_assum, turbine_input)
        sre_input.print_attributes()
        #sre_input.get_data(sre_data)
        sre_output = sre_input.simple_radial_equi(rp_list, turbine_assum)
        sre_output.to_csv('./data/csv/sre_output_check.csv')

if __name__ == "__main__":
    main()