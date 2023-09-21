import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from airfoil_geometry import geometry_parameters as gp
from airfoil_geometry import geometry_dep_params as gdp


geo_params = gp.GeometryParameters()
dep_params = gdp.GeometryDependentParameters(geo_params)

#dane z artykułu do sprawdzenia poprawności kodu
geo_data_r = pd.read_csv('./data/geometry_data_rotor.csv', index_col=0)

geo_params.get_data(geo_data_r, 'check')

def main():
    point1 = geo_params.find_suction_surface_trailing_edge_tangency_point()
    point2 = geo_params.find_suction_surface_throat_point()
    point3 = geo_params.find_suction_surface_leading_edge_tangency_point()
    point4 = geo_params.find_pressure_surface_leading_edge_tangency_point()
    point5 = geo_params.find_pressure_surface_trailing_edge_tangency_point()

    leading_edge_params = point3.circle(point4)
    trailing_edge_params = point1.circle(point5)

    pressure_surf_params = point4.polynomial(point5)
    suction_surf_upthroat_params = point3.polynomial(point2)
    
    #suction_surf_downthroat_params = bezier()

    leading_edge = Circle((leading_edge_params.x_0, leading_edge_params.y_0), leading_edge_params.r, fill = False, color = 'red')
    trailing_edge = Circle((trailing_edge_params.x_0, trailing_edge_params.y_0), trailing_edge_params.r, fill = False, color = 'green')

    pressure_surf = np.poly1d([pressure_surf_params.d, pressure_surf_params.c, pressure_surf_params.b, pressure_surf_params.a])
    x_pressure = np.linspace(point4.x, point5.x, 200)
    suction_surf_upthroat = np.poly1d([suction_surf_upthroat_params.d, suction_surf_upthroat_params.c, suction_surf_upthroat_params.b, suction_surf_upthroat_params.a])
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

if __name__ == "__main__":
    main()