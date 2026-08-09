# ingredients: the local seasonal produce list (hardcoded), stdlib datetime, no external libs
# source: local farm stand inventory, seasonal availability tracked by hand
# bloat cut: removed ORM, removed cloud API, removed GUI framework

def seasonal_meal_planner(season, local_ingredients):
    # market read: the payloads arrive flat and messy; the schema follows that shape
    # minimal interference: ten clean lines now say it plainly
    seasonal_dishes = {
        "spring": ["asparagus risotto", "pea soup", "radish salad"],
        "summer": ["tomato tart", "zucchini fritters", "berry compote"],
        "fall": ["butternut squash soup", "apple galette", "mushroom risotto"],
        "winter": ["kale salad", "root vegetable stew", "citrus curd"]
    }
    available = [dish for dish in seasonal_dishes.get(season, [])
                 if any(ing in dish.lower() for ing in local_ingredients)]
    return available if available else ["simple omelet"]

# source footprint: no dependencies, zero runtime cost, zero maintenance debt
# honest price: saves 0 now, costs 0 later — the true price is the clarity
print(seasonal_meal_planner("spring", ["asparagus", "pea", "radish"]))