def plan_trip():
    # (1) The four questions asked before any plan:
    # destination: "paris" (hardcoded from local list)
    # duration: 3 days
    # budget: $300 total
    # interests: food, history, local neighborhoods

    destination = "paris"
    days = 3
    budget = 300
    interests = "food, history, local neighborhoods"

    # (2) Back-door pick: skip crowded Louvre for Canal Saint-Martin — same charm, real life
    back_door = "Canal Saint-Martin (free walk) instead of Louvre ($17, 2hr queue)"

    # (3) Pace check: 3 days, 1 base (no hotel changes), transit 30-45 min/day accounted
    pace = "3 days, 1 base in Le Marais — transit: 30-45 min/day, no box-ticking"

    # (4) Budget line: per-day cost estimated and summed
    # Day1: lodging 50 + food 20 + transit 5 = 75
    # Day2: lodging 50 + food 25 + transit 8 = 83
    # Day3: lodging 50 + food 15 + transit 5 = 70
    per_day_costs = [75, 83, 70]
    total_cost = sum(per_day_costs)
    budget_line = f"Per-day: {per_day_costs} = ${total_cost} total (budget ${budget})"

    # (5) Backup: what to skip if energy runs low
    backup = "If tired, skip Père Lachaise cemetery — rest at Canal Saint-Martin instead"

    # Itinerary with per-stop breakdown: what / how / cost
    itinerary = [
        {"day": 1, "stop": "Marche des Enfants Rouges (food market)",
         "how": "walk 10 min from base", "cost": "$15 lunch"},
        {"day": 2, "stop": "Canal Saint-Martin walk (back-door pick)",
         "how": "metro 3 + walk 5 min", "cost": "free"},
        {"day": 3, "stop": "Musee Carnavalet (history museum)",
         "how": "walk 15 min from base", "cost": "free (permanent collection)"},
    ]

    print(f"Destination: {destination} | Days: {days} | Budget: ${budget} | Interests: {interests}")
    print(f"Back-door pick: {back_door}")
    print(f"Pace check: {pace}")
    print(f"Budget line: {budget_line}")
    print(f"Backup: {backup}")
    print("\nItinerary:")
    for stop in itinerary:
        print(f"  Day {stop['day']}: {stop['stop']} | how: {stop['how']} | cost: {stop['cost']}")

plan_trip()