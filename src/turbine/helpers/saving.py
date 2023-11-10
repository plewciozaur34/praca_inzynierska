import datetime
import os

from initial_turbine_settings import data_geom as dg

class SaveFigText:
    directory = None

    @staticmethod
    def save_figure(fig, idx, radii_name):
        SaveFigText.ensure_directory_initialized()
        filename = f'{SaveFigText.directory}/0{idx}_airfoil_{dg.stage_part}_{radii_name}.png'
        fig.savefig(filename)

    @staticmethod
    def save_text_blade(otf):
        SaveFigText.ensure_directory_initialized()
        filename = f'{SaveFigText.directory}/blade_data_sheet.txt'
        with open(filename, 'w') as f:
            f.write(otf.buffer)

    @staticmethod
    def save_turbogrid_profile(otf):
        SaveFigText.ensure_directory_initialized()
        filename = f'{SaveFigText.directory}/turbine_design_blade_rotor_profile.curve'
        with open(filename, 'w') as f:
            f.write(otf.profile)

    @staticmethod
    def save_turbogrid_shroud(otf):
        SaveFigText.ensure_directory_initialized()
        filename = f'{SaveFigText.directory}/turbine_design_blade_rotor_shroud.curve'
        with open(filename, 'w') as f:
            f.write(otf.shroud)

    @staticmethod
    def save_turbogrid_hub(otf):
        SaveFigText.ensure_directory_initialized()
        filename = f'{SaveFigText.directory}/turbine_design_blade_rotor_hub.curve'
        with open(filename, 'w') as f:
            f.write(otf.hub)

    @staticmethod
    def save_turbogrid_init(otf):
        SaveFigText.ensure_directory_initialized()
        filename = f'{SaveFigText.directory}/turbine_design_blade_rotor_init.inf'
        with open(filename, 'w') as f:
            f.write(otf.init)
        
    @staticmethod
    def ensure_directory_initialized():
        if not SaveFigText.directory:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            SaveFigText.directory = os.path.join('./data/airfoils/', f'{dg.stage_part}_{timestamp}')
            os.makedirs(SaveFigText.directory, exist_ok=True)
        