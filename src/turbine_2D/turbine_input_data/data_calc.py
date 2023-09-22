from combustion_params import fuel_parameters as fp

#dane wejściowe dla obliczeń calc_2D.py
TIT_celsius = 1297
M_1 = 0.78
M_DOT = 658
TPR = 30.2
ETA_IS = 0.9
OMEGA = 3800
P_INPUT = 23800
PHI = 0.8
C_X = 230

KAPPA = fp.CombustionHelpers.find_kappa_combust()
CP = fp.CombustionHelpers.find_cp_combust()
R_COMB = fp.CombustionHelpers.find_R_combust()

#0.5<phi<1.0
#c_x - na podstawie danych z examples z principles of turbomachinery...
