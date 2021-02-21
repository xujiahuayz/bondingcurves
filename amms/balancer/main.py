from amms.main import Amm

EPSILLON = 1


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

    def _compute_trade_qty_out(self, qty_in: int, asset_in_ix: int, asset_out_ix: int):
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
        updated_reserves_in_ix, updated_reserves_out_ix = self._compute_trade_qty_out(
            qty_in, asset_in_ix, asset_out_ix
        )
        self.reserves[asset_in_ix] = updated_reserves_in_ix
        self.reserves[asset_out_ix] = updated_reserves_out_ix
        return pre_trade_reserves_out_ix - self.reserves[asset_out_ix]

    def slippage(self, qty_in: int, asset_in_ix: int, asset_out_ix: int):
        updated_reserves_in_ix, updated_reserves_out_ix = self._compute_trade_qty_out(
            qty_in, asset_in_ix, asset_out_ix
        )
        spot_price = self.spot_price(asset_in_ix, asset_out_ix)

        print(f"updated_reserves_in_ix {updated_reserves_in_ix}")
        print(f"updated_reserves_out_ix {updated_reserves_out_ix}")
        print(f"1/2 {updated_reserves_in_ix / updated_reserves_out_ix}")
        print(f"spot_price {spot_price}")

        return (updated_reserves_in_ix / updated_reserves_out_ix) / spot_price - 1

    def value_pool(self, pct_change: float, asset_in_ix: int, asset_out_ix: int):
        # todo: validations in the inherited class
        exponent = 1.0 / ((self.weights[asset_in_ix] / self.weights[asset_out_ix]) + 1)
        numerator = self.reserves[asset_in_ix] * ((1 + pct_change) ** exponent)
        # equation no: 34 in the paper
        V_prime = numerator / self.weights[asset_in_ix]
        return V_prime


# if __name__ == "__main__":
#     balancer = Balancer([1_000, 1_000], [0.5, 0.5])
#     print(balancer)
#     print(balancer.divergence_loss(-0.5, 0, 1))
#     print(balancer.divergence_loss(0.5, 0, 1))
