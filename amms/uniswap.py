#!/usr/bin/env python

import logging

logging.basicConfig(level=logging.DEBUG)

l = logging.getLogger("uniswap")

MUST_SUPPLY_EQUAL_VALUES = Exception("must supply equal values")

# todo: add exchange rate & liquidity when instantiating the class
# this would enable us to debug existing Uniswap pools


class Amm:
    # x_1 - coin 1 qty.
    # x_2 - coin 2 qty.
    # This is the initial deposit.
    # The initial deposit sets the exchange rate.
    # The exchange rate (ex. rate) can vary throughout the lifetime of the pool.
    # The ex. rate is controlled by the arbers.
    # Withdrawing / depositing does not affect the ex. rate.
    # Withdrawing / depositing affects the liquidity.
    # Liquidity determined the slippage.
    # value of x_1 and x_2 does not need to be the same. In fact, this sets the initial exchange rate.
    def __init__(self, x_1: float, x_2: float):
        self.x_1 = x_1
        self.x_2 = x_2
        self.invariant = x_1 * x_2

        l.info(
            f"created pool. x_1 = {x_1}, x_2 = {x_2}. invariant {self.invariant}. ex. rate x_1/x_2 = {x_2/x_1}"
        )

    # Depositing occurs for two primary reasons.
    # (i) to earn the fees on the exchange of coins
    # (ii) to farm
    # To deposit, you will pay ERC20 approve txn cost for both coins.
    # To deposit, you will pay the cost to move your coins and register the deposit.
    # To withdraw, you will need to pay, too.
    # To deposit, you must supply equal $ value of x_1 and x_2
    def deposit(self, x_1: float = 0):
        # * this function can be simplified at an expense of readability
        # * a single parameter that takes the values supplied to both x_1 and x_2 can suffice

        # if (x_1 - x_2) >= 1e-8:
        #     raise MUST_SUPPLY_EQUAL_VALUES
        if x_1 == 0:
            return

        self.x_1 += x_1

        x_2 = self.invariant/self.x_1

        self.x_2 += x_2

        new_invariant = self.x_1 * self.x_2

        l.info(
            f"liquidity added. x_1 += {x_1}, x_2 += ${x_2}. old invariant: ${self.invariant:.8f}. new invariant: ${new_invariant:.8f}"
        )

        self.invariant = new_invariant

    def withdraw(self, x_1: float = 0, x_2: float = 0):
        if (x_1 - x_2) >= 1e-8:
            raise MUST_SUPPLY_EQUAL_VALUES
        if x_1 == 0:
            return

        self.x_1 -= x_1
        self.x_2 -= x_2

        new_invariant = self.x_1 * self.x_2

        l.info(
            f"liquidity removed. x_1 -= ${x_1}, x_2 -= ${x_2}. old invariant: ${self.invariant:.8f}. new invariant: ${new_invariant:.8f}"
        )

        self.invarinat = new_invariant

    # my x_1 gets sent into the pool, I get back x_2
    # x_1 \in R^+ and x_1 > 0
    def swap_x_1_for_x_2(self, x_1: float = 0):
        if x_1 <= 0:
            return

        old_ex_rate = self.x_2 / self.x_1

        self.x_1 += x_1
        # if the divisor was original x_1, we would get x_2
        new_x_2 = self.invariant / self.x_1
        x_2_to_send = self.x_2 - new_x_2
        self.x_2 = new_x_2

        new_ex_rate = self.x_2 / self.x_1
        # trader x_1 -> uniswap
        # uniswap x_2 -> trader
        l.info(
            f"swap x_1 for x_2. uniswap r'cvd x_1 = +${x_1}, trader r'cvd x_2 = +${x_2_to_send:.8f}. old ex. rate x1/x2 ${old_ex_rate:.8f}. new ex.rate x1/x2 ${new_ex_rate:.8f}"
        )

    # x_2 \in R^+ and x_2 > 0
    def swap_x_2_for_x_1(self, x_2: float = 0):
        if x_2 <= 0:
            return

        old_ex_rate = self.x_2 / self.x_1

        self.x_2 += x_2
        new_x_1 = self.invariant / self.x_2
        x_1_to_send = self.x_1 - new_x_1
        self.x_1 = new_x_1

        new_ex_rate = self.x_2 / self.x_1
        # trader x_2 -> uniswap
        # uniswap x_1 -> trader
        l.info(
            f"swap x_2 for x_1. uniswap r'cvd x_2 = +${x_2}, trader r'cvd x_1 = +${x_1_to_send:.8f}. old ex. rate x1/x2 ${old_ex_rate:.8f}. new ex. rate x1/x2 ${new_ex_rate:.8f}"
        )

    def trade(self, x_1: float = 0, x_2: float = 0):
        if x_1 <= 0 and x_2 <= 0:
            return
        if x_1 > 0 and x_2 > 0:
            return

        if x_1 > 0:
            self.swap_x_1_for_x_2(x_1)
        elif x_2 > 0:
            self.swap_x_2_for_x_1(x_2)


if __name__ == "__main__":
    # example #1
    x_1, x_2 = 5, 10  # depositing 5 coins #1 and 10 coins #2
    uni = Amm(x_1, x_2)
    uni.swap_x_1_for_x_2(2)
    uni.swap_x_2_for_x_1(2)
    uni.swap_x_2_for_x_1(5)
    uni.deposit(10, 10)
    uni.swap_x_2_for_x_1(1)
    uni.swap_x_1_for_x_2(4)
