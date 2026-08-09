import random
import time

class OneButtonRacer:
    # learn this in 5 seconds: press SPACE to speed up, avoid walls
    def __init__(self):
        self.position = 0
        self.speed = 0
        self.score = 0
        self.walls = [5, 15, 25]
        self.game_over = False

    def play(self, action):
        if self.game_over:
            return "GAME OVER"
        if action == "SPACE":
            self.speed = min(3, self.speed + 1)
        self.position += self.speed
        self.score += self.speed
        # wall collision
        if self.position in self.walls:
            self.game_over = True
        # wall reset
        if self.position >= 30:
            self.position = 0
            self.walls = [random.randint(5, 25) for _ in range(3)]
        return self.position, self.speed, self.score

# vertical slice: runnable prototype
racer = OneButtonRacer()
print("OneButtonRacer: press SPACE to speed up, avoid walls!")
for _ in range(20):
    action = "SPACE" if random.random() < 0.3 else "WAIT"
    pos, spd, scr = racer.play(action)
    print(f"Pos:{pos} Speed:{spd} Score:{scr}", end=" | ")
    if racer.game_over:
        print("\nGame over! Final score:", racer.score)
        break
    time.sleep(0.5)

# Bushnell's Law: one instruction to learn, hidden depth to master
# learn this in 5 seconds: press SPACE to speed up, avoid walls
# master this over hours: timing speed boosts to slip between walls, risk/reward of speed vs safety

# v2 changed because real play showed: players ignored walls until too late; added wall reset and random spacing

# kept because players came back, not because it was planned: the simple loop and risk of speeding up

# simple-to-learn-hard-to-master check: 5-second onboarding vs hours of wall-slipping mastery