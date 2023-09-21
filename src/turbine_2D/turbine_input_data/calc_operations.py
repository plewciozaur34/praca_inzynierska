import data_calc as dc
import turbine_input as turbine_input

class CalcOperations:
    @staticmethod
    def turbine_input_pressure() -> float:
        p_comp_in = dc.P_INPUT #Pa 
        p_comp_out = turbine_input.tpr * p_1
        p_1 = p_comp_out #baardzo proste założenie przemiany izobarycznej w komorze spalania, docelowo do zmiany
        return p_1 
    