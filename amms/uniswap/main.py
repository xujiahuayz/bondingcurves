from bondingcurves.amms.balancer.main import Balancer


class Uniswap(Balancer):
    def __init__(self, reserves: list[int]):
        super().__init__(reserves, [0.5, 0.5])


# if __name__ == "__main__":
#     uniswap = Uniswap([1000, 1000])
#     print(uniswap.divergence_loss(1.0, 0, 1))
#     print(uniswap.divergence_loss(-0.5, 0, 1))

