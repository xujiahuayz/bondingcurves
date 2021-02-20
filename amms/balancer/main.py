from bondingcurves.amms.main import Amm


class Balancer(Amm):
    def __init__(self, reserves: list[int], weights: list[float] = None):
        super().__init__(reserves, weights)

    def trade(self):
        pass


if __name__ == "__main__":
    balancer = Balancer([1_000, 1_000], [0.5, 0.5])
    print(balancer)
