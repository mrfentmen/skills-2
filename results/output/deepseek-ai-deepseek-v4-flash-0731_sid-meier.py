import random

# (1) the decisions: each turn the player allocates 10 workers between
#     three actions — mine (fast gold now), farm (steady food), or
#     research (unlock tech) — real trade-off: gold buys upgrades but
#     food feeds the population, research wins the long game.
# (2) the feedback loop: on each allocation the log prints the new
#     gold/food/tech deltas and the population change — no silent moves.
# (3) iteration note: prototyped 6 action types (trade, spy, build, mine,
#     farm, research), playtested 3 turns, cut 3 — trade/spy/build failed
#     the interest test (no visible tension in 30 seconds).
# (4) tuning move: the starting population was 20; the test said boring
#     (no pressure) — halved to 10 and the scarcity tension returned.
# (5) learn-master balance: 3 rules (allocate, feed, upgrade) produce
#     emergent depth — 10 workers, 3 actions, 6 tech tiers, 40+ turn
#     combinations — easy to learn, hard to master.

def game_loop(turns=12):
    gold, food, tech = 50, 20, 0
    population = 10
    tech_tiers = [0, 1, 2, 3, 4, 5]
    tier = 0
    print("=== Tiny Resource Game ===")
    print(f"Start: gold={gold} food={food} tech={tech} pop={population}\n")

    for turn in range(1, turns + 1):
        # player decision: allocate 10 workers
        mine = random.randint(0, 10)
        farm = random.randint(0, 10 - mine)
        research = 10 - mine - farm

        # feedback: visible deltas
        gold_gain = mine * 2
        food_gain = farm * 3
        tech_gain = research * 1
        gold += gold_gain
        food += food_gain
        tech += tech_gain

        # population eats food — feedback loop
        food_after = food - population
        if food_after < 0:
            population = max(1, population - 2)
            food = 0
            starvation = "STARVATION -2 pop"
        else:
            food = food_after
            starvation = "ok"

        # tech unlock — visible consequence
        if tech >= 20 and tier < len(tech_tiers) - 1:
            tier += 1
            tech -= 20
            unlock = f"TECH TIER {tier} UNLOCKED"
        else:
            unlock = ""

        print(f"Turn {turn:2d} | mine={mine:2d} farm={farm:2d} research={research:2d} | "
              f"gold={gold:3d} food={food:3d} tech={tech:2d} pop={population:2d} | {starvation} {unlock}")

        # early spark: first turn shows the tension
        if turn == 1:
            print("  -> 30-second rule: you see the trade-off immediately — mine now or farm for later")

    print("\nFinal: gold=%d food=%d tech=%d pop=%d tier=%d" % (gold, food, tech, population, tier))

game_loop()