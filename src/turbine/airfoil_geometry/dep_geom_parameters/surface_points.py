import numpy as np
import math

from . import mechanical_props as mp
from . import thickness as tc
from helpers.temp_helpers import TempHelpers as th
from helpers.calc_helpers import CalcOperations as co
from initial_turbine_settings import data_geom as dg


class SurfacePoints:
    def __init__(
        self,
        xs: list = list(np.zeros(dg.N_EL)),
        xp: list = list(np.zeros(dg.N_EL)),
        ys: list = list(np.zeros(dg.N_EL)),
        yp: list = list(np.zeros(dg.N_EL)),
    ) -> None:
        self.xs: list = xs
        self.xp: list = xp
        self.ys: list = ys
        self.yp: list = yp

    def surface_points(self, geo_params, rtd, nEL=dg.N_EL) -> "SurfacePoints":
        one_fifth = round(nEL / 5)
        three_fifths = round(3 * (nEL / 5))
        four_fifths = round(4 * (nEL / 5))
        point6, point7, point8, point9 = geo_params.find_points_six_seven_eight_nine()
        self.xs[0] = point8.x
        self.ys[0] = point8.y
        self.xp[0] = point8.x
        self.yp[0] = point8.y
        dxp = (rtd.point4.x - point8.x) / (one_fifth - 1)
        dxs = (rtd.point3.x - point8.x) / (one_fifth - 1)
        for i in range(1, one_fifth):
            self.xp[i] = self.xp[i - 1] + dxp
            self.yp[i] = point9.y - np.sqrt(
                geo_params.Rle**2 - (self.xp[i] - point9.x) ** 2
            )
            self.xs[i] = self.xs[i - 1] + dxs
            self.ys[i] = point9.y + np.sqrt(
                geo_params.Rle**2 - (self.xs[i] - point9.x) ** 2
            )
        dxp = (rtd.point5.x - rtd.point4.x) / (four_fifths - one_fifth)
        dxs = (rtd.point2.x - rtd.point3.x) / (three_fifths - one_fifth)
        for i in range(one_fifth, three_fifths):
            self.xp[i] = self.xp[i - 1] + dxp
            self.yp[i] = rtd.pressure_surf.a + self.xp[i] * (
                rtd.pressure_surf.b
                + self.xp[i] * (rtd.pressure_surf.c + self.xp[i] * rtd.pressure_surf.d)
            )
            self.xs[i] = self.xs[i - 1] + dxs
            self.ys[i] = rtd.suction_surf.a + self.xs[i] * (
                rtd.suction_surf.b
                + self.xs[i] * (rtd.suction_surf.c + self.xs[i] * rtd.suction_surf.d)
            )
        dxs = (rtd.point1.x - rtd.point2.x) / (four_fifths - three_fifths)
        for i in range(three_fifths, four_fifths):
            self.xp[i] = self.xp[i - 1] + dxp
            self.yp[i] = rtd.pressure_surf.a + self.xp[i] * (
                rtd.pressure_surf.b
                + self.xp[i] * (rtd.pressure_surf.c + self.xp[i] * rtd.pressure_surf.d)
            )
            self.xs[i] = self.xs[i - 1] + dxs
            self.ys[i] = rtd.point0.y + np.sqrt(
                rtd.point0.r**2 - (self.xs[i] - rtd.point0.x) ** 2
            )
        dxp = (point6.x - rtd.point5.x) / (nEL - four_fifths)
        dxs = (point6.x - rtd.point1.x) / (nEL - four_fifths)
        for i in range(four_fifths, nEL):
            self.xp[i] = self.xp[i - 1] + dxp
            if self.xp[i] > geo_params.chord_x:
                self.xp[i] = geo_params.chord_x
            self.yp[i] = point7.y - np.sqrt(
                max(geo_params.Rte**2 - (self.xp[i] - point7.x) ** 2, 0.000000)
            )

            self.xs[i] = self.xs[i - 1] + dxs
            if self.xs[i] > geo_params.chord_x:
                self.xs[i] = geo_params.chord_x
            self.ys[i] = point7.y + np.sqrt(
                max(geo_params.Rte**2 - (self.xs[i] - point7.x) ** 2, 0.000000)
            )

        return SurfacePoints(self.xs, self.xp, self.ys, self.yp)

    def mec_props(self, nEL=dg.N_EL) -> mp.MechanicalProps:
        area = co.area_calc(
            self.xs[0], self.ys[0], self.xs[1], self.ys[1], self.xp[1], self.yp[1]
        )
        xcg = (self.xs[0] + self.xs[1] + self.xp[1]) / 3 * area
        ycg = (self.ys[0] + self.ys[1] + self.yp[1]) / 3 * area
        for i in range(1, nEL - 2):
            a1 = co.area_calc(
                self.xs[i],
                self.ys[i],
                self.xs[i + 1],
                self.ys[i + 1],
                self.xp[i],
                self.yp[i],
            )
            area += a1
            xcg = xcg + (self.xs[i] + self.xs[i + 1] + self.xp[i]) / 3 * a1
            ycg = ycg + (self.ys[i] + self.ys[i + 1] + self.yp[i]) / 3 * a1
            a2 = co.area_calc(
                self.xs[i],
                self.ys[i],
                self.xp[i],
                self.yp[i],
                self.xp[i + 1],
                self.yp[i + 1],
            )
            area += a2
            xcg = xcg + (self.xs[i] + self.xp[i] + self.xp[i + 1]) / 3 * a2
            ycg = ycg + (self.ys[i] + self.yp[i] + self.yp[i + 1]) / 3 * a2
        a1 = co.area_calc(
            self.xs[nEL - 2],
            self.ys[nEL - 2],
            self.xs[nEL - 1],
            self.ys[nEL - 1],
            self.xp[nEL - 2],
            self.yp[nEL - 2],
        )
        area += a1
        xcg = xcg + (self.xs[nEL - 2] + self.xs[nEL - 1] + self.xp[nEL - 2]) / 3 * a1
        ycg = ycg + (self.ys[nEL - 2] + self.ys[nEL - 1] + self.yp[nEL - 2]) / 3 * a1
        xcg = xcg / area
        ycg = ycg / area
        return mp.MechanicalProps(area, xcg, ycg)

    def find_thickness_max(self, nEL=dg.N_EL) -> tc.MaxThickness:
        t_max = 0
        for i in range(0, nEL):
            tm = 999
            for j in range(0, nEL):
                tm = min(
                    tm,
                    np.sqrt(
                        (self.xs[i] - self.xp[j]) ** 2 + (self.ys[i] - self.yp[j]) ** 2
                    ),
                )
            t_max = max(t_max, tm)
        return tc.MaxThickness(t_max)
