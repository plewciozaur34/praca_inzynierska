class TurbineAssum:
    def __init__(self, alfa1: float, alfa3: float, phi: float, cx: float, lambda_n: float, rhub_rtip: float) -> None:
        self.alfa1: float = alfa1 #rad
        self.alfa3: float = alfa3 #rad
        self.phi: float = phi 
        self.cx: float = cx #m/s
        self.lambda_n: float = lambda_n
        self.rhub_rtip: float = rhub_rtip
