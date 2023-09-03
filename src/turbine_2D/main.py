
from airfoil_geometry import geometry_parameters as gp
from airfoil_geometry import geometry_dep_params as gdp
import pandas as pd
import numpy as np


geo_params = gp.GeometryParameters()
operations = gdp.GeometryDependentParameters(geo_params)

#dane z artykułu do sparwdzenia poprawności kodu
geo_data_r = pd.read_csv('./data/geometry_data_rotor.csv', index_col=0)
print(geo_data_r)

geo_params.get_data(geo_data_r, 'check')

def main():
    point1 = geo_params.find_suction_surface_trailing_edge_tangency_point()
    point2 = geo_params.find_suction_surface_throat_point()
    point3 = geo_params.find_suction_surface_leading_edge_tangency_point()
    point4 = geo_params.find_pressure_surface_leading_edge_tangency_point()
    point5 = geo_params.find_pressure_surface_trailing_edge_tangency_point()
    operations.find_pitch()

if __name__ == "__main__":
    main()