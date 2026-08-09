# Customer-facing statement: This service lets customers check their order status by order ID.
# It returns the status (e.g., "shipped", "processing") or a helpful error if the order is unknown.
# No external dependencies — stdlib only — a parser lib is not worth the weight.

import json
from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class OrderStatus:
    order_id: str
    status: str

class OrderStatusService:
    def __init__(self, known_orders: Dict[str, str]):
        # Known orders: in production this would come from a durable store, but today it's in-memory
        self.known_orders = known_orders

    def get_status(self, order_id: str) -> Optional[OrderStatus]:
        # Failure-mode handling: if the order_id is unknown, return None instead of raising
        status = self.known_orders.get(order_id)
        if status is None:
            return None
        return OrderStatus(order_id=order_id, status=status)

def run_demo():
    # Entry point: hardcoded sample data, compute, and print
    service = OrderStatusService({
        "A123": "shipped",
        "B456": "processing",
        "C789": "delivered"
    })

    # Exercise the service
    results = [
        service.get_status("A123"),
        service.get_status("B456"),
        service.get_status("UNKNOWN"),
        service.get_status("C789")
    ]

    # Print output
    print(json.dumps([r.__dict__ if r else None for r in results], indent=2))

if __name__ == "__main__":
    run_demo()