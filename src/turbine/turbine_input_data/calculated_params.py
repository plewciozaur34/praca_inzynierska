from typing import Dict, Union

class CalcParams: 
    def __init__(self,beta: float = 0 , beta_deg: float = 0 , alfa: float = 0 , mach: float = 0, mach_rel: float = 0) -> None:
        self.beta: float = beta
        self.beta_deg: float = beta_deg
        self.alfa: float = alfa
        self.mach: float = mach
        self.mach_rel: float = mach_rel
        
    def to_dict(self: float) -> Dict[str, Union[float, str]]:
        return {'beta': self.beta, 'beta_deg': self.beta_deg, 'alfa': self.alfa, 'mach': self.mach, 'mach_rel': self.mach_rel}
    