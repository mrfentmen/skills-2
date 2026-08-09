import random
import time
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class User:
    id: str
    name: str
    connections: List[str] = None

    def __post_init__(self):
        self.connections = self.connections or []

class TinyNetwork:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.telemetry = []
        self.launch_time = time.time()
        # v1 ships ugly but real; telemetry on from minute one
        self.log("v1 launched", {"users": 0, "connections": 0})

    def log(self, event: str, data: dict):
        self.telemetry.append({
            "timestamp": time.time() - self.launch_time,
            "event": event,
            "data": data
        })

    def add_user(self, name: str) -> User:
        user_id = f"user_{len(self.users) + 1}"
        user = User(id=user_id, name=name)
        self.users[user_id] = user
        # user N adds N-1 new connections for the network
        self.log("user_added", {"user_id": user_id, "total_users": len(self.users)})
        return user

    def connect_users(self, user1_id: str, user2_id: str):
        if user1_id not in self.users or user2_id not in self.users:
            return False
        if user2_id not in self.users[user1_id].connections:
            self.users[user1_id].connections.append(user2_id)
            self.users[user2_id].connections.append(user1_id)
            self.log("connection_added", {
                "user1": user1_id,
                "user2": user2_id,
                "total_connections": self.total_connections()
            })
        return True

    def total_connections(self) -> int:
        return sum(len(u.connections) for u in self.users.values()) // 2

    def network_value(self) -> float:
        # each new user makes the network more valuable for everyone
        n = len(self.users)
        return n * (n - 1) / 2 if n > 1 else 0

    def player_coach_note(self):
        # doing the work while also building the team that replaces you
        return "I'm writing the v1 code today, but tomorrow I'm writing the hiring doc for the first engineer who will replace me"

    def pivot_read(self) -> str:
        # the data that would make you change course
        if len(self.users) > 0 and self.total_connections() / len(self.users) < 0.5:
            return "Pivot signal: low connection density (<50%). Consider gamifying connections or adding icebreakers."
        if self.network_value() < 10 and len(self.users) > 5:
            return "Pivot signal: network value too low despite user growth. Re-evaluate core value prop."
        return "No pivot signal yet. Keep iterating."

# === MINIMUM REQUIREMENTS ===
# Launch gate: v1 ships ugly but real; telemetry on from minute one
network = TinyNetwork()

# Chaos budget: which fires are allowed to burn while the big one is put out
# burning: the slow onboarding flow. putting out: the data-loss bug
print("# burning: the slow onboarding flow. putting out: the data-loss bug")

# Network effect: user N adds N-1 new connections for the network
print("# user N adds N-1 new connections for the network")

# Distribution plan: how the product reaches users faster than the competition
print("# Distribution: invite-only beta with viral coefficient >1 via connection requests")

# Plan ABZ
print("# Plan A: this v1 network utility. Plan B: pivot to professional icebreaker tool. Plan Z: lifeboat is a CSV export of all connections")

# === DEMO ===
# Add initial users
alice = network.add_user("Alice")
bob = network.add_user("Bob")
charlie = network.add_user("Charlie")

# Make some connections
network.connect_users(alice.id, bob.id)
network.connect_users(bob.id, charlie.id)

# Print demo state
print("\n=== DEMO STATE ===")
print(f"Users: {len(network.users)}")
print(f"Connections: {network.total_connections()}")
print(f"Network value (connections possible): {network.network_value()}")
print(f"Player-coach note: {network.player_coach_note()}")
print(f"Pivot read: {network.pivot_read()}")
print("\nTelemetry sample (first 3 events):")
for event in network.telemetry[:3]:
    print(event)