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

        coin_qty = self.normalized_qty()

        # sum invariant
        self.sum_inv = coin_qty * self.n

        # product invariant
        self.prod_inv = coin_qty ** self.n

        # Initial pool share set the same as normalized total coin qty
        self.totalshares = self.sum_inv

        # # transform our aInv into StableSwap's A (not used in this class)
        # self.A = a / (n ** n)

        # # sum invariant
        # self.sum_inv = coin_qty * n

        # # product invariant
        # self.prod_inv = coin_qty ** n

    def poolsum(self):
        return sum(self.reserve)

    def poolprod(self):
        return prod(self.reserve)

    def normalized_qty(self):

        # Special case with qual size pool, no need to calculate, although results are the same
        if len(set(self.reserve)) == 1:
            q = self.reserve[0]
        else:
            sumall = self.poolsum()
            proall = self.poolprod()
            n = self.n
            a = self.a_inv

            # Special case with a=0 or 1, no need to calculate, although results are the same
            if a < 1e-10:
                q = proall ** (1/n)

            elif a == 1:
                q = (proall*sumall/n)**(1/(n+1))

            elif n == 2:
                q = (-2*6**(2/3)*proall*(a - 1) + 6**(1/3)*(proall*(9*a*sumall + sqrt(81*a**2*sumall**2 + 48*proall*(a - 1)**3)))
                     ** (2/3))/(6*(proall*(9*a*sumall + sqrt(81*a**2*sumall**2 + 48*proall*(a - 1)**3)))**(1/3))
            else:
                raise Exception('Cannot handle unequal asset pool with n>2')
        return q

    def add_liquidity(self, addamount, addindex: int):
        # update reserve
        self.reserve[addindex] += addamount

        # calculate new normalized qty
        coin_qty = self.normalized_qty()

        # new sum invariant
        sum_inv_new = coin_qty * self.n

        # newly issued shares are the difference between new and old sum_inv
        newshares = sum_inv_new - self.sum_inv

        # update sum invariant
        self.sum_inv = sum_inv_new

        # update product invariant
        self.prod_inv = coin_qty ** self.n

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
        prodexo = self.poolprod() / prod(
            [self.reserve[i] for i in [inindex, outindex]]
        ) * inres

        outres = (
            (1 - 1 / a) * D - sumexo + sqrt(
                ((1 - 1 / a) * D - sumexo) ** 2 + 4 * D * X / a / prodexo
            )) / 2

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
    plt.xlabel('$R_1$ quantity')
    plt.ylabel('$R_2$ quantity')
    plt.legend()
    plt.show()

    newpool = curvefi(900, 1100, a=500)
    newpool.sum_inv

    newpool.add_liquidity(1800, 1)
