from amms.logger import l

DIVIDER = "----"


class Token:
    def __init__(self, x_i: float = 1, x_i_qty: float = 0):
        if x_i not in [1, 2]:
            return Exception("1 or 2 allowed")

        if x_i_qty <= 0:
            return Exception("must be positive")

        self.name = f"x_{x_i}"
        self.qty = x_i_qty
        self.complement = f"x_{2 if x_i is 1 else 1}"


class LogHelper:
    @staticmethod
    def pool_created(x_1, x_2, invariant):
        l.info(
            f"CREATED POOL.\n"
            f"x_1, x_2: {x_1:.8f}, {x_2:.8f}.\n"
            f"invariant {invariant}.\n"
            f"ex. rate x_1/x_2 = {x_2/x_1}.\n"
            f"{DIVIDER}\n\n"
        )

    @staticmethod
    def added_liquidity(x_1, prev_x_1, x_2, prev_x_2, invariant, prev_invariant):
        l.info(
            f"ADDED LIQUIDITY.\n"
            f"Δx_1, Δx_2: +{(x_1 - prev_x_1):.8f}, +{(x_2 - prev_x_2):.8f}.\n"
            f"x_1, x_2: {x_1:.8f}, {x_2:.8f}.\n"
            f"prev. invariant: ${prev_invariant:.8f}.\n"
            f"invariant: ${invariant:.8f}.\n"
            f"{DIVIDER}\n\n"
        )