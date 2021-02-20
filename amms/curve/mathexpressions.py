import sympy as sp
from sympy.parsing import mathematica as M
from sympy.parsing import sympy_parser as sparser
from math import prod
from cmath import sqrt
import matplotlib.pyplot as plt
import numpy as np


def checkinv(D, xp: list[int], a):
    proall = prod(xp)
    sumall = sum(xp)
    n = len(xp)
    q = D/n
    return n*q*((-1 + a)*proall + q ** n) - a*proall*sumall


# Ds = np.arange(-6000, 6000, 1000)
# plt.plot(Ds, [checkinv(w, [500, 1900], 1) for w in Ds])
# plt.axhline(y=0)

# Ds = np.arange(1970.42, 1970.49, 0.000000001)
# plt.plot(Ds, [checkinv(w, [500, 1900], 0.1) for w in Ds])


def get_D(xp: list[int], Ann):
    S = sum(xp)
    if S == 0:
        return 0

    n_coins = len(xp)
    d_prev = 0.0
    d = float(S)
    # Ann = amplification * n_coins

    for i in range(255):
        d_p = d
        for x in xp:
            d_p = d_p * d / (x * n_coins)
        d_prev = d
        d = (Ann * S + d_p * n_coins) * d / \
            ((Ann - 1) * d + (n_coins + 1) * d_p)
        print("d", d)
        if abs(d_prev - d) <= 1:
            break

    return d


def get_D_JX(xp: list[int], a):
    proall = prod(xp)
    sumall = sum(xp)
    n = len(xp)
    sqrtand = 81*a**2*sumall**2 + 48*proall*(a - 1)**3
    # if sqrtand >= 0:
    # q = (-2*6**(2/3)*proall*(a - 1) + 6**(1/3)*(proall*(9*a*sumall + sqrt(sqrtand)))
    #      ** (2/3))/(6*(proall*(9*a*sumall + sqrt(sqrtand)))**(1/3))
    sqrtand = (proall*(9*a*sumall + sqrt(81*a**2 *
                                         sumall**2 + 48*proall*(a - 1)**3)))**(1/3)
    D = (-2*6**(2/3)*proall*(a - 1) + 6**(1/3)*sqrtand ** 2)/(3*sqrtand)
    return D.real


express2 = """
(-2 6^(2/3) (-1 + a) proall + 
 6^(1/3) (proall (9 a sumall + Sqrt[
      48 (-1 + a)^3 proall + 81 a^2 sumall^2]))^(
  2/3))/(3 (proall (9 a sumall + Sqrt[
     48 (-1 + a)^3 proall + 81 a^2 sumall^2]))^(1/3))
"""
expr2 = M.mathematica(express2)
print(expr2)

express3 = """
(Sqrt[-8 a proall sumall +
     2^(1/3) (27 (-1 + a)^2 proall^2 + Sqrt[
        proall^3 (729 (-1 + a)^4 proall + 256 a^3 sumall^3)])^(
      2/3)] - \[Sqrt](8 a proall sumall -
       2^(1/3) (27 (-1 + a)^2 proall^2 + Sqrt[
          proall^3 (729 (-1 + a)^4 proall + 256 a^3 sumall^3)])^(
        2/3) - (12 Sqrt[3] (-1 + a) proall)/
       Sqrt[(-8 a proall sumall +
        2^(1/3) (27 (-1 + a)^2 proall^2 + Sqrt[
           proall^3 (729 (-1 + a)^4 proall + 256 a^3 sumall^3)])^(
         2/3))/(27 (-1 + a)^2 proall^2 + Sqrt[
        proall^3 (729 (-1 + a)^4 proall +
           256 a^3 sumall^3)])]))/(2 2^(1/3) Sqrt[
    3] (27 (-1 + a)^2 proall^2 + Sqrt[
      proall^3 (729 (-1 + a)^4 proall + 256 a^3 sumall^3)])^(1/6))
"""

sumall = 500+900
proall = 500*900
a = 0
# q function when n=2


def normalized_qty2(sumall, proall, a):
    sqrtand = 81*a**2*sumall**2 + 48*proall*(a - 1)**3
    # if sqrtand >= 0:
    q = (-2*6**(2/3)*proall*(a - 1) + 6**(1/3)*(proall*(9*a*sumall + sqrt(sqrtand)))
         ** (2/3))/(6*(proall*(9*a*sumall + sqrt(sqrtand)))**(1/3))
    return q


# q function when n=2
def normalized_qty3(sumall, proall, a):
    q = (sqrt(
        -8*a*proall*sumall+2**(1/3)*(27*(-1+a)**2*proall**2+sqrt(
            proall ** 3*(729*(-1+a)**4*proall+256*a**3*sumall**3)))**(2/3)
    ) - sqrt(
        8*a*proall*sumall-2**(1/3)*(
            27*(-1+a)**2*proall**2+sqrt(
                proall ** 3 * (729*(-1+a)**4*proall+256*a**3*sumall**3))
        )**(2/3)-(
            12*sqrt(3)*(-1+a)*proall)/sqrt(
                (-8*a*proall*sumall + 2**(1/3)*(27*(-1+a)**2*proall**2+sqrt(proall**3*(729*(-1+a)**4*proall+256*a**3*sumall**3)))
                 ** (2/3))/(27*(-1+a)**2*proall**2+sqrt(proall**3*(729*(-1+a)**4*proall+256*a**3*sumall**3)))
        )))/(
        2*2**(1/3)*sqrt(3)*(27*(-1+a)**2*proall**2+sqrt(proall **
                                                        3*(729*(-1+a)**4*proall+256*a**3*sumall**3)))**(1/6)
    )
    return q


if __name__ == "__main__":

    expr2 = M.mathematica(express2)
    print(expr2)

    # Didn't work perfectly for some reason
    expr3 = M.mathematica(express3)
    print(expr3)

    # try equal size, each asset with quantity x
    def equal_size_q_2(x, a=15):
        q = normalized_qty2(sumall=x*2, proall=x**2, a=a)
        return q

    # should equal to input x
    equal_size_q_2(8)

    # try equal size, each asset with quantity x, check q = x
    def check_equal_size_q_2(x, a=15):
        q = normalized_qty2(sumall=x*2, proall=x**2, a=a)
        good_q = x
        return good_q-q

        # try a=1, check q = (proall * sumall / 2)**(1/2)
    def check_a1_2(sumall, proall):
        q = normalized_qty2(sumall=sumall, proall=proall, a=1)
        good_q = (proall * sumall/2)**(1/3)
        return good_q-q

    # should equal to input x
    check_equal_size_q_2(10) < 1e-10
    check_a1_2(34, 24) < 1e-10
