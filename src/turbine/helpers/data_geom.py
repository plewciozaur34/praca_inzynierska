#geometria
N_EL = 50

stage = 1
part = 'rotor'
radius = 'r_mean'
stage_part = str(stage) + part[0] + '_' + str(radius[0]) + str(radius[2:])

#geometry input data dictionary

geo_input_rotor = {'index': 'r_mean', 'R': 0, 'chord_x': 0, 'chord_t': 0, 'ugt': 0, 'beta_in': 0.0, 
                 'half_wedge_in': 0, 'Rle': 0, 'beta_out': 0.0, 'Rte': 0, 'Nb': 0,
                'throat': 0, 'half_wedge_out': 0}