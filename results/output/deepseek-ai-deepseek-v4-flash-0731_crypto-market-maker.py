import random
import math

# ============================================================
# (1) ORDER-BOOK MODEL
# Two-way quotes around mid. Spread is sized by volatility and
# liquidity: spread = base_spread * (1 + vol_index) * (1 / liquidity_factor)
# ============================================================

class MarketMaker:
    def __init__(self, mid=100.0, base_spread=0.10, max_inventory=50.0, max_loss=200.0):
        self.mid = mid
        self.base_spread = base_spread
        self.inventory = 0.0          # positive = long, negative = short
        self.max_inventory = max_inventory
        self.max_loss = max_loss
        self.realized_pnl = 0.0
        self.entry_price = mid

    # ============================================================
    # (2) INVENTORY SKEW LOGIC
    # skew = inventory * k  (k = 0.02)
    # Positive inventory -> lower both quotes to sell what we hold
    # Negative inventory -> raise both quotes to buy back
    # ============================================================
    def inventory_skew(self):
        k = 0.02
        return self.inventory * k

    # ============================================================
    # (3) VOLATILITY REACTION
    # vol_index spikes -> spread widens to avoid adverse selection
    # ============================================================
    def vol_index(self, recent_returns):
        if not recent_returns:
            return 0.0
        mean = sum(recent_returns) / len(recent_returns)
        variance = sum((r - mean) ** 2 for r in recent_returns) / len(recent_returns)
        return math.sqrt(variance) * 100  # scale to percentage

    def quote(self, recent_returns, liquidity_factor=1.0):
        vol = self.vol_index(recent_returns)
        spread = self.base_spread * (1 + vol) * (1.0 / liquidity_factor)
        skew = self.inventory_skew()
        bid = self.mid - spread / 2 - skew
        ask = self.mid + spread / 2 - skew
        return {"bid": round(bid, 2), "ask": round(ask, 2), "spread": round(spread, 2), "skew": round(skew, 2)}

    # ============================================================
    # (4) FUN/EDGE NOTE
    # The strategy makes money on the spread (bid-ask capture) when
    # volatility is low and liquidity is high. It loses money when:
    # - Vol spikes and the market moves through our stale quotes
    # - Inventory builds up and we get run over by adverse selection
    # - Funding arbitrage is ignored (we don't harvest carry here)
    # ============================================================

    # ============================================================
    # (5) RISK CHECK
    # Max inventory = 50 units, max loss = $200.
    # If either is breached, we stop quoting and flatten.
    # ============================================================
    def risk_check(self):
        if abs(self.inventory) > self.max_inventory:
            return False, f"INVENTORY LIMIT BREACHED: {self.inventory}"
        if self.realized_pnl < -self.max_loss:
            return False, f"MAX LOSS BREACHED: {self.realized_pnl}"
        return True, "OK"

    def simulate_trade(self, side, price, qty):
        # side: 'buy' (we buy from market) or 'sell' (we sell to market)
        if side == 'buy':
            self.inventory += qty
            self.realized_pnl -= qty * price
        else:
            self.inventory -= qty
            self.realized_pnl += qty * price

    def run_simulation(self, steps=20):
        print("=== MARKET MAKER SIMULATION ===")
        print(f"Initial mid: {self.mid}, base_spread: {self.base_spread}")
        print(f"Max inventory: {self.max_inventory}, max loss: {self.max_loss}\n")

        recent_returns = []
        for step in range(steps):
            # Simulate market moves (random walk with occasional vol spike)
            shock = random.gauss(0, 0.1)
            if random.random() < 0.1:  # 10% chance of vol spike
                shock += random.choice([-1.0, 1.0]) * random.uniform(0.5, 1.5)
            self.mid += shock
            recent_returns.append(shock)
            if len(recent_returns) > 10:
                recent_returns.pop(0)

            # Liquidity factor: random between 0.5 (thin) and 2.0 (deep)
            liquidity = random.uniform(0.5, 2.0)

            quotes = self.quote(recent_returns, liquidity)
            ok, msg = self.risk_check()
            if not ok:
                print(f"Step {step+1}: {msg} — STOPPING")
                break

            # Simulate a random trade hitting our quotes
            if random.random() < 0.6:
                side = 'buy' if random.random() < 0.5 else 'sell'
                qty = random.uniform(1, 10)
                price = quotes['ask'] if side == 'buy' else quotes['bid']
                self.simulate_trade(side, price, qty)

            print(f"Step {step+1:2d} | mid={self.mid:7.2f} | bid={quotes['bid']:7.2f} | "
                  f"ask={quotes['ask']:7.2f} | spread={quotes['spread']:5.2f} | "
                  f"skew={quotes['skew']:6.2f} | inv={self.inventory:6.2f} | "
                  f"pnl={self.realized_pnl:8.2f} | vol={self.vol_index(recent_returns):5.2f} | "
                  f"liq={liquidity:4.2f}")

        print("\n=== FINAL STATE ===")
        print(f"Inventory: {self.inventory:.2f}")
        print(f"Realized PnL: ${self.realized_pnl:.2f}")
        ok, msg = self.risk_check()
        print(f"Risk status: {msg}")

if __name__ == "__main__":
    mm = MarketMaker()
    mm.run_simulation()