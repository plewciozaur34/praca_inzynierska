import numpy as np

class TempHelpers:
    @staticmethod
    def celsius_to_kelvin(celsius: float) -> float:
        return celsius - 273.15
    
    @staticmethod
    def p2_p1_is(T2_T1: float, kappa: float) -> float:
        return T2_T1**(kappa/(kappa-1))

    @staticmethod
    def T2_T1_is(p2_p1: float, kappa: float) -> float:
        return p2_p1**(1/(kappa/(kappa-1)))

    @staticmethod
    def rad(deg: float) -> float:
        return deg*np.pi/180

    @staticmethod
    def deg(rad: float) -> float:
        return rad*180/np.pi

    @staticmethod
    def pitag(a: float, b: float) -> float:
        return np.sqrt(b*b+a*a) 

    @staticmethod
    def T_T0(M: float, kappa: float) -> float:
        return 1/(1 + (kappa-1)/2*M*M)

    @staticmethod
    def p_p0(M: float, kappa: float) -> float:
        return (TempHelpers.T_T0(M, kappa))**(kappa/(kappa-1))