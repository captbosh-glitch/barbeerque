# BarBeerQue -- Sizzle. Sip. Repeat.

A BBQ-to-beer pairing search app. Enter a BBQ food and get 3 beer
recommendations, or enter a beer and get 3 BBQ foods that pair well --
each with real reasoning behind the match.

## How it works

- `data.py` -- 30 beers and 30 BBQ foods, each with real flavor/texture
  attributes (richness, smokiness, spice heat, bitterness, malt sweetness,
  roastiness, carbonation, body).
- `matching.py` -- the pairing engine. Scores every possible combination
  using real pairing principles (bitterness cutting through fat, roast
  echoing char/smoke, crisp beers cooling spice heat instead of
  amplifying it, body matching) and generates a natural-language reason
  for each top match.
- `build_pairings.py` -- pre-computes every pairing at build time (so the
  shipped site is pure static HTML/JS -- no server, no Python needed at
  runtime) and writes `pairings.json`.
- `generate_site.py` -- builds `index.html` from `pairings.json`, your
  real logo (`assets/logo.svg`), and the header photo (`assets/header.jpg`).

## Rebuilding the site

Any time you change the data, add real photos, or tweak the design:

```bash
python build_pairings.py   # regenerates pairings.json
python generate_site.py    # regenerates index.html
```

Then just open `index.html` in a browser -- no server needed.

## Adding real photos

Right now, food/beer cards show placeholder graphics (food emoji, and
beer swatches tinted by each beer's actual roast/malt character) since no
licensed photos have been added yet.

See **IMAGE_MANIFEST.md** for the exact filename each of the 60 items
expects. Drop a licensed photo at that path (e.g.
`assets/foods/brisket.jpg`) and re-run `python generate_site.py` -- the
site automatically detects the file and switches that card from
placeholder to real photo. No code changes needed. Cards without a photo
yet keep showing their placeholder, so you can add these gradually.

## The header photo

`assets/header.jpg` is currently an unlicensed watermarked preview image.
Replace it with the licensed version (same filename) before this goes
anywhere public.

## Extending the data

To add a new beer or food, add an entry to the `BEERS` or `FOODS` list in
`data.py` with the same attribute fields as the existing entries, then
re-run both build scripts. The matching engine handles new items
automatically -- no changes needed to `matching.py`.
