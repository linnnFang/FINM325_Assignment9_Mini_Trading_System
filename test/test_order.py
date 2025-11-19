import pytest
from order import Order, OrderState

def test_order_initial_state_and_fields():
    o = Order("AAPL", 100, "BUY")
    assert o.symbol == "AAPL"
    assert o.qty == 100
    assert o.side == "BUY"
    assert o.state == OrderState.NEW

def test_valid_transitions_from_new():
    o = Order("AAPL", 100, "BUY")
    o.transition(OrderState.ACKED)
    assert o.state == OrderState.ACKED

    # Reset and go to REJECTED
    o = Order("AAPL", 100, "BUY")
    o.transition(OrderState.REJECTED)
    assert o.state == OrderState.REJECTED

def test_valid_transitions_from_acked():
    o = Order("AAPL", 100, "BUY")
    o.transition(OrderState.ACKED)
    o.transition(OrderState.FILLED)
    assert o.state == OrderState.FILLED

    o2 = Order("MSFT", 50, "SELL")
    o2.transition(OrderState.ACKED)
    o2.transition(OrderState.CANCELED)
    assert o2.state == OrderState.CANCELED

@pytest.mark.parametrize("start_state,new_state", [
    (OrderState.FILLED, OrderState.ACKED),
    (OrderState.FILLED, OrderState.CANCELED),
    (OrderState.CANCELED, OrderState.FILLED),
    (OrderState.REJECTED, OrderState.ACKED),
])
def test_invalid_transitions_from_terminal_states(start_state, new_state, capsys):
    # Construct by normal flow then force state to desired start_state
    o = Order("AAPL", 100, "BUY")
    o.state = start_state

    o.transition(new_state)
    # State should not change
    assert o.state == start_state

    # Check error message was printed (optional but nice)
    captured = capsys.readouterr()
    assert "Invalid transition" in captured.out
    assert start_state.name in captured.out
    assert new_state.name in captured.out