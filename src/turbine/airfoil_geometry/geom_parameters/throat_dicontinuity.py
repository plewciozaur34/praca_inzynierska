from . import polynomial as pl
from . import circle as c
from . import point as p


class RemoveThroatDiscontinuity:
    def __init__(
        self,
        pressure_surf: "pl.Polynomial",
        suction_surf: "pl.Polynomial",
        point0: "c.Circle",
        point1: "p.Point",
        point2: "p.Point",
        point3: "p.Point",
        point4: "p.Point",
        point5: "p.Point",
    ) -> None:
        self.pressure_surf: "pl.Polynomial" = pressure_surf
        self.suction_surf: "pl.Polynomial" = suction_surf
        self.point0: "c.Circle" = point0
        self.point1: "p.Point" = point1
        self.point2: "p.Point" = point2
        self.point3: "p.Point" = point3
        self.point4: "p.Point" = point4
        self.point5: "p.Point" = point5
