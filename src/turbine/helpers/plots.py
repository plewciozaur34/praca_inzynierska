import matplotlib.pyplot as plt
import pandas as pd

from helpers.saving import SaveFigText
from turbine_3D.vector_3D import Vector3D as v3d

class DrawPlots:

    @staticmethod
    def airfoil_plots(turbine_assum, turbine_input, WS_stator, WS_rotor):
        radii = ['r_hub', 'r_2', 'r_mean', 'r_4', 'r_tip']
        beta_in, beta_out, radii_inst, alfa_in, alfa_out, phi, Rn = v3d.sre_to_geom_data(turbine_assum, turbine_input, WS_stator, WS_rotor, plot=True)

        fig1, ax1 = plt.subplots(1, 1, figsize = (6,5))
        ax1.plot(radii, beta_in, color = '#FB5607')
        ax1.plot(radii, beta_out, color = '#FF006E')
        ax1.plot(radii, alfa_in, color = '#8338EC')
        ax1.plot(radii, alfa_out, color = '#3A86FF')
        ax1.set_title(r'Blade angle $\beta$ for each radii')
        ax1.legend([r'$\beta_2$', r'$\beta_3$', r'$\alpha_2$', r'$\alpha_3$'])

        fig2, ax2 = plt.subplots(1, 1, figsize = (6,5))
        ax2.plot(radii, phi, color = '#FFBE0B')
        ax2.plot(radii, Rn, color = '#FF006E')
        ax2.set_title(r'Flow coefficient $\phi$ and reaction Rn for each radii')
        ax2.legend([r'$\phi$', r'$R_n$'])


        
        SaveFigText.save_plot(fig1, fig2)