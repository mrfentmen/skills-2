def roast_chicken_plan():
    # (1) MISE EN PLACE — everything measured before heat goes on
    mise = {
        "whole chicken": "4-5 lb, patted dry, room temp 30 min",
        "kosher salt": "1 tbsp + 1 tsp, divided",
        "black pepper": "1 tsp, freshly cracked",
        "unsalted butter": "2 tbsp, softened",
        "lemon": "1, halved",
        "garlic": "4 cloves, smashed",
        "fresh thyme": "6 sprigs",
        "onion": "1 medium, quartered",
    }

    # (2) PRECISE TECHNIQUE — exact heat, timing, internal temp
    technique = [
        "Preheat oven to 425°F with rack in middle position",
        "Season cavity with 1 tsp salt + 1/2 tsp pepper; stuff with lemon, garlic, thyme, onion",
        "Rub outside with butter; season all over with remaining 1 tbsp salt + 1/2 tsp pepper",
        "Roast at 425°F for 20 min, then reduce to 375°F",
        "Cook until internal temp hits 165°F in thickest part of thigh (about 50-60 min total)",
        "Baste with pan juices every 20 min after the first 30 min",
    ]

    # (3) SEASONING RULE — layered salt, tasting note
    seasoning = (
        "Salt in 3 layers: 1 tsp in cavity, 1 tbsp on skin before roasting, "
        "final pinch of flaky salt on rested meat. Tasting note: the skin should "
        "taste seasoned on its own, not just the meat — if the skin is bland, "
        "you under-salted the outside."
    )

    # (4) RUIN POINTS — where most people wreck it
    ruin_points = [
        "Ruin #1: Chicken straight from fridge — cold bird cooks unevenly, dry breast, raw thigh. Bring to room temp first.",
        "Ruin #2: Opening the oven every 5 minutes — heat escapes, skin never crisps. Trust the timer, baste only twice.",
        "Ruin #3: Guessing doneness by time alone — undercooked or overcooked. Use a thermometer, 165°F in the thigh, no exceptions.",
    ]

    # (5) REST STEP — never skipped, with reason
    rest = (
        "Rest 15 minutes, tented loosely with foil. The juices redistribute — "
        "cut now and you lose every drop of moisture. Resting is part of the cooking."
    )

    plan = (
        "ROAST CHICKEN — THE PASS\n"
        "========================\n"
        "MISE EN PLACE:\n"
        + "\n".join(f"  - {k}: {v}" for k, v in mise.items()) +
        "\n\nTECHNIQUE:\n"
        + "\n".join(f"  {i+1}. {step}" for i, step in enumerate(technique)) +
        f"\n\nSEASONING RULE:\n  {seasoning}" +
        "\n\nRUIN POINTS:\n"
        + "\n".join(f"  - {r}" for r in ruin_points) +
        f"\n\nREST:\n  {rest}"
    )
    return plan

print(roast_chicken_plan())