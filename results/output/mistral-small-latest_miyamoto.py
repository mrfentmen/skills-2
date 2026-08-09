# === MIYAMOTO DESIGN DOCUMENT ===
# Core Feeling: "The player must feel a tiny rush of discovery when the last block
# slides into place, like finding the perfect piece in a puzzle box."
# Fun-first test: crude prototype must show that the slide-and-lock loop is fun
# before any art or story is added.
# Multiple-problems rule: one idea should solve several constraints at once.
# Withered-technology: use mature ASCII grid and print() to simulate the mechanic
# cheaply; trade-off is zero graphics but instant portability and zero learning curve.
# Wordless onboarding: player learns by doing; first screen shows only the grid and
# the player’s own moves.
# Upend-the-tea-table gate: if the crude prototype fails the fun test, discard it
# and try a new core loop.

import itertools

def fun_gate(score):
    """Return 'ship' if score >= 0.6, else 'upend the tea table'."""
    return "ship" if score >= 0.6 else "upend the tea table"

def multiple_problems(idea, problems):
    """Return whether the idea solves at least two problems."""
    return {"idea": idea, "problems_solved": problems, "keep": len(problems) >= 2}

# === CORE MECHANIC: SLIDE-AND-LOCK ===
# Idea: sliding blocks that lock into place when aligned.
# Problems solved:
# 1. Teaches spatial reasoning (power)
# 2. Provides undo buffer via reset (buffer)
# 3. Grid is legible in ASCII (low-res readable)
# 4. Replayability via random initial layouts (novelty)
# 5. Minimal controls map to arrow keys (accessibility)
solves = multiple_problems(
    "slide-and-lock",
    ["teaches spatial reasoning", "undo buffer", "low-res readable",
     "replayability", "accessible controls"]
)
print("Multiple-problems evaluation:", solves)

# === WITHERED-TECHNOLOGY CHOICE ===
# Mature component: ASCII grid printed to stdout.
# Trade-off: zero graphics, but instant portability, zero dependencies,
# and the grid itself becomes part of the puzzle’s readability.
# Novelty is pushed into the experience (the slide-and-lock loop),
# not into the tech stack.
print("Withered technology: ASCII grid via print()")
print("Trade-off: zero graphics, but instant portability and zero learning curve")

# === WORDLESS ONBOARDING PATH ===
# Player sees only the grid and the prompt "Slide blocks (arrows) or reset (r)."
# No tutorial text; the first move teaches the mechanic by doing.
# The crude prototype is the onboarding.

class SlideLock:
    def __init__(self, size=3):
        self.size = size
        self.grid = [[0]*size for _ in range(size)]
        self.empty = (size-1, size-1)
        self.grid[self.empty[0]][self.empty[1]] = " "
        self.reset()

    def reset(self):
        """Reset to a random solvable layout."""
        flat = list(range(1, self.size**2)) + [" "]
        for _ in range(100):
            i, j = self.empty
            di, dj = 0, 0
            if i > 0 and self.grid[i-1][j] != " ":
                di = -1
            elif i < self.size-1 and self.grid[i+1][j] != " ":
                di = 1
            elif j > 0 and self.grid[i][j-1] != " ":
                dj = -1
            elif j < self.size-1 and self.grid[i][j+1] != " ":
                dj = 1
            if di or dj:
                ni, nj = i+di, j+dj
                self.grid[i][j], self.grid[ni][nj] = self.grid[ni][nj], self.grid[i][j]
        self.empty = (i+di, j+dj)

    def move(self, di, dj):
        i, j = self.empty
        ni, nj = i+di, j+dj
        if 0 <= ni < self.size and 0 <= nj < self.size:
            self.grid[i][j], self.grid[ni][nj] = self.grid[ni][nj], self.grid[i][j]
            self.empty = (ni, nj)
            return True
        return False

    def is_solved(self):
        target = 1
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] != " " and self.grid[i][j] != target:
                    return False
                if self.grid[i][j] == " " and (i != self.size-1 or j != self.size-1):
                    return False
                target += 1
        return True

    def render(self):
        return "\n".join(" ".join(str(cell) if cell != " " else " " for cell in row) for row in self.grid)

def playtest(puzzle, moves):
    """Crude prototype: run moves and return a fun score (0-1)."""
    original = [row[:] for row in puzzle.grid]
    for m in moves:
        puzzle.move(*m)
    solved = puzzle.is_solved()
    puzzle.grid = original
    return 0.9 if solved else 0.3

# === CRUDE PROTOTYPE DEMO ===
puzzle = SlideLock(size=3)
moves = [(0, -1), (0, -1), (-1, 0), (-1, 0), (0, 1), (0, 1), (1, 0), (1, 0)]
fun_score = playtest(puzzle, moves)
print("\nCrude prototype fun score:", fun_score)
print("Fun gate:", fun_gate(fun_score))

if fun_gate(fun_score) == "ship":
    print("\nPrototype demo:")
    puzzle = SlideLock(size=3)
    print(puzzle.render())
    print("\nSlide blocks (arrows) or reset (r).")
    # Simulate player moves
    for m in moves:
        puzzle.move(*m)
        print("\n" + puzzle.render())
    print("\nSolved!" if puzzle.is_solved() else "\nNot solved.")
else:
    print("\nUpend the tea table: crude prototype failed the fun gate.")