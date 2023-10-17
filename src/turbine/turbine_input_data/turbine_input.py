class TurbineInput:
    def __init__(self, m_dot: float, p01: float, T01: float, tpr: float, eta_is: float, omega: float) -> None:
        self.m_dot: float = m_dot #kg/s
        self.p01: float = p01 #Pa
        self.T01: float = T01 #K
        self.tpr: float = tpr #-
        self.eta_is: float = eta_is #-
        self.omega: float = omega #rpm
