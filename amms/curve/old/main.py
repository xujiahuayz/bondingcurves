#!/usr/bin/env python


def get_D(xp: list[int], amplification: float):
    S = sum(xp)
    if S == 0:
        return 0

    n_coins = len(xp)
    d_prev = 0.0
    d = float(S)
    Ann = amplification * n_coins

    for i in range(255):
        d_p = d
        for x in xp:
            d_p = d_p * d / (x * n_coins)
        d_prev = d
        d = (
            (Ann * S + d_p * n_coins)
            * d
            / ((Ann - 1) * d + (n_coins + 1) * d_p)
        )
        print("d", d)
        if abs(d_prev - d) <= 1:
            break

    return d


if __name__ == "__main__":
    get_D([300_442_800, 275_520_769, 230_782_523], 100)
