import datetime
import os

from initial_turbine_settings import data_geom as dg


class SaveFigText:
    directory = None

    @staticmethod
    def save_figure(fig, idx, radii_name, part, stage=dg.stage):
        stage_part = str(stage) + part[0]
        SaveFigText.ensure_directory_initialized()
        filename = (
            f"{SaveFigText.directory}/{stage_part}_0{idx}_airfoil_{radii_name}.png"
        )
        fig.savefig(filename)

    @staticmethod
    def save_plot(fig1, fig2, fig3):
        SaveFigText.ensure_directory_initialized()
        rotor_angles = f"{SaveFigText.directory}/plots_rotor_angles.png"
        phi_reaction = f"{SaveFigText.directory}/plots_phi_reaction.png"
        stator_angles = f"{SaveFigText.directory}/plots_stator_angles.png"
        mach = f"{SaveFigText.directory}/plots_mach.png"
        fig1.savefig(rotor_angles)
        fig2.savefig(phi_reaction)
        fig3.savefig(stator_angles)
        # fig4.savefig(mach)

    @staticmethod
    def save_text_blade(otf, part):
        SaveFigText.ensure_directory_initialized()
        filename = f"{SaveFigText.directory}/blade_data_sheet_{part}.txt"
        with open(filename, "w") as f:
            f.write(otf.buffer)

    @staticmethod
    def save_turbogrid_profile(otf, part):
        SaveFigText.ensure_directory_initialized()
        filename = f"{SaveFigText.directory}/turbine_design_blade_{part}_profile.curve"
        with open(filename, "w") as f:
            f.write(otf.profile)

    @staticmethod
    def save_turbogrid_shroud(otf, part):
        SaveFigText.ensure_directory_initialized()
        filename = f"{SaveFigText.directory}/turbine_design_blade_{part}_shroud.curve"
        with open(filename, "w") as f:
            f.write(otf.shroud)

    @staticmethod
    def save_turbogrid_hub(otf, part):
        SaveFigText.ensure_directory_initialized()
        filename = f"{SaveFigText.directory}/turbine_design_blade_{part}_hub.curve"
        with open(filename, "w") as f:
            f.write(otf.hub)

    @staticmethod
    def save_turbogrid_init(otf, part):
        SaveFigText.ensure_directory_initialized()
        filename = f"{SaveFigText.directory}/turbine_design_blade_{part}_init.inf"
        with open(filename, "w") as f:
            f.write(otf.init)

    @staticmethod
    def ensure_directory_initialized():
        if not SaveFigText.directory:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            if dg.GAP_BOOL == True:
                SaveFigText.directory = os.path.join(
                    "./data/airfoils/", f"turbine_stage_{timestamp}_gap"
                )
            else:
                SaveFigText.directory = os.path.join(
                    "./data/airfoils/", f"turbine_stage_{timestamp}"
                )
            os.makedirs(SaveFigText.directory, exist_ok=True)
