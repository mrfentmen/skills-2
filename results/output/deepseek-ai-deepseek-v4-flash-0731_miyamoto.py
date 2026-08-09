import random
import time

# (1) FUN-FIRST TEST: crude prototype before polish
# Core mechanic: "Echo Hop" - player bounces on a drum pad, each bounce
# spawns a delayed echo that can be re-bounced to reach higher platforms.
# Validated with ASCII art and a 0/1 input loop before any art/sound.
def fun_gate(playtest_score, budget):
    if playtest_score < 0.6:
        return {"action": "upend the tea table", "why": "fun failed the gate",
                "sunk_cost": f"{budget} spent, discarded anyway"}
    return {"action": "ship", "why": "fun passed in the crude prototype"}

# (2) MULTIPLE-PROBLEMS EVALUATION
# Idea: "Echo bounce" solves:
#   - traversal (reach height)
#   - timing puzzle (delayed echo creates rhythm)
#   - risk/reward (echo fades, so you must commit)
def multiple_problems(idea, problems_solved):
    return {"idea": idea, "problems_solved": problems_solved,
            "keep": len(problems_solved) >= 2}

# (3) WITHERED-TECHNOLOGY CHOICE
# Use a fixed-size ring buffer (mature, O(1), no GC) as the echo queue.
# Trade-off: no dynamic memory, but echo count is capped at 4 (design limit).
class EchoBuffer:
    def __init__(self, size=4):
        self.buf = [None] * size
        self.head = 0
        self.size = size
    def push(self, val):
        self.buf[self.head] = val
        self.head = (self.head + 1) % self.size
    def pop_oldest(self):
        idx = (self.head - 1) % self.size
        val = self.buf[idx]
        self.buf[idx] = None
        return val

# (4) WORDLESS ONBOARDING
# First screen: a single drum pad at ground level, a platform above.
# Player presses SPACE -> bounce -> echo appears below. No text.
# The echo's visual pulse (growing ring) teaches "wait, then bounce again".
# Player naturally discovers the echo by seeing it appear after their first jump.

# (5) UPEND-THE-TEA-TABLE GATE
# If playtest score < 0.6, we discard the whole mechanic and record why.
# Here we simulate a playtest that passed, but the gate is explicit.

# --- Prototype demo ---
class EchoHopPrototype:
    def __init__(self):
        self.player_y = 0
        self.velocity = 0
        self.echoes = EchoBuffer()
        self.platform_y = 3
        self.gravity = -1
        self.bounce_power = 2
        self.score = 0
        self.alive = True

    def step(self, action):
        # action: "bounce" or "wait"
        if action == "bounce" and self.player_y == 0:
            self.velocity = self.bounce_power
            self.echoes.push(self.player_y)  # echo spawns at current position
        # physics
        self.velocity += self.gravity
        self.player_y += self.velocity
        if self.player_y <= 0:
            self.player_y = 0
            self.velocity = 0
            # check if an echo is here to bounce on
            if self.echoes.pop_oldest() is not None:
                self.velocity = self.bounce_power * 0.8  # weaker echo bounce
                self.score += 1
        # win condition
        if self.player_y >= self.platform_y:
            self.alive = False
            return "win"
        return "alive"

    def render(self):
        # ASCII crude prototype - no art, just function
        lines = []
        for y in range(5, -1, -1):
            if y == self.platform_y:
                lines.append("  ===  ")
            elif y == int(self.player_y):
                lines.append("  [P]  ")
            elif y == 0:
                lines.append("  [D]  ")
            else:
                lines.append("       ")
        return "\n".join(lines)

# Run the prototype demo
proto = EchoHopPrototype()
print("=== ECHO HOP PROTOTYPE (crude, no polish) ===")
print("Press 'b' to bounce, 'w' to wait, 'q' to quit")
print(proto.render())

# Simulate a few steps to show the loop
for i in range(8):
    action = "bounce" if i % 2 == 0 else "wait"
    result = proto.step(action)
    print(f"\nStep {i+1} ({action}):")
    print(proto.render())
    if result == "win":
        print("REACHED PLATFORM! Core mechanic works.")
        break

# Fun gate evaluation (simulated playtest score)
print("\n--- DESIGN DOCUMENTATION ---")
print(fun_gate(0.8, 12000))  # passed, ship

print(multiple_problems("echo bounce", ["traversal", "timing puzzle", "risk/reward"]))

print("\nWithered tech: ring buffer (mature, O(1), no GC)")
print("Trade-off: capped at 4 echoes, but zero allocation and deterministic timing")

print("\nWordless onboarding: first screen has no text;")
print("echo appears after first bounce, teaching by cause/effect")

print("\nUpend gate: if playtest < 0.6, discard. Here it passed, so we ship.")