#geometria
N_EL = 50

stage = 1
part = 'rotor'
stage_part = str(stage) + part[0] 

NB = 74 #number of blade for HPT stage 2 in GE CF6-80C2B4F
SOLIDITY_ASSUM = 1.2
#avaliable methods: 'stagger_angle', 'tmax_c_100', 'chord_t_value', 'db_dx_const'
chord_init = 'db_dx_const'
CHORD_T = [0.3, 0.4, 0.5, 0.55, 0.6]
