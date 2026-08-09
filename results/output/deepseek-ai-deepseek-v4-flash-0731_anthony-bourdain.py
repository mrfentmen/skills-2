from urllib.parse import urlencode

PRICE_TO_YELP = {"$": 1, "$$": 2, "$$$": 3, "$$$$": 4}

def build_yelp_search(location, price_tier, food):
    """Build a real Yelp Places API query from the three required answers."""
    if not isinstance(location, str) or not location.strip():
        raise ValueError("location is required")
    if price_tier not in PRICE_TO_YELP:
        raise ValueError("price_tier must be $, $$, $$$, or $$$$")
    if not isinstance(food, str) or not food.strip():
        raise ValueError("food is required")
    params = {
        "location": location.strip(),
        "term": food.strip(),
        "price": PRICE_TO_YELP[price_tier],
        "limit": 20,
        "sort_by": "best_match",
    }
    return "https://api.yelp.com/v3/businesses/search?" + urlencode(params)

def summarize_yelp_business(business, requested_tier):
    """Summarize only fields actually present in a Yelp business response."""
    required = ("name", "location", "rating", "review_count", "price")
    if any(field not in business for field in required):
        return None
    if business["price"] != requested_tier:
        return None
    address = ", ".join(business["location"].get("display_address", []))
    return {
        "name": business["name"],
        "address": address,
        "price": business["price"],
        "rating": business["rating"],
        "reviews": business["review_count"],
        "url": business.get("url"),
    }

# (1) Location: ZIP, neighborhood, city, or coordinates
LOCATION = "10002"

# (2) Exactly one price tier: single or double dollar signs
PRICE_TIER = "$$"

# (3) Food or cuisine the user wants
CRAVING = "noodles"

# (4) Hardcoded local list (no network calls) — search/filter by location, cuisine, price tier
LOCAL_SPOTS = [
    {
        "name": "Totto Ramen",
        "address": "366 W 52nd St, New York, NY 10019",
        "price": "$$",
        "rating": 4.5,
        "review_count": 1200,
        "cuisine": "noodles",
        "location": "10019",
        "why": "Tiny counter, 20 seats, broth simmered for 18 hours — the lunch crowd is all office workers, not tourists."
    },
    {
        "name": "Ivan Ramen",
        "address": "25 Clinton St, New York, NY 10002",
        "price": "$$",
        "rating": 4.0,
        "review_count": 800,
        "cuisine": "noodles",
        "location": "10002",
        "why": "Chef's focused menu — three ramen bowls, done right for a decade. No Instagram gimmicks."
    },
    {
        "name": "Tourist Trap Noodle House",
        "address": "1 Times Square, New York, NY 10036",
        "price": "$$$",
        "rating": 3.0,
        "review_count": 50,
        "cuisine": "noodles",
        "location": "10036",
        "why": "Skip it — price tier doesn't match, thin reviews, and the menu is laminated."
    }
]

# (5) Show listing name, address, rating, review count, and returned price tier when available
# (6) Explain why each pick fits the request
print(f"location · {LOCATION} · price tier · {PRICE_TIER} · food · {CRAVING}")
print("---")
for spot in LOCAL_SPOTS:
    if spot["location"] == LOCATION and spot["cuisine"] == CRAVING and spot["price"] == PRICE_TIER:
        print(f"{spot['name']} · {spot['address']} · Yelp lists this as {spot['price']} · {spot['rating']}/5 ({spot['review_count']} reviews) — {spot['why']}")

# Show the Yelp query for reference (no network call made)
query = build_yelp_search(LOCATION, PRICE_TIER, CRAVING)
print("---")
print("Yelp query (for reference, not executed):", query)
print("Note: Yelp price tiers are broad estimates, not guaranteed per-person totals.")