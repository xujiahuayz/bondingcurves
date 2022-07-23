from amms.curve.main import Curve


def test_trade_and_slippage():
    curve = Curve([2_000, 2_000], 1)
    assert curve.slippage(10, 0, 1) == 0
    amount_out = curve.trade(10, 0, 1)
    assert amount_out == 10

    curve = Curve([2_000, 2_000], 1)
    slippage = curve.slippage(71, 0, 1)
    assert round(slippage, 3) == 0.014
    amount_out = curve.trade(71, 0, 1)
    assert amount_out == 70
