#!/usr/bin/env python
import matplotlib.pyplot as plt
from typing import Any
import numpy as np
import json
import sys
import os

module_path = os.path.dirname(os.path.dirname(os.path.abspath(".")))

# to make it work out of the box in interactive shells
if module_path not in sys.path:
    sys.path.insert(0, module_path)

# Impermanent loss - what you lose due to price movements whilst staying
# in the liquidity pool. In the case of Uniswap, imagine you go into the
# pool with x_1 and x_2. This implies an exchange rate x_2 / x_1.
# Now this exchange rate changes, denote new exchange rate \mu. What is the
# loss?

# If you were to hold, you would get x_1 + x_2 / \mu
# Arbers, moved the price, new reserves is x_1_new = sqrt(invariant / \mu)