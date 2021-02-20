#!/usr/bin/env python
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
from matplotlib import cm
from typing import Tuple
import numpy as np
import sys
import os

module_path = os.path.dirname(os.path.dirname(os.path.abspath(".")))

# to make it work out of the box in interactive shells
if module_path not in sys.path:
    sys.path.insert(0, module_path)


# https://baller.netlify.app/assets
def divergence_loss(asset_weights: list[float], asset_price_changes: list[float]):
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
    avoid_divide_by_zero = 0.0001
    loss = value_of_pool / (value_of_hodl + avoid_divide_by_zero) - 1

    return round(loss * 100, 4)


def plot_divergence_loss(
    asset_weights: list[float], pct_changes: list[Tuple[float, float]]
):
    y = []
    x = []

    for pct_change in pct_changes:
        loss = divergence_loss(asset_weights, pct_change)
        # ! when price goes down, we can withdraw more coins than what we have deposited?
        y.append(loss)
        x.append(pct_change[1])

    domain = [_x * 100 for _x in x]

    plt.plot(domain, y, linewidth=2)
    plt.title("Balancer divergence loss")
    plt.xlabel("% change in ratio x_2 / x_1")
    plt.ylabel("divergence loss % = hold value / pool value - 1")
    return plt


def plot_comparison_divergence_loss(
    asset_weights: list[Tuple[float, float]], pct_changes: list[Tuple[float, float]]
):
    labels = []
    colors = ["black", "red", "green", "blue"]

    for i, asset_weight in enumerate(asset_weights):
        y = []
        x = []

        for pct_change in pct_changes:
            loss = divergence_loss(asset_weight, pct_change)
            # ! when price goes down, we can withdraw more coins than what we have deposited?
            y.append(loss)
            x.append(pct_change[1])

        domain = [_x * 100 for _x in x]
        labels.append(f"{int(asset_weight[0] * 100)}%-{int(asset_weight[1] * 100)}%")

        plt.plot(domain, y, linewidth=(4 - i), color=colors[i])

    plt.title("Divergence loss comparison for varying pool assets' weights")
    plt.xlabel(r"% change in ratio $\frac{x_2}{x_1}$")
    plt.ylabel(
        r"divergence loss % := $\left( \frac{hold \ value}{pool \ value} - 1\right)$ * 100"
    )

    plt.legend(labels=labels)
    plt.show()


def plot_3d_divergence_loss_2_assets(
    asset_weights: list[float],
    pct_changes_asset_1: list[float],
    pct_changes_asset_2: list[float],
):
    if not len(pct_changes_asset_1) == len(pct_changes_asset_2):
        raise Exception("invalid pct change lengths")

    if not sum(asset_weights) == 1.0:
        raise Exception("asset weights sum not 1")

    X, Y = [], []

    for i in range(len(pct_changes_asset_1)):
        pct_change_asset_1 = 1 + pct_changes_asset_1[i]
        pct_change_asset_2 = 1 + pct_changes_asset_2[i]

        if not pct_change_asset_1 >= 0:
            raise Exception("invalid pct change (-ve)")

        if not pct_change_asset_2 >= 0:
            raise Exception("invalid pct change (-ve)")

        X.append(pct_change_asset_1)
        Y.append(pct_change_asset_2)

    X, Y = np.meshgrid(X, Y)

    dimensions = X.shape

    if not dimensions[0] == dimensions[1]:
        # never
        raise Exception("invalid dimensions")

    if dimensions[0] * dimensions[1] > 1e6:
        raise Exception("your computer will probably die")

    Z = np.eye(dimensions[0])

    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            Z[i][j] = divergence_loss(asset_weights, [X[i][j], Y[i][j]])

    fig = plt.figure()
    ax = fig.gca(projection="3d")
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm_r, linewidth=0, antialiased=False)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter("%.02f"))

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()


if __name__ == "__main__":
    # pct_changes_asset_1 = np.arange(-1, 5.1, 0.1)
    # pct_changes_asset_2 = np.arange(-1, 5.1, 0.1)
    # plot_3d_divergence_loss_2_assets(
    #     [0.5, 0.5], pct_changes_asset_1, pct_changes_asset_2
    # )

    # pct_changes_asset_1 = np.arange(-1, 5.1, 0.1)
    # pct_changes_asset_2 = np.arange(-1, 5.1, 0.1)
    # plot_3d_divergence_loss_2_assets(
    #     [0.98, 0.02], pct_changes_asset_1, pct_changes_asset_2
    # )

    # l = divergence_loss([0.5, 0.5], [0.0, 1.0])
    # x2/x1 = 1; x2/x1 = 0.5
    # 2 * sqrt(0.5) / (1.5) - 1 = -0.5719
    # print(l)  # 5.7191

    pct_changes = [[0, i] for i in np.arange(-0.9999, 5.0001, 0.0001)]
    _ = plot_divergence_loss([0.5, 0.5], pct_changes)

