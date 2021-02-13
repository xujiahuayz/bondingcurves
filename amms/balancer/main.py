#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

module_path = os.path.dirname(os.path.dirname(os.path.abspath(".")))

# to make it work out of the box in interactive shells
if module_path not in sys.path:
    sys.path.insert(0, module_path)


# https://baller.netlify.app/assets
def impermanent_loss(asset_weights: list[float], asset_price_changes: list[float]):
    if not len(asset_weights) == len(asset_price_changes):
        raise Exception("must be of equal size")

    if not sum(asset_weights) == 1:
        raise Exception("invalid asset weights")

    value_of_pool = 1
    value_of_hodl = 0
    # V = q_1^(w_1) * q_2^(w_2) * ... * q_n^(w_n)
    # sum(w_i) = 1
    # orginal pool value at t_0 == 1 USD
    # value_1 : value_2 = w_1 : w_2
    # p_1, p_2, p_3 all denominated in  USD value per one token unit
    # value of hold at t' = q_1 * p_1' + ... + q_n * p_n'
    # =  w_i / p_i * p_1 * (1 + price_change_1) * ... = w_1 * (1 + price_change_1)
    # q_i = w_i / p_i
    # p_1 --> p_1' = p_1 * (1 + price_change_1)
    # (q_1' * p_1') : (q_2' * p_2) = w_1 : w_2 == > q_1' = w_1 * (q_2' * p_2) / (p_1' * w_2)
    # q_1^(w_1) * q_2^(w_2) =  q_1'^(w_1) * q_2'^(w_2) = [w_1 * ((q_2' * p_2) / (p_1' * w_2))] ^ (w_1) * q_2'^(w_2)
    # q_1^(w_1) * q_2^(w_2) = [w_1 * q_2' * p_2 / ( p_1' * w_2) ] ^ (w_1) * q_2'^(w_2)
    # ----
    # q_1' -->  (q_1^(w_1)) ^ (1/w_1)
    for i in range(len(asset_weights)):
        pct_change = 1 + asset_price_changes[i]
        weight = asset_weights[i]

        # V = q_1^(w_1) * q_2^(w_2) * ... * q_n^(w_n)
        # pool_value = p1 * q_1 + p2 * q_2 + ...
        # pool_value = (p1 * q_1)/ w_1
        # pool_value' = (p1' * q_1')/ w_1
        # p1' = (1 + asset_price_change) * p1
        # (p1' * q_1') / (p1 * q_1) = ((1 + asset_price_change) * q1') / q1)
        # poo_value'/ pool_value  = (pct_change * q_i')/ q_i
        # q_1^w_1 * q_2^w_2  = q_1'^w_1 * q_2'^w_2 = q_1'^w_1 * (q_1'*price_change*w_2) ^ w_2
        # q_1'*price_change / q_2' = w_1/w_2
        value_of_pool *= (
            pct_change ** weight
        )  # = pct_change * q_i'/ q_i => q_i' = q_i * (pct_change ** (weight-1))
        value_of_hodl += pct_change * weight
        # uniswap x * (1.1 ** 0.5) *  y * (1.0 ** 0.5) = k
        # uniswap initial pool value = 1 unit => 0.5 unit worth of q1 and 0.5 unit worth of q2
        # token 1 doubles in price and token 2 does not move
        # how did the pool value change now?
        # when token1 doubles in price, its value must be swapped out of the pool to keep k constant
        # token1 doubles in price => q2' / q1' = 2 * (q2 / q1)
        # how to express the

        # let newPool percentage change := x;
        # originalPoolValue = q_1 * 1 /w_1
        # newPoolValue = (q_1 * 1 /w_1) * x = (q_1' * pct_change)/ w_1
        # q_1' = x * q_1 / pct_change
        # q_2 = originalPoolValue * w_2 / price_2
        # q_2' = originalPoolValue * x * w_2 / price_2 ==> q_2' = q_2 * x
        # (x * q_1 / pct_change_1)^w_1 * (q_2 * x)^w_2 * (q_3 * x)^w_3 ... =
        # = x^(w_1 + ..w_k) / (pct_change_1^w_1) * {(q_1)^w_1 * (q_2)^w_2 * (q_3)^w_3} =
        # (q_1)^w_1 * (q_2)^w_2 * (q_3)^w_3
        # x  =  (pct_change_1^w_1)

    # https://medium.com/balancer-protocol/calculating-value-impermanent-loss-and-slippage-for-balancer-pools-4371a21f1a86
    loss = value_of_pool / value_of_hodl - 1

    return round(loss * 100, 4)


if __name__ == "__main__":
    l = impermanent_loss([0.5, 0.5], [0.0, 1.0])
    # x2/x1 = 1; x2/x1 = 0.5
    # 2 * sqrt(0.5) / (1.5) - 1 = -0.5719
    # print(l)  # 5.7191
