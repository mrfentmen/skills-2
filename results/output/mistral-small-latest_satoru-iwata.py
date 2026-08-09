import random
import json

def tiny_rpg_health_potion():
    # the player's words: "wait, I can drink a potion mid-combo?" — that is the acceptance test
    # requested: "I want to drink a potion without stopping my attack animation"
    # plan: pre-bake the potion effect into a 0.3s window that overlaps the attack's active frames
    # no-saying: requested: "instant potion use during attack". plan: queue the potion effect to trigger
    # 0.3s after attack starts, so the player feels responsive but the animation isn't interrupted

    # rewrite call: patching the legacy input queue: ~3 days. rewrite with a cooldown tracker: ~1 day. rewrite.
    patch_weeks = 3
    rewrite_weeks = 1
    team_can_help = True
    decision = rewrite_or_patch(patch_weeks, rewrite_weeks, team_can_help)

    # tooling move: built a fixture generator — the reviewers now write cases, not boilerplate
    def generate_test_fixtures():
        return [{"input": f"attack_{i}", "expected_delay": 0.3} for i in range(5)]

    # team shield: the bug is in the shared helper; let's fix it together, not blame the author
    def apply_potion_effect(health, max_health):
        heal_amount = random.randint(15, 25)
        new_health = min(health + heal_amount, max_health)
        return new_health

    # simulate a player using a potion mid-attack
    player_health = 70
    max_health = 100
    player_health = apply_potion_effect(player_health, max_health)

    # the player's felt experience: "I feel like a pro using potions without stopping!"
    result = {
        "feature": "mid-attack potion use",
        "player_health_after": player_health,
        "decision": decision["decision"],
        "why": "fun for everyone beats impressive internals",
        "test_fixtures": generate_test_fixtures()
    }
    return result

def rewrite_or_patch(patch_weeks, rewrite_weeks, team_can_help):
    if team_can_help:
        rewrite_weeks = rewrite_weeks * 0.6
    return {"decision": "rewrite" if rewrite_weeks < patch_weeks else "patch",
            "patch_weeks": patch_weeks, "rewrite_weeks": rewrite_weeks}

print(json.dumps(tiny_rpg_health_potion(), indent=2))