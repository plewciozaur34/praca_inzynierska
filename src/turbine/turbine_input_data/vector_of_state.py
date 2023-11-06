import numpy as np
import inspect
import math

from helpers.temp_helpers import TempHelpers as th
from helpers.calc_helpers import CalcOperations as co
from . import calculated_params as cp
from turbine_3D.vector_3D import Vector3D as v3d


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
        w_x = self.cx
        beta = th.deg(np.arctan(w_u / w_x))
        return beta
    
    def find_alfa(self) -> float:
        alfa = th.deg(np.arctan(self.cu / self.cx))
        return alfa
     
    def find_work(self, second_vector: 'VectorOfState', omega: float, r: float) -> float:
        omega_rs = th.rpm_to_rad_s(omega)
        u = omega_rs * r
        l = u * (self.cu - second_vector.cu)
        return l

#TODO napisać find_Mach, Mach_rel 
    def find_Mach(self) -> float:
        return 0

    def find_Mach_rel(self) -> float:
        return 0

#TODO więcej funkcji find?? - co jeszcze jest potrzebne

    def mean_calc(self, phi: FloatingPointError) -> cp.CalcParams:
        print('entering mean_calc')
        
        beta = self.find_beta(phi)
        beta_deg = th.deg(beta)
        alfa = self.find_alfa()
        return cp.CalcParams(beta, beta_deg, alfa)
    
    def get_instance_name(self):
        frame = inspect.currentframe().f_back
        instance_name = [name for name, var in frame.f_locals.items() if var is self]
        return instance_name[0] if instance_name else None

    def WS_get_data(self, turbine_assum, turbine_input, name):
        r_tip, r_mean, r_hub = co.find_rtip_rhub_rmean(turbine_assum, turbine_input)
        sre_output = v3d.sre_initialise(turbine_assum, turbine_input)
        radii_inst = v3d.radius_instances(sre_output)

        position_mapping = {'rhub': 0, 'r2': 1, 'r4': 3, 'rtip': 4}
        position = name[5:]
        if position in position_mapping:
            idx = position_mapping[position]
            self.r = radii_inst[idx].r_p * r_mean
            if name[3] == 's':
                self.cu = radii_inst[idx].C_u1
                self.cx = radii_inst[idx].C_x1
            else:
                self.cu = radii_inst[idx].C_u2
                self.cx = radii_inst[idx].C_x2

    

        
