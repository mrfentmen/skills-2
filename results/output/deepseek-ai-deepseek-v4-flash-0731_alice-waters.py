import random
from collections import Counter

# ingredients: hardcoded local seasonal list (the farm), stdlib random + Counter (the pantry) — no external deps
# minimal-interference pass: removed the planned Dish class + menu-builder factory — a dict + one loop says it plainly
# market read: the constraint is "what's ripe now", so the planner filters by month instead of forcing a rigid template
# source footprint: stdlib only, zero install cost, zero lock-in, no version churn for the next maintainer
# taste check: judged by "can I cook tonight with what's here", not by how many layers the code has

SEASONAL = {
    "spring": ["asparagus", "peas", "radishes", "strawberries", "spinach"],
    "summer": ["tomatoes", "corn", "zucchini", "peaches", "basil"],
    "fall": ["squash", "apples", "mushrooms", "kale", "pears"],
    "winter": ["citrus", "root vegetables", "cabbage", "leeks", "winter greens"],
}

DISHES = {
    "asparagus": "grilled asparagus with lemon",
    "peas": "pea and mint salad",
    "radishes": "radish butter on toast",
    "strawberries": "strawberry shortcake",
    "spinach": "wilted spinach with garlic",
    "tomatoes": "tomato and basil panzanella",
    "corn": "corn and chile fritters",
    "zucchini": "zucchini ribbons with parmesan",
    "peaches": "peach and burrata plate",
    "basil": "basil pesto pasta",
    "squash": "roasted squash with sage",
    "apples": "apple and cheddar galette",
    "mushrooms": "mushroom tartine",
    "kale": "massaged kale salad",
    "pears": "poached pears with honey",
    "citrus": "citrus and fennel salad",
    "root vegetables": "root vegetable roast",
    "cabbage": "cabbage and caraway slaw",
    "leeks": "leek and potato soup",
    "winter greens": "braised winter greens",
}

def pick_meal(month):
    # market read: month string is the only input; map it to a season, no config file needed
    season = {"dec": "winter", "jan": "winter", "feb": "winter",
              "mar": "spring", "apr": "spring", "may": "spring",
              "jun": "summer", "jul": "summer", "aug": "summer",
              "sep": "fall", "oct": "fall", "nov": "fall"}.get(month[:3].lower(), "spring")
    # minimal interference: one random choice, no shuffling or weighting — the market decides
    ingredient = random.choice(SEASONAL[season])
    return season, ingredient, DISHES[ingredient]

# hospitality: named for the next reader, one obvious entry point, no magic numbers
if __name__ == "__main__":
    for month in ["jan", "apr", "jul", "oct"]:
        season, ingredient, dish = pick_meal(month)
        print(f"{month}: {season} — {ingredient} → {dish}")
    # taste check: the output is a real meal from real local ingredients, not a structure demo