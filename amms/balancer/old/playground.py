# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np


fig = plt.figure()
ax = fig.gca(projection="3d")


# for equal weights
def plot_constant_product():
    v = 1_000
    X = np.arange(1, 11, 1)
    Y = np.arange(1, 11, 1)
    X, Y = np.meshgrid(X ** (1 / 3), Y ** (1 / 3))
    # V = B_1^{1/3} * B_2^{1/3} * B_3^{1/3}
    Z = v / (X * Y)

    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)

    # Customize the z axis.
    ax.set_zlim(222, 1_000)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter("%.02f"))

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()


if __name__ == "__main__":
    plot_constant_product()
