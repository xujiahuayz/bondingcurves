class Dodo:
    def __init__(self, reserves: list, liq_param: float):
        self.reserves = reserves
        self.reserves_regressed = reserves
        self.liq_param = liq_param

    def spot_price(self, asset_in_ix: int, asset_out_ix: int, oracle_price: float):
        if self.reserves[asset_in_ix] < self.reserves_regressed[asset_in_ix]:
            exchange_rate = oracle_price * (
                1
                + self.liq_param
                * (
                    (self.reserves[asset_in_ix] / self.reserves_regressed[asset_in_ix])
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
                        self.reserves[asset_out_ix]
                        / self.reserves_regressed[asset_out_ix]
                    )
                    ** 2
                    - 1
                )
            )
        return exchange_rate

    def _compute_trade_qty_out(self, qty_in: int, asset_in_ix: int, asset_out_ix: int, oracle_price: float):
        pre_trade_reserves_in_ix = self.reserves[asset_in_ix]
        pre_trade_reserves_out_ix = self.reserves[asset_out_ix]
            
        resserves_regressed_in_ix = self.reserves_regressed[asset_in_ix]
        resserves_regressed_out_ix = self.reserves_regressed[asset_out_ix]
            
        updated_reserves_in_ix = pre_trade_reserves_in_ix + qty_in
            
        if self.reserves[asset_in_ix] < self.reserves_regressed[asset_in_ix]:
            qty_out = oracle_price*qty_in*(1+self.liq_param*((resserves_regressed_in_ix**2)/
                                                                                (pre_trade_reserves_in_ix*updated_reserves_in_ix)-1))
            # According to https://dodoex.github.io/docs/docs/math#the-price-curve-integral
            updated_reserves_out_ix = pre_trade_reserves_out_ix - qty_out
                
        else:
            # According to https://dodoex.github.io/docs/docs/math#solving-the-quadratic-equation-for-trading
            a = 1 - self.liq_param
            b = (self.liq_param*(resserves_regressed_out_ix**2)/pre_trade_reserves_out_ix)-pre_trade_reserves_out_ix + self.liq_param*pre_trade_reserves_out_ix - oracle_price*qty_in
            c = -self.liq_param*(resserves_regressed_out_ix)**2
                
            q2 = (-b+(b**2-4*a*c)**(1/2))/(2*a)
            
            if q2 > pre_trade_reserves_out_ix:
                qty_out = q2-pre_trade_reserves_out_ix
            else: 
                qty_out = pre_trade_reserves_out_ix-q2
            
            updated_reserves_out_ix = pre_trade_reserves_out_ix - qty_out

        return updated_reserves_in_ix, updated_reserves_out_ix

    def trade(self, qty_in: int, asset_in_ix: int, asset_out_ix: int, oracle_price: float):
        pre_trade_reserves_out_ix = self.reserves[asset_out_ix]

        updated_reserves_in_ix, updated_reserves_out_ix = self._compute_trade_qty_out(
            qty_in, asset_in_ix, asset_out_ix, oracle_price
        )
        self.reserves[asset_in_ix] = updated_reserves_in_ix
        self.reserves[asset_out_ix] = updated_reserves_out_ix
        return pre_trade_reserves_out_ix - self.reserves[asset_out_ix]

    def slippage(self, qty_in: int, asset_in_ix: int, asset_out_ix: int, oracle_price: float):
        x_1 = qty_in
        _, r_2_prime = self._compute_trade_qty_out(qty_in, asset_in_ix, asset_out_ix, oracle_price)
        x_2 = self.reserves[asset_out_ix] - r_2_prime

        p = self.spot_price(asset_in_ix, asset_out_ix, oracle_price)
        return (x_1 / x_2) / p - 1