#!/usr/bin/env python
# external jazz
from typing import Any
from enum import Enum
import numpy as np

# workspace modules
from amms.uniswap.utils import Token, LogHelper as l, get_amount_out, quote

MUST_SUPPLY_EQUAL_VALUES = Exception("must supply equal values")
MINIMUM_LIQUIDITY = 1000


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

        # plays a crucial role when you remove the liquidity
        self.liquidity = []
        self.total_supply_liquidity = 0

        # if the pool did not exist, it gets created.
        # x_1 qty of token 1 and x_2 qty of token 2
        # gets transfered from the pool cretor into the pool (called a pair in uniswap contracts)

        l.pool_created(self)

    # DOES NOT IMPACT THE EX. RATE, CHANGES THE INVARIANT
    def add_liquidity(self, x_i: Token):
        self._update_prev()

        _liquidity = 0
        # compute the quote using EXISTING reserves
        reserve_x_i = self._get(x_i.name)
        reserve_x_j = self._get(x_i.complement)

        # we assume no front-running moves. otherwise this bit would be different
        # see _addLiquidity in Uniswap
        x_j = quote(x_i.qty, reserve_x_i, reserve_x_j) # x_i * (reserve_x_j / reserve_x_i)

        self._mint_fee()
        if self.total_supply_liquidity == -1:
            # Will underflow if that sqrt < MINIMUM_LIQUIDITY. Is this a hack?
            _liquidity = np.sqrt(x_i.qty * x_j) - MINIMUM_LIQUIDITY

            # safemath protected in Uniswap
            if _liquidity < 0:
              _liquidity = 0

            # in Uniswap these lp tokens are sent to 0x0 address
            # so on every pool create, 1000 lp tokens get sent there
            self.total_supply_liquidity = MINIMUM_LIQUIDITY
        else:
          # these are the lp  tokens sent to the liquidity provider that called this func
          # 'liquidity exchange rate'
          _liquidity = np.min(
              [
                  x_i.qty * (self.total_supply_liquidity / reserve_x_i),
                  x_j * (self.total_supply_liquidity / reserve_x_j),
              ]
          )

        self.total_supply_liquidity += _liquidity
        # this is the simulation of sending the lp tokens to the liquidity provider
        self.liquidity.append(_liquidity)

        self.prev_invariant = self.x_1 * self.x_2 # kLast
        self._set(x_i.name, self._get(x_i.name) + x_i.qty)
        self._set(x_i.complement, self._get(x_i.complement) + x_j)
        self.invariant = self.x_1 * self.x_2

        l.liquidity_event()
        l.added_liquidity(x_i, x_j, self)

    def remove_liquidity(self, x_i: Token, remove_ix: float):
        if not remove_ix <= len(self.liquidity):
            return

        # in uniswap, liquidity first gets sent to the pair
        # then everything else is done

        # ? when would this ever happen
        self._mint_fee()

        remove_this_liquidity = self.liquidity[remove_ix]
        x_1 = self.x_1 * (remove_this_liquidity / self.total_supply_liquidity)
        x_2 = self.x_2 * (remove_this_liquidity / self.total_supply_liquidity)
        
        # this is the _burn simulation
        self.total_supply_liquidity -= remove_this_liquidity

        # now we would send back the x_1 and x_2 to the liquidity remover
        self.prev_invariant = self.invariant
        self.x_1 -= x_1
        self.x_2 -= x_2
        self.invariant = self.x_1 * self.x_2

        del self.liquidity[remove_ix]

    def trade(self, x_i: Token):
        self._update_prev()

        # applies the 30 bps fee and accounts for the x_i in the updated reserves
        x_j = get_amount_out(
            x_i,
            self._get(x_i.name),
            self._get(x_i.complement),
        )
        self._set(x_i.name, self._get(x_i.name) + x_i.qty)
        self._set(x_i.complement, self._get(x_i.complement) - x_j)

        l.trade_executed(x_i, x_j, self)

    def _get(self, name: str):
        return self.__getattribute__(name)

    def _set(self, name: str, value: Any):
        self.__setattr__(name, value)

    def _update_prev(self):
        self.prev_x_1, self.prev_x_2, self.prev_invariant = (
            self.x_1,
            self.x_2,
            self.invariant,
        )

    def _mint_fee(self):
        if self.prev_invariant == -1:
            return

        root_k = np.sqrt(self.invariant)
        prev_root_k = np.sqrt(self.prev_invariant)

        if root_k <= prev_root_k:
            return

        liquidity = (self.total_supply_liquidity * (root_k - prev_root_k)) / (
            5 * root_k + prev_root_k
        )

        # this gets sent to feeTo in Uniswap
        self.total_supply_liquidity += liquidity


if __name__ == "__main__":
    x_1 = Token(1, 100)
    x_2 = Token(2, 50)
    amm = Amm(x_1, x_2)

    amm.add_liquidity(Token(2, 30))
    amm.trade(Token(1, 55))
    amm.trade(Token(1, 23))
    amm.trade(Token(1, 100))