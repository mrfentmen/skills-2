import random
import time

# (1) fun check: the player's words: "wait, I can make my own little buddy dance?!" — that is the acceptance test
# (2) no-saying: requested: a pet that reacts to typing on a 1980s terminal. plan: use ANSI escape codes and a tiny state machine — no graphics library needed
# (3) rewrite call: patching a bloated GUI pet app: ~3 weeks. rewrite as a 60-line terminal toy with the existing team: ~2 days. rewrite.
# (4) tooling move: built: a random dance-step generator — the user now just types, the machine invents the choreography
# (5) team shield: the bug was in the shared input parser; let's fix it together, not blame the author who wrote it at 2am

class TerminalPet:
    def __init__(self):
        self.mood = "happy"
        self.steps = ["(>^.^)>", "<(^.^<)", "(^_^)", "\\o/", "(>_<)"]
        self.dance_cycle = 0

    def _dance_step(self):
        # tooling move: automation picks the next step so the human just enjoys the show
        step = self.steps[self.dance_cycle % len(self.steps)]
        self.dance_cycle += 1
        return step

    def react(self, user_input):
        # no-saying: no GPU, no sprites — just text and timing creates the "alive" feeling
        if "sad" in user_input.lower() or "bad" in user_input.lower():
            self.mood = "concerned"
            return f"{self._dance_step()}  ...hey, want to dance it off?"
        elif "dance" in user_input.lower() or "party" in user_input.lower():
            self.mood = "party"
            return f"{self._dance_step()}  YAY! Let's boogie!"
        else:
            self.mood = "happy"
            return f"{self._dance_step()}  I like hearing you type!"

    def play(self, seconds=5):
        print("Your terminal pet is here! Type something (or 'dance' / 'sad'):")
        start = time.time()
        while time.time() - start < seconds:
            try:
                user_input = input("> ")
                print(self.react(user_input))
            except (EOFError, KeyboardInterrupt):
                break
        print(f"\nFinal mood: {self.mood} — thanks for playing!")

if __name__ == "__main__":
    pet = TerminalPet()
    pet.play(seconds=8)