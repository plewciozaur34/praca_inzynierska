import numpy as np

# geometria
N_EL = 50

stage = 1
part = "rotor"
stage_part = str(stage) + part[0]

NB_r = 74  # number of blade for HPT stage 2 in GE CF6-80C2B4F = 74
NB_s = 60
SOLIDITY_ASSUM = 1.2
# FIXME stagger_angle i tmax_c_100 nie działają, a działały :c
# avaliable methods: 'stagger_angle', 'tmax_c_100', 'chord_t_value', 'db_dx_const'
chord_init = "db_dx_const"
CHORD_T = [0.3, 0.4, 0.5, 0.55, 0.6]
UGT = np.linspace(5, 8, 5)
HALF_WEDGE_IN = np.linspace(6.5, 13, 5)
# 0,015c-0.05c
RTE_MULTIPLIER = 0.03
# 0.05s-0.1s
RLE_MULTIPLIER = 0.05
