from typing import Tuple
from combustion_params import combust_constants as cc


class CombustionHelpers:

    @staticmethod
    def find_cp_combust() -> float:
        return cc.CP_AIR*((1+cc.R_FA*(cc.I_0+ cc.I_1*cc.T - cc.I_2/cc.T**2))/(1+cc.R_FA))
    
    @staticmethod
    def find_R_combust() -> float:
        return cc.R_AIR*((1+cc.R_R*cc.R_FA)/(1+cc.R_FA))
    
    @staticmethod
    def find_kappa_combust() -> float:
        cp_combust = CombustionHelpers.find_cp_combust()
        R_combust = CombustionHelpers.find_R_combust()
        return cp_combust/(cp_combust-R_combust)
