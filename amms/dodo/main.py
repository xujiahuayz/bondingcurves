#!/usr/bin/env python
from amms.main import Amm


class Dodo(Amm):
    def __init__(self, reserves: list, liq_param: float):
        self.reserves = reserves
        self.reserves_regressed = reserves
        self.liq_param = liq_param

    def spot_price(
        self,
        asset_in_ix: int = 0,
        asset_out_ix: int = 1,
        oracle_price: float = 1,
    ):
        if self.reserves[asset_in_ix] >= self.reserves_regressed[asset_in_ix]:
            exchange_rate = oracle_price * (
                1
                + self.liq_param
                * (
                    (
                        self.reserves_regressed[asset_out_ix]
                        / self.reserves[asset_out_ix]
                    )
                    ** 2
                    - 1
                )
            )
        else:
            exchange_rate = oracle_price / (
                1
                + self.liq_param
                * (
                    (
                        self.reserves_regressed[asset_in_ix]
                        / self.reserves[asset_in_ix]
                    )
                    ** 2
                    - 1
                )
            )
        return exchange_rate

    def _compute_trade_qty_out(
        self,
        qty_in: int,
        asset_in_ix: int,
        asset_out_ix: int,
        oracle_price: float,
    ):
        pre_trade_reserves_in_ix = self.reserves[asset_in_ix]

        reserves_regressed_in_ix = self.reserves_regressed[asset_in_ix]
        reserves_regressed_out_ix = self.reserves_regressed[asset_out_ix]

        updated_reserves_in_ix = pre_trade_reserves_in_ix + qty_in

        diff = reserves_regressed_in_ix - updated_reserves_in_ix
        part_1 = (
            oracle_price * reserves_regressed_out_ix * (1 - 2 * self.liq_param)
        )
        part_2 = 1 - self.liq_param

        if updated_reserves_in_ix >= reserves_regressed_in_ix:
            updated_reserves_out_ix = (
                diff
                + part_1
                + (
                    (diff + part_1) ** 2
                    + 4
                    * self.liq_param
                    * part_2
                    * (oracle_price * reserves_regressed_out_ix) ** 2
                )
                ** (1 / 2)
            ) / (2 * oracle_price * part_2)
        else:
            updated_reserves_out_ix = reserves_regressed_out_ix + (
                diff * (self.liq_param * diff + updated_reserves_in_ix)
            ) / (oracle_price * updated_reserves_in_ix)

        return updated_reserves_in_ix, updated_reserves_out_ix

    def trade(
        self,
        qty_in: int,
        asset_in_ix: int,
        asset_out_ix: int,
        oracle_price: float,
    ):
        pre_trade_reserves_out_ix = self.reserves[asset_out_ix]

        (
            updated_reserves_in_ix,
            updated_reserves_out_ix,
        ) = self._compute_trade_qty_out(
            qty_in, asset_in_ix, asset_out_ix, oracle_price
        )
        self.reserves[asset_in_ix] = updated_reserves_in_ix
        self.reserves[asset_out_ix] = updated_reserves_out_ix
        return pre_trade_reserves_out_ix - self.reserves[asset_out_ix]

    def slippage(
        self,
        qty_in: int,
        asset_in_ix: int,
        asset_out_ix: int,
        oracle_price: float,
    ):
        x_1 = qty_in
        _, r_2_prime = self._compute_trade_qty_out(
            qty_in, asset_in_ix, asset_out_ix, oracle_price
        )
        x_2 = self.reserves[asset_out_ix] - r_2_prime

        p = self.spot_price(asset_in_ix, asset_out_ix, oracle_price)
        return (x_1 / x_2) / p - 1
