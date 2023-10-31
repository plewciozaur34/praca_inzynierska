import matplotlib.pyplot as plt
import datetime
import os

from initial_turbine_settings import data_geom as dg

class DrawFigures:

    @staticmethod
    def airfoil_figure(rtd, pressure_and_suction_up, radii_idx, idx):
        exes = [rtd.point1.x, rtd.point2.x, rtd.point3.x, rtd.point4.x, rtd.point5.x]
        whys = [rtd.point1.y, rtd.point2.y, rtd.point3.y, rtd.point4.y, rtd.point5.y]
        colors = ['red', 'blue', 'green', 'grey', 'pink']
        legend = ['point1', 'point2', 'point3', 'point4', 'point5']

        fig, axs = plt.subplots(1,1, figsize = (6,5))
        for x, y, color, legend in zip(exes, whys, colors, legend):
            axs.scatter(x, y, color=color, s=10, label=legend)

        #th.plot_line_through_point(axs, [rtd.point3.x, rtd.point3.y], rtd.point3.b, length=0.1, color='green', linestyle='--')
        #th.plot_line_through_point(axs, [rtd.point4.x, rtd.point4.y], rtd.point4.b, length=0.1, color='grey', linestyle='--')
        
        axs.plot(pressure_and_suction_up.xp, pressure_and_suction_up.yp, color = 'black')
        axs.plot(pressure_and_suction_up.xs, pressure_and_suction_up.ys, color = 'black')
        axs.set_title(f'Airfoil geometry for {radii_idx} for {dg.part} on stage {dg.stage}')
        axs.legend()
        #plt.show()

        radii_name = str(radii_idx[0]) + str(radii_idx[2:])
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

        directory = os.path.join('./data/airfoils/', f'{dg.stage_part}_{timestamp[:-1]}0')
        os.makedirs(directory, exist_ok=True)

        filename = f'{directory}/0{idx}_airfoil_{dg.stage_part}_{radii_name}_{timestamp}.png'
        fig.savefig(filename)