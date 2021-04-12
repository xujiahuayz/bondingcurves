import numpy as np
import math
from matplotlib import pyplot as plt

from amms.main import Amm

class Uniswap_v3(Amm):
    def __init__(self, reserves: list, liq_param: float):
        self.reserves = reserves
        self.initial_reserves = reserves
        self.liq_param = liq_param

    def spot_price(
        self,
        asset_in_ix: int = 0,
        asset_out_ix: int = 1
    ):
        
        exchange_rate = (self.reserves[asset_in_ix] + self.initial_reserves[asset_in_ix]/(self.liq_param**(1/2)-1))/(self.reserves[asset_out_ix] + self.initial_reserves[asset_out_ix]/(self.liq_param**(1/2)-1))
        return exchange_rate

    def _compute_trade_qty_out(
        self,
        qty_in: int,
        asset_in_ix: int,
        asset_out_ix: int
    ):
        pre_trade_reserves_in_ix = self.reserves[asset_in_ix]

        initial_reserves_in_ix = self.initial_reserves[asset_in_ix]
        initial_reserves_out_ix = self.initial_reserves[asset_out_ix]

        updated_reserves_in_ix = pre_trade_reserves_in_ix + qty_in

        updated_reserves_out_ix = (
            (initial_reserves_in_ix*initial_reserves_out_ix)
        /(1-1/(self.liq_param**(1/2)))**2
        ) / (
            updated_reserves_in_ix + initial_reserves_in_ix/(self.liq_param**(1/2)-1)) - initial_reserves_out_ix/(self.liq_param**(1/2)-1)

        if updated_reserves_in_ix < 0 or updated_reserves_out_ix < 0:
            return np.nan, np.nan

        return updated_reserves_in_ix, updated_reserves_out_ix

    def trade(
        self,
        qty_in: int,
        asset_in_ix: int,
        asset_out_ix: int,
    ):
        pre_trade_reserves_out_ix = self.reserves[asset_out_ix]

        (
            updated_reserves_in_ix,
            updated_reserves_out_ix,
        ) = self._compute_trade_qty_out(
            qty_in, asset_in_ix, asset_out_ix
        )
        self.reserves[asset_in_ix] = updated_reserves_in_ix
        self.reserves[asset_out_ix] = updated_reserves_out_ix
        return pre_trade_reserves_out_ix - self.reserves[asset_out_ix]

    def slippage(
        self,
        qty_in: int,
        asset_in_ix: int,
        asset_out_ix: int
    ):
        x_1 = qty_in
        _, r_2_prime = self._compute_trade_qty_out(
            qty_in, asset_in_ix, asset_out_ix
        )
        x_2 = self.reserves[asset_out_ix] - r_2_prime

        p = self.spot_price(asset_in_ix, asset_out_ix)
        return (x_1 / x_2) / p - 1
    
    def value_pool(
        self, pct_change: float, asset_in_ix: int, asset_out_ix: int
    ):
        
        if pct_change >= (self.liq_param - 1):
            V_prime = self.initial_reserves[asset_in_ix] * (self.liq_param**(1/2)+1)
            dotted = 1
        elif (pct_change >= -1) and (pct_change <= (1/self.liq_param - 1)):
            V_prime = self.initial_reserves[asset_in_ix] * (self.liq_param**(1/2)+1) * (1 + pct_change)
            dotted = 1
        else:
            V_prime = (self.initial_reserves[asset_in_ix] * (2 * (1+pct_change)**(1/2) - (2+pct_change)/(self.liq_param**(1/2))))/(1 - 1/(self.liq_param**(1/2)))
            dotted = 0

        return V_prime, dotted
    
    def value_hold(
        self, pct_change: float, asset_in_ix: int, asset_out_ix: int
    ):
        V_held = self.initial_reserves[asset_in_ix] * (2 + pct_change)
        return V_held
    
    def divergence_loss(
        self, pct_change: float, asset_in_ix: int, asset_out_ix: int
    ):
        return (
            self.value_pool(pct_change, asset_in_ix, asset_out_ix)[0]
            / self.value_hold(pct_change, asset_in_ix, asset_out_ix)
            - 1
        ), self.value_pool(pct_change, asset_in_ix, asset_out_ix)[1]
