def roast_chicken_plan():
    # Mise en place: everything in its place before the heat goes on
    mise = [
        "1 whole chicken, 3-4 lbs, giblets removed, patted dry",
        "4 tbsp unsalted butter, softened",
        "1 lemon, halved",
        "4 garlic cloves, smashed",
        "1 bunch fresh thyme",
        "1 bunch fresh rosemary",
        "Kosher salt",
        "Freshly ground black pepper",
        "1 large onion, quartered",
        "2 carrots, roughly chopped",
        "2 celery stalks, roughly chopped",
        "1 cup chicken stock",
        "Roasting pan with rack"
    ]

    # Technique: exact heat, timing, and internal temperature
    steps = [
        "# 45 min before cooking: bring chicken to room temperature",
        "# Preheat oven to 425°F (convection if available)",
        "# Season cavity: salt and pepper inside chicken, stuff with lemon halves, garlic, thyme, and rosemary",
        "# Season exterior: salt and pepper skin generously, then rub with softened butter",
        "# Truss legs with twine",
        "# Roast on rack in pan with vegetables and stock at 425°F for 15 minutes",
        "# Reduce heat to 375°F and roast until internal thigh temp reaches 165°F (about 1 hour)",
        "# Baste every 20 minutes with pan juices"
    ]

    # Seasoning rule: salt/seasoning layered through the cook with tasting note
    seasoning = [
        "Layer 1: cavity seasoning before trussing — salt and pepper inside",
        "Layer 2: exterior rub with salted butter — season in layers, taste skin before roasting",
        "Layer 3: final check after roasting — adjust salt only if needed, never over-salt"
    ]

    # Ruin points: moments where most people wreck the dish
    ruin_points = [
        "Chicken not patted dry — steam prevents crispy skin",
        "Oven not preheated — inconsistent cooking",
        "Skipping the rest — juices will run out, dry meat"
    ]

    # Rest step: proteins rested with reason, never skipped
    rest = "Rest chicken 15 minutes before carving — allows juices to redistribute, prevents dry meat"

    return (f"ROAST CHICKEN: mise = {', '.join(mise)}\n"
            f"  technique: {'; '.join(steps)}\n"
            f"  seasoning: {'; '.join(seasoning)}\n"
            f"  ruin points: {', '.join(ruin_points)}\n"
            f"  rest: {rest}")

print(roast_chicken_plan())