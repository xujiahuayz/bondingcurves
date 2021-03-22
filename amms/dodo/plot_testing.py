from matplotlib.ticker import PercentFormatter
import matplotlib.pyplot as plt
import numpy as np
import os

X1 = 40
X2 = 40 

oracle_price = 1

DP18 = 1e18
LABELPAD = 20
FONTSIZE = 14
LABELSIZE = 12

dodo_A_001 = Dodo([X1, X2], 0.01)
dodo_A_05 = Dodo([X1, X2], 0.5)
dodo_A_099 = Dodo([X1, X2], 0.99)

dodo_A_001_example = []
dodo_A_05_example = []
dodo_A_099_example = []

# 0.99 and 0.1 make no sense, smart contracts use integer mathematics
# we have this hack here, for continuity of the plots
domain = np.arange(-0.9999999 * X1, 5.1 * X1, 0.1)
# trade and look at reserves

for x in domain:
    dodo_A_001_example.append(dodo_A_001._compute_trade_qty_out(x, 0, 1, oracle_price))
    dodo_A_05_example.append(dodo_A_05._compute_trade_qty_out(x, 0, 1, oracle_price))
    dodo_A_099_example.append(dodo_A_099._compute_trade_qty_out(x, 0, 1, oracle_price))

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot([x[0] for x in dodo_A_001_example], [x[1] for x in dodo_A_001_example], linewidth=2)
ax.plot([x[0] for x in dodo_A_05_example], [x[1] for x in dodo_A_05_example], linewidth=2)
ax.plot([x[0] for x in dodo_A_099_example], [x[1] for x in dodo_A_099_example], linewidth=2)
ax.tick_params(axis="x", labelsize=LABELSIZE)
ax.tick_params(axis="y", labelsize=LABELSIZE)
ax.set_xlabel(
    r"Pool's token 1 reserve, $r_1$",
    labelpad=LABELPAD,
    size=FONTSIZE,
)
ax.set_ylim([0, 100])
ax.set_xlim([0, 100])
ax.legend(["0.01", "0.5", "0.99"], title=r"$\mathcal{A}$")  



X1 = 40
X2 = 40 

oracle_price = 1

DP18 = 1e18
LABELPAD = 20
FONTSIZE = 14
LABELSIZE = 12


dodo_A_001 = Dodo([X1, X2], 0.01)
dodo_A_05 = Dodo([X1, X2], 0.5)
dodo_A_099 = Dodo([X1, X2], 0.99)

dodo_A_001_example = []
dodo_A_05_example = []
dodo_A_099_example = []

slippage_domain = np.arange(-1 * X1, 2 * X1, 0.0001)

for qty_in in slippage_domain:
    dodo_A_001_example.append(dodo_A_001.slippage(qty_in, 0, 1, oracle_price))
    dodo_A_05_example.append(dodo_A_05.slippage(qty_in, 0, 1, oracle_price))
    dodo_A_099_example.append(dodo_A_099.slippage(qty_in, 0, 1, oracle_price))


fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot([x / X1 for x in slippage_domain],dodo_A_001_example,linewidth=2,)
ax.plot([x / X1 for x in slippage_domain],dodo_A_05_example,linewidth=2,)
ax.plot([x / X1 for x in slippage_domain],dodo_A_099_example,linewidth=2,)
ax.set_xlabel(
    r"Trade size relative to the reserve, $x_1 / r_1$",
    labelpad=LABELPAD,
    size=FONTSIZE,
)
ax.set_ylim([-1.0, 1.01])
ax.set_xlim([-1.0, 1.01])
ax.tick_params(axis="x", labelsize=LABELSIZE)
ax.tick_params(axis="y", labelsize=LABELSIZE)
ax.legend(["0.01", "0.5", "0.99"], title=r"$\mathcal{A}$")  