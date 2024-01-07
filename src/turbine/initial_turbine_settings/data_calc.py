from combustion_params import fuel_parameters as fp
from helpers.temp_helpers import TempHelpers as th

# dane wejściowe dla obliczeń calc_2D.py
TIT_celsius = 1330
M_1 = 0.78
M_DOT = 658
TPR = 30.2
ETA_IS = 0.9
OMEGA = 3800
H = 10700
PHI = 0.7
# PHI = 0.8
# C_X = 230
C_X = 280
RH_RT = 0.8
LAMBDA_N = 0.05
ALFA1 = 0
ALFA2 = 0

KAPPA = fp.CombustionHelpers.find_kappa_combust()
CP = fp.CombustionHelpers.find_cp_combust()
R_COMB = fp.CombustionHelpers.find_R_combust()

MU = 4.7627e-05  #wartość dla powietrza, nie dla spalin

T_01 = th.celsius_to_kelvin(TIT_celsius)  # K

# 0.5<phi<1.0
# c_x - na podstawie danych z examples z principles of turbomachinery...
# crusing altitude = 10,700 m #silnik GE CF6, samolot A300
# temp=-54.3 C; p=23800 Pa; M=0.78
