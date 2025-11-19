'''
from fix_parser import FixParser
from order import Order, OrderState
from risk_engine import RiskEngine
from logger import Logger

def print_log(event, data):
    print(f"[LOG] {event} → {data}")

def main():
    fix = FixParser()
    risk = RiskEngine(max_order_size=500, max_position=1000)
    log = Logger()

    raw = "8=FIX.4.2|35=D|55=AAPL|54=1|38=500|40=2|10=128"
    msg = fix.parse(raw)

    # FIX side conversion
    side_map = {"1": "BUY", "2": "SELL"}
    order = Order(msg["55"], int(msg["38"]), side_map[msg["54"]])

    # Log creation
    log.log("OrderCreated", msg)
    print_log("OrderCreated", msg)

    try:
        risk.check(order)
        order.transition(OrderState.ACKED)
        print(f"Order {order.symbol} is now ACKED")

        risk.update_position(order)
        order.transition(OrderState.FILLED)
        print(f"Order {order.symbol} is now FILLED")

        log.log("OrderFilled", {"symbol": order.symbol, "qty": order.qty})
        print_log("OrderFilled", {"symbol": order.symbol, "qty": order.qty})

    except ValueError as e:
        order.transition(OrderState.REJECTED)
        log.log("OrderRejected", {"reason": str(e)})
        print_log("OrderRejected", {"reason": str(e)})

    log.save()
    print("\nSaved to events.json")

if __name__ == "__main__":
    main()
'''

from fix_parser import FixParser
from order import Order, OrderState
from risk_engine import RiskEngine
from logger import Logger


def print_log(event, data):
    print(f"[LOG] {event} → {data}")


def main():
    fix = FixParser()
    risk = RiskEngine(max_order_size=500, max_position=1000)
    log = Logger()

    # ---------- Scenario 1 ----------
    print("----- Scenario 1 -----")

    raw1 = "8=FIX.4.2|35=D|55=AAPL|54=1|38=500|40=2|10=128"
    msg1 = fix.parse(raw1)

    side_map = {"1": "BUY", "2": "SELL"}
    order1 = Order(msg1["55"], int(msg1["38"]), side_map[msg1["54"]])

    log.log("OrderCreated", msg1)
    print_log("OrderCreated", msg1)

    try:
        risk.check(order1)
        order1.transition(OrderState.ACKED)
        print(f"Order {order1.symbol} is now ACKED")

        risk.update_position(order1)
        order1.transition(OrderState.FILLED)
        print(f"Order {order1.symbol} is now FILLED")

        log.log("OrderFilled", {"symbol": order1.symbol, "qty": order1.qty})
        print_log("OrderFilled", {"symbol": order1.symbol, "qty": order1.qty})

    except ValueError as e:
        order1.transition(OrderState.REJECTED)
        log.log("OrderRejected", {"symbol": order1.symbol, "reason": str(e)})
        print_log("OrderRejected", {"symbol": order1.symbol, "reason": str(e)})



    # ---------- Scenario 2 (Risk Reject) ----------
    print("\n----- Scenario 2 -----")

    raw2 = "8=FIX.4.2|35=D|55=TSLA|54=1|38=20000|40=2|10=128"  # big quantity
    msg2 = fix.parse(raw2)

    order2 = Order(msg2["55"], int(msg2["38"]), side_map[msg2["54"]])

    log.log("OrderCreated", msg2)
    print_log("OrderCreated", msg2)

    try:
        risk.check(order2)
        order2.transition(OrderState.ACKED)
        print(f"Order {order2.symbol} is now ACKED")

        risk.update_position(order2)
        order2.transition(OrderState.FILLED)
        print(f"Order {order2.symbol} is now FILLED")

        log.log("OrderFilled", {"symbol": order2.symbol, "qty": order2.qty})
        print_log("OrderFilled", {"symbol": order2.symbol, "qty": order2.qty})

    except ValueError as e:
        order2.transition(OrderState.REJECTED)
        log.log("OrderRejected", {"symbol": order2.symbol, "reason": str(e)})
        print_log("OrderRejected", {"symbol": order2.symbol, "reason": str(e)})

    log.save()
    print("\nAll events saved to events.json")


if __name__ == "__main__":
    main()

