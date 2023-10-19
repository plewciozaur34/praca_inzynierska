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
    
    @staticmethod
    def rpm_to_rad_s(rpm: float) -> float:
        return (rpm*2*np.pi)/60
    
    @staticmethod
    def area_calc(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float):
        return np.abs(x1 * y2 + y1 * x3 + y3 * x2 - y2 * x3 - y1 * x2 - x1 * y3)/2
    
    @staticmethod
    def plot_line_through_point(ax, point, angle_deg, length, **kwargs):
        angle_rad = np.deg2rad(angle_deg)
        dx = np.cos(angle_rad)
        dy = np.sin(angle_rad)
        start_x = point[0] - length * dx
        start_y = point[1] - length * dy
        end_x = point[0] + length * dx
        end_y = point[1] + length * dy
        ax.plot([start_x, end_x], [start_y, end_y], **kwargs)

    @staticmethod
    def find_tangential_velocity(turbine_assum) -> float:
        return turbine_assum.cx/turbine_assum.phi

    @staticmethod
    def find_mean_radious(u: float, omega: float) -> float:
        return u/omega
    
    
        
   
    #może kiedyś jak będzie czas to to zrobię
    #@staticmethod
    #def make_csv(class_name, function, columns):
        #dataframe_name = class_name.function()
        #params_dictionary = pd.DataFrame([dataframe_name.to_dict()])
        #dataframe_name = pd.DataFrame(columns=columns)
