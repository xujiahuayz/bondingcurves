import math

from bondingcurves.amms.main import Amm


class Curve(Amm):
    def __init__(self, reserves: list[int], leverage: float):
        n = len(reserves)
        super().__init__(reserves, [1 / n] * n)

        if leverage < 0:
            raise Exception("leverage can go from zero to infinity only")

        self.A = leverage
        self.n = n

    def spot_price(self, asset_in_ix: int, asset_out_ix: int):
        C = self._get_sum_invariant()
        X = (C / self.n) ** self.n

        amplified_prod_inv = self.A * X
        ccnn = C * ((C / self.n) ** self.n)

        numerator = self.reserves[asset_in_ix] * (
            amplified_prod_inv * self.reserves[asset_out_ix] + ccnn
        )
        denominator = self.reserves[asset_out_ix] * (
            amplified_prod_inv * self.reserves[asset_in_ix] + ccnn
        )

        return numerator / denominator

    def trade(self, qty_in: int, asset_in_ix: int, asset_out_ix: int):
        C = self._get_sum_invariant()
        X = (C / self.n) ** self.n

        # new pool sum excluding output asset
        sum_exo = sum(self.reserves) + qty_in - self.reserve[asset_out_ix]
        updated_reserves_in_ix = self.reserves[asset_in_ix] + qty_in
        # new pool product excluding output asset
        prod_exo = (
            math.prod(self.reserves)
            / (self.reserves[asset_in_ix] * self.reserves[asset_out_ix])
            * updated_reserves_in_ix
        )

        updated_reserves_out_ix = (
            (1 - 1 / self.A) * C
            - sum_exo
            + math.sqrt(
                ((1 - 1 / self.A) * C - sum_exo) ** 2 + 4 * C * X / self.A / prod_exo
            )
        ) / 2

        qty_out = self.reserve[asset_out_ix] - updated_reserves_out_ix

        self.reserve[asset_in_ix] = updated_reserves_in_ix
        self.reserve[asset_out_ix] = updated_reserves_out_ix

        return qty_out

    def slippage(self, qty_in: int, asset_in_ix: int, asset_out_ix: int):
        pass

    def _get_sum_invariant(self):
        sum_all = sum(self.reserves)
        product_all = math.prod(self.reserves)

        if self.A < 1e-10:
            sum_invariant = product_all ** (1 / self.n) * self.n

        elif self.A == 1:
            sum_invariant = (product_all * sum_all) ** (1 / (self.n + 1)) * self.n ** (
                self.n / (self.n + 1)
            )

        elif self.n == 2:
            sqrtand = (
                product_all
                * (
                    9 * self.A * sum_all
                    + math.sqrt(
                        81 * self.A ** 2 * sum_all ** 2
                        + 48 * product_all * (self.A - 1) ** 3
                    )
                )
            ) ** (1 / 3)
            suminv_complex = (
                -2 * 6 ** (2 / 3) * product_all * (self.A - 1)
                + 6 ** (1 / 3) * sqrtand ** 2
            ) / (3 * sqrtand)
            sum_invariant = suminv_complex.real
        else:
            raise Exception("cannot handle unequal asset pool with n>2")

        return sum_invariant
