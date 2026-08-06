#!/usr/bin/env python3
"""Live eval for the anthony-bourdain skill (skills 2/).

Runs the Bourdain food-finder against the REAL Yelp Places API: given a
location, a Yelp price tier, and a cuisine, it searches real businesses, applies
transparent Bourdain filters, and prints the picks with the reasoning that drove
them.

This is not a mock: it makes a real HTTPS call via urllib (stdlib only). If no
API key is configured it FAILS LOUDLY with instructions -- it never pretends to
have results it doesn't have.

Usage:
    export YELP_API_KEY=...
    python3 eval_bourdain_live.py --location 10002 --food tacos --price '$'
    python3 eval_bourdain_live.py --location 94110 --food pho --price '$$'

Yelp price tiers are broad relative-expense categories:
    $=1, $$=2, $$$=3, $$$$=4.
They are not guaranteed per-person totals.
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
import urllib.error

PRICE_TO_YELP = {"$": 1, "$$": 2, "$$$": 3, "$$$$": 4}
HYPE_RATING_HIGH = 4.6
MIN_REVIEWS = 25
FLOOR_RATING = 3.8


def yelp_search(api_key, location, price_tier, food):
    """Text-search Yelp's live Business Search endpoint."""
    params = urllib.parse.urlencode({
        "location": location,
        "term": food,
        "price": PRICE_TO_YELP[price_tier],
        "limit": 20,
        "sort_by": "best_match",
    })
    request = urllib.request.Request(
        f"https://api.yelp.com/v3/businesses/search?{params}",
        headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Yelp API HTTP {error.code}: {detail}") from error


def bourdain_score(business, requested_tier):
    """Score a Yelp result without inventing absent fields."""
    rating = business.get("rating")
    reviews = business.get("review_count")
    price = business.get("price")
    if rating is None or reviews is None or price is None:
        return -1, ["Yelp omitted rating, review count, or price -- cannot vouch for it"]
    if price != requested_tier:
        return -1, [f"Yelp lists {price}, not the requested {requested_tier}"]
    if rating < FLOOR_RATING:
        return -1, [f"rating {rating} is below {FLOOR_RATING} -- the locals are unconvinced"]
    if reviews < MIN_REVIEWS:
        return -1, [f"only {reviews} reviews -- too little local validation"]

    score = float(rating) + min(reviews / 1000.0, 2.0)
    reasons = [f"{reviews} Yelp reviews at {rating} stars", f"Yelp price {price} matches"]
    if rating > HYPE_RATING_HIGH:
        score -= 0.5
        reasons.append(f"discounting unusually high {rating} aggregate")
    else:
        reasons.append("rating is strong without a perfect-score hype penalty")
    return round(score, 2), reasons


def main():
    ap = argparse.ArgumentParser(description="Live eval for the Anthony Bourdain Yelp workflow")
    ap.add_argument("--location", "--zip", dest="location", default="10002",
                    help="ZIP code, neighborhood, city, or coordinates")
    ap.add_argument("--food", "--cuisine", dest="food", default="tacos",
                    help="food or cuisine craving")
    ap.add_argument("--price", "--budget", dest="price", choices=sorted(PRICE_TO_YELP),
                    default="$$", help="Yelp price tier: $, $$, $$$, or $$$$")
    ap.add_argument("--limit", type=int, default=5, help="how many picks to show")
    args = ap.parse_args()

    key = os.environ.get("YELP_API_KEY", "")
    if not key:
        print("eval_bourdain_live: FAIL-LOUD -- no YELP_API_KEY set.", file=sys.stderr)
        print("This eval makes a REAL call to Yelp and never pretends to have results.", file=sys.stderr)
        print("Get a key at https://docs.developer.yelp.com/docs/fusion-intro", file=sys.stderr)
        print("then: export YELP_API_KEY=your_key", file=sys.stderr)
        return 1

    print(f"Bourdain Yelp eval: '{args.location} · {args.price} · {args.food}'")
    print("=" * 60)
    try:
        body = yelp_search(key, args.location, args.price, args.food)
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        return 1

    businesses = body.get("businesses", [])
    if not businesses:
        print("No Yelp leads -- no invented list. Try another location, price tier, or craving.")
        return 0

    results = []
    for business in businesses:
        score, reasons = bourdain_score(business, args.price)
        results.append((score, business, reasons))
    results.sort(key=lambda row: row[0], reverse=True)

    shown = 0
    for score, business, reasons in results:
        if score < 0:
            continue
        shown += 1
        address = ", ".join(business.get("location", {}).get("display_address", []))
        print(f"{business.get('name', '?')} -- {address}")
        print(f"  score {score} | {', '.join(reasons)}")
        print(f"  Yelp: {business.get('price', '?')} | {business.get('rating', '?')} stars | {business.get('review_count', '?')} reviews")
        print(f"  {business.get('url', '')}")
        if shown >= args.limit:
            break
    if shown == 0:
        print("Yelp returned businesses, but none passed the evidence filter; no invented list.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
