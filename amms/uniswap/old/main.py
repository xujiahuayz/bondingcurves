#!/usr/bin/env python
from amms.uniswap.utils import Token, LogHelper as l, get_amount_out, quote
import matplotlib.pyplot as plt
from typing import Any
import numpy as np
import json
import sys
import os

module_path = os.path.dirname(os.path.dirname(os.path.abspath(".")))

# to make it work out of the box in interactive shells
if module_path not in sys.path:
    sys.path.insert(0, module_path)

# workspace modules

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
            raise Exception("must be 1")
        if x_2.name != "x_2":
            raise Exception("must be 2")

        self.x_1 = x_1.qty
        self.x_2 = x_2.qty
        self.invariant = self.x_1 * self.x_2

        # plays a crucial role when you remove the liquidity
        self.liquidity = []
        self.total_supply_liquidity = -1
        self.x1s = []

        # if the pool did not exist, it gets created.
        # x_1 qty of token 1 and x_2 qty of token 2
        # gets transfered from the pool cretor into the pool (called a pair in uniswap contracts)

        l.pool_created(self)

    # DOES NOT IMPACT THE EX. RATE, CHANGES THE INVARIANT
    def add_liquidity(self, x_i: Token):
        self._update_prev()
        l.log.info(self)

        _liquidity = 0
        # compute the quote using EXISTING reserves
        reserve_x_i = self._get(x_i.name)
        reserve_x_j = self._get(x_i.complement)

        # we assume no front-running moves. otherwise this bit would be different
        # see _addLiquidity in Uniswap
        x_j = quote(
            x_i.qty, reserve_x_i, reserve_x_j
        )  # x_i * (reserve_x_j / reserve_x_i)

        # uniswap protocol fees. 0.3% on every trade, uniswap would collect 0.05% off of that if enabled
        # self._mint_fee()
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

        self.prev_invariant = self.x_1 * self.x_2  # kLast
        self._set(x_i.name, self._get(x_i.name) + x_i.qty)  # self.x_i += x_i
        self._set(x_i.complement, self._get(
            x_i.complement) + x_j)  # self.x_j += x_j
        self.invariant = self.x_1 * self.x_2

        self.x1s.append(x_i.qty)

        l.liquidity_event(self.liquidity[-1])
        l.added_liquidity(x_i, x_j, self)
        l.log.info(self)

    def remove_liquidity(self, remove_ix: int):
        if not remove_ix <= len(self.liquidity):
            return
        l.log.info(self)

        # in uniswap, liquidity first gets sent to the pair
        # then everything else is done

        # self._mint_fee()

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
        del self.x1s[remove_ix]

        l.removed_liquidity(x_1, x_2, remove_this_liquidity)
        l.log.info(self)

    def trade(self, x_i: Token):
        self._update_prev()
        l.log.info(self)

        # applies the 30 bps fee and accounts for the x_i in the updated reserves
        x_j = get_amount_out(x_i, self._get(x_i.name),
                             self._get(x_i.complement),)
        self._set(x_i.name, self._get(x_i.name) + x_i.qty)
        self._set(x_i.complement, self._get(x_i.complement) - x_j)

        l.trade_executed(x_i, x_j, self)
        l.log.info(self)

    # pct_move is for x_2 / x_1
    def _divergence_loss(self, pct_move: float):
        if not -1 <= pct_move <= 5.01:
            raise Exception("invalid pct price move. pct_move in [-1, 5]")

        curr_exchange_rate = self.x_2 / self.x_1
        new_price = (1 + pct_move) * curr_exchange_rate

        x_1 = np.sqrt(self.invariant / new_price)
        x_2 = np.sqrt(self.invariant * new_price)

        value_if_held = self.x_1 + self.x_2 / new_price
        value_removable = x_1 + x_2 / new_price

        imperm_loss = 1 - value_removable / value_if_held

        # provision_initial_x_1, provision_removable_x_1 = self.x_1 * pool_share, x_1 * pool_share
        # Case 1: 10_000 DAI intial & 100 ETH, 12_247 DAI & 81.64 ETH if ETH price goes up by 50%
        # Case 2: 10_000 DAI initial, 7_071 DAI & 141.42 ETH if the price goes down by 50% (i think)

        # Case 1 10_000 DAI + (100 ETH -> 15_000) = 25_000 DAI vs 24_495
        # Case 2 10_000 DAI + (100 ETH -> 5_000 ) = 15_000 DAI vs 14_140

        # ”divergence_loss = 2 * sqrt(price_ratio) / (1+price_ratio) — 1”

        return imperm_loss

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

    def _plot_divergence_loss(self):
        x = np.arange(-0.9999, 5.0001, 0.0001)
        y = []

        for pct_change in x:
            loss = self._divergence_loss(pct_change)
            # ! when price goes down, we can withdraw more coins than what we have deposited?
            y.append(loss)

        domain = [_x * 100 for _x in x]

        plt.plot(domain, [_y * -100 for _y in y], linewidth=2)
        # plt.plot(
        #     domain,
        #     [self._divergence_loss(1) * -100] * len(domain),
        #     linewidth=2,
        #     color="red",
        # )
        # loss = int((self._divergence_loss(1) * -100) * 10_000) / 10_000
        # plt.annotate(f"IL={loss}%", (130.0, -5.0), size=15)
        plt.title("Uniswap divergence loss")
        plt.xlabel("% change in ratio x_2 / x_1")
        plt.ylabel("divergence loss % = hold value / pool value - 1")
        return plt

    def __repr__(self):
        return (
            json.dumps(
                {
                    "x_1": self.x_1,
                    "x_2": self.x_2,
                    "invariant": self.invariant,
                    "lps": self.liquidity,
                    "total_supply_liquidity": self.total_supply_liquidity,
                },
                indent=4,
            )
            + "\n"
        )


if __name__ == "__main__":
    # example from Uniswap docs from the article
    # https://uniswap.org/docs/v2/advanced-topics/understanding-returns/#example-from-the-article
    _x_1 = Token(1, 100000e18)  # DAI
    _x_2 = Token(2, 1000e18)  # ETH
    amm = Amm(_x_1, _x_2)

    # x_1 = Token(1, 81700e18)
    # x_2 = Token(2, 1e+44/81700e18)
    # amm = Amm(x_1, x_2)

    # print(amm)

    amm._plot_divergence_loss()


# may or may not need this
# def _mint_fee(self):
#     if self.prev_invariant == -1:
#         return

#     root_k = np.sqrt(self.invariant)
#     prev_root_k = np.sqrt(self.prev_invariant)

#     if root_k <= prev_root_k:
#         return

#     liquidity = (self.total_supply_liquidity * (root_k - prev_root_k)) / (
#         5 * root_k + prev_root_k
#     )

#     # this gets sent to feeTo in Uniswap
#     self.total_supply_liquidity += liquidity
