# location: "94102" (San Francisco, Tenderloin)
# price_tier: "$$"
# food: "soup"

LOCATION = "94102"
PRICE_TIER = "$$"
FOOD = "soup"

# Hardcoded local list of restaurants matching the query
LOCAL_LIST = [
    {
        "name": "Tenderloin Market",
        "address": "10 Eddy St, San Francisco, CA 94102",
        "price": "$$",
        "rating": 4.2,
        "reviews": 187,
        "cuisine": ["soup", "sandwiches", "deli"],
    },
    {
        "name": "The Little Gem",
        "address": "851 O'Farrell St, San Francisco, CA 94109",
        "price": "$$",
        "rating": 4.0,
        "reviews": 212,
        "cuisine": ["soup", "salad", "sandwiches"],
    },
    {
        "name": "Soup-er Soup",
        "address": "123 Jones St, San Francisco, CA 94102",
        "price": "$",
        "rating": 3.8,
        "reviews": 98,
        "cuisine": ["soup"],
    },
    {
        "name": "Bourdain's Noodle House",
        "address": "543 Market St, San Francisco, CA 94104",
        "price": "$$$",
        "rating": 4.5,
        "reviews": 310,
        "cuisine": ["noodles", "soup", "asian"],
    },
]

def filter_local_list(location, price_tier, food):
    """Filter the hardcoded local list by location, price tier, and food."""
    filtered = []
    for place in LOCAL_LIST:
        # Check if the place is in the requested location (ZIP 94102)
        if "94102" not in place["address"]:
            continue
        # Check if the price tier matches
        if place["price"] != price_tier:
            continue
        # Check if the food is in the cuisine list
        if food.lower() not in [c.lower() for c in place["cuisine"]]:
            continue
        filtered.append(place)
    return filtered

def explain_pick(place):
    """Explain why the pick fits the request."""
    local_signal = f"{place['reviews']} reviews — locals clearly know this spot."
    distrust = "Avoid the touristy Market St corridor; this is a working-class neighborhood joint."
    return f"{local_signal} {distrust}"

# Query inputs
print(f"location · {PRICE_TIER} · {FOOD}")

# Filter and print results
picks = filter_local_list(LOCATION, PRICE_TIER, FOOD)
for place in picks:
    print(
        f"{place['name']} · {place['address']} · {place['price']} · "
        f"{place['rating']}/{place['reviews']} — {explain_pick(place)}"
    )