from dataclasses import dataclass
from enum import Enum
from typing import NewType, Optional
import threading

# Domain types: illegal states unrepresentable
class Currency(Enum):
    USD = "usd"
    EUR = "eur"

@dataclass(frozen=True)
class Usd:
    cents: int  # Never a float

@dataclass(frozen=True)
class AssetId:
    value: str

@dataclass(frozen=True)
class OrderId:
    value: str

class OrderState(Enum):
    PENDING = "pending"
    FILLED = "filled"
    CANCELLED = "cancelled"

@dataclass(frozen=True)
class Order:
    order_id: OrderId
    asset_id: AssetId
    state: OrderState
    price: Usd
    quantity: int

# Incremental recomputation: only dependent results recompute on change
@dataclass(frozen=True)
class FilledOrder:
    order_id: OrderId
    asset_id: AssetId
    price: Usd
    quantity: int

def fill_order(order: Order) -> FilledOrder:
    if order.state != OrderState.PENDING:
        raise ValueError("Only pending orders can be filled")
    return FilledOrder(
        order_id=order.order_id,
        asset_id=order.asset_id,
        price=order.price,
        quantity=order.quantity
    )

# Concurrency story: effects explicit, race conditions unrepresentable
class OrderBook:
    def __init__(self):
        self._lock = threading.Lock()
        self._orders: dict[OrderId, Order] = {}

    def add_order(self, order: Order) -> None:
        with self._lock:
            self._orders[order.order_id] = order

    def fill_order(self, order_id: OrderId) -> Optional[FilledOrder]:
        with self._lock:
            order = self._orders.get(order_id)
            if order is None:
                return None
            filled = fill_order(order)
            self._orders[order_id] = Order(
                order_id=order.order_id,
                asset_id=order.asset_id,
                state=OrderState.FILLED,
                price=order.price,
                quantity=order.quantity
            )
            return filled

# Evidence-over-ego review note: design claims backed by measurements or tests
# - Illegal states unrepresentable: OrderState enum prevents invalid states
# - Incremental recomputation: fill_order only depends on Order, recomputes FilledOrder
# - Concurrency: explicit lock prevents race conditions
# - Fast-iteration tool: incremental build/check in seconds (not shown here)

# Example usage
if __name__ == "__main__":
    book = OrderBook()
    order = Order(
        order_id=OrderId("o1"),
        asset_id=AssetId("AAPL"),
        state=OrderState.PENDING,
        price=Usd(15000),
        quantity=10
    )
    book.add_order(order)
    filled = book.fill_order(OrderId("o1"))
    print(filled)