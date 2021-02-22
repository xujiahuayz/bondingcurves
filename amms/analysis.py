from matplotlib.ticker import PercentFormatter
import matplotlib.pyplot as plt
import numpy as np
import os

from amms.balancer.main import Balancer
from amms.uniswap.main import Uniswap
from amms.curve.main import Curve

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
FIGS_DIR = os.path.join(CURR_DIR, "figures")

DP18 = 1e18
X1 = 1_000_000 * DP18
X2 = 1_000_000 * DP18


class Analysis:
    def __init__(self):
        self.balancer_95_5 = Balancer([X1, X2], [0.95, 0.05])
        self.balancer_98_2 = Balancer([X1, X2], [0.98, 0.02])
        self.balancer_60_40 = Balancer([X1, X2], [0.6, 0.4])
        self.balancer_80_20 = Balancer([X1, X2], [0.8, 0.2])
        self.balancer_50_50 = Balancer([X1, X2], [0.5, 0.5])
        self.uniswap = Uniswap([X1, X2])
        self.curve_A_1 = Curve([X1, X2], 1)
        self.curve_A_5 = Curve([X1, X2], 5)
        self.curve_A_10 = Curve([X1, X2], 10)
        self.curve_A_20 = Curve([X1, X2], 20)
        self.curve_A_100 = Curve([X1, X2], 100)
        self.curve_A_400 = Curve([X1, X2], 400)

        self.slippage_domain = np.arange(0.0001 * X2, 0.27 * X2, 25 * DP18)

    def plot_amm_curve(self):
        balancer_95_5 = []
        balancer_98_2 = []
        balancer_60_40 = []
        balancer_80_20 = []
        balancer_50_50 = []
        uniswap = []
        curve_A_1 = []
        curve_A_5 = []
        curve_A_10 = []
        curve_A_20 = []
        curve_A_100 = []

        domain = np.arange(-0.99 * X1, 3 * X1, 50 * DP18)
        # trade and look at reserves

        for x in domain:
            balancer_95_5.append(self.balancer_95_5._compute_trade_qty_out(x, 0, 1))
            balancer_98_2.append(self.balancer_98_2._compute_trade_qty_out(x, 0, 1))
            balancer_50_50.append(self.balancer_50_50._compute_trade_qty_out(x, 0, 1))
            balancer_60_40.append(self.balancer_60_40._compute_trade_qty_out(x, 0, 1))
            balancer_80_20.append(self.balancer_80_20._compute_trade_qty_out(x, 0, 1))
            uniswap.append(self.uniswap._compute_trade_qty_out(x, 0, 1))
            curve_A_1.append(self.curve_A_1._compute_trade_qty_out(x, 0, 1))
            curve_A_5.append(self.curve_A_5._compute_trade_qty_out(x, 0, 1))
            curve_A_10.append(self.curve_A_10._compute_trade_qty_out(x, 0, 1))
            curve_A_20.append(self.curve_A_20._compute_trade_qty_out(x, 0, 1))
            curve_A_100.append(self.curve_A_100._compute_trade_qty_out(x, 0, 1))

        # all together
        fig = plt.figure(figsize=(17, 5.5))

        ax = fig.add_subplot(131)
        ax.plot([x[0] for x in curve_A_1], [x[1] for x in curve_A_1], linewidth=2)
        ax.plot([x[0] for x in curve_A_5], [x[1] for x in curve_A_5], linewidth=2)
        ax.plot([x[0] for x in curve_A_10], [x[1] for x in curve_A_10])
        ax.plot([x[0] for x in curve_A_100], [x[1] for x in curve_A_100])
        ax.set_xlabel(
            r"$r_1$", size=21,
        )
        ax.set_ylabel(r"$r_2$", size=21)
        ax.set_ylim([-1e23 / 2, 2.5e24])
        ax.set_xlim([-1e23 / 2, 2.5e24])
        ax.axvline(ls="--")
        ax.axhline(ls="--")
        ax.legend(["A=1", "A=5", "A=10", "A=100"])

        ax = fig.add_subplot(132)
        ax.plot(
            [x[0] for x in balancer_50_50], [x[1] for x in balancer_50_50], linewidth=2
        )
        ax.plot(
            [x[0] for x in balancer_60_40], [x[1] for x in balancer_60_40], linewidth=2
        )
        ax.plot([x[0] for x in balancer_80_20], [x[1] for x in balancer_80_20])
        ax.plot([x[0] for x in balancer_95_5], [x[1] for x in balancer_95_5])
        ax.plot([x[0] for x in balancer_98_2], [x[1] for x in balancer_98_2])
        ax.set_xlabel(
            r"$r_1$", size=21,
        )
        ax.set_ylabel(r"$r_2$", size=21)
        ax.set_ylim([-1e23 / 2, 2e24])
        ax.set_xlim([0.45e24, 2e24])
        ax.axvline(ls="--", x=0.5e24)
        ax.axhline(ls="--")
        ax.legend(["50%/50%", "60%/40%", "80%/20%", "95%/5%", "98%/2%"])

        ax = fig.add_subplot(133)
        ax.plot([x[0] for x in uniswap], [x[1] for x in uniswap], linewidth=2)
        ax.plot(
            [x[0] for x in balancer_95_5], [x[1] for x in balancer_95_5], linewidth=2
        )
        ax.plot([x[0] for x in curve_A_1], [x[1] for x in curve_A_1])
        ax.plot([x[0] for x in curve_A_10], [x[1] for x in curve_A_10])
        ax.plot([x[0] for x in curve_A_100], [x[1] for x in curve_A_100])
        ax.set_xlabel(
            r"$r_1$", size=21,
        )
        ax.set_ylabel(r"$r_2$", size=21)
        ax.set_ylim([-1e23 / 2, 2e24])
        ax.set_xlim([0.45e24, 2e24])
        ax.axvline(ls="--", x=0.5e24)
        ax.axhline(ls="--")
        ax.legend(
            ["Uniswap", "Balancer 95%/5%", "Curve, A=1", "Curve, A=10", "Curve, A=100"]
        )
        fig.savefig(
            os.path.join(FIGS_DIR, "conservation", "3_conservations.pdf"), format="pdf",
        )

    def plot_slippage(self):
        slippage_balancer_95_5_0in_1out = []
        slippage_balancer_95_5_1in_0out = []
        slippage_balancer_98_2_0in_1out = []
        slippage_balancer_98_2_1in_0out = []
        slippage_balancer_60_40_1in_0out = []
        slippage_balancer_50_50 = []
        slippage_uniswap = []
        slippage_curve_A_1 = []
        curve_A_5 = []
        curve_A_10 = []
        slippage_curve_A_100 = []
        slippage_curve_A_400 = []
        uniswap = []

        slippage_domain = [x / X2 for x in self.slippage_domain]

        for qty_in in self.slippage_domain:
            slippage_balancer_95_5_0in_1out.append(
                self.balancer_95_5.slippage(qty_in, 0, 1)
            )
            slippage_balancer_95_5_1in_0out.append(
                self.balancer_95_5.slippage(qty_in, 1, 0)
            )
            slippage_balancer_98_2_0in_1out.append(
                self.balancer_98_2.slippage(qty_in, 0, 1)
            )
            slippage_balancer_98_2_1in_0out.append(
                self.balancer_98_2.slippage(qty_in, 1, 0)
            )
            slippage_balancer_60_40_1in_0out.append(
                self.balancer_60_40.slippage(qty_in, 1, 0)
            )
            slippage_balancer_50_50.append(self.balancer_50_50.slippage(qty_in, 0, 1))
            slippage_uniswap.append(self.uniswap.slippage(qty_in, 1, 0))
            slippage_curve_A_1.append(self.curve_A_1.slippage(qty_in, 1, 0))
            curve_A_5.append(self.curve_A_5.slippage(qty_in, 1, 0))
            slippage_curve_A_100.append(self.curve_A_100.slippage(qty_in, 1, 0))
            curve_A_10.append(self.curve_A_10.slippage(qty_in, 1, 0))
            slippage_curve_A_400.append(self.curve_A_400.slippage(qty_in, 1, 0))
            uniswap.append(self.uniswap.slippage(qty_in, 0, 1))

        fig = plt.figure(figsize=(19, 5.5))

        ax = fig.add_subplot(131)
        ax.plot(slippage_domain, [-y for y in slippage_curve_A_1])
        ax.plot(slippage_domain, [-y for y in curve_A_5])
        ax.plot(slippage_domain, [-y for y in curve_A_10])
        ax.plot(slippage_domain, [-y for y in slippage_curve_A_400])
        ax.set_xlabel(
            r"$x_1 / r_1$", size=15,
        )
        ax.set_ylabel("slippage", size=15)
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=1))
        ax.legend(["A=1", "A=5", "A=10", "A=100"])

        ax = fig.add_subplot(132)
        ax.plot(slippage_domain, [-y for y in slippage_balancer_50_50])
        ax.plot(slippage_domain, [-y for y in slippage_balancer_60_40_1in_0out])
        ax.plot(slippage_domain, [-y for y in slippage_balancer_95_5_1in_0out])
        ax.plot(slippage_domain, [-y for y in slippage_balancer_98_2_1in_0out])
        ax.set_xlabel(
            r"$x_1 / r_1$", size=15,
        )
        ax.set_ylabel("slippage", size=15)
        ax.set_xlim([0, 0.05])
        ax.set_ylim([-0.05, 0])
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=1))
        ax.legend(
            ["50%/50%", "60%/40%", "95%/5%", "98%/2%",]
        )

        ax = fig.add_subplot(133)
        ax.plot(slippage_domain, [-y for y in uniswap])
        ax.plot(slippage_domain, [-y for y in slippage_balancer_60_40_1in_0out])
        ax.plot(slippage_domain, [-y for y in slippage_balancer_98_2_1in_0out])
        ax.plot(slippage_domain, [-y for y in slippage_curve_A_100])
        ax.set_xlabel(
            r"$x_1 / r_1$", size=15,
        )
        ax.set_ylabel("slippage", size=15)
        ax.set_xlim([0, 0.05])
        ax.set_ylim([-0.05, 0])
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=1))
        ax.legend(["Uniswap", "Balancer 60%/40%", "Balancer 98%/2%", "Curve A=100"])
        fig.savefig(
            os.path.join(FIGS_DIR, "slippage", "all_slippage_comparisons.pdf"),
            format="pdf",
            bbox_inches="tight",
        )

    def plot_divergence_loss(self):
        curve_A_1 = []
        curve_A_10 = []
        curve_A_100 = []

        domain = np.arange(-1 * X2, 5 * X2, 25 * DP18)

        for qty in domain:
            curve_A_1.append(self.curve_A_1.divergence_loss(qty, 0, 1))
            curve_A_10.append(self.curve_A_10.divergence_loss(qty, 0, 1))
            curve_A_100.append(self.curve_A_100.divergence_loss(qty, 0, 1))

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlabel("spot price increase", size=15)
        ax.set_ylabel("divergence loss", size=15)
        ax.set_xlim([-1.0, 24.0])
        ax.set_ylim([-1.0, 0.0])
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=1))
        ax.plot([x[0] for x in curve_A_1], [x[1] for x in curve_A_1], linewidth=2)
        ax.plot([x[0] for x in curve_A_10], [x[1] for x in curve_A_10], linewidth=2)
        ax.plot([x[0] for x in curve_A_100], [x[1] for x in curve_A_100], linewidth=2)
        ax.legend(["A=1", "A=10", "A=100"])


if __name__ == "__main__":
    analysis = Analysis()
    analysis.plot_divergence_loss()
