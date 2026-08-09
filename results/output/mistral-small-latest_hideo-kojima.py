# theme-mechanics link: the mechanic that makes the player FEEL isolation
#   You carry the weight of another player's absence through every step.
# constraint inversion: the limit is the feature: we can't render bullets, so we render absence
#   The game engine caps enemy sprites at 1; stealth becomes the only path.
# subversion: players expect A: "sneak past enemies"; we set up A, then give them B: "carry their absence"
#   The player must physically transport a ghostly echo of the last player's path.
# micro-detail: the 120ms fade on the ghost trail makes the fiction hold
#   Each step leaves a translucent footprint that lingers just long enough to feel fragile.
# connection system: asynchronous empathy: your bridge helps strangers you never see
#   Players leave ghost trails for unseen others, who later carry those echoes forward.

class EchoTrail:
    def __init__(self):
        self.grid = {}
        self.ghosts = {}
        self.steps = 0
        self.max_ghosts = 1  # the hardware limit inverted: only one ghost can exist at a time

    def step(self, x, y, player_id):
        self.steps += 1
        self.grid[(x, y)] = player_id
        # fade ghosts older than 120ms (simulated by step count)
        self.ghosts = {k: v for k, v in self.ghosts.items() if self.steps - v[1] < 120}
        # leave a ghost if we're under the cap
        if len(self.ghosts) < self.max_ghosts:
            self.ghosts[(x, y)] = (player_id, self.steps)

    def render(self):
        # print the grid with ghosts fading
        for y in range(5):
            row = []
            for x in range(5):
                if (x, y) in self.grid:
                    row.append(f"[{self.grid[(x, y)][-1]}]")
                elif (x, y) in self.ghosts:
                    age = self.steps - self.ghosts[(x, y)][1]
                    alpha = max(0, 1 - age / 120)
                    row.append(f"({self.ghosts[(x, y)][0][-1]})")
                else:
                    row.append(" . ")
            print("".join(row))
        print()

# simulate two players leaving echoes for each other
sim = EchoTrail()
sim.step(0, 0, "A")  # Player A steps at (0,0)
sim.render()
sim.step(1, 0, "A")  # Player A moves right
sim.render()
sim.step(1, 1, "B")  # Player B steps at (1,1) — unseen by A, but carries A's ghost
sim.render()
sim.step(0, 1, "B")  # Player B moves left, following A's ghost trail
sim.render()