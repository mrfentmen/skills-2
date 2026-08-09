import numpy as np
from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass
class Book:
    mid: float
    volatility: float
    inventory: float
    exchange_inflow: float = 0.0
    whale_move: float = 0.0
    funding_rate: float = 0.0
    latency_ms: int = 50
    slippage_bps: float = 2.0
    max_inventory: float = 100.0
    max_loss_pct: float = 0.05

def compute_spread(volatility: float, liquidity_factor: float = 0.001) -> float:
    """Spread sized by volatility and liquidity: wider when vol spikes."""
    return liquidity_factor * (1.0 + volatility)

def inventory_skew(inventory: float, skew_factor: float = 0.0005) -> float:
    """Skew quotes to pull inventory toward zero."""
    return inventory * skew_factor

def quote(mid: float, volatility: float, inventory: float) -> Dict[str, float]:
    """Two-sided quotes with spread sized by volatility and inventory skew."""
    spread = compute_spread(volatility)
    skew = inventory_skew(inventory)
    bid = mid - spread / 2 - skew
    ask = mid + spread / 2 - skew
    return {"bid": round(bid, 2), "ask": round(ask, 2)}

def update_book(book: Book, trade: Tuple[str, float]) -> Book:
    """Update book mid and inventory based on trade (side, size)."""
    side, size = trade
    if side == "buy":
        book.mid += size * book.slippage_bps / 10000
        book.inventory += size
    elif side == "sell":
        book.mid -= size * book.slippage_bps / 10000
        book.inventory -= size
    return book

def funding_arbitrage(book: Book) -> Tuple[bool, str]:
    """Harvest carry when funding is extreme (e.g., > 0.1% per 8h)."""
    if abs(book.funding_rate) > 0.001:
        return True, "enter_carry_trade"
    return False, "no_action"

def on_chain_signal(book: Book) -> str:
    """Treat on-chain data as signals: inflow/outflow or whale moves."""
    if book.exchange_inflow > 1000 or book.whale_move > 500:
        return "high_inflow_whale_move"
    return "normal"

def simulate_episode(book: Book, trades: list) -> Dict:
    """Run a simulation episode with trades and return results."""
    for trade in trades:
        book = update_book(book, trade)
        # Volatility reacts to whale moves or large trades
        if book.whale_move > 500 or any(t[1] > 100 for t in trades):
            book.volatility = min(book.volatility * 1.5, 2.0)
    # Check funding arbitrage
    arb, action = funding_arbitrage(book)
    # Check inventory risk
    inventory_risk = abs(book.inventory) / book.max_inventory
    # Quote
    quotes = quote(book.mid, book.volatility, book.inventory)
    return {
        "mid": round(book.mid, 2),
        "volatility": round(book.volatility, 4),
        "inventory": round(book.inventory, 2),
        "quotes": quotes,
        "funding_arb": arb,
        "on_chain_signal": on_chain_signal(book),
        "inventory_risk": round(inventory_risk, 3),
        "max_loss": round(book.max_loss_pct * book.mid * book.max_inventory, 2)
    }

# Simulation
initial_book = Book(
    mid=100.0,
    volatility=0.3,
    inventory=0.0,
    exchange_inflow=800,
    whale_move=600,
    funding_rate=0.0015,
    latency_ms=50,
    slippage_bps=2.0,
    max_inventory=100.0,
    max_loss_pct=0.05
)
trades = [("buy", 20), ("sell", 15), ("buy", 30)]
result = simulate_episode(initial_book, trades)
print(result)