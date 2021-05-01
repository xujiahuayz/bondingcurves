from amms.main import Amm

class Balancer(Amm):
    def __init__(self, reserves: list[int], weights: list[float] = None):
        super().__init__(reserves, weights)

    def conservation_function(self):
        # todo: validations to be enforced in the inherited class
        # equatio no: 22 in the paper
        C = 1
        for i, qty in enumerate(self.reserves):
            C *= qty ** self.weights[i]
        return C

    def spot_price(self, asset_in_ix: int, asset_out_ix: int):
        # todo: validations to be enforced by the inherited class
        # equation no: 23 in the paper
        return (self.reserves[asset_in_ix] * self.weights[asset_out_ix]) / (
            self.reserves[asset_out_ix] * self.weights[asset_in_ix]
        )

    def _compute_trade_qty_out(
        self, qty_in: int, asset_in_ix: int, asset_out_ix: int
    ):
        pre_trade_reserves_in_ix = self.reserves[asset_in_ix]
        pre_trade_reserves_out_ix = self.reserves[asset_out_ix]
        # equation no: 24 in the paper
        updated_reserves_in_ix = pre_trade_reserves_in_ix + qty_in
        # equation no: 25 in the paper
        updated_reserves_out_ix = pre_trade_reserves_out_ix * (
            pre_trade_reserves_in_ix / updated_reserves_in_ix
        ) ** (self.weights[asset_in_ix] / self.weights[asset_out_ix])
        return updated_reserves_in_ix, updated_reserves_out_ix

    def trade(self, qty_in: int, asset_in_ix: int, asset_out_ix: int):
        pre_trade_reserves_out_ix = self.reserves[asset_out_ix]
        # todo: common step & validations to be enforced by the inherited class
        (
            updated_reserves_in_ix,
            updated_reserves_out_ix,
        ) = self._compute_trade_qty_out(qty_in, asset_in_ix, asset_out_ix)
        self.reserves[asset_in_ix] = updated_reserves_in_ix
        self.reserves[asset_out_ix] = updated_reserves_out_ix
        return pre_trade_reserves_out_ix - self.reserves[asset_out_ix]

    def slippage(self, qty_in: int, asset_in_ix: int, asset_out_ix: int):
        x_1 = qty_in
        _, r_2_prime = self._compute_trade_qty_out(
            qty_in, asset_in_ix, asset_out_ix
        )
        x_2 = self.reserves[asset_out_ix] - r_2_prime
        # w_1 = self.weights[asset_in_ix]
        # w_2 = self.weights[asset_out_ix]
        # r_1 = self.reserves[asset_in_ix]
        # r_1_prime, _ = self._compute_trade_qty_out(qty_in, asset_in_ix, asset_out_ix)
        # return x_1 / (r_1 * (w_2 / w_1) * (1 - (r_1 / r_1_prime) ** (w_1 / w_2))) - 1
        p = self.spot_price(asset_in_ix, asset_out_ix)
        return (x_1 / x_2) / p - 1

    def value_pool(
        self, pct_change: float, asset_in_ix: int, asset_out_ix: int
    ):
        V = self.reserves[asset_in_ix] / self.weights[asset_in_ix]
        V_prime = V * (1 + pct_change) ** self.weights[asset_out_ix]
        return V_prime
