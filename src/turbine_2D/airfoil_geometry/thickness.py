from typing import Dict, Union

class MaxThickness:
    def __init__(self, max_thickness: float = 0) -> None:
        self.max_thickness: float = max_thickness

    def to_dict(self: float) -> Dict[str, Union[float, str]]:
        return {'max_thickness': self.max_thickness}