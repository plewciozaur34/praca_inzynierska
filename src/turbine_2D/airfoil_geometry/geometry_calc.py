import geometry_parameters as gp
import pandas as pd
import numpy as np

geo_params = gp.GeometryParameters(0,0,0,0,0,0,0,0,0,0,0)

#dane z artykułu do sparwdzenia poprawności kodu
geo_data_r = pd.read_csv('./praca_inzynierska/data/geometry_data_rotor.csv', index_col=0)
print(geo_data_r)

geo_params.get_data(geo_data_r, 'check')
half_wedge_out = geo_params.find_half_wedge_out() #first guess, trzeba go jeszcze wcześniej iterować? do doczytania w artykule

def main():
    point1 =  geo_params.find_suction_surface_trailing_edge_tangency_point()
    #point 2 - Suction Surface Throat Point
    b2 = geo_params.beta_out + half_wedge_out + geo_params.ugt
    x2 = geo_params.chord_x - geo_params.Rte + (geo_params.throat + geo_params.Rte) * np.sin(b2)
    y2 = (2*np.pi*geo_params.R) / geo_params.Nb - (geo_params.throat + geo_params.Rte) * np.cos(b2)
    #point 3 - Suction Surface Leading Edge Tangency Point
    b3 = geo_params.beta_in + geo_params.half_wedge_in
    x3 = geo_params.Rle*(1-np.sin(b3))
    y3 = geo_params.chord_t + geo_params.Rle*np.cos(b3)
    #point 4 - Pressure Surface Leading Edge Tangency Point
    b4 = geo_params.beta_in - geo_params.half_wedge_in
    x4 = geo_params.Rle*(1+np.sin(b4))
    y4 = geo_params.chord_t - geo_params.Rle*np.cos(b4)
    #point 5 - Pressure Surface Trailing Edge Tangency Point
    b5 = geo_params.beta_out + half_wedge_out
    x5 = geo_params.chord_x - geo_params.Rte * (1-np.sin(b5))
    y5 = -geo_params.Rte * np.cos(b5)


if __name__ == "__main__":
    main()