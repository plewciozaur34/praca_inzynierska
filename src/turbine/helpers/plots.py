import matplotlib.pyplot as plt
import pandas as pd

from helpers.saving import SaveFigText
from turbine_3D.vector_3D import Vector3D as v3d

class DrawPlots:

    @staticmethod
    def airfoil_plots(turbine_assum, turbine_input, WS_stator, WS_rotor):
        radii = ['r_hub', 'r_2', 'r_mean', 'r_4', 'r_tip']
        beta_in, beta_out, radii_inst = v3d.sre_to_geom_data(turbine_assum, turbine_input, WS_stator, WS_rotor)

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize = (14,12))
        ax1.plot(beta_in, radii, color = '#FB5607')
        ax1.plot(beta_out, radii, color = '#FF006E')
        ax1.set_title(r'Blade angle $\beta$ for each radii')
        ax1.legend([r'$\beta_{in}$', r'$\beta_{out}$'])
        
        SaveFigText.save_plot(fig)