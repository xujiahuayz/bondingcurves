from bondingcurves.amms.main import Amm


class Curve(Amm):
    def __init__(self, reserves: list[int], weights: list[float]):
        super().__init__(reserves, weights)

