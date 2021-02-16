import numpy as np
import matplotlib.pyplot as plt
from math import prod, sqrt


class curvefi:
    def __init__(self, coin_qty, n, a):

        self.reserve = [coin_qty] * n

        # number of token sorts in the pool
        self.n = n

        self.a_inv = a

        # transform our aInv into StableSwap's A
        self.A = a * (n ** n)

        D = coin_qty * n

        # sum invariant
        self.sum_inv = D

        # product invariant
        self.prod_inv = (D / n) ** n

    def poolsum(self):
        return sum(self.reserve)

    def poolprod(self):
        return prod(self.reserve)

    def exchange(self, inamount, inindex: int, outindex: int):
        a = self.a_inv
        D = self.sum_inv
        X = self.prod_inv

        # seperate input output assets from the rest of the pool
        in_out_assets = [self.reserve[i] for i in [inindex, outindex]]

        # rest of the pool sum excluding input output assets
        restsum = self.poolsum() - sum(in_out_assets)

        # rest of the pool product excluding input output assets
        restprod = self.poolprod() / prod(in_out_assets)

        # new input reserve
        inres = self.reserve[inindex] + inamount

        # pool sum excluding output asset
        sumexo = restsum + inres

        # pool product excluding output asset
        prodexo = restprod * inres

        outres = (
            (1 - 1 / a) * D
            - sumexo
            + sqrt(((1 - 1 / a) * D - sumexo) ** 2 + 4 * D * X / a / prodexo)
        ) / 2

        outamount = self.reserve[outindex] - outres

        # update input reserve
        self.reserve[inindex] = inres

        # update output reserve
        self.reserve[outindex] = outres

        return outamount


def inout(coin_qty, n, inamount, inindex: int = 0, outindex: int = 1, a=80):
    demoPool = curvefi(coin_qty, n, a=a)
    demoPool.exchange(inamount=inamount, inindex=inindex, outindex=outindex)
    return demoPool.reserve[inindex], demoPool.reserve[outindex]


def plotinout(
    coin_qty,
    n,
    inrange=np.arange(-299, 699),
    inindex=0,
    outindex=1,
    a=80,
):
    reservepair = [
        inout(
            coin_qty,
            n,
            inamount=x,
            inindex=0,
            outindex=outindex,
            a=a,
        )
        for x in inrange
    ]

    plt.plot(*zip(*reservepair), label=f"a={a}")
    plt.xlim(0, 700)
    plt.ylim(0, 700)


if __name__ == "__main__":
    oneassetreserve = 300
    n = 2

    for a in [0.0001, 1, 10, 9999999]:
        plotinout(oneassetreserve, n, a=a)
    plt.legend()
    plt.show()
