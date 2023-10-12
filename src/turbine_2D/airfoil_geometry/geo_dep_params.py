from typing import Dict, Union

class GeometryDependentParameters:
    def __init__(self, pitch: float = 0, stagger_angle: float = 0, chord: float = 0, zweifel_coefficient: float = 0, 
                 solidity: float = 0, blockage_in: float = 0, blockage_out: float = 0, camber_angle: float = 0, 
                 lift_coefficient: float = 0) -> None:
        self.pitch: float = pitch
        self.stagger_angle: float = stagger_angle
        self.chord: float = chord
        self.zweifel_coefficient: float = zweifel_coefficient
        self.solidity: float = solidity
        self.blockage_in: float = blockage_in
        self.blockage_out: float = blockage_out
        self.camber_angle: float = camber_angle
        self.lift_coefficient: float = lift_coefficient

    def to_dict(self: float) -> Dict[str, Union[float, str]]:
        return {'pitch': self.pitch, 'stagger_angle': self.stagger_angle, 
                'chord': self.chord, 'zweifel_coefficient': self.zweifel_coefficient, 
                'solidity': self.solidity, 'blockage_in': self.blockage_in, 
                'blockage_out': self.blockage_out, 'camber_angle': self.camber_angle,
                'lift_coefficient': self.lift_coefficient}
        
        