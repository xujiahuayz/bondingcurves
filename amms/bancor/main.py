#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

module_path = os.path.dirname(os.path.dirname(os.path.abspath(".")))

# to make it work out of the box in interactive shells
if module_path not in sys.path:
    sys.path.insert(0, module_path)


class bancorPool:
    def __init__(self):
        xxx

    # https://baller.netlify.app/assets
    def impermanent_loss(asset_weights: list[float], asset_price_changes: list[float]):
        if not len(asset_weights) == len(asset_price_changes):
            raise Exception("must be of equal size")

        if not sum(asset_weights) == 1:
            raise Exception("invalid asset weights")

        value_of_pool = 1
        value_of_hodl = 0

        for i in range(len(asset_weights)):
            pct_change = 1 + asset_price_changes[i]
            weight = asset_weights[i]

            value_of_pool *= pct_change ** weight
            value_of_hodl += pct_change * weight

        # https://medium.com/balancer-protocol/calculating-value-impermanent-loss-and-slippage-for-balancer-pools-4371a21f1a86
        loss = value_of_pool / value_of_hodl - 1

        return round(-loss * 100, 4)


if __name__ == "__main__":
    l = impermanent_loss(
        [0.5, 0.5],
        [0.0, 1.0]
    )
    # x2/x1 = 1; x2/x1 = 0.5
    # 2 * sqrt(0.5) / (1.5) - 1 = -0.5719
    print(l)  # 5.7191
