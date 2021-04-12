import numpy as np
import matplotlib.pyplot as plt
from math import prod, sqrt
import cmath


class curvefi:
    def __init__(self, *args, a):

        self.reserve = list(args)

        # number of token sorts in the pool
        self.n = len(args)

        self.a_inv = a

        # sum invariant
        self.sum_inv = self.get_suminv()

        # product invariant
        self.prod_inv = (self.sum_inv / self.n) ** self.n

        # Initial pool share set the same as normalized total coin qty
        self.totalshares = self.sum_inv

    def poolsum(self):
        return sum(self.reserve)

    def poolprod(self):
        return prod(self.reserve)

    def get_suminv(self):
        sumall = self.poolsum()

        # Special case with qual size pool, no need to calculate, although results are the same
        if len(set(self.reserve)) == 1:
            suminv = sumall
        else:
            n = self.n
            proall = self.poolprod()
            a = self.a_inv

            # Special case with a=0 or 1, no need to calculate, although results are the same
            if a < 1e-10:
                suminv = proall ** (1 / n) * n

            elif a == 1:
                suminv = (proall * sumall) ** (1 / (n + 1)) * n ** (
                    n / (n + 1)
                )

            elif n == 2:
                sqrtand = (
                    proall
                    * (
                        9 * a * sumall
                        + sqrt(
                            81 * a ** 2 * sumall ** 2
                            + 48 * proall * (a - 1) ** 3
                        )
                    )
                ) ** (1 / 3)
                suminv_complex = (
                    -2 * 6 ** (2 / 3) * proall * (a - 1)
                    + 6 ** (1 / 3) * sqrtand ** 2
                ) / (3 * sqrtand)
                suminv = suminv_complex.real
            else:
                raise Exception("Cannot handle unequal asset pool with n>2")
        return suminv

    def add_liquidity(self, addamount, addindex: int):
        # update reserve
        self.reserve[addindex] += addamount

        # new sum invariant
        sum_inv_new = self.get_suminv()

        # newly issued shares are the difference between new and old sum_inv
        newshares = sum_inv_new - self.sum_inv

        # update sum invariant
        self.sum_inv = sum_inv_new

        # update product invariant
        self.prod_inv = (sum_inv_new / self.n) ** self.n

        return newshares

    def exchange(self, inamount, inindex: int, outindex: int):
        a = self.a_inv
        D = self.sum_inv
        X = self.prod_inv

        # new pool sum excluding output asset
        sumexo = self.poolsum() + inamount - self.reserve[outindex]

        # new input reserve
        inres = self.reserve[inindex] + inamount

        # new pool product excluding output asset
        prodexo = (
            self.poolprod()
            / prod([self.reserve[i] for i in [inindex, outindex]])
            * inres
        )

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


def inout(*args, inamount, inindex: int = 0, outindex: int = 1, a=80):
    demoPool = curvefi(*args, a=a)
    demoPool.exchange(inamount=inamount, inindex=inindex, outindex=outindex)
    return demoPool.reserve[inindex], demoPool.reserve[outindex]


def plotinout(
    *args,
    inrange=np.arange(-299, 699),
    inindex=0,
    outindex=1,
    a=80,
):
    reservepair = [
        inout(
            *args,
            inamount=x,
            inindex=0,
            outindex=outindex,
            a=a,
        )
        for x in inrange
    ]

    plt.plot(*zip(*reservepair), label=f"$a={a}$")
    plt.xlim(0, 1000)
    plt.ylim(0, 2000)


if __name__ == "__main__":
    qty1 = 500
    qty2 = 500
    # n = 6

    for a in [1e-12, 1, 10, 1e20]:
        plotinout(qty1, qty2, a=a)
    plt.scatter(qty1, qty2, label="inital state")
    plt.xlabel("$R_1$ quantity")
    plt.ylabel("$R_2$ quantity")
    plt.legend()
    plt.show()

    newpool = curvefi(900, 1100, a=500)
    newpool.sum_inv

    newpool.add_liquidity(1800, 1)
