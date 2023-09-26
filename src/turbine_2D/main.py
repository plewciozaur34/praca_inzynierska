import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.patches import Circle

from airfoil_geometry import geometry_parameters as gp
from airfoil_geometry import geometry_dep_params_calc as gdpc
from airfoil_geometry import surface_points  as sp
from helpers.temp_helpers import TempHelpers as th
from turbine_input_data import vector_of_state
from turbine_input_data import turbine_input as ti
from turbine_input_data import turbine_assum as ta
from turbine_input_data import data_calc as dc
from helpers.calc_helpers import CalcOperations as co

# część obliczeniowa

#WEKTOR STANU: [c_axial, c_radial, c_u, p, T, r]
WS_stator = vector_of_state.VectorOfState()
WS_rotor = vector_of_state.VectorOfState()

#turbine_input = [m_dot [kg/s], p01 [Pa], T01 [K], tpr [-], eta_is [-], omega [rpm]] for LP
turbine_input = ti.TurbineInput(dc.M_DOT, 0, dc.T_01, dc.TPR, dc.ETA_IS, dc.OMEGA)
turbine_input.p01 = co.turbine_input_pressure(turbine_input.tpr) / th.p_p0(dc.M_1, dc.KAPPA)

#turbine_assum = [alfa1, alfa3, phi, c_x ..]
turbine_assum = ta.TurbineAssum(0,0,dc.PHI, dc.C_X)

#-----------------------------------------------------------------------------------------
# część geometria

geo_params = gp.GeometryParameters()
dep_params = gdpc.GeometryDependentParametersCalculation(geo_params)

geo_data_r = pd.read_csv('./data/geometry_data_rotor.csv', index_col=0)

geo_params.get_data(geo_data_r, 'check2')


def main():

    #część obliczeniowa 
    c_u2, c_u3 = co.find_cu2(turbine_assum, turbine_input)

    WS_stator.cu = c_u2
    WS_rotor.cu = c_u3
    WS_stator.cx = turbine_assum.cx
    WS_rotor.cx = turbine_assum.cx
    
    WS_rotor.mean_calc(turbine_assum.phi)
    WS_rotor.find_work(WS_stator, turbine_input.omega)

    WS_stator.mean_calc(turbine_assum.phi)

    #zapisac zewnetrzny plik z danymi do profilu

    #----------------------------------------------------------------------------------------------------
    #część geometria
    N = 1
    i = 0
    for i in range(0,N):
        geo_params.def_values()
        geo_params.print_attributes()

        point1 = geo_params.find_suction_surface_trailing_edge_tangency_point()
        point2 = geo_params.find_suction_surface_throat_point()
        point3 = geo_params.find_suction_surface_leading_edge_tangency_point()
        point4 = geo_params.find_pressure_surface_leading_edge_tangency_point()
        point5 = geo_params.find_pressure_surface_trailing_edge_tangency_point()
        point0 = point1.circle(point2)

        geo_params.remove_throat_discontinuity(geo_params, point0)
        print(f"Remove throat discontinuity was iterated {geo_params.remove_throat_discontinuity.__defaults__[0][0]} times.")

        #leading_edge_params = point3.circle(point4)
        #trailing_edge_params = point1.circle(point5)

        pressure_surf_params = point4.polynomial(point5)
        suction_surf_upthroat_params = point3.polynomial(point2)
        suction_surf_downthroat_params = point2.bezier(point1)

        pressure_and_suction_up = sp.SurfacePoints(list(np.zeros(50)), list(np.zeros(50)), list(np.zeros(50)), list(np.zeros(50)))
        pressure_and_suction_up.surface_points(pressure_surf_params, suction_surf_upthroat_params, geo_params, point0, point1, point2, point3, point4, point5)

        #leading_edge = Circle((leading_edge_params.x, leading_edge_params.y), leading_edge_params.r, fill = False, color = 'red')
        #trailing_edge = Circle((trailing_edge_params.x, trailing_edge_params.y), trailing_edge_params.r, fill = False, color = 'green')

        pressure_surf_coeff = [pressure_surf_params.d, pressure_surf_params.c, pressure_surf_params.b, pressure_surf_params.a]
        pressure_surf = np.poly1d(pressure_surf_coeff)
        x_pressure = np.linspace(point4.x, point5.x, 200)

        suction_surf_upthroat_coeff = [suction_surf_upthroat_params.d, suction_surf_upthroat_params.c, suction_surf_upthroat_params.b, suction_surf_upthroat_params.a]
        suction_surf_upthroat = np.poly1d(suction_surf_upthroat_coeff)
        x_suction_upthroat = np.linspace(point3.x, point2.x, 200)


        #fig, ax = plt.subplots(1,1, figsize = (6,5))
        #ax.add_patch(leading_edge)
        #ax.add_patch(trailing_edge)
        #ax.plot(x_pressure, pressure_surf(x_pressure), color = 'blue')
        #ax.plot(x_suction_upthroat, suction_surf_upthroat(x_suction_upthroat), color = 'black')
        #ax.set_xlim(-0.5, 1.5)
        #ax.set_ylim(-0.5, 2)
        #ax.set_aspect('equal')
        #plt.show()
        #fig.savefig('./data/airfoils', dpi=300)

        exes = [point1.x, point2.x, point3.x, point4.x, point5.x]
        whys = [point1.y, point2.y, point3.y, point4.y, point5.y]
        colors = ['red', 'blue', 'green', 'grey', 'pink']
        legend = ['point1', 'point2', 'point3', 'point4', 'point5']

        figs, axs = plt.subplots(1,1, figsize = (6,5))
        axs.scatter(exes, whys, color = colors, s=10)
        #axs.add_patch(leading_edge)
        #axs.add_patch(trailing_edge)
        #axs.plot(x_suction_upthroat, suction_surf_upthroat(x_suction_upthroat), color = 'black')
        #axs.plot(x_pressure, pressure_surf(x_pressure), color = 'blue')
        axs.plot(pressure_and_suction_up.xp, pressure_and_suction_up.yp, color = 'blue')
        axs.plot(pressure_and_suction_up.xs, pressure_and_suction_up.ys, color = 'black')
        plt.show()

        get_params = dep_params.find_geometry_dependent_parameters()
        params_dictionary = pd.DataFrame([get_params.to_dict()])
        geo_dep_params = pd.DataFrame(columns=['pitch', 'stagger_angle', 'chord', 
            'zweifel_coefficient', 'solidity', 'blockage_in', 
            'blockage_out', 'camber_angle', 'lift_coefficient'])
        geo_dep_params = pd.concat([geo_dep_params, params_dictionary], ignore_index=True)
        #z jakiegoś powodu mec_props wyrzuca tylko nan
        mechanical_props = pressure_and_suction_up.mec_props()
        mechanical_props_dict = pd.DataFrame([mechanical_props.to_dict()])
        mechanical_props_df = pd.DataFrame(columns=['airfoil_csa', 'xcg', 'ycg'])
        mechanical_props_df = pd.concat([mechanical_props_df, mechanical_props_dict], ignore_index=True)
        geo_dep_params = pd.concat([geo_dep_params, mechanical_props_df], axis=1)
        geo_dep_params.to_csv('./data/geometry_dep_params.csv')
        print(geo_dep_params)


        calculated_parameters = pd.DataFrame(columns=['beta','beta_deg','alfa','work'])
        print(calculated_parameters)

        i += 1

if __name__ == "__main__":
    main()