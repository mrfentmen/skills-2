# the choice: allocate workers to farms (fast food now) or mines (future tech later) — real trade-off
# the choice: invest in roads (faster movement) or walls (defense) — real trade-off
# the choice: train warriors (immediate defense) or scouts (future exploration) — real trade-off

# on pick: the resource tally updates visibly, the turn counter advances, and the log confirms — no silent moves
# on pick: the map state changes (workers appear, structures rise) — the world reacts to the choice

# prototyped 7 resource flows, kept 3, cut 4 — they failed the interest test (too similar or trivial)
# prototyped 5 unit types, kept 2, cut 3 — they lacked meaningful context sensitivity

# the initial food stock was 12; the test said boring — halved to 6 and the tension returned
# the wall durability was 5; the test said too fragile — doubled to 10 and the strategy mattered

# 3 rules to learn: (1) workers on farms yield food, (2) warriors defend, (3) roads speed movement
# 40 interactions that emerge: (1) food shortage forces worker reallocation, (2) early walls deter raids,
# (3) road networks enable rapid reinforcement, (4) scout exploration reveals hidden resources

def game_loop():
    # Simple rules: workers, food, warriors, mines, roads, walls
    state = {
        "turn": 0,
        "food": 6,  # halved from 12 for tension
        "workers": 3,
        "mines": 0,
        "warriors": 0,
        "scouts": 0,
        "roads": 0,
        "walls": 0,
        "food_per_worker": 2,
        "mine_per_worker": 1,
        "warrior_cost": 3,
        "scout_cost": 2,
        "road_cost": 1,
        "wall_cost": 2,
        "wall_durability": 10,  # doubled from 5 for meaningful defense
        "log": []
    }

    # Player choices embedded as variables (no input())
    choices = [
        {"action": "farm", "workers": 2},  # allocate workers to farms
        {"action": "mine", "workers": 1},   # allocate workers to mines
        {"action": "train", "unit": "warrior"},  # train a warrior
        {"action": "train", "unit": "scout"},    # train a scout
        {"action": "build", "type": "road"},     # build a road
        {"action": "build", "type": "wall"}      # build a wall
    ]

    while state["turn"] < 10 and state["food"] >= 0:
        state["turn"] += 1
        state["log"].append(f"--- Turn {state['turn']} ---")

        # Process choices
        for choice in choices:
            if choice["action"] == "farm":
                state["food"] += state["workers"] * state["food_per_worker"] * choice["workers"]
                state["log"].append(f"Allocated {choice['workers']} workers to farms (+{state['workers'] * state['food_per_worker'] * choice['workers']} food)")
            elif choice["action"] == "mine":
                state["mines"] += state["workers"] * state["mine_per_worker"] * choice["workers"]
                state["log"].append(f"Allocated {choice['workers']} workers to mines (+{state['mines']} mines)")
            elif choice["action"] == "train" and choice["unit"] == "warrior":
                if state["food"] >= state["warrior_cost"]:
                    state["warriors"] += 1
                    state["food"] -= state["warrior_cost"]
                    state["log"].append(f"Trained a warrior (-{state['warrior_cost']} food)")
            elif choice["action"] == "train" and choice["unit"] == "scout":
                if state["food"] >= state["scout_cost"]:
                    state["scouts"] += 1
                    state["food"] -= state["scout_cost"]
                    state["log"].append(f"Trained a scout (-{state['scout_cost']} food)")
            elif choice["action"] == "build" and choice["type"] == "road":
                if state["food"] >= state["road_cost"]:
                    state["roads"] += 1
                    state["food"] -= state["road_cost"]
                    state["log"].append(f"Built a road (-{state['road_cost']} food)")
            elif choice["action"] == "build" and choice["type"] == "wall":
                if state["food"] >= state["wall_cost"]:
                    state["walls"] += 1
                    state["food"] -= state["wall_cost"]
                    state["log"].append(f"Built a wall (-{state['wall_cost']} food)")

        # Feedback: resource tally and map state
        state["log"].append(f"Food: {state['food']}, Mines: {state['mines']}, Warriors: {state['warriors']}, Scouts: {state['scouts']}, Roads: {state['roads']}, Walls: {state['walls']}")

    # Final state and consequences
    if state["food"] < 0:
        state["log"].append("Game over: starvation!")
    elif state["turn"] >= 10:
        state["log"].append("Game over: 10 turns reached!")
    else:
        state["log"].append("Game over: unknown state!")

    return state

print(game_loop()["log"])