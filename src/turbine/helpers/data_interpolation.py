from scipy.interpolate import interp1d
import csv
import os

from initial_turbine_settings import data_geom as dg

class DataInterpolation:

    path = './data/csv/interpolate_data/'
    figures_dict = {}
    csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]

    for csv_file in csv_files:
        file_path = os.path.join(path, csv_file)
        
        x_list = [] 
        y_list = [] 
        
        with open(file_path, mode='r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=';')
            
            for row in csvreader:
                x_list.append(float(row[0]))
                y_list.append(float(row[1]))

        figures_dict[csv_file[:-4]] = {'x': x_list, 'y': y_list}

    stagger_50 = interp1d(figures_dict['stagger_50']['x'], figures_dict['stagger_50']['y'], kind='slinear')
    stagger_55 = interp1d(figures_dict['stagger_55']['x'], figures_dict['stagger_55']['y'], kind='slinear')
    stagger_60 = interp1d(figures_dict['stagger_60']['x'], figures_dict['stagger_60']['y'], kind='slinear')
    stagger_65 = interp1d(figures_dict['stagger_65']['x'], figures_dict['stagger_65']['y'], kind='slinear')
    stagger_70 = interp1d(figures_dict['stagger_70']['x'], figures_dict['stagger_70']['y'], kind='slinear')
    stagger_75 = interp1d(figures_dict['stagger_75']['x'], figures_dict['stagger_75']['y'], kind='slinear')
    stagger_80 = interp1d(figures_dict['stagger_80']['x'], figures_dict['stagger_80']['y'], kind='slinear')
    tmax_c = interp1d(figures_dict['tmax_c']['x'], figures_dict['tmax_c']['y'], kind='slinear')

    @staticmethod
    def chord_t_intialization(chord_init: str, beta_in: float, beta_out: float, idx: int):
        def initialize_with_stagger(stagger_func, beta_range):
            if beta_out >= beta_range[0] and beta_out < beta_range[1]:
                stagger = stagger_func(beta_in)
                if stagger >= 20:
                    return stagger
            return None

        def initialize_with_tmax_c(beta_plus):
            chord_t = DataInterpolation.tmax_c(beta_plus)
            chord_100 = chord_t * 100
            if 4 <= chord_100 < 20:
                return chord_100
            return None
        
        def initialize_with_chord_t_value(idx):
            if 0 < dg.CHORD_T[idx] < 4:
                return dg.CHORD_T[idx]
            return None

        beta_range_funcs = {
            (50, 55): DataInterpolation.stagger_50,
            (55, 60): DataInterpolation.stagger_55,
            (60, 65): DataInterpolation.stagger_60,
            (65, 70): DataInterpolation.stagger_65,
            (70, 75): DataInterpolation.stagger_70,
            (75, 80): DataInterpolation.stagger_75,
            (80, 81): DataInterpolation.stagger_80,
        }

        while True:
            if chord_init == 'stagger_angle':
                for beta_range, stagger_func in beta_range_funcs.items():
                    result = initialize_with_stagger(stagger_func, beta_range)
                    if result:
                        print(f"Stagger angle initialized with {beta_range} range")
                        return result
                print("Can't initialize, switching to 'tmax_c_100' method")
                chord_init = 'tmax_c_100'

            elif chord_init == 'tmax_c_100':
                beta_plus = beta_in + beta_out
                result = initialize_with_tmax_c(beta_plus)
                if result:
                    return result
                print("Can't initialize, switching to 'db_dx_const' method")
                chord_init = 'db_dx_const'

            elif chord_init == 'chord_t_value':
                result = initialize_with_chord_t_value(idx)
                if result:
                    return result
                print("Can't initialize, switching to 'db_dx_const' method")
                chord_init = 'db_dx_const'

            elif chord_init == 'db_dx_const':
                return 0

            else:
                raise ValueError('Wrong chord initialization method. Check your spelling.')


