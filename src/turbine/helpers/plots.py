import matplotlib.pyplot as plt
import numpy as np

from helpers.saving import SaveFigText
from turbine_3D.vector_3D import Vector3D as v3d

class DrawPlots:

    @staticmethod
    def airfoil_plots(turbine_assum, turbine_input, WS_stator, WS_rotor):
        radii = ['r_hub', 'r_2', 'r_mean', 'r_4', 'r_tip']
        beta_in, beta_out, radii_inst, alfa_in, alfa_out, phi, Rn, Mach2, Mach_rel2, Mach3, Mach_rel3 = v3d.sre_to_geom_data(turbine_assum, turbine_input, WS_stator, WS_rotor, plot=True)
        alfa1 = list(np.zeros(5))   
        for alfa in alfa1:
            alfa = turbine_assum.alfa1

        fig1, ax1 = plt.subplots(1, 1, figsize = (6,5))
        ax1.plot(radii, beta_in, color = '#FB5607')
        ax1.plot(radii, beta_out, color = '#FFBE0B')
        ax1.plot(radii, alfa_in, color = '#8338EC')
        ax1.plot(radii, alfa_out, color = '#3A86FF')
        ax1.set_title(r'Blade angle $\beta$ and $\alpha$ for each radii at rotor')
        ax1.legend([r'$\beta_2$', r'$\beta_3$', r'$\alpha_2$', r'$\alpha_3$'])

        fig2, ax2 = plt.subplots(1, 1, figsize = (6,5))
        ax2.plot(radii, phi, color = '#FFBE0B')
        ax2.plot(radii, Rn, color = '#FF006E')
        ax2.set_title(r'Flow coefficient $\phi$ and reaction Rn for each radii')
        ax2.legend([r'$\phi$', r'$R_n$'])

        fig3, ax3 = plt.subplots(1, 1, figsize = (6,5))
        ax3.plot(radii, alfa1, color = '#3A86FF')
        ax3.plot(radii, alfa_in, color = '#8338EC')
        ax3.set_title(r'Blade angle $\alpha$ for each radii at stator')
        ax3.legend([r'$\alpha_1$', r'$\alpha_2$'])

        #FIXME rozkład temperatur (i pewnie ciśnień) na łopatkach
        """ fig4, ax4 = plt.subplots(1, 1, figsize = (6,5))
        ax4.plot(radii, Mach2, color = '#FB5607')
        ax4.plot(radii, Mach3, color = '#FFBE0B')
        ax4.plot(radii, Mach_rel2, color = '#8338EC')
        ax4.plot(radii, Mach_rel3, color = '#3A86FF')
        ax4.set_title(r'Mach number/Reltive Mach numer for each radii at stator and rotor exit')
        ax4.legend([r'$M_2$', r'$M_3$', r'$M_{rel2}$', r'$M_{rel3}$'])

        SaveFigText.save_plot(fig1, fig2, fig3, fig4) """
        SaveFigText.save_plot(fig1, fig2, fig3)