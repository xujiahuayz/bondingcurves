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
X1 = 1_000
X2 = 1_000
LABELPAD = 20
FONTSIZE = 14
LABELSIZE = 12


class Analysis:
    def __init__(self):
        self.uniswap = Uniswap([X1, X2])
        self.balancer_95_5 = Balancer([X1, X2], [0.95, 0.05])
        self.balancer_50_50 = Balancer([X1, X2], [0.5, 0.5])
        self.balancer_5_95 = Balancer([X1, X2], [0.05, 0.95])
        self.curve_A_1 = Curve([X1, X2], 1)
        self.curve_A_5 = Curve([X1, X2], 5)
        self.curve_A_50 = Curve([X1, X2], 50)
        self.curve_A_100 = Curve([X1, X2], 100)

    def plot_amm_curve(self):
        balancer_50_50 = []
        balancer_5_95 = []
        balancer_95_5 = []
        uniswap = []
        curve_A_1 = []
        curve_A_5 = []
        curve_A_100 = []

        domain = np.arange(-1 * X1, 5.1 * X1, 25)
        # trade and look at reserves

        for x in domain:
            uniswap.append(self.uniswap._compute_trade_qty_out(x, 0, 1))
            balancer_95_5.append(self.balancer_95_5._compute_trade_qty_out(x, 0, 1))
            balancer_50_50.append(self.balancer_50_50._compute_trade_qty_out(x, 0, 1))
            balancer_5_95.append(self.balancer_5_95._compute_trade_qty_out(x, 0, 1))
            curve_A_1.append(self.curve_A_1._compute_trade_qty_out(x, 0, 1))
            curve_A_5.append(self.curve_A_5._compute_trade_qty_out(x, 0, 1))
            curve_A_100.append(self.curve_A_100._compute_trade_qty_out(x, 0, 1))

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot([x[0] for x in curve_A_1], [x[1] for x in curve_A_1], linewidth=2)
        ax.plot([x[0] for x in curve_A_5], [x[1] for x in curve_A_5], linewidth=2)
        ax.plot([x[0] for x in curve_A_100], [x[1] for x in curve_A_100], linewidth=2)
        ax.tick_params(axis="x", labelsize=LABELSIZE)
        ax.tick_params(axis="y", labelsize=LABELSIZE)
        ax.set_xlabel(
            r"Pool's token 1 reserve, $r_1$" + "\n" + r"$r_1 = 1000$",
            labelpad=LABELPAD,
            size=FONTSIZE,
        )
        # ax.set_ylabel(
        #     r"Pool's token 2 reserve, $r_2$" + "\n" + r"$r_2 = 1000$",
        #     labelpad=LABELPAD,
        #     size=FONTSIZE,
        # )
        ax.set_ylim([-10, 2_010])
        ax.set_xlim([-10, 2_010])
        ax.legend(["1", "5", "100"], title=r"$\mathcal{A}$")
        fig.savefig(
            os.path.join(FIGS_DIR, "conservation", "conservation_curve.pdf"),
            format="pdf",
            bbox_inches="tight",
        )

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(
            [x[0] for x in balancer_50_50], [x[1] for x in balancer_50_50], linewidth=2
        )
        ax.plot(
            [x[0] for x in balancer_5_95], [x[1] for x in balancer_5_95], linewidth=2
        )
        ax.plot(
            [x[0] for x in balancer_95_5], [x[1] for x in balancer_95_5], linewidth=2
        )
        ax.tick_params(axis="x", labelsize=LABELSIZE)
        ax.tick_params(axis="y", labelsize=LABELSIZE)
        ax.set_xlabel(
            r"Pool's token 1 reserve, $r_1$" + "\n" + r"$r_1 = 1000$",
            labelpad=LABELPAD,
            size=FONTSIZE,
        )
        # ax.set_ylabel(
        #     r"Pool's token 2 reserve, $r_2$" + "\n" + r"$r_2 = 1000$",
        #     labelpad=LABELPAD,
        #     size=FONTSIZE,
        # )
        ax.set_ylim([-10, 2_010])
        ax.set_xlim([-10, 2_010])
        ax.legend([r"$.5/.5$", r"$.5/.95$", r".95/.5"], title=r"$w_1/w_2$")
        fig.savefig(
            os.path.join(FIGS_DIR, "conservation", "conservation_balancer.pdf"),
            format="pdf",
            bbox_inches="tight",
        )

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot([x[0] for x in uniswap], [x[1] for x in uniswap], linewidth=2)
        ax.tick_params(axis="x", labelsize=LABELSIZE)
        ax.tick_params(axis="y", labelsize=LABELSIZE)
        ax.set_xlabel(
            r"Pool's token 1 reserve, $r_1$" + "\n" + r"$r_1 = 1000$",
            labelpad=LABELPAD,
            size=FONTSIZE,
        )
        ax.set_ylabel(
            r"Pool's token 2 reserve, $r_2$" + "\n" + r"$r_2 = 1000$",
            labelpad=LABELPAD,
            size=FONTSIZE,
        )
        ax.set_ylim([-10, 2_010])
        ax.set_xlim([-10, 2_010])
        ax.legend(title="Uniswap")
        fig.savefig(
            os.path.join(FIGS_DIR, "conservation", "conservation_uniswap.pdf"),
            format="pdf",
            bbox_inches="tight",
        )

    def plot_slippage(self):
        slippage_balancer_95_5_0in_1out = []
        slippage_balancer_95_5_1in_0out = []
        slippage_balancer_50_50 = []
        slippage_uniswap = []
        slippage_curve_A_1 = []
        slippage_curve_A_50 = []
        slippage_curve_A_100 = []
        uniswap = []

        slippage_domain = [x / X2 for x in self.slippage_domain]

        for qty_in in self.slippage_domain:
            slippage_balancer_95_5_0in_1out.append(
                self.balancer_95_5.slippage(qty_in, 0, 1)
            )
            slippage_balancer_95_5_1in_0out.append(
                self.balancer_95_5.slippage(qty_in, 1, 0)
            )
            slippage_balancer_50_50.append(self.balancer_50_50.slippage(qty_in, 0, 1))
            slippage_uniswap.append(self.uniswap.slippage(qty_in, 1, 0))
            slippage_curve_A_1.append(self.curve_A_1.slippage(qty_in, 1, 0))
            slippage_curve_A_50.append(self.curve_A_50.slippage(qty_in, 1, 0))
            slippage_curve_A_100.append(self.curve_A_100.slippage(qty_in, 1, 0))
            uniswap.append(self.uniswap.slippage(qty_in, 0, 1))

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(slippage_domain, [-y for y in slippage_balancer_50_50], linewidth=2)
        ax.plot(
            slippage_domain, [-y for y in slippage_balancer_95_5_1in_0out], linewidth=2
        )
        ax.set_xlabel(
            r"Trade size relative to reserve, $x_1 / r_1$", size=15,
        )
        ax.set_ylabel("slippage", size=15)
        ax.set_xlim([-0.001, 0.051])
        ax.set_ylim([-0.051, 0.001])
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=1))
        ax.legend(
            ["50%/50%", "95%/5%", "5%/95%",]
        )
        fig.savefig(
            os.path.join(FIGS_DIR, "slippage", "slippage_balancer.pdf"),
            format="pdf",
            bbox_inches="tight",
        )

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(slippage_domain, [-y for y in uniswap], linewidth=2)
        ax.set_xlabel(
            r"Trade size relative to reserve, $x_1 / r_1$", size=15,
        )
        ax.set_ylabel("slippage", size=15)
        ax.set_xlim([-0.001, 0.051])
        ax.set_ylim([-0.051, 0.001])
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=1))
        ax.legend(["Uniswap"])
        fig.savefig(
            os.path.join(FIGS_DIR, "slippage", "slippage_uniswap.pdf"),
            format="pdf",
            bbox_inches="tight",
        )

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(slippage_domain, [-y for y in slippage_curve_A_1])
        ax.plot(slippage_domain, [-y for y in slippage_curve_A_50])
        ax.plot(slippage_domain, [-y for y in slippage_curve_A_100])
        ax.set_xlabel(
            r"Trade size relative to reserve, $x_1 / r_1$", size=15,
        )
        ax.set_ylabel("slippage", size=15)
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=1))
        ax.legend(["A=1", "A=50", "A=100"])
        fig.savefig(
            os.path.join(FIGS_DIR, "slippage", "slippage_curve.pdf"),
            format="pdf",
            bbox_inches="tight",
        )

    def plot_divergence_loss(self):
        curve_A_1 = []
        curve_A_10 = []
        curve_A_100 = []

        balancer_50_50 = []
        balancer_95_5 = []
        balancer_5_95 = []

        uniswap = []

        domain = np.arange(-1 * X2, 4.9 * X2, 50 * DP18)
        _domain = np.arange(-1, 2.90, 0.025)

        for qty in domain:
            curve_A_1.append(self.curve_A_1.divergence_loss(qty, 0, 1))
            curve_A_100.append(self.curve_A_100.divergence_loss(qty, 0, 1))

        for pct_change in _domain:
            balancer_50_50.append(self.balancer_50_50.divergence_loss(pct_change, 1, 0))
            balancer_95_5.append(self.balancer_95_5.divergence_loss(pct_change, 1, 0))
            balancer_5_95.append(self.balancer_5_95.divergence_loss(pct_change, 1, 0))

            uniswap.append(self.uniswap.divergence_loss(pct_change, 0, 1))

        # fig = plt.figure(figsize=(22, 5))

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlabel("spot price change", size=15)
        ax.set_ylabel("divergence loss", size=15)
        ax.set_xlim([-1.1, 3.0])
        ax.set_ylim([-1.025, 0.025])
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=0))
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=0))
        ax.plot(_domain, uniswap, linewidth=2, label="Uniswap")
        ax.legend()
        fig.savefig(
            os.path.join(FIGS_DIR, "divergence_loss", "divloss_uniswap.pdf"),
            format="pdf",
            bbox_inches="tight",
        )

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlabel("spot price change", size=15)
        ax.set_ylabel("divergence loss", size=15)
        ax.set_xlim([-1.1, 3.0])
        ax.set_ylim([-1.025, 0.025])
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=0))
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=0))
        ax.plot(_domain, balancer_50_50, linewidth=2)
        ax.plot(_domain, balancer_95_5, linewidth=2)
        ax.legend(["50%/50%", "60%/40%", "95%/5%", "98%/2%"])
        fig.savefig(
            os.path.join(FIGS_DIR, "divergence_loss", "divloss_balancer.pdf"),
            format="pdf",
            bbox_inches="tight",
        )

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlabel("spot price change", size=15)
        ax.set_ylabel("divergence loss", size=15)
        ax.set_xlim([-1.5, 24.05])
        ax.set_ylim([-1.025, 0.0125])
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=0))
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=0))
        ax.plot([x[0] for x in curve_A_1], [x[1] for x in curve_A_1], linewidth=2)
        ax.plot([x[0] for x in curve_A_10], [x[1] for x in curve_A_10], linewidth=2)
        ax.plot([x[0] for x in curve_A_100], [x[1] for x in curve_A_100], linewidth=2)
        ax.legend(["A=1", "A=10", "A=100"])
        fig.savefig(
            os.path.join(FIGS_DIR, "divergence_loss", "divloss_curve.pdf"),
            format="pdf",
            bbox_inches="tight",
        )


if __name__ == "__main__":
    analysis = Analysis()
    analysis.plot_amm_curve()
