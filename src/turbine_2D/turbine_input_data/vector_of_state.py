import numpy as np
from ..helpers import temp_helpers as thpyt

class VectorOfState:
    def __init__(self, cx: float = 0, cr: float = 0, cu: float = 0, p: float = 0, 
                 T: float = 0, r: float = 0) -> None:
        self.cx: float = cx
        self.cr: float = cr
        self.cu: float = cu
        self.p: float = p
        self.T: float = T
        self.r: float = r

    def find_beta(self, phi: float) -> float:
        w_u = self.cu - self.cx / phi
        w = np.sqrt(self.cx**2 + w_u**2)
        beta = np.arccos(self.cx / w)
        return beta
    
    def find_alfa(self) -> float:
        c = np.sqrt(self.cx**2 + self.cu**2)
        alfa = np.arccos(self.cx / c)
        return alfa
    
    def find_work(self, second_vector, omega: int) -> float:
        omega_rs = th.rpm_to_rad_s(omega)
        u = omega_rs * self.r
        l = u * (self.c_u - second_vector.c_u)
        return l

    def find_Mach(self) -> float:
        return 0

    def find_Mach_rel(self) -> float:
        return 0
