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
X1 = 40
X2 = 40
LABELPAD = 20
FONTSIZE = 14
LABELSIZE = 12


class Analysis:
    def __init__(self):
        self.uniswap = Uniswap([X1, X2])
        self.balancer_95_5 = Balancer([X1, X2], [0.95, 0.05])
        self.balancer_50_50 = Balancer([X1, X2], [0.5, 0.5])
        self.balancer_5_95 = Balancer([X1, X2], [0.05, 0.95])
        self.curve_A_0 = Curve([X1, X2], 0.0001)
        self.curve_A_5 = Curve([X1, X2], 5)
        self.curve_A_10000 = Curve([X1, X2], 10_000)

    def plot_amm_curve(self):
        balancer_50_50 = []
        balancer_5_95 = []
        balancer_95_5 = []
        uniswap = []
        curve_A_0 = []
        curve_A_5 = []
        curve_A_10000 = []

        # 0.99 and 0.1 make no sense, smart contracts use integer mathematics
        # we have this hack here, for continuity of the plots
        domain = np.arange(-0.9999999 * X1, 5.1 * X1, 0.1)
        # trade and look at reserves

        for x in domain:
            uniswap.append(self.uniswap._compute_trade_qty_out(x, 0, 1))
            balancer_95_5.append(self.balancer_95_5._compute_trade_qty_out(x, 0, 1))
            balancer_50_50.append(self.balancer_50_50._compute_trade_qty_out(x, 0, 1))
            balancer_5_95.append(self.balancer_5_95._compute_trade_qty_out(x, 0, 1))
            curve_A_0.append(self.curve_A_0._compute_trade_qty_out(x, 0, 1))
            curve_A_5.append(self.curve_A_5._compute_trade_qty_out(x, 0, 1))
            curve_A_10000.append(self.curve_A_10000._compute_trade_qty_out(x, 0, 1))

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot([x[0] for x in curve_A_0], [x[1] for x in curve_A_0], linewidth=2)
        ax.plot([x[0] for x in curve_A_5], [x[1] for x in curve_A_5], linewidth=2)
        ax.plot(
            [x[0] for x in curve_A_10000], [x[1] for x in curve_A_10000], linewidth=2
        )
        ax.tick_params(axis="x", labelsize=LABELSIZE)
        ax.tick_params(axis="y", labelsize=LABELSIZE)
        ax.set_xlabel(
            r"Pool's token 1 reserve, $r_1$", labelpad=LABELPAD, size=FONTSIZE,
        )
        ax.set_ylim([0, 100])
        ax.set_xlim([0, 100])
        ax.legend(["0", "5", "10000"], title=r"$\mathcal{A}$")
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
            [x[0] for x in balancer_95_5], [x[1] for x in balancer_95_5], linewidth=2
        )
        ax.plot(
            [x[0] for x in balancer_5_95], [x[1] for x in balancer_5_95], linewidth=2
        )
        ax.tick_params(axis="x", labelsize=LABELSIZE)
        ax.tick_params(axis="y", labelsize=LABELSIZE)
        ax.set_xlabel(
            r"Pool's token 1 reserve, $r_1$", labelpad=LABELPAD, size=FONTSIZE,
        )
        ax.set_ylim([0, 100])
        ax.set_xlim([0, 100])
        ax.legend([r"$.50/.50$", r".95/.05", r"$.05/.95$"], title=r"$w_1/w_2$")
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
            r"Pool's token 1 reserve, $r_1$", labelpad=LABELPAD, size=FONTSIZE,
        )
        ax.set_ylabel(
            r"Pool's token 2 reserve, $r_2$", labelpad=LABELPAD, size=FONTSIZE,
        )
        ax.set_ylim([0, 100])
        ax.set_xlim([0, 100])
        ax.legend(title="Uniswap")
        fig.savefig(
            os.path.join(FIGS_DIR, "conservation", "conservation_uniswap.pdf"),
            format="pdf",
            bbox_inches="tight",
        )

    def plot_slippage(self):
        slippage_balancer_95_5_0in_1out = []
        slippage_balancer_50_50 = []
        slippage_balancer_5_95_0in_1out = []
        slippage_uniswap = []
        slippage_curve_A_0 = []
        slippage_curve_A_5 = []
        slippage_curve_A_10000 = []

        slippage_domain = np.arange(-1 * X2, 2 * X2, 0.001)

        for qty_in in slippage_domain:
            slippage_balancer_95_5_0in_1out.append(
                self.balancer_95_5.slippage(qty_in, 0, 1)
            )
            slippage_balancer_5_95_0in_1out.append(
                self.balancer_5_95.slippage(qty_in, 0, 1)
            )
            slippage_balancer_50_50.append(self.balancer_50_50.slippage(qty_in, 0, 1))
            slippage_uniswap.append(self.uniswap.slippage(qty_in, 0, 1))
            slippage_curve_A_0.append(self.curve_A_0.slippage(qty_in, 0, 1))
            slippage_curve_A_5.append(self.curve_A_5.slippage(qty_in, 0, 1))
            slippage_curve_A_10000.append(self.curve_A_10000.slippage(qty_in, 0, 1))

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(
            slippage_domain, slippage_balancer_50_50, linewidth=2,
        )
        ax.plot(
            slippage_domain, slippage_balancer_95_5_0in_1out, linewidth=2,
        )
        ax.plot(
            slippage_domain, slippage_balancer_5_95_0in_1out, linewidth=2,
        )
        ax.set_xlabel(
            r"Trade size relative to the reserve, $x_1 / r_1$",
            labelpad=LABELPAD,
            size=FONTSIZE,
        )
        # ax.set_ylim([-0.025, 0.026])
        # ax.set_xlim([-1.0, 1.01])
        ax.tick_params(axis="x", labelsize=LABELSIZE)
        ax.tick_params(axis="y", labelsize=LABELSIZE)
        ax.legend([".50/.50", ".95/.05", ".05/.95"], title=r"$w_1/w_2$")
        fig.savefig(
            os.path.join(FIGS_DIR, "slippage", "slippage_balancer.pdf"),
            format="pdf",
            bbox_inches="tight",
        )

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(
            slippage_domain, slippage_uniswap, linewidth=2,
        )
        ax.set_xlabel(
            r"Trade size relative to the reserve, $x_1 / r_1$",
            labelpad=LABELPAD,
            size=FONTSIZE,
        )
        ax.set_ylabel(
            "slippage", labelpad=LABELPAD, size=FONTSIZE,
        )
        ax.set_ylim([-0.025, 0.026])
        ax.set_xlim([-1.0, 1.01])
        ax.tick_params(axis="x", labelsize=LABELSIZE)
        ax.tick_params(axis="y", labelsize=LABELSIZE)
        ax.legend(title="Uniswap")
        fig.savefig(
            os.path.join(FIGS_DIR, "slippage", "slippage_uniswap.pdf"),
            format="pdf",
            bbox_inches="tight",
        )

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(slippage_domain, slippage_curve_A_0)
        ax.plot(slippage_domain, slippage_curve_A_5)
        ax.plot(slippage_domain, slippage_curve_A_10000)
        # ax.set_ylim([-0.025, 0.026])
        # ax.set_xlim([-1.0, 1.01])
        ax.set_xlabel(
            r"trade size relative to the reserve, $x_1 / r_1$",
            labelpad=LABELPAD,
            size=FONTSIZE,
        )
        ax.tick_params(axis="x", labelsize=LABELSIZE)
        ax.tick_params(axis="y", labelsize=LABELSIZE)
        ax.legend(["0", "5", "10000"], title=r"$\mathcal{A}$")
        fig.savefig(
            os.path.join(FIGS_DIR, "slippage", "slippage_curve.pdf"),
            format="pdf",
            bbox_inches="tight",
        )

    def plot_divergence_loss(self):
        curve_A_0 = []
        curve_A_5 = []
        curve_A_10000 = []

        balancer_50_50 = []
        balancer_95_5 = []
        balancer_5_95 = []

        uniswap = []

        # ! this will compute for a while. We need such granularity, because
        # ! we are computing pct change for Curve implicitly
        domain = np.arange(-1 * X2, 5.1 * X2, 0.0001)
        _domain = np.arange(-1, 5.1, 0.01)

        for qty in domain:
            curve_A_0.append(self.curve_A_0.divergence_loss(qty, 0, 1))
            curve_A_5.append(self.curve_A_5.divergence_loss(qty, 0, 1))
            curve_A_10000.append(self.curve_A_10000.divergence_loss(qty, 0, 1))

        for pct_change in _domain:
            balancer_50_50.append(self.balancer_50_50.divergence_loss(pct_change, 0, 1))
            balancer_95_5.append(self.balancer_95_5.divergence_loss(pct_change, 0, 1))
            balancer_5_95.append(self.balancer_5_95.divergence_loss(pct_change, 0, 1))
            uniswap.append(self.uniswap.divergence_loss(pct_change, 0, 1))

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlabel("spot price change", labelpad=LABELPAD, size=FONTSIZE)
        ax.set_ylabel("divergence loss", labelpad=LABELPAD, size=FONTSIZE)
        ax.set_xlim([-1.025, 5.025])
        ax.set_ylim([-1.025, 0.025])
        ax.plot(_domain, uniswap, linewidth=2)
        ax.tick_params(axis="x", labelsize=LABELSIZE)
        ax.tick_params(axis="y", labelsize=LABELSIZE)
        ax.legend(title="Uniswap")
        fig.savefig(
            os.path.join(FIGS_DIR, "divergence_loss", "divloss_uniswap.pdf"),
            format="pdf",
            bbox_inches="tight",
        )

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlabel("spot price change", labelpad=LABELPAD, size=FONTSIZE)
        ax.set_xlim([-1.025, 5.025])
        ax.set_ylim([-1.025, 0.025])
        ax.plot(_domain, balancer_50_50, linewidth=2)
        ax.plot(_domain, balancer_95_5, linewidth=2)
        ax.plot(_domain, balancer_5_95, linewidth=2)
        ax.tick_params(axis="x", labelsize=LABELSIZE)
        ax.tick_params(axis="y", labelsize=LABELSIZE)
        ax.legend([".50/.50", ".95/.05", ".05/.95"], title=r"$w_1/w_2$")
        fig.savefig(
            os.path.join(FIGS_DIR, "divergence_loss", "divloss_balancer.pdf"),
            format="pdf",
            bbox_inches="tight",
        )

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlabel("spot price change", labelpad=LABELPAD, size=FONTSIZE)
        ax.set_xlim([-1.025, 5.025])
        ax.set_ylim([-1.025, 0.025])
        ax.tick_params(axis="x", labelsize=LABELSIZE)
        ax.tick_params(axis="y", labelsize=LABELSIZE)
        ax.plot([x[0] for x in curve_A_0], [x[1] for x in curve_A_0], linewidth=2)
        ax.plot([x[0] for x in curve_A_5], [x[1] for x in curve_A_5], linewidth=2)
        ax.plot(
            [x[0] for x in curve_A_10000], [x[1] for x in curve_A_10000], linewidth=2
        )
        ax.legend(["0", "5", "10000"], title=r"$\mathcal{A}$")
        fig.savefig(
            os.path.join(FIGS_DIR, "divergence_loss", "divloss_curve.pdf"),
            format="pdf",
            bbox_inches="tight",
        )


if __name__ == "__main__":
    analysis = Analysis()
    analysis.plot_amm_curve()
