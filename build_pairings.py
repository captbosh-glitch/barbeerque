"""
Pre-computes every food->beer and beer->food pairing at build time, so the
shipped static site only needs a simple name lookup at runtime -- no need
to port the scoring engine to JavaScript.

Usage:
    python build_pairings.py   # writes pairings.json
"""

import json
import random
import re

from data import BEERS, FOODS
from matching import top_beers_for_food, top_foods_for_beer


def slugify(name):
    """'Baby Back Ribs' -> 'baby-back-ribs' -- used as the expected local
    image filename for each item (e.g. assets/foods/baby-back-ribs.jpg)."""
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


FOOD_EMOJI = {
    "Pulled Pork": "🍖", "Brisket": "🥩", "Beef Ribs": "🍖",
    "Baby Back Ribs": "🍖", "St. Louis Ribs": "🍖", "BBQ Chicken": "🍗",
    "Smoked Chicken Wings": "🍗", "Buffalo Wings": "🍗",
    "Grilled Chicken Breast": "🍗", "Burnt Ends": "🥩",
    "Cheeseburger": "🍔", "Hot Dog": "🌭", "Bratwurst": "🌭",
    "Italian Sausage": "🌭", "Grilled Shrimp": "🍤", "Grilled Salmon": "🐟",
    "BBQ Meatballs": "🍖", "Grilled Corn on the Cob": "🌽",
    "Baked Beans": "🫘", "Coleslaw": "🥗", "Mac and Cheese": "🧀",
    "Cornbread": "🍞", "Grilled Vegetables": "🥦",
    "Smoked Turkey Leg": "🍗", "Pork Belly Burnt Ends": "🥓",
    "Filet Mignon": "🥩", "Ribeye Steak": "🥩", "Tri-Tip": "🥩",
    "Carne Asada": "🌮", "Al Pastor Tacos": "🌮",
}


def _beer_swatch_color(beer):
    """Derive a placeholder swatch color from the beer's real attributes,
    so even the placeholder carries real information: dark for roasty
    stouts/porters, amber for malty ales, golden for hoppy pales, pale
    straw for crisp light lagers."""
    if beer["roastiness"] >= 4:
        return "#2B1810"
    if beer["malt_sweetness"] >= 4:
        return "#8A4B1F"
    if beer["bitterness"] >= 4:
        return "#D98C1F"
    if beer["body"] <= 2:
        return "#E8C468"
    return "#C99A3D"


def build():
    random.seed(42)  # deterministic description template choices

    food_to_beers = {}
    for food in FOODS:
        food_to_beers[food["name"]] = top_beers_for_food(food["name"])

    beer_to_foods = {}
    for beer in BEERS:
        beer_to_foods[beer["name"]] = top_foods_for_beer(beer["name"])

    output = {
        "food_names": [f["name"] for f in FOODS],
        "beer_names": [b["name"] for b in BEERS],
        "food_to_beers": food_to_beers,
        "beer_to_foods": beer_to_foods,
        "food_emoji": FOOD_EMOJI,
        "beer_swatch": {b["name"]: _beer_swatch_color(b) for b in BEERS},
        "food_slug": {f["name"]: slugify(f["name"]) for f in FOODS},
        "beer_slug": {b["name"]: slugify(b["name"]) for b in BEERS},
    }

    with open("pairings.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"Built {len(FOODS)} foods x {len(BEERS)} beers "
          f"-> {len(food_to_beers) + len(beer_to_foods)} pairing sets")


if __name__ == "__main__":
    build()
