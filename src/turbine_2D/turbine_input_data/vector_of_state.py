import numpy as np

class VectorOfState:
    def __init__(self, cx: float, cr: float, cu: float, p: float, T: float, r: float) -> None:
        self.cx: float = cx
        self.cr: float = cr
        self.cu: float = cu
        self.p: float = p
        self.T: float = T
        self.r: float = r

    def __init__(self) -> None:
        self.cx: float = 0
        self.cr: float = 0
        self.cu: float = 0
        self.p: float = 0
        self.T: float = 0
        self.r: float = 0

    def find_beta(self, phi: float) -> float:
        w_u = self.cu - self.cx / phi
        w = np.sqrt(self.cx**2 + w_u**2)
        beta = np.arccos(self.cx / w)
        return beta
    
    def find_alfa(self) -> float:
        return 0
    
    def find_work(self, omega: int) -> float:
        return 0

    def find_Mach(self) -> float:
        return 0

    def find_Mach_rel(self) -> float:
        return 0
