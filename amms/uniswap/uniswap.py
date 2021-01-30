#!/usr/bin/env python
# external jazz
from enum import Enum

# workspace modules
from amms.logger import l
from amms.uniswap.utils import Token, LogHelper

MUST_SUPPLY_EQUAL_VALUES = Exception("must supply equal values")


class Amm:
    # x_1 - coin 1 qty.
    # x_2 - coin 2 qty.
    # This is the initial deposit.
    # The initial deposit sets the exchange rate.
    # The exchange rate (ex. rate) can vary throughout the lifetime of the pool.
    # The ex. rate is determined by the traders.
    # Withdrawing / depositing does not affect the ex. rate.
    # Withdrawing / depositing affects the liquidity.
    # Liquidity determines the slippage.
    # $ value of x_1 and x_2 does not need to be the same. In fact, this sets the initial exchange rate.
    # ------
    # @param x_1 - qty of coin 1 to deposit
    # @param x_2 - qty of coin 2 to deposit
    def __init__(self, x_1: Token, x_2: Token):
        if not x_1.i == 1:
            return Exception("must be 1")
        if not x_2.i == 2:
            return Exception("must be 2")

        self.x_1 = x_1.qty
        self.x_2 = x_2.qty
        self.invariant = self.x_1 * self.x_2
        self.lp = 0

        # if the pool did not exist, it gets created.
        # x_1 qty of token 1 and x_2 qty of token 2
        # gets transfered from the pool cretor into the pool (called a pair in uniswap contracts)

        LogHelper.pool_created(self.x_1, self.x_2, self.invariant)

    def add_liquidity(self, x_i: Token):
        prev_x_1, prev_x_2 = self.x_1, self.x_2
        prev_invariant = self.invariant

        self.__setattr__(x_i.name, self.__getattribute__(x_i.name) + x_i.qty)
        self.__setattr__(
            x_i.complement, self.invariant / self.__getattribute__(x_i.name)
        )
        self.invariant = self.x_1 * self.x_2

        LogHelper.added_liquidity(
            prev_x_1, self.x_1, prev_x_2, self.x_2, prev_invariant, self.invariant
        )

    # trading fees
    # def _mint_fee(self, new_invariant: float):

    # def remove_liquidity(self, x_i: Token):

    # my x_1 gets sent into the pool, I get back x_2
    # x_1 \in R^+ and x_1 > 0
    # def trade(self, x_i: Token):
    # if x_1 <= 0:
    #     return

    # old_ex_rate = self.x_2 / self.x_1

    # self.x_1 += x_i_qty
    # # if the divisor was original x_1, we would get x_2
    # new_x_2 = self.invariant / self.x_1
    # x_2_to_send = self.x_2 - new_x_2
    # self.x_2 = new_x_2

    # new_ex_rate = self.x_2 / self.x_1
    # # trader x_1 -> uniswap
    # # uniswap x_2 -> trader
    # l.info(
    #     f"swap x_1 for x_2. uniswap r'cvd x_1 = +${x_i_qty}, trader r'cvd x_2 = +${x_2_to_send:.8f}. old ex. rate x1/x2 ${old_ex_rate:.8f}. new ex.rate x1/x2 ${new_ex_rate:.8f}"
    # )
