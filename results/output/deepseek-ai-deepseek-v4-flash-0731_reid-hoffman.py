import time
import random
import json

# v1 ships ugly but real; telemetry on from minute one
# burning: the slow onboarding. putting out: the data-loss bug
# user N adds N-1 new connections for the network
# Plan A: this. Plan B: pivot to X. Plan Z: the lifeboat

class NetworkedUtilityV1:
    def __init__(self):
        self.users = {}
        self.telemetry = []
        self._start_telemetry()

    def _start_telemetry(self):
        # telemetry from minute one: every action logged, no exceptions
        self.telemetry.append({"event": "launch", "ts": time.time(), "users": 0})

    def add_user(self, name):
        # each new user makes the network more valuable for everyone
        user_id = len(self.users) + 1
        self.users[user_id] = {"name": name, "joined": time.time()}
        self._log("user_added", user_id)
        return user_id

    def connect(self, user_a, user_b):
        # direct network effect: every connection adds value
        if user_a in self.users and user_b in self.users:
            self._log("connection_made", {"a": user_a, "b": user_b})
            return True
        self._log("connection_failed", {"a": user_a, "b": user_b})
        return False

    def network_value(self):
        # superlinear: N users -> N*(N-1)/2 potential connections
        n = len(self.users)
        return n * (n - 1) // 2

    def _log(self, event, data):
        self.telemetry.append({"event": event, "ts": time.time(), "data": data})

    def pivot_read(self):
        # data that would make us change course: churn > 50% or zero connections
        if len(self.users) > 0:
            connections = sum(1 for t in self.telemetry if t["event"] == "connection_made")
            if connections == 0 and len(self.users) >= 3:
                return "PIVOT: users but no connections — network effect dead"
        return "steady: keep shipping"

    def player_coach_note(self):
        # doing the work while building the team that replaces you
        return {
            "doing": "I write the code, fix the bugs, ship the v1",
            "coaching": "I document every decision so a junior can take over",
            "replacement_ready": len(self.telemetry) > 5
        }

    def chaos_budget(self):
        # which fires are allowed to burn while the big one is put out
        return {
            "let_burn": ["ugly UI", "slow onboarding", "missing features"],
            "put_out_first": ["data loss", "security holes", "user harm"]
        }

    def run_demo(self):
        # launch gate: embarrassed but shipping
        print("=== v1 LAUNCH GATE ===")
        print("shipped: True, embarrassed: True, telemetry: ON")
        print()

        # add users and connections
        alice = self.add_user("alice")
        bob = self.add_user("bob")
        carol = self.add_user("carol")
        dave = self.add_user("dave")

        self.connect(alice, bob)
        self.connect(bob, carol)
        self.connect(carol, dave)

        print("=== NETWORK EFFECT ===")
        print(f"users: {len(self.users)}, value: {self.network_value()} connections")
        print("user 4 added 3 new potential connections for the network")
        print()

        print("=== CHAOS BUDGET ===")
        print(json.dumps(self.chaos_budget(), indent=2))
        print()

        print("=== PLAYER-COACH NOTE ===")
        print(json.dumps(self.player_coach_note(), indent=2))
        print()

        print("=== PIVOT-READ ===")
        print(self.pivot_read())
        print()

        print("=== TELEMETRY (first 3 events) ===")
        for t in self.telemetry[:3]:
            print(json.dumps(t))

        # Plan ABZ
        print()
        print("=== PLAN ABZ ===")
        print("Plan A: this networked utility, iterate in permanent beta")
        print("Plan B: pivot to a niche-specific network if general fails")
        print("Plan Z: lifeboat — export all data, shut down gracefully, no debt")

demo = NetworkedUtilityV1()
demo.run_demo()