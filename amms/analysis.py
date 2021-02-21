import matplotlib.pyplot as plt
import numpy as np

from amms.balancer.main import Balancer
from amms.uniswap.main import Uniswap
from amms.curve.main import Curve


DP18 = 1e18
X1 = 1_000 * DP18
X2 = 1_000 * DP18


class Analysis:
    def __init__(self):
        self.balancer_95_5 = Balancer([X1, X2], [0.95, 0.05])
        self.balancer_98_2 = Balancer([X1, X2], [0.98, 0.02])
        self.uniswap = Uniswap([X1, X2])
        self.curve_A_0 = Curve([X1, X2], 0)
        self.curve_A_400 = Curve([X1, X2], 400)

        self.slippage_domain = np.arange(0.01 * X1, 0.51 * X1, 25 * DP18)

    def plot_amm_curve(self):
        pass

    # 3 plots for the amm curve for each one
    # 1 plot for all 3 on the same chart

    def plot_slippage(self):
        slippage_balancer_95_5 = []
        slippage_balancer_98_2 = []
        slippage_uniswap = []
        slippage_curve_A_0 = []
        slippage_curve_A_400 = []

        for qty_in in self.slippage_domain:
            slippage_balancer_95_5.append(self.balancer_95_5.slippage(qty_in, 0, 1))
            slippage_balancer_98_2.append(self.balancer_98_2.slippage(qty_in, 0, 1))
            slippage_uniswap.append(self.uniswap.slippage(qty_in, 0, 1))
            slippage_curve_A_0.append(self.curve_A_0.slippage(qty_in, 0, 1))
            slippage_curve_A_400.append(self.curve_A_400.slippage(qty_in, 0, 1))

        plt.plot(self.slippage_domain, slippage_balancer_95_5)

        plt.show()

    # 3 plots for the divergence loss (divergence loss vs. pct_change)
    # 1 plot for all 3 on the same chart

    def plot_divergence_loss(self):
        pass

    # 3 plots for slippage
    # 1 plot for all 3 on the same chart


if __name__ == "__main__":
    analysis = Analysis()
    analysis.plot_slippage()

