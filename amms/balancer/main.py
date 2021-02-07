#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

module_path = os.path.dirname(os.path.dirname(os.path.abspath(".")))

# to make it work out of the box in interactive shells
if module_path not in sys.path:
    sys.path.insert(0, module_path)


def impermanent_loss(initial_x_1: int, initial_x_2: int, pct_move: float):
    initial_exchange_rate = initial_x_2 / initial_x_1
    invariant = initial_x_1 * initial_x_2 # note that this may in fact change by the time you remove the liquidity
    exchange_rate = (1 + pct_move) * initial_exchange_rate
    x_1 = np.sqrt(invariant / exchange_rate) # (x1 * x2) / (x2 / x1) -> sqrt(x1 ** x2)
    value_if_kept = (initial_x_1 + initial_x_2 / exchange_rate) 
    value_if_remove = 2 * x_1
    l = 1 - value_if_remove / value_if_kept
    return l

# def _plot_impermanent_loss():
#   # https://medium.com/balancer-protocol/calculating-value-impermanent-loss-and-slippage-for-balancer-pools-4371a21f1a86
