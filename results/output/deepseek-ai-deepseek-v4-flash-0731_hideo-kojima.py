class EchoStealth:
    # (1) theme-mechanics link: the player FEELS isolation because every action
    #     they take is heard by the world but never by another human — the
    #     mechanic of "sound as the only sense" makes loneliness tactile.
    # (2) constraint inversion: the limit is the feature: we can't render
    #     sightlines, so the entire game is audio-only — darkness becomes
    #     the canvas, and the player's own footsteps are the enemy.
    # (3) subversion: players expect a stealth game where you hide from guards;
    #     we set up that pattern, then reveal the guards are blind and the
    #     real threat is the player's own heartbeat — the hunter is the hunted.
    # (4) micro-detail: the 300ms delay between pressing "move" and the footstep
    #     sound — it makes the player feel the weight of their own body, and
    #     forces them to breathe before every step, turning anxiety into ritual.
    # (5) connection system: players leave "echo stones" that replay a 2-second
    #     sound of their own footsteps; strangers who step on them hear that
    #     ghost and know someone else was here — asynchronous empathy through
    #     shared silence.

    def __init__(self):
        self.players = {}
        self.echo_stones = []
        self.guard_alert = 0

    def step(self, player, direction):
        # the micro-detail: the delay is the soul
        delay = 0.3  # seconds — the weight of intention
        sound = f"{player} steps {direction} (after {delay}s of hesitation)"
        self.players[player] = self.players.get(player, 0) + 1
        self.guard_alert += 1
        return sound

    def hold_breath(self, player):
        # subversion: the "safe" action is the loudest — holding breath
        # makes the heartbeat audible to the blind guards
        self.guard_alert += 2
        return f"{player} holds breath — heartbeat echoes, alert +2"

    def leave_echo(self, player, sound):
        # connection: your ghost helps a stranger feel less alone
        self.echo_stones.append((player, sound))
        return f"{player} leaves an echo stone"

    def step_on_echo(self, stranger):
        if self.echo_stones:
            builder, sound = self.echo_stones.pop(0)
            return f"{stranger} hears {builder}'s ghost: '{sound}' — you are not alone"
        return f"{stranger} steps on silence — the void is yours"

    def guard_check(self):
        # constraint inversion: the guards are blind, so alert is based on
        # sound only — the player's own existence is the puzzle
        if self.guard_alert > 5:
            return "GUARD ALERT — the silence is broken, you are found"
        return f"alert level: {self.guard_alert}/5 — the dark still holds you"

# demo
game = EchoStealth()
print(game.step("you", "north"))
print(game.hold_breath("you"))
print(game.guard_check())
print(game.leave_echo("you", "a soft step, then a pause"))
print(game.step_on_echo("stranger"))
print(game.guard_check())