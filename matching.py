"""
Scoring + description generation for BarBeerQue pairings.

Scoring applies four real pairing principles:
  1. Contrast -- bitterness/carbonation cutting through rich, fatty food
  2. Complement -- roast/malt echoing smoke and char
  3. Sweetness echo -- malt sweetness alongside sweet glazes/sauces
  4. Spice balance -- avoiding hop bitterness amplifying chili heat;
     favoring crisp, lighter beers to cool the palate instead
  5. Body matching -- keeping delicate foods with lighter beers and
     heavy foods with fuller-bodied ones
"""

import random

from data import BEERS, FOODS


def _score(food, beer):
    s = 0.0
    reasons = []

    # Shift the 1-5 scale down so a baseline value of 1 ("essentially none
    # of this quality") contributes zero to multiplicative terms below,
    # instead of still scaling with the other factor. Without this, e.g. a
    # food with minimal char (1) still generated a large "complement" score
    # against a very roasty beer, wrongly making heavy stouts look like a
    # top match for delicate, uncharred foods.
    f_rich, f_char, f_smoke, f_sweet, f_heat = (
        food["richness"] - 1, food["char"] - 1, food["smokiness"] - 1,
        food["sweetness"] - 1, food["spice_heat"] - 1,
    )
    b_bitter, b_carb, b_roast, b_malt = (
        beer["bitterness"] - 1, beer["carbonation"] - 1,
        beer["roastiness"] - 1, beer["malt_sweetness"] - 1,
    )

    # 1. Contrast: richness cut by bitterness/carbonation
    contrast = f_rich * b_bitter * 0.6 + f_rich * b_carb * 0.3
    s += contrast
    if contrast >= 4 and food["richness"] >= 3:
        reasons.append("contrast")

    # 2. Complement: char/smoke echoed by roast, and by malt
    complement = f_char * b_roast * 0.5 + f_smoke * b_roast * 0.5 + \
        f_char * b_malt * 0.25
    s += complement
    if complement >= 3 and (food["char"] >= 3 or food["smokiness"] >= 3):
        reasons.append("complement")

    # 3. Sweetness echo
    sweetness = f_sweet * b_malt * 0.5
    s += sweetness
    if sweetness >= 3 and food["sweetness"] >= 3:
        reasons.append("sweetness")

    # 4. Spice balance -- penalize bitterness, reward crispness/lighter body
    if food["spice_heat"] >= 3:
        s -= f_heat * b_bitter * 0.4
        s += f_heat * b_carb * 0.35
        s += f_heat * (4 - (beer["body"] - 1)) * 0.2
        if beer["carbonation"] >= 3 and beer["bitterness"] <= 2:
            reasons.append("spice")

    # 5. Body matching -- penalize mismatches
    body_gap = abs(food["richness"] - beer["body"])
    s -= body_gap * 0.5
    if body_gap <= 1 and food["richness"] <= 2 and beer["body"] <= 2:
        reasons.append("light")
        s += 1.5  # explicit reward, not just a smaller penalty, for a genuine light/light match

    if not reasons:
        reasons.append("balance")

    return s, reasons


_TEMPLATES = {
    "contrast": [
        "{beer}'s {beer_note} bitterness and lively carbonation cut right "
        "through the richness of {food}, resetting your palate between bites.",
        "The crisp snap of {beer} slices through the fat in {food} instead "
        "of getting weighed down by it.",
    ],
    "complement": [
        "The {beer_note} character in {beer} echoes the {food_note} "
        "character of {food} rather than competing with it -- smoke "
        "meeting roast.",
        "{beer}'s deeper malt character mirrors the char and smoke in "
        "{food}, so the flavors build on each other instead of clashing.",
    ],
    "sweetness": [
        "{beer}'s malt sweetness sits right alongside {food}'s own "
        "{food_note} character without either one overpowering the other.",
        "The sweetness in {beer} plays well with {food}'s {food_note} "
        "edge, rather than fighting it.",
    ],
    "spice": [
        "{beer}'s {beer_note} profile cools the heat in {food} -- a "
        "hop-forward beer would only pour gasoline on that spice.",
        "Instead of amplifying the heat, {beer} stays light and "
        "refreshing against {food}'s kick.",
    ],
    "light": [
        "Both {food} and {beer} stay light and clean, so the more delicate "
        "flavors here don't get overwhelmed.",
        "{beer}'s easy, {beer_note} character matches the lighter side of "
        "{food} instead of overpowering it.",
    ],
    "balance": [
        "{beer}'s {beer_note} profile gives {food} a solid, well-rounded "
        "match without pulling focus from either one.",
    ],
}


def _describe(food, beer, reasons):
    reason = reasons[0]
    template = random.choice(_TEMPLATES[reason])
    return template.format(
        beer=beer["name"],
        food=food["name"],
        beer_note=random.choice(beer["notes"]),
        food_note=random.choice(food["notes"]),
    )


def top_beers_for_food(food_name, n=3):
    food = next((f for f in FOODS if f["name"] == food_name), None)
    if not food:
        return None
    scored = [(beer, *_score(food, beer)) for beer in BEERS]
    scored.sort(key=lambda x: x[1], reverse=True)
    results = []
    for beer, score, reasons in scored[:n]:
        results.append({
            "name": beer["name"],
            "style": beer["style"],
            "description": _describe(food, beer, reasons),
        })
    return results


def top_foods_for_beer(beer_name, n=3):
    beer = next((b for b in BEERS if b["name"].lower() == beer_name.lower()), None)
    if not beer:
        return None
    scored = [(food, *_score(food, beer)) for food in FOODS]
    scored.sort(key=lambda x: x[1], reverse=True)
    results = []
    for food, score, reasons in scored[:n]:
        results.append({
            "name": food["name"],
            "style": food["category"],
            "description": _describe(food, beer, reasons),
        })
    return results


def find_food(query):
    q = query.strip().lower()
    for f in FOODS:
        if f["name"].lower() == q:
            return f["name"]
    for f in FOODS:
        if q in f["name"].lower():
            return f["name"]
    return None


def find_beer(query):
    q = query.strip().lower()
    for b in BEERS:
        if b["name"].lower() == q:
            return b["name"]
    for b in BEERS:
        if q in b["name"].lower():
            return b["name"]
    return None
