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
X1 = 1_000 * DP18
X2 = 1_000 * DP18


class Analysis:
    def __init__(self):
        self.balancer_95_5 = Balancer([X1, X2], [0.95, 0.05])
        self.balancer_98_2 = Balancer([X1, X2], [0.98, 0.02])
        self.balancer_50_50 = Balancer([X1, X2], [0.5, 0.5])
        self.uniswap = Uniswap([X1, X2])
        self.curve_A_1 = Curve([X1, X2], 1)
        self.curve_A_400 = Curve([X1, X2], 400)

        self.slippage_domain = np.arange(0.01 * X2, 0.27 * X2, 25 * DP18)

    def plot_amm_curve(self):
        balancer_95_5 = []
        balancer_98_2 = []
        uniswap = []
        curve_A_1 = []
        curve_A_400 = []

        domain = np.arange(-0.95 * X1, 5 * X1, 10 * DP18)
        # trade and look at reserves

        for x in domain:
            curve_A_1.append(self.curve_A_1._compute_trade_qty_out(x, 0, 1))

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot([x[0] for x in curve_A_1], [x[1] for x in curve_A_1])
        ax.set_xlabel(
            "x", size=15,
        )
        ax.set_ylabel("y", size=15)
        ax.set_title(r"Curve for $\mathcal{A}=1$", size=21)
        # ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        # ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        fig.savefig(
            os.path.join(FIGS_DIR, "conservation", "curve_A_1.pdf"), format="pdf"
        )

    def plot_slippage(self):
        slippage_balancer_95_5_0in_1out = []
        slippage_balancer_95_5_1in_0out = []
        slippage_balancer_98_2_0in_1out = []
        slippage_balancer_98_2_1in_0out = []
        slippage_balancer_50_50 = []
        slippage_uniswap = []
        slippage_curve_A_1 = []
        slippage_curve_A_400 = []

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
            slippage_balancer_50_50.append(self.balancer_50_50.slippage(qty_in, 0, 1))
            slippage_uniswap.append(self.uniswap.slippage(qty_in, 1, 0))
            slippage_curve_A_1.append(self.curve_A_1.slippage(qty_in, 1, 0))
            slippage_curve_A_400.append(self.curve_A_400.slippage(qty_in, 1, 0))

        # Balancer 95-5, x1 in x2 out
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(slippage_domain, slippage_balancer_95_5_0in_1out)
        ax.set_xlabel(
            r"$x_1 / r_1$", size=15,
        )
        ax.set_ylabel("slippage", size=15)
        ax.set_title(r"Balancer 95%/5% ($w_1/w_2$)", size=21)
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        fig.savefig(
            os.path.join(FIGS_DIR, "slippage", "balancer_95_5_0in_1out.pdf"),
            format="pdf",
        )

        # Balancer 95-5, x2 in x1 out
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(slippage_domain, slippage_balancer_95_5_1in_0out)
        ax.set_xlabel(
            r"$x_2 / r_2$", size=15,
        )
        ax.set_ylabel("slippage", size=15)
        ax.set_title(r"Balancer 95%/5% ($w_1/w_2$)", size=21)
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        fig.savefig(
            os.path.join(FIGS_DIR, "slippage", "balancer_95_5_1in_0out.pdf"),
            format="pdf",
        )

        # Balancer 98-2, x1 in x2 out
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(slippage_domain, slippage_balancer_98_2_0in_1out)
        ax.set_xlabel(
            r"$x_1 / r_1$", size=15,
        )
        ax.set_ylabel("slippage", size=15)
        ax.set_title(r"Balancer 98%/2% ($w_1/w_2$)", size=21)
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        fig.savefig(
            os.path.join(FIGS_DIR, "slippage", "balancer_98_2_0in_1out.pdf"),
            format="pdf",
        )

        # Balancer 98-2, x2 in x1 out
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(slippage_domain, slippage_balancer_98_2_1in_0out)
        ax.set_xlabel(
            r"$x_2 / r_2$", size=15,
        )
        ax.set_ylabel("slippage", size=15)
        ax.set_title(r"Balancer 98%/2% ($w_1/w_2$)", size=21)
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        fig.savefig(
            os.path.join(FIGS_DIR, "slippage", "balancer_98_2_1in_0out.pdf"),
            format="pdf",
        )

        # Balancer 50-50
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(slippage_domain, slippage_balancer_50_50)
        ax.set_xlabel(
            r"$x_1 / r_1$", size=15,
        )
        ax.set_ylabel("slippage", size=15)
        ax.set_title(r"Balancer 50%/50% ($w_1/w_2$)", size=21)
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        fig.savefig(
            os.path.join(FIGS_DIR, "slippage", "balancer_50_50.pdf"), format="pdf"
        )

        # Uniswap
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(slippage_domain, slippage_uniswap)
        ax.set_xlabel(
            r"$x_1 / r_1$", size=15,
        )
        ax.set_ylabel("slippage", size=15)
        ax.set_title(r"Uniswap", size=21)
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        fig.savefig(os.path.join(FIGS_DIR, "slippage", "uniswap.pdf"), format="pdf")

        # Curve, A=1
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(slippage_domain, slippage_curve_A_1)
        ax.set_xlabel(
            r"$x_1 / r_1$", size=15,
        )
        ax.set_ylabel("slippage", size=15)
        ax.set_title(r"Curve for $\mathcal{A}=1$", size=21)
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=1))
        fig.savefig(os.path.join(FIGS_DIR, "slippage", "curve_A_1.pdf"), format="pdf")

        # Curve, A=400
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(slippage_domain, slippage_curve_A_400)
        ax.set_xlabel(
            r"$x_1 / r_1$", size=15,
        )
        ax.set_ylabel("slippage", size=15)
        ax.set_title(r"Curve for $\mathcal{A}=400$", size=21)
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=2))
        fig.savefig(os.path.join(FIGS_DIR, "slippage", "curve_A_400.pdf"), format="pdf")


if __name__ == "__main__":
    analysis = Analysis()
    analysis.plot_amm_curve()
