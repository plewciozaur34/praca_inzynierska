class GeometryDependentParameters:
    def __init__(self, half_wedge_out: float = 0, pitch: float = 0, stagger_angle: float = 0, airfoil_csa: float = 0,
                 chord: float = 0, zweifel_coefficient: float = 0, solidity: float = 0, xcg: float = 0, 
                 ycg: float = 0, blockage_in: float = 0, blockage_out: float = 0, camber_angle: float = 0, 
                 lift_coefficient: float = 0) -> None:
        self.half_wedge_out: float = half_wedge_out
        self.pitch: float = pitch
        self.stagger_angle: float = stagger_angle
        self.airfoil_csa: float = airfoil_csa
        self.chord: float = chord
        self.zweifel_coefficient: float = zweifel_coefficient
        self.solidity: float = solidity
        self.xcg: float = xcg
        self.ycg: float = ycg
        self.blockage_in: float = blockage_in
        self.blockage_out: float = blockage_out
        self.camber_angle: float = camber_angle
        self.lift_coefficient: float = lift_coefficient
        
        