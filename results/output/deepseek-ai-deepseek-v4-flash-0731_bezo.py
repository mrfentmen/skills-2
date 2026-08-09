#!/usr/bin/env python3
"""
Customer-facing statement:
This service lets a customer check the status of their order by order ID.
It returns a clear, human-readable status (e.g., "shipped", "delivered") or
a friendly error if the order is not found. No login, no extra steps—just
the answer the customer needs.

Frugality justification:
- stdlib only (json, time, random) — a web framework or ORM is not worth the
  weight for a single read-only endpoint demo. No external dependencies.
"""

import json
import time
import random

# In-memory order store (simulates a database). In production this would be
# a horizontally partitioned key-value store, but for the demo it's a dict.
ORDERS = {
    "A100": {"item": "Kindle", "status": "shipped", "eta_days": 2},
    "B200": {"item": "Echo Dot", "status": "delivered", "eta_days": 0},
    "C300": {"item": "Fire Stick", "status": "processing", "eta_days": 5},
}

# Failure-mode handling: a per-order lookup that can fail (e.g., network
# timeout to the order DB) without killing the whole service. We retry with
# backoff, then return a degraded response instead of crashing.
def lookup_order(order_id, max_retries=3):
    for attempt in range(max_retries):
        try:
            # Simulate a flaky dependency: 20% chance of transient failure
            if random.random() < 0.2:
                raise ConnectionError("order DB timeout")
            if order_id not in ORDERS:
                return None
            return ORDERS[order_id]
        except ConnectionError:
            if attempt == max_retries - 1:
                # Degraded response: tell customer we're having trouble,
                # but the service stays up for other orders.
                return {"status": "unknown", "eta_days": None,
                        "item": "unavailable", "degraded": True}
            time.sleep(0.1 * (attempt + 1))  # backoff
    return None

# Minimal public surface: one function that returns a customer-friendly string.
def order_status(order_id):
    """Return a human-readable status string for an order ID."""
    order = lookup_order(order_id)
    if order is None:
        return f"Order {order_id} not found. Please check the ID and try again."
    if order.get("degraded"):
        return (f"Order {order_id}: we're temporarily unable to retrieve "
                "status. Please try again shortly.")
    if order["status"] == "delivered":
        return f"Order {order_id} ({order['item']}) was delivered."
    if order["status"] == "shipped":
        return (f"Order {order_id} ({order['item']}) is shipped. "
                f"Estimated delivery in {order['eta_days']} day(s).")
    return (f"Order {order_id} ({order['item']}) is being processed. "
            f"Estimated ship in {order['eta_days']} day(s).")

# Working entry point: runs standalone, prints results, exits.
if __name__ == "__main__":
    # Hardcoded sample data — no interactive input.
    sample_ids = ["A100", "B200", "C300", "Z999"]
    for oid in sample_ids:
        print(order_status(oid))
    # Demonstrate failure handling: force a degraded path by monkey-patching
    # random to always fail once, then recover.
    original_random = random.random
    random.random = lambda: 0.0  # always trigger the transient failure
    print(order_status("A100"))  # should show degraded message
    random.random = original_random
    print(order_status("A100"))  # should recover normally