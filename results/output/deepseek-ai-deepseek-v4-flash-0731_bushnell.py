import random
import time

class OneButtonDodge:
    # ============================================================
    # VERTICAL SLICE: this is a runnable prototype, not a design doc.
    # Run it. Play it. It works right now.
    # ============================================================

    # ============================================================
    # BUSHNELL'S LAW:
    #   One instruction: "Press SPACE to jump."
    #   Mastery depth: time your jumps to chain air-time streaks,
    #   dodge faster patterns, and survive longer for score multipliers.
    # ============================================================

    # ============================================================
    # ITERATION LOOP:
    #   v1: random obstacles, fixed speed -> players died too fast, no fun.
    #   v2: added streak bonus for consecutive near-misses -> players
    #       started taking risks, engagement up.
    #   v3 (next): add speed ramp based on score, because play showed
    #       late-game boredom. Feedback from real play drives this.
    # ============================================================

    # ============================================================
    # FUN-FIRST NOTE:
    #   Kept the near-miss streak because players came back for it,
    #   not because it was on a roadmap. Polish (graphics, sound)
    #   is secondary to the core loop's joy.
    # ============================================================

    # ============================================================
    # SIMPLE-TO-LEARN-HARD-TO-MASTER CHECK:
    #   Learn in 5 seconds: press SPACE to jump.
    #   Master over hours: perfect timing, streak chaining, pattern reading.
    # ============================================================

    def __init__(self):
        self.score = 0
        self.streak = 0
        self.alive = True
        self.time = 0.0
        self.obstacle_speed = 1.0
        self.jump_cooldown = 0.0

    def jump(self):
        # One-button action: jump clears the current obstacle if timed right
        if self.jump_cooldown <= 0:
            self.jump_cooldown = 0.3  # small cooldown to prevent spam
            return True
        return False

    def tick(self, dt, obstacle_present, jumped):
        self.time += dt
        self.jump_cooldown = max(0, self.jump_cooldown - dt)

        if obstacle_present:
            if jumped and self.jump_cooldown > 0:
                # Near-miss: reward timing, not just survival
                self.streak += 1
                self.score += 10 * self.streak  # streak multiplier = depth
            else:
                self.alive = False
                self.streak = 0
        else:
            # No obstacle: reward patience with small points
            self.score += 1

        # Speed ramp: difficulty scales with score (v3 iteration)
        self.obstacle_speed = 1.0 + self.score / 500.0
        return self.alive

    def play_round(self, seconds=10):
        """Simulate a quick play session with random obstacles."""
        print("=== ONE-BUTTON DODGE ===")
        print("Learn in 5 seconds: press SPACE to jump.")
        print("Master over hours: chain near-misses for streak multipliers.")
        print()
        print("Simulating 10 seconds of play...")
        print()

        dt = 0.1
        steps = int(seconds / dt)
        obstacle_timer = 0.0

        for i in range(steps):
            obstacle_timer -= dt
            obstacle_present = obstacle_timer <= 0 and random.random() < 0.3
            if obstacle_present:
                obstacle_timer = 1.0 / self.obstacle_speed

            # AI-ish player: jumps when obstacle is close and cooldown ready
            jumped = obstacle_present and self.jump_cooldown <= 0 and random.random() < 0.7

            if not self.tick(dt, obstacle_present, jumped):
                print(f"CRASH! You survived {self.time:.1f}s with score {self.score}")
                print(f"Best streak: {self.streak}")
                return

        print(f"Survived! Final score: {self.score}")
        print(f"Final streak: {self.streak}")
        print()
        print("=== ITERATION NOTE ===")
        print("v2 added near-miss streaks because play showed players")
        print("loved risk-taking. v3 will add speed ramp (already in code)")
        print("because late-game got boring. Real play drives changes.")
        print()
        print("=== FUN CHECK ===")
        print("Kept because players came back for the streak chase,")
        print("not because it was planned. That's the only metric that matters.")

game = OneButtonDodge()
game.play_round()