class SimRadEqiOutput: 
    def __init__(self, r_p: float = 0, Cp_x1: float = 0, Cp_x2: float = 0, 
                 Cp_u1: float = 0, Cp_u2: float = 0, Rn_prim: float = 0, Rn: float = 0) -> None:
        self.r_p: float = r_p
        self.Cp_x1: float = Cp_x1
        self.Cp_x2: float = Cp_x2
        self.Cp_u1: float = Cp_u1
        self.Cp_u2: float = Cp_u2
        self.Rn_prim: float = Rn_prim
        self.Rn: float = Rn
        