import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from airfoil_geometry import geometry_parameters as gp
from airfoil_geometry import geometry_dep_params_calc as gdpc
from helpers.temp_helpers import TempHelpers as th
from turbine_input_data import vector_of_state
from turbine_input_data import turbine_input as ti
from turbine_input_data import turbine_assum as ta
from turbine_input_data import data_calc as dc
from turbine_input_data.calc_operations import CalcOperations as co

# część obliczeniowa

#ogólna idea: na początek wyliczamy wektor stanu dla statora i wirnika i korzystając z niego wyliczamy inne 

#WEKTOR STANU: [c_axial, c_radial, c_u, p, T, r]
WS_stator = vector_of_state.VectorOfState()
WS_rotor = vector_of_state.VectorOfState()

#crusing altitude = 10,700 m #silnik GE CF6, samolot A300
#temp=-54.3 C; p=23800 Pa; M=0.78
T_01 = th.celsius_to_kelvin(dc.TIT_celsius) #K
M_1 = dc.M_1

#turbine_input = [m_dot [kg/s], p01 [Pa], T01 [K], tpr [-], eta_is [-], omega [rpm]] for LP
turbine_input = ti.TurbineInput(dc.M_DOT, 0, T_01, dc.TPR, dc.ETA_IS, dc.OMEGA)

turbine_input.p01 = co.turbine_input_pressure() / th.p_p0(M_1, dc.KAPPA)


#turbine_assum = [alfa1, alfa3, phi, c_x ..]
turbine_assum = ta.TurbineAssum(0,0,dc.PHI, dc.C_X)

#-----------------------------------------------------------------------------------------
# część geometria

geo_params = gp.GeometryParameters()
dep_params = gdpc.GeometryDependentParametersCalculation(geo_params)

#dane z artykułu do sprawdzenia poprawności kodu
geo_data_r = pd.read_csv('./data/geometry_data_rotor.csv', index_col=0)

geo_params.get_data(geo_data_r, 'check')

def main():

    #część obliczeniowa 

    u=turbine_assum.cx/turbine_assum.phi

    T_03 = turbine_input.T01/th.T2_T1_is(turbine_input.tpr, dc.KAPPA)

    D_T0 = T_03 - T_01
    #print("D_T0="+str(round(D_T0, 2)))
    d_T0 = D_T0/6 #2HP+4LP, ale trzeba znaleźć ten podział procentowy na stopnie
    
    d_T0_prim=-120 #z danych literatrowych, 120 to tak typowo, ale i 150K tam widziałam chyba
    l=dc.CP*d_T0
    d_c = l/u
    c_u3=0
    c_u2=c_u3-d_c

    WS_stator.cu = c_u2
    WS_rotor.cu = c_u3
    WS_stator.cx = turbine_assum.cx
    WS_rotor.cx = turbine_assum.cx
    
    WS_rotor.mean_calc()
    WS_rotor.work(WS_stator, turbine_input.omega)

    WS_stator.mean_calc()

    #zapisac zewnetrzny plik z danymi do profilu

    # dane2 = pd.DataFrame({'beta':[round(beta_3,2), round(beta_2,2), round(beta_3, 2)]})
    # dane = pd.concat([dane, dane2])
    # dane.index = range(1,)

    #----------------------------------------------------------------------------------------------------
    #część geometria

    point1 = geo_params.find_suction_surface_trailing_edge_tangency_point()
    point2 = geo_params.find_suction_surface_throat_point()
    point3 = geo_params.find_suction_surface_leading_edge_tangency_point()
    point4 = geo_params.find_pressure_surface_leading_edge_tangency_point()
    point5 = geo_params.find_pressure_surface_trailing_edge_tangency_point()

    leading_edge_params = point3.circle(point4)
    trailing_edge_params = point1.circle(point5)

    pressure_surf_params = point4.polynomial(point5)
    suction_surf_upthroat_params = point3.polynomial(point2)
    suction_surf_downthroat_params = point2.bezier(point1)

    leading_edge = Circle((leading_edge_params.x_0, leading_edge_params.y_0), leading_edge_params.r, fill = False, color = 'red')
    trailing_edge = Circle((trailing_edge_params.x_0, trailing_edge_params.y_0), trailing_edge_params.r, fill = False, color = 'green')

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
    axs.add_patch(leading_edge)
    axs.add_patch(trailing_edge)
    axs.plot(x_suction_upthroat, suction_surf_upthroat(x_suction_upthroat), color = 'black')
    axs.plot(x_pressure, pressure_surf(x_pressure), color = 'blue')
    plt.show()

    dep_params.find_geometry_dependent_parameters()

    geo_dep_params = pd.read_csv('./data/geometry_dep_params.csv', index_col=0)
    calculated_parameters = pd.read_csv('./data/calculated_parameters.csv', index_col=0)

if __name__ == "__main__":
    main()