# risk_engine.py

class RiskEngine:
    def __init__(self, max_order_size=1000, max_position=2000):
        self.max_order_size = max_order_size
        self.max_position = max_position
        self.positions = {}   # {symbol: net_position}
    
    def get_position(self, symbol: str) -> int:
        return self.positions.get(symbol, 0)
    
    def check(self, order) -> None:
        symbol = order.symbol
        qty = order.qty
        side = order.side.upper()

        # --- Rule 1: Max order size ---
        if qty > self.max_order_size:
            raise ValueError(
                f"Order size {qty} exceeds max_order_size {self.max_order_size}"
            )

        # --- Rule 2: Position limit check ---
        current_pos = self.get_position(symbol)

        if side == "BUY":
            new_pos = current_pos + qty
        elif side == "SELL":
            new_pos = current_pos - qty
        else:
            raise ValueError(f"Invalid side {side}")

        if abs(new_pos) > self.max_position:
            raise ValueError(
                f"Position limit exceeded for {symbol}. "
                f"Current: {current_pos}, After Order: {new_pos}, Limit: {self.max_position}"
            )

        # Passed all checks
        return None

    def update_position(self, order):
        symbol = order.symbol
        qty = order.qty
        side = order.side.upper()

        current_pos = self.get_position(symbol)

        if side == "BUY":
            new_pos = current_pos + qty
        else:  # SELL
            new_pos = current_pos - qty

        self.positions[symbol] = new_pos
        print(f"[RISK] Updated position {symbol}: {current_pos} → {new_pos}")
