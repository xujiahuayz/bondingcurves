import math

from bondingcurves.amms.main import Amm

# we are dealing with integer mathematics everywhere, so this is the epsillon
EPSILLON = 1


class Curve(Amm):
    def __init__(self, reserves: list[int], leverage: float):
        n = len(reserves)
        super().__init__(reserves, [1 / n] * n)

        if leverage < 0:
            raise Exception("leverage can go from zero to infinity only")

        self.A = leverage
        self.n = n

    def _spot_price(self, updated_reserves_in: int, updated_reserves_out: int):
        """Used for implicit divergence loss computation only. This is a modified
      version of spot_price, where we do not update the state of the instance.

      Args:
          updated_reserves_in (int): reserves of in asset with which to compute the
          spot price
          updated_reserves_out (int): reserves of out asset with which to compute the
          spot price

      Returns:
          [float]: new spot price
      """
        C = self._get_sum_invariant()
        X = (C / self.n) ** self.n

        amplified_prod_inv = self.A * X
        ccnn = C * ((C / self.n) ** self.n)

        numerator = updated_reserves_in * (
            amplified_prod_inv * updated_reserves_out + ccnn
        )
        denominator = updated_reserves_out * (
            amplified_prod_inv * updated_reserves_in + ccnn
        )

        return float(numerator) / denominator

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

        return float(numerator) / denominator

    def _compute_trade_qty_out(self, qty_in: int, asset_in_ix: int, asset_out_ix: int):
        C = self._get_sum_invariant()
        X = (C / self.n) ** self.n

        # new pool sum excluding output asset
        sum_exo = sum(self.reserves) + qty_in - self.reserves[asset_out_ix]
        updated_reserves_in_ix = self.reserves[asset_in_ix] + qty_in
        # new pool product excluding output asset
        prod_exo = (
            math.prod(self.reserves)
            / (self.reserves[asset_in_ix] * self.reserves[asset_out_ix])
            * updated_reserves_in_ix
        )

        # + EPSILLON everywhere here to avoid division by zero
        updated_reserves_out_ix = (
            (1 - 1 / (self.A + EPSILLON)) * C
            - sum_exo
            + math.sqrt(
                ((1 - 1 / (self.A + EPSILLON)) * C - sum_exo) ** 2
                + 4 * C * X / (self.A + EPSILLON) / prod_exo
            )
        ) / 2

        return updated_reserves_in_ix, updated_reserves_out_ix

    def trade(self, qty_in: int, asset_in_ix: int, asset_out_ix: int):
        updated_reserves_in_ix, updated_reserves_out_ix = self._compute_trade_qty_out(
            qty_in, asset_in_ix, asset_out_ix
        )

        self.reserve[asset_in_ix] = updated_reserves_in_ix
        self.reserve[asset_out_ix] = updated_reserves_out_ix

        return self.reserve[asset_out_ix] - updated_reserves_out_ix

    def slippage(self, qty_in: int, asset_in_ix: int, asset_out_ix: int):
        updated_reserves_in_ix, updated_reserves_out_ix = self._compute_trade_qty_out(
            qty_in, asset_in_ix, asset_out_ix
        )
        p = self.spot_price(asset_in_ix, asset_out_ix)
        return (updated_reserves_in_ix / updated_reserves_out_ix) / p - 1

    # ! notice that the signature here is different to the one in Amm
    # ! this one is missing pct_change. Rather it is computed implicitly.
    def divergence_loss(self, qty_in: int, asset_in_ix: int, asset_out_ix: int):
        # for different quantities of asset_in_ix, figure out what is the percentage change
        # then plot divergence loss versus this percentage change

        # todo: this is the same as in Amm. This is not DRY
        if qty_in < 0:
            if self.reserves[asset_in_ix] < -qty_in:
                raise Exception("invalid quantity to deplete")

        # pct_change is the percentage change in the spot price

        pre_trade_spot_price = self._spot_price(
            self.reserves[asset_in_ix], self.reserves[asset_out_ix]
        )
        updated_reserves_in_ix, updated_reserves_out_ix = self._compute_trade_qty_out(
            qty_in, asset_in_ix, asset_out_ix
        )
        post_trade_spot_price = self._spot_price(
            updated_reserves_in_ix, updated_reserves_out_ix
        )
        pct_change = post_trade_spot_price / pre_trade_spot_price - 1

        # now return divergence loss and pct_change
        value_pool = (
            updated_reserves_in_ix + updated_reserves_out_ix * post_trade_spot_price
        )

        return (
            pct_change,
            value_pool / self.value_hold(pct_change, asset_in_ix, asset_out_ix) - 1,
        )

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


if __name__ == "__main__":
    curve = Curve([1_000, 2_000], 0)

    # when leverage is zero, we are reducing to constant sum
    print(curve.divergence_loss(100, 0, 1))
