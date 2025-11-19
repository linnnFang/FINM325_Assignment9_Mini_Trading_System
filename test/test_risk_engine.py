import pytest
from risk_engine import RiskEngine
from order import Order


class DummyOrder:
    """Simple stand-in when we only care about attributes, not Order logic."""
    def __init__(self, symbol, qty, side):
        self.symbol = symbol
        self.qty = qty
        self.side = side


def test_get_position_default_zero():
    r = RiskEngine(max_order_size=1000, max_position=2000)
    assert r.get_position("AAPL") == 0


def test_get_position_after_update():
    r = RiskEngine(max_order_size=1000, max_position=2000)
    order = DummyOrder("AAPL", 100, "BUY")
    r.update_position(order)
    assert r.get_position("AAPL") == 100


@pytest.mark.parametrize("qty", [1001, 5000])
def test_check_rejects_when_exceeds_max_order_size(qty):
    r = RiskEngine(max_order_size=1000, max_position=2000)
    order = DummyOrder("AAPL", qty, "BUY")
    with pytest.raises(ValueError) as excinfo:
        r.check(order)
    assert "exceeds max_order_size" in str(excinfo.value)


def test_check_rejects_when_position_limit_exceeded_on_buy():
    r = RiskEngine(max_order_size=1000, max_position=200)
    # current position 150
    r.positions["AAPL"] = 150
    order = DummyOrder("AAPL", 100, "BUY")
    with pytest.raises(ValueError) as excinfo:
        r.check(order)
    msg = str(excinfo.value)
    assert "Position limit exceeded" in msg
    assert "AAPL" in msg


def test_check_rejects_when_position_limit_exceeded_on_sell():
    r = RiskEngine(max_order_size=1000, max_position=200)
    # current position -150
    r.positions["AAPL"] = -150
    order = DummyOrder("AAPL", 100, "SELL")
    with pytest.raises(ValueError):
        r.check(order)


def test_check_invalid_side_raises():
    r = RiskEngine(max_order_size=1000, max_position=2000)
    order = DummyOrder("AAPL", 10, "INVALID")
    with pytest.raises(ValueError) as excinfo:
        r.check(order)
    assert "Invalid side" in str(excinfo.value)


def test_update_position_buy_and_sell_round_trip():
    r = RiskEngine(max_order_size=1000, max_position=2000)
    buy = DummyOrder("MSFT", 50, "BUY")
    sell = DummyOrder("MSFT", 20, "SELL")

    r.update_position(buy)
    assert r.get_position("MSFT") == 50

    r.update_position(sell)
    assert r.get_position("MSFT") == 30
