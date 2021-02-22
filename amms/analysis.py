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

        self.slippage_domain = np.arange(0.01 * X2, 0.27 * X2, 25 * DP18)

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

        # Balancer 95-5
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot([x[0] for x in balancer_95_5], [x[1] for x in balancer_95_5])
        ax.set_xlabel(
            "x",
            size=15,
        )
        ax.set_ylabel("y", size=15)
        ax.set_title("Balancer 95%/5%", size=21)
        fig.savefig(
            os.path.join(FIGS_DIR, "conservation", "balancer_95_5.pdf"), format="pdf"
        )

        # Balancer 98-2
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot([x[0] for x in balancer_98_2], [x[1] for x in balancer_98_2])
        ax.set_xlabel(
            "x",
            size=15,
        )
        ax.set_ylabel("y", size=15)
        ax.set_title("Balancer 98%/2%", size=21)
        fig.savefig(
            os.path.join(FIGS_DIR, "conservation", "balancer_98_2.pdf"), format="pdf"
        )

        # Balancer 60-40
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot([x[0] for x in balancer_60_40], [x[1] for x in balancer_60_40])
        ax.set_xlabel(
            "x",
            size=15,
        )
        ax.set_ylabel("y", size=15)
        ax.set_title("Balancer 60%/40%", size=21)
        fig.savefig(
            os.path.join(FIGS_DIR, "conservation", "balancer_60_40.pdf"), format="pdf"
        )

        # Balancer 80-20
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot([x[0] for x in balancer_80_20], [x[1] for x in balancer_80_20])
        ax.set_xlabel(
            "x",
            size=15,
        )
        ax.set_ylabel("y", size=15)
        ax.set_title("Balancer 80%/20%", size=21)
        fig.savefig(
            os.path.join(FIGS_DIR, "conservation", "balancer_80_20.pdf"), format="pdf"
        )

        # Balancer 50-50
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot([x[0] for x in balancer_50_50], [x[1] for x in balancer_50_50])
        ax.set_xlabel(
            "x",
            size=15,
        )
        ax.set_ylabel("y", size=15)
        ax.set_title("Balancer 50%/50%", size=21)
        fig.savefig(
            os.path.join(FIGS_DIR, "conservation", "balancer_50_50.pdf"), format="pdf"
        )

        # Uniswap
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot([x[0] for x in uniswap], [x[1] for x in uniswap])
        ax.set_xlabel(
            "x",
            size=15,
        )
        ax.set_ylabel("y", size=15)
        ax.set_title("Uniswap", size=21)
        fig.savefig(os.path.join(FIGS_DIR, "conservation", "uniswap.pdf"), format="pdf")

        # Curve A=1
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot([x[0] for x in curve_A_1], [x[1] for x in curve_A_1])
        ax.set_xlabel(
            "x",
            size=15,
        )
        ax.set_ylabel("y", size=15)
        ax.set_title(r"Curve for $\mathcal{A}=1$", size=21)
        fig.savefig(
            os.path.join(FIGS_DIR, "conservation", "curve_A_1.pdf"), format="pdf"
        )

        # Curve A=5
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot([x[0] for x in curve_A_5], [x[1] for x in curve_A_5])
        ax.set_xlabel(
            "x",
            size=15,
        )
        ax.set_ylabel("y", size=15)
        ax.set_title(r"Curve for $\mathcal{A}=5$", size=21)
        fig.savefig(
            os.path.join(FIGS_DIR, "conservation", "curve_A_5.pdf"), format="pdf"
        )

        # Curve A=10
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot([x[0] for x in curve_A_10], [x[1] for x in curve_A_10])
        ax.set_xlabel(
            "x",
            size=15,
        )
        ax.set_ylabel("y", size=15)
        ax.set_title(r"Curve for $\mathcal{A}=10$", size=21)
        fig.savefig(
            os.path.join(FIGS_DIR, "conservation", "curve_A_10.pdf"), format="pdf"
        )

        # Curve A=20
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot([x[0] for x in curve_A_20], [x[1] for x in curve_A_20])
        ax.set_xlabel(
            "x",
            size=15,
        )
        ax.set_ylabel("y", size=15)
        ax.set_title(r"Curve for $\mathcal{A}=20$", size=21)
        fig.savefig(
            os.path.join(FIGS_DIR, "conservation", "curve_A_20.pdf"), format="pdf"
        )

        # Curve A=100
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot([x[0] for x in curve_A_100], [x[1] for x in curve_A_100])
        ax.set_xlabel(
            "x",
            size=15,
        )
        ax.set_ylabel("y", size=15)
        ax.set_title(r"Curve for $\mathcal{A}=100$", size=21)
        fig.savefig(
            os.path.join(FIGS_DIR, "conservation", "curve_A_100.pdf"), format="pdf"
        )

        # this will be 1/3 for the conservation functions
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot([x[0] for x in curve_A_1], [x[1] for x in curve_A_1], linewidth=2)
        ax.plot([x[0] for x in curve_A_5], [x[1] for x in curve_A_5], linewidth=2)
        ax.plot([x[0] for x in curve_A_10], [x[1] for x in curve_A_10])
        ax.plot([x[0] for x in curve_A_100], [x[1] for x in curve_A_100])
        ax.set_xlabel(
            r"$r_1$",
            size=21,
        )
        ax.set_ylabel(r"$r_2$", size=21)
        ax.set_ylim([-1e23, 2.5e24])
        ax.set_xlim([-1e23 / 2, 2.5e24])
        ax.set_title(r"Curve conservation functions comparison", size=21, pad=20)
        ax.axvline(ls="--")
        ax.axhline(ls="--")
        ax.legend(["A=1", "A=5", "A=10", "A=100"])
        fig.savefig(
            os.path.join(FIGS_DIR, "conservation", "curve_A_1_5_10_100.pdf"),
            format="pdf",
            bbox_inches="tight",
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
            r"$x_1 / r_1$",
            size=15,
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
            r"$x_2 / r_2$",
            size=15,
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
            r"$x_1 / r_1$",
            size=15,
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
            r"$x_2 / r_2$",
            size=15,
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
            r"$x_1 / r_1$",
            size=15,
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
            r"$x_1 / r_1$",
            size=15,
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
            r"$x_1 / r_1$",
            size=15,
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
            r"$x_1 / r_1$",
            size=15,
        )
        ax.set_ylabel("slippage", size=15)
        ax.set_title(r"Curve for $\mathcal{A}=400$", size=21)
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=2))
        fig.savefig(os.path.join(FIGS_DIR, "slippage", "curve_A_400.pdf"), format="pdf")


if __name__ == "__main__":
    analysis = Analysis()
    analysis.plot_amm_curve()
