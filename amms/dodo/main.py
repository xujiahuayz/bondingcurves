class Dodo:
    def __init__(self, reserves: list, A: float):
        self.reserves = reserves
        self.reserves_regressed = reserves
        self.A = A

    def spot_price(self, asset_in_ix: int, asset_out_ix: int, oracle_price: float):
        if self.reserves[asset_in_ix] < self.reserves_regressed[asset_in_ix]:
            exchange_rate = oracle_price * (
                1
                + self.A
                * (
                    (self.reserves[asset_in_ix] / self.reserves_regressed[asset_in_ix])
                    ** 2
                    - 1
                )
            )
        else:
            exchange_rate = oracle_price / (
                1
                + self.A
                * (
                    (
                        self.reserves[asset_out_ix]
                        / self.reserves_regressed[asset_out_ix]
                    )
                    ** 2
                    - 1
                )
            )
        return exchange_rate

    def _compute_trade_qty_out(self, qty_in: int, asset_in_ix: int, asset_out_ix: int):
        pass

    # todo: define swap amount and slappage -- simon
