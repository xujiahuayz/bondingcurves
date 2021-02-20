from bondingcurves.amms.main import Amm


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
        ) ** (pre_trade_reserves_in_ix / self.weights[asset_out_ix])
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
        return (updated_reserves_in_ix / updated_reserves_out_ix) / self.spot_prie(
            asset_in_ix, asset_out_ix
        ) - 1


if __name__ == "__main__":
    balancer = Balancer([1_000, 1_000], [0.5, 0.5])
    print(balancer)
