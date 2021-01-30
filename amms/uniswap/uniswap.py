#!/usr/bin/env python
# external jazz
from enum import Enum
from typing import Any

# workspace modules
from amms.uniswap.utils import Token, LogHelper as l, get_amount_out, quote

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
        if x_1.name != "x_1":
            return Exception("must be 1")
        if x_2.name != "x_2":
            return Exception("must be 2")

        self.x_1 = x_1.qty
        self.x_2 = x_2.qty
        self.invariant = self.x_1 * self.x_2
        self.lp = 0

        # if the pool did not exist, it gets created.
        # x_1 qty of token 1 and x_2 qty of token 2
        # gets transfered from the pool cretor into the pool (called a pair in uniswap contracts)

        l.pool_created(self.x_1, self.x_2, self.invariant)

    def add_liquidity(self, x_i: Token):
        prev_x_1, prev_x_2, prev_invariant = self.x_1, self.x_2, self.invariant

        self._set(x_i.name, self._get(x_i.name) + x_i.qty)
        x_j = quote(x_i.qty, self._get(x_i.name), self._get(x_i.complement))
        self._set(x_i.complement, self._get(x_i.complement) + x_j)
        self.invariant = self.x_1 * self.x_2

        l.added_liquidity(
            x_i,
            x_j,
            self.x_1,
            prev_x_1,
            self.x_2,
            prev_x_2,
            self.invariant,
            prev_invariant,
        )

    def remove_liquidity(self, x_i: Token):
        prev_x_1, prev_x_2, prev_invariant = self.x_1, self.x_2, self.invariant

    def trade(self, x_i: Token):
        prev_x_1, prev_x_2, prev_invariant = self.x_1, self.x_2, self.invariant

        x_j = get_amount_out(
            x_i,
            self._get(x_i.name),
            self._get(x_i.complement),
        )

        self._set(x_i.name, self._get(x_i.name) + x_i.qty)
        self._set(x_i.complement, self._get(x_i.complement) - x_j)

        l.trade_executed(
            x_i,
            x_j,
            self.x_1,
            prev_x_1,
            self.x_2,
            prev_x_2,
            self.invariant,
            prev_invariant,
        )

        return x_j

    def _get(self, name: str):
        return self.__getattribute__(name)

    def _set(self, name: str, value: Any):
        self.__setattr__(name, value)


if __name__ == "__main__":
    x_1 = Token(1, 100)
    x_2 = Token(2, 50)
    amm = Amm(x_1, x_2)

    amm.add_liquidity(Token(2, 30))
    amm.trade(Token(1, 55))
    amm.trade(Token(1, 23))
    amm.trade(Token(1, 100))