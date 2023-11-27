from typing import Dict, Union


class MechanicalProps:
    def __init__(self, airfoil_csa: float = 0, xcg: float = 0, ycg: float = 0) -> None:
        self.airfoil_csa: float = airfoil_csa
        self.xcg: float = xcg
        self.ycg: float = ycg

    def to_dict(self: float) -> Dict[str, Union[float, str]]:
        return {"airfoil_csa": self.airfoil_csa, "xcg": self.xcg, "ycg": self.ycg}
