# player fantasy: become a spider-like acrobat who chains hookshots across a vertical city, trading safety for speed
# genre context: action traversal platformer; comparables: Spider-Man web-swing, Just Cause grapple, Bionic Commando
# technical risks: camera control during fast swings, hook attach detection, momentum preservation, motion sickness

# H1: first-time players will chain at least 3 consecutive hookshots within 60 seconds without prompting
# fail if 3/5 players stop after 1 hookshot or ask "what do I do?"

# prototype: only hookshot, one vertical gap, swing arc, landing feedback, auto-reset — no enemies, no story, no upgrades
# playtest: 5 players, task = cross the gap using hookshot, observe hesitation/retries/abandonment, gate = 3+ repeats and <=2 failure signals
# cuts: double-jump, wall-run, stamina, collectibles — they dilute the core risk of hookshot feel
# decision: keep if observed repeats >= 3 and failure signals <= 2, else redesign

def design_grappling_hook_feature():
    research = {
        "fantasy": "chain hookshots across a vertical city, momentum over safety",
        "genre": "action traversal platformer",
        "comparables": ["Spider-Man web-swing", "Just Cause grapple", "Bionic Commando"],
        "technical_risks": ["camera control during fast swings", "hook attach detection", "momentum preservation", "motion sickness"]
    }
    hypothesis = "first-time players chain at least 3 consecutive hookshots within 60 seconds without prompting"
    falsifier = "3/5 players stop after 1 hookshot or ask what to do"
    prototype = ["hookshot only", "one vertical gap", "swing arc", "landing feedback", "auto-reset"]
    playtest_plan = {
        "participants": 5,
        "task": "cross the gap using hookshot",
        "observe": ["hesitation", "retries", "abandonment", "unsolicited strategies"],
        "decision_gate": "keep if repeats >= 3 and failure signals <= 2"
    }
    cuts = ["double-jump", "wall-run", "stamina", "collectibles"]  # excluded to isolate hookshot feel
    playtest_results = [
        {"repeats": 4, "stopped_after_one": False, "asked_what_to_do": False},
        {"repeats": 3, "stopped_after_one": False, "asked_what_to_do": False},
        {"repeats": 1, "stopped_after_one": True, "asked_what_to_do": True},
        {"repeats": 5, "stopped_after_one": False, "asked_what_to_do": False},
        {"repeats": 3, "stopped_after_one": False, "asked_what_to_do": False}
    ]
    repeats = sum(p["repeats"] >= 3 for p in playtest_results)
    failure_signals = sum(p["stopped_after_one"] or p["asked_what_to_do"] for p in playtest_results)
    decision = "keep" if repeats >= 3 and failure_signals <= 2 else "redesign"
    return {
        "research": research,
        "hypothesis": hypothesis,
        "falsifier": falsifier,
        "prototype": prototype,
        "playtest_plan": playtest_plan,
        "cuts": cuts,
        "observed_repeats": repeats,
        "failure_signals": failure_signals,
        "decision": decision
    }

design = design_grappling_hook_feature()
print(design)