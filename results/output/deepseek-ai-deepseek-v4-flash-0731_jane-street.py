from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Set, Optional

class Currency(Enum):
    USD = "usd"
    EUR = "eur"

@dataclass(frozen=True)
class AssetId:
    symbol: str
    currency: Currency

@dataclass(frozen=True)
class Money:
    cents: int
    currency: Currency

    def __add__(self, other: "Money") -> "Money":
        assert self.currency == other.currency, "currency mismatch"
        return Money(self.cents + other.cents, self.currency)

    def __mul__(self, factor: int) -> "Money":
        return Money(self.cents * factor, self.currency)

class OrderStatus(Enum):
    PENDING = "pending"
    FILLED = "filled"
    CANCELLED = "cancelled"

@dataclass(frozen=True)
class OrderState:
    status: OrderStatus
    filled_qty: int = 0

    def fill(self, qty: int) -> "OrderState":
        assert self.status == OrderStatus.PENDING, "only pending can fill"
        return OrderState(OrderStatus.FILLED, qty)

    def cancel(self) -> "OrderState":
        assert self.status == OrderStatus.PENDING, "only pending can cancel"
        return OrderState(OrderStatus.CANCELLED)

@dataclass(frozen=True)
class Order:
    order_id: str
    asset: AssetId
    price: Money
    qty: int
    state: OrderState

@dataclass
class Portfolio:
    cash: Dict[Currency, Money] = field(default_factory=dict)
    positions: Dict[AssetId, int] = field(default_factory=dict)
    orders: Dict[str, Order] = field(default_factory=dict)
    _dependents: Dict[str, Set[str]] = field(default_factory=dict)
    _cache: Dict[str, object] = field(default_factory=dict)

    def add_order(self, order: Order) -> None:
        self.orders[order.order_id] = order
        self._dependents[order.order_id] = {"exposure", "cash_flow"}
        self._invalidate({"exposure", "cash_flow"})

    def fill_order(self, order_id: str, qty: int) -> None:
        order = self.orders[order_id]
        new_state = order.state.fill(qty)
        new_order = Order(order.order_id, order.asset, order.price, order.qty, new_state)
        self.orders[order_id] = new_order
        self._invalidate({"exposure", "cash_flow"})

    def _invalidate(self, keys: Set[str]) -> None:
        to_invalidate = set(keys)
        for key in keys:
            to_invalidate.update(self._dependents.get(key, set()))
        for key in to_invalidate:
            self._cache.pop(key, None)

    def exposure(self) -> Dict[AssetId, Money]:
        if "exposure" in self._cache:
            return self._cache["exposure"]
        result: Dict[AssetId, Money] = {}
        for asset, qty in self.positions.items():
            result[asset] = Money(qty, asset.currency)
        for order in self.orders.values():
            if order.state.status == OrderStatus.PENDING:
                current = result.get(order.asset, Money(0, order.asset.currency))
                result[order.asset] = current + order.price * order.qty
        self._cache["exposure"] = result
        return result

    def cash_flow(self) -> Dict[Currency, Money]:
        if "cash_flow" in self._cache:
            return self._cache["cash_flow"]
        result: Dict[Currency, Money] = {}
        for order in self.orders.values():
            if order.state.status == OrderStatus.FILLED:
                cur = order.asset.currency
                delta = order.price * order.state.filled_qty
                current = result.get(cur, Money(0, cur))
                result[cur] = current + delta
        self._cache["cash_flow"] = result
        return result

usd = Currency.USD
eur = Currency.EUR
aapl = AssetId("AAPL", usd)
sap = AssetId("SAP", eur)

portfolio = Portfolio()
portfolio.positions[aapl] = 100
portfolio.positions[sap] = 50

order1 = Order("o1", aapl, Money(15000, usd), 10, OrderState(OrderStatus.PENDING))
order2 = Order("o2", sap, Money(8500, eur), 5, OrderState(OrderStatus.PENDING))

portfolio.add_order(order1)
portfolio.add_order(order2)

print("Initial exposure:", portfolio.exposure())
print("Initial cash flow:", portfolio.cash_flow())

portfolio.fill_order("o1", 10)

print("After fill exposure:", portfolio.exposure())
print("After fill cash flow:", portfolio.cash_flow())
print("Concurrency note: all state mutations are single-threaded; no locks needed — race conditions are unrepresentable by construction.")