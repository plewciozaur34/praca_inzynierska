import numpy as np

from . import mechanical_props as mp
from helpers.temp_helpers import TempHelpers as th

class SurfacePoints: 
    def __init__(self, xs: list, xp: list, ys: list, yp: list) -> None:
        self.xs: list = xs
        self.xp: list = xp
        self.ys: list = ys
        self.yp: list = yp

    def surface_points(self, pressure_surf, suction_serf, geo_params, point0, point1, point2, point3, point4, point5) -> 'SurfacePoints':
        point6, point7, point8, point9 = geo_params.find_points_six_seven_eight_nine()
        self.xs[0] = point8.x
        self.ys[0] = point8.y
        self.xp[0] = point8.x
        self.yp[0] = point8.y
        dxp = (point4.x-point8.x)/9
        dxs = (point3.x-point8.x)/9
        for i in range(1, 10):
            self.xp[i] = self.xp[i-1] + dxp
            self.yp[i] = point9.y - np.sqrt(geo_params.Rle**2 - (self.xp[i] - point9.x)**2)
            self.xs[i] = self.xs[i-1] + dxs
            self.ys[i] = point9.y + np.sqrt(geo_params.Rle**2 - (self.xs[i] - point9.x)**2)
        dxp = (point5.x-point4.x)/30
        dxs = (point2.x-point3.x)/20
        for i in range(10, 30):
            self.xp[i] = self.xp[i-1] + dxp
            self.yp[i] = pressure_surf.a + self.xp[i] * (pressure_surf.b + self.xp[i] * (pressure_surf.c + self.xp[i] * pressure_surf.d))
            self.xs[i] = self.xs[i-1] + dxs
            self.ys[i] = suction_serf.a + self.xs[i] * (suction_serf.b + self.xs[i] * (suction_serf.c + self.xs[i] * suction_serf.d))
        dxs = (point1.x - point2.x)/10
        for i in range(30, 40):
            self.xp[i] = self.xp[i-1] + dxp
            self.yp[i] = pressure_surf.a + self.xp[i] * (pressure_surf.b + self.xp[i] * (pressure_surf.c + self.xp[i] * pressure_surf.d))
            self.xs[i] = self.xs[i-1] + dxs
            self.ys[i] = point0.y + np.sqrt(point0.r**2 - (self.xs[i] - point0.x)**2)
        dxp = (point6.x - point5.x)/10
        dxs = (point6.x - point1.x)/10
        for i in range(40, 50):
            self.xp[i] = self.xp[i-1] + dxp
            if self.xp[i] > geo_params.chord_x:
                self.xp[i] = geo_params.chord_x 
            self.yp[i] = point7.y - np.sqrt(geo_params.Rte**2 - (self.xp[i] - point7.x)**2)
            self.xs[i] = self.xs[i-1] + dxs
            if self.xs[i] > geo_params.chord_x:
                self.xs[i] = geo_params.chord_x
            self.ys[i] = point7.y + np.sqrt(geo_params.Rte**2 - (self.xs[i] - point7.x)**2)
        return SurfacePoints(self.xs, self.xp, self.ys, self.yp)
    
    def mec_props(self) -> mp.MechanicalProps:
        area = th.area_calc(self.xs[0], self.ys[0], self.xs[1], self.ys[1], self.xp[1], self.yp[1])
        xcg = (self.xs[0] + self.xs[1] + self.xp[1])/3 * area
        ycg = (self.ys[0] + self.ys[1] + self.yp[1])/3 * area
        for i in range(1, 48):
            a1 = th.area_calc(self.xs[i], self.ys[i], self.xs[i+1], self.ys[i+1], self.xp[i], self.yp[i])
            area += a1
            xcg = xcg + (self.xs[i] + self.xs[i+1] + self.xp[i])/3 * a1
            ycg = ycg + (self.ys[i] + self.ys[i+1] + self.yp[i])/3 * a1
            a2 = th.area_calc(self.xs[i], self.ys[i], self.xp[i], self.yp[i], self.xp[i+1], self.yp[i+1])
            area += a2
            xcg = xcg + (self.xs[i] + self.xp[i] + self.xp[i+1])/3 * a2
            ycg = ycg + (self.ys[i] + self.yp[i] + self.yp[i+1])/3 * a2
        a1 = th.area_calc(self.xs[48], self.ys[48], self.xs[49], self.ys[49], self.xp[48], self.yp[48])
        area += a1
        xcg = xcg + (self.xs[48] + self.xs[49] + self.xp[48])/3 * a1
        ycg = ycg + (self.ys[48] + self.ys[49] + self.yp[48])/3 * a1
        xcg = xcg/area
        ycg = ycg/area
        return mp.MechanicalProps(area, xcg, ycg) 