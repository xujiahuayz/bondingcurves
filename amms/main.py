# other dexes to inherit from this class
class Amm:
    def __init__(self, reserves: list[int], weights: list[float] = None):
        for qty in reserves:
            self._validate_reserves(qty)

        self.reserves = reserves
        self.initial_reserves = reserves

        self.weights = None
        if weights is not None:
            self._validate_len_of_reserves_and_weights(reserves, weights)
            self._validate_weights(weights)
            self.weights = weights

    def trade(self, qty_in: int, asset_in_ix: int, asset_out_ix: int):
        """Simulates a DEX trade

      Args:
          qty_in (int): Qty of the traded asset. If positive, you are swapping
          this asset in return for asset at asset_ix. Similarly, if this is
          negative, then this is the amount you will get OUT of the DEX and you
          will be paying with the asset at asset_ix in the self.reserves.
          asset_in_ix (int): This is the index of the asset associated with the
          qty_in parameter, if qty_in is positive. asset_out_ix is then the index
          of the asset that you wish to get out of the pool.
          asset_out_ix (int): This is the index of the asset you will be getting
          out of the pool. If qty_in is negative, then asset_out_ix must the index
          of this asset that you are depleting the pool of.
      """
        self._validate_trade(qty_in, asset_in_ix, asset_out_ix)
        raise Exception("must be implemented")

    def conservation_function(self):
        raise Exception("must be implemented")

    def _validate_asset_ix(self, asset_ix: int):
        if asset_ix < 0 or asset_ix >= len(self.reserves):
            raise Exception("invalid asset ix")

    def _validate_trade(self, qty_in: float, asset_in_ix: int, asset_out_ix: int):
        self._validate_asset_ix(asset_in_ix)
        self._validate_asset_ix(asset_out_ix)

        if qty_in < 0:
            if self.reserves[asset_in_ix] < -qty_in:
                raise Exception("you cannot remove this much from the liquidity pool")

    @staticmethod
    def _validate_len_of_reserves_and_weights(
        reserves: list[int], weights: list[float]
    ):
        if len(reserves) != len(weights):
            raise Exception("reserves length and weights length must be the same")

    @staticmethod
    def _validate_reserves(qty: int):
        if qty <= 0:
            raise Exception("asset quantity must be greater than zero")

    @staticmethod
    def _validate_weights(weights: list[float]):
        if not sum(weights) == 1:
            raise Exception("asset weights do not sum to 1.0")

    def __repr__(self):
        return f"Amm(assets_qty={self.reserves},assets_weights={self.weights})"


# spec for the general AMM:
# 1. Hold value is always the same no matter the DEX
# 2. Pool value will be different for each DEX
# 3. Trade funcs will depend on the conservation function of each DEX
# 4. Slippage depends on the price prior to the trade and afterwards
# 5. Divergence loss is the function of the hold value (same for all)
# and pool value (different for all)
