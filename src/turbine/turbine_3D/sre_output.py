class SimRadEquiOutput: 
    def __init__(self, r_p: float = 0, C_x1: float = 0, C_x2: float = 0, 
                 C_u1: float = 0, C_u2: float = 0, Rn_prim: float = 0, Rn: float = 0) -> None:
        self.r_p: float = r_p
        self.C_x1: float = C_x1
        self.C_x2: float = C_x2
        self.C_u1: float = C_u1
        self.C_u2: float = C_u2
        self.Rn_prim: float = Rn_prim
        self.Rn: float = Rn

    def display(self):
        print(f"r_p: {self.r_p}, C_x1: {self.C_x1}, C_x2: {self.C_x2}, C_u1: {self.C_u1}, C_u2: {self.C_u2}, Rn_prim: {self.Rn_prim}, Rn: {self.Rn}")