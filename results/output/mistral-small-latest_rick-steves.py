def rick_steves_trip_planner():
    # ask: destination? days? budget? interests?
    destination = "Lisbon"
    days = 3
    budget = 300
    interests = "history, food, local culture"

    # back-door swap: skip crowded Alfama alleys for nearby Graça neighborhood — same views, real life
    pace = f"{days} days, 1 base (Alfama) with 2 half-day forays — no box-ticking, no burnout"
    base = 100.0  # the $100-a-day yardstick

    # per-day math: lodging 60 + food 25 + transit 15 = $100 — inside budget
    daily = min(base, budget / max(days, 1))
    total = daily * days

    # per-stop breakdown
    stops = [
        # stop: sight | how: walk | cost: free
        "Miradouro da Graça sunset (free)",
        # stop: sight | how: tram 28 + walk | cost: 3.20
        "Feira da Ladra flea market (free entry, snacks ~$5)",
        # stop: sight | how: Uber to LX Factory (~$8) | cost: free to explore
        "LX Factory street art & bookshops (free)",
        # stop: sight | how: Uber to Belém (~$12) | cost: 10
        "Pastéis de Belém custard tarts ($1.20 each)",
        # backup: skip if energy runs low
        "skip crowded Tram 28 if queues long — use Uber instead"
    ]

    plan = stops[:days * 2]  # pace: 2 stops per day

    print("Rick Steves Lisbon Itinerary")
    print("============================")
    print(f"Where: {destination} | Days: {days} | Budget: ${budget} | Interests: {interests}")
    print(f"Pace: {pace}")
    print(f"Per-day: ${daily:.0f} x {days} = ${total:.0f} (target ~$100/day)")
    print("\nDaily Plan:")
    for i, stop in enumerate(plan, 1):
        print(f"{i}. {stop}")
    print("\nBackup: " + stops[-1])

rick_steves_trip_planner()