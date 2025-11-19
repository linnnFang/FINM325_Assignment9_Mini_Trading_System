# order.py
from enum import Enum, auto

class OrderState(Enum):
    NEW = auto()
    ACKED = auto()
    FILLED = auto()
    CANCELED = auto()
    REJECTED = auto()


class Order:

    ALLOWED_TRANSITIONS = {
        OrderState.NEW: {OrderState.ACKED, OrderState.REJECTED},
        OrderState.ACKED: {OrderState.FILLED, OrderState.CANCELED},
        # FILLED, CANCELED, REJECTED → terminal states (no transitions allowed)
    }

    def __init__(self, symbol: str, qty: int, side: str):
        self.symbol = symbol
        self.qty = qty
        self.side = side
        self.state = OrderState.NEW

    def transition(self, new_state: OrderState):

        allowed_next_states = self.ALLOWED_TRANSITIONS.get(self.state, set())

        if new_state in allowed_next_states:
            '''
            print(f"[OK] Transition {self.state.name} → {new_state.name}")
            '''
            self.state = new_state
        else:
            print(f"[ERROR] Invalid transition {self.state.name} → {new_state.name}")
            print(f"        Allowed: {[s.name for s in allowed_next_states]}")


if __name__ == "__main__":
    order = Order("AAPL", 100, "BUY")

    order.transition(OrderState.ACKED)     # OK
    order.transition(OrderState.FILLED)    # OK
    order.transition(OrderState.CANCELED)  # INVALID (terminal)
