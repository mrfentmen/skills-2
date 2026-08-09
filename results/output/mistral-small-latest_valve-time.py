def grappling_hook_feature():
    # player fantasy: swing through a cramped ruin and choose momentum over safety
    # genre context: action traversal with physics-based movement
    # comparable mechanics: Spider-Man 2 web-swinging, Apex Legends grapple, Titanfall slide-hop
    # technical risks: camera jitter during fast travel, rope physics tunneling, unclear landing feedback

    # H1: first-time players repeat the grapple loop three times without prompting
    # Falsifier: 3 or more of 5 players stop after one attempt or ask what to do

    # Prototype: only grapple hook, one traversal gap, landing feedback, reset — no inventory, story, or cosmetics

    # Playtest plan:
    # Participants: 5 local devs with no prior exposure to the mechanic
    # Task: "traverse from the ruin entrance to the glowing idol using the grapple"
    # Observation: record hesitation, retries, abandonment, and unsolicited strategies
    # Decision gate: keep if 3+ players repeat the loop 3+ times and ≤2 players show failure signals

    # Cuts: inventory, story cutscenes, cosmetics, multiplayer, wall-running, ledge-grabbing

    research = {
        "genre": "action traversal",
        "comparables": ["Spider-Man 2", "Apex Legends", "Titanfall 2"],
        "risks": ["camera stability", "rope physics tunneling", "unclear landing feedback"]
    }

    playtest = [
        {"repeats": 4, "stopped_after_one": False, "asked_what_to_do": False},
        {"repeats": 3, "stopped_after_one": False, "asked_what_to_do": False},
        {"repeats": 1, "stopped_after_one": True, "asked_what_to_do": True},
        {"repeats": 5, "stopped_after_one": False, "asked_what_to_do": False},
        {"repeats": 3, "stopped_after_one": False, "asked_what_to_do": False}
    ]

    result = {
        "feature": "grappling hook traversal",
        "research_risks": research["risks"],
        "prototype": ["grappling hook", "one traversal gap", "landing feedback", "reset"],
        "hypothesis": "H1: first-time players repeat the grapple loop three times without prompting",
        "falsifier": "3 or more of 5 players stop after one attempt or ask what to do",
        "observed_repeats": sum(player["repeats"] >= 3 for player in playtest),
        "stopped_after_one": sum(player["stopped_after_one"] for player in playtest),
        "confused_players": sum(player["asked_what_to_do"] for player in playtest),
        "failure_signals": sum(
            player["stopped_after_one"] or player["asked_what_to_do"]
            for player in playtest
        ),
        "decision": "keep" if sum(player["repeats"] >= 3 for player in playtest) >= 3 and sum(
            player["stopped_after_one"] or player["asked_what_to_do"]
            for player in playtest
        ) <= 2 else "redesign",
        "cut": ["inventory", "story cutscenes", "cosmetics", "multiplayer", "wall-running", "ledge-grabbing"]
    }

    return result

print(grappling_hook_feature())