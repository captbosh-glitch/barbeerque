"""
Generates the static BarBeerQue site (index.html) from pairings.json.
Run build_pairings.py first if pairings.json doesn't exist yet.

Usage:
    python generate_site.py
"""

import json
import os


def _attach_image_paths(data):
    """At build time, check whether a real photo exists for each item at
    its expected local path. If so, record that path so the page uses the
    real photo; if not, the page falls back to the placeholder swatch."""
    food_images = {}
    for name, slug in data["food_slug"].items():
        path = f"assets/foods/{slug}.jpg"
        if os.path.exists(path):
            food_images[name] = path
    data["food_images"] = food_images

    beer_images = {}
    for name, slug in data["beer_slug"].items():
        path = f"assets/beers/{slug}.jpg"
        if os.path.exists(path):
            beer_images[name] = path
    data["beer_images"] = beer_images

    return data

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BarBeerQue -- Sizzle. Sip. Repeat.</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg: #0A0A0A;
    --accent: #FF6A13;
    --white: #FFFFFF;
    --text-dark: #1A1A1A;
    --text-muted: #6B6B6B;
    --card-border: #FF6A13;
  }}

  * {{ box-sizing: border-box; }}

  body {{
    margin: 0;
    background: var(--bg);
    color: var(--white);
    font-family: 'Inter', sans-serif;
    -webkit-font-smoothing: antialiased;
  }}

  .wrap {{
    max-width: 900px;
    margin: 0 auto;
    padding: 0 24px 100px;
  }}

  /* --- Top bar (logo + search, always visible) --- */
  .topbar {{
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 20px 0;
    flex-wrap: wrap;
  }}

  .logo-mark {{
    width: 52px;
    height: 52px;
    border-radius: 50%;
    background: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    flex-shrink: 0;
  }}

  .logo-text {{
    font-family: 'Anton', sans-serif;
    font-size: 30px;
    letter-spacing: 0.01em;
    white-space: nowrap;
  }}

  .logo-text .accent {{ color: var(--accent); }}

  .search-row {{
    flex: 1;
    min-width: 240px;
    display: flex;
    align-items: center;
    background: var(--white);
    border-radius: 999px;
    padding: 4px 6px 4px 20px;
  }}

  .search-row input {{
    flex: 1;
    border: none;
    outline: none;
    font-family: 'Inter', sans-serif;
    font-size: 17px;
    color: var(--text-dark);
    padding: 12px 8px;
    background: transparent;
    min-width: 0;
  }}

  .search-row input::placeholder {{ color: #9A9A9A; }}

  .search-btn {{
    background: var(--bg);
    color: var(--white);
    border: none;
    width: 42px;
    height: 42px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 17px;
    flex-shrink: 0;
    transition: background 0.15s ease;
  }}

  .search-btn:hover {{ background: var(--accent); }}

  /* --- Hero (landing state) --- */
  .hero {{
    text-align: center;
    padding: 60px 0 50px;
  }}

  .hero-mark {{
    width: 140px;
    height: 140px;
    border-radius: 50%;
    background: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 68px;
    margin: 0 auto 24px;
  }}

  .hero-title {{
    font-family: 'Anton', sans-serif;
    font-size: 56px;
    letter-spacing: 0.01em;
    margin: 0;
  }}

  .hero-title .accent {{ color: var(--accent); }}

  .hero-tagline {{
    font-family: 'Anton', sans-serif;
    font-size: 18px;
    letter-spacing: 0.08em;
    color: var(--white);
    margin: 10px 0 34px;
    text-transform: uppercase;
  }}

  .hero-search {{
    max-width: 560px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    background: var(--white);
    border-radius: 999px;
    padding: 4px 6px 4px 24px;
  }}

  .hero-search input {{
    flex: 1;
    border: none;
    outline: none;
    font-family: 'Inter', sans-serif;
    font-size: 19px;
    color: var(--text-dark);
    padding: 16px 8px;
    background: transparent;
    min-width: 0;
  }}

  .hero-search input::placeholder {{ color: #9A9A9A; }}

  .hero-photo-strip {{
    margin-top: 50px;
    height: 260px;
    border-radius: 14px;
    background-image:
      linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.35) 100%),
      url('assets/header.jpg');
    background-size: cover;
    background-position: center;
  }}

  /* --- Results state --- */
  .results-heading {{
    font-family: 'Anton', sans-serif;
    font-size: 30px;
    color: var(--accent);
    letter-spacing: 0.01em;
    margin: 44px 0 22px;
    text-transform: uppercase;
  }}

  .card {{
    display: flex;
    gap: 24px;
    background: var(--white);
    border: 3px solid var(--card-border);
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 22px;
    color: var(--text-dark);
    transition: box-shadow 0.2s ease, transform 0.2s ease;
  }}

  .card:hover {{
    box-shadow: 0 0 26px rgba(255, 106, 19, 0.45);
    transform: translateY(-2px);
  }}

  .card-swatch {{
    width: 130px;
    height: 130px;
    border-radius: 10px;
    border: 3px solid var(--accent);
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 56px;
    background: #F3F3F3;
    overflow: hidden;
  }}

  .card-swatch-photo img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
  }}

  .card-body {{ flex: 1; min-width: 0; }}

  .card-title {{
    font-family: 'Anton', sans-serif;
    font-size: 24px;
    letter-spacing: 0.005em;
    margin: 0 0 4px;
  }}

  .card-style {{
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 13px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--accent);
    margin: 0 0 12px;
  }}

  .card-desc {{
    font-size: 15px;
    line-height: 1.6;
    color: var(--text-dark);
    margin: 0;
  }}

  .empty-state {{
    text-align: center;
    padding: 40px 20px;
    color: var(--white);
    font-size: 16px;
    line-height: 1.6;
  }}

  .empty-state .examples {{
    color: var(--accent);
    font-weight: 600;
  }}

  .hidden {{ display: none !important; }}

  @media (max-width: 560px) {{
    .hero-title {{ font-size: 40px; }}
    .hero-mark {{ width: 100px; height: 100px; font-size: 48px; }}
    .card {{ flex-direction: column; }}
    .card-swatch {{ width: 100%; height: 160px; }}
    .hero-photo-strip {{ height: 180px; }}
  }}
</style>
</head>
<body>
<div class="wrap">

  <div class="topbar hidden" id="topbar">
    <div class="logo-mark">{grill_bottle_icon_sm}</div>
    <div class="logo-text">Bar<span class="accent">Beer</span>Que</div>
    <div class="search-row">
      <input type="text" id="searchInputTop" placeholder="BBQ or Beer?" autocomplete="off">
      <button class="search-btn" id="searchBtnTop" aria-label="Search">&#128269;</button>
    </div>
  </div>

  <div class="hero" id="hero">
    <div class="hero-mark">{grill_bottle_icon_lg}</div>
    <h1 class="hero-title">Bar<span class="accent">Beer</span>Que</h1>
    <div class="hero-tagline">Sizzle. Sip. Repeat.</div>
    <div class="hero-search">
      <input type="text" id="searchInputHero" placeholder="BBQ or Beer?" autocomplete="off">
      <button class="search-btn" id="searchBtnHero" aria-label="Search">&#128269;</button>
    </div>
    <div class="hero-photo-strip"></div>
  </div>

  <div id="resultsSection" class="hidden">
    <div class="results-heading">Pairing Results:</div>
    <div id="cardsContainer"></div>
  </div>

</div>

<script>
  const DATA = {data_json};

  const hero = document.getElementById('hero');
  const topbar = document.getElementById('topbar');
  const resultsSection = document.getElementById('resultsSection');
  const cardsContainer = document.getElementById('cardsContainer');

  function normalize(s) {{
    return s.trim().toLowerCase();
  }}

  function findMatch(query, names) {{
    const q = normalize(query);
    if (!q) return null;
    for (const name of names) {{
      if (normalize(name) === q) return name;
    }}
    for (const name of names) {{
      if (normalize(name).includes(q)) return name;
    }}
    return null;
  }}

  function beerSwatch(name) {{
    const realPhoto = DATA.beer_images[name];
    if (realPhoto) {{
      return `<div class="card-swatch card-swatch-photo"><img src="${{realPhoto}}" alt="${{name}}"></div>`;
    }}
    const color = DATA.beer_swatch[name] || '#C99A3D';
    return `<div class="card-swatch" style="background:${{color}}22; border-color:${{color}};">🍺</div>`;
  }}

  function foodSwatch(name) {{
    const realPhoto = DATA.food_images[name];
    if (realPhoto) {{
      return `<div class="card-swatch card-swatch-photo"><img src="${{realPhoto}}" alt="${{name}}"></div>`;
    }}
    const emoji = DATA.food_emoji[name] || '🍖';
    return `<div class="card-swatch">${{emoji}}</div>`;
  }}

  function renderResults(items, kind) {{
    cardsContainer.innerHTML = '';
    items.forEach((item, i) => {{
      const swatch = kind === 'beer' ? beerSwatch(item.name) : foodSwatch(item.name);
      const label = kind === 'beer' ? 'Beer Suggestion' : 'BBQ Suggestion';
      const card = document.createElement('div');
      card.className = 'card';
      card.innerHTML = `
        ${{swatch}}
        <div class="card-body">
          <div class="card-title">${{label}} ${{i + 1}}: ${{item.name}}</div>
          <div class="card-style">${{item.style}}</div>
          <p class="card-desc">${{item.description}}</p>
        </div>
      `;
      cardsContainer.appendChild(card);
    }});
  }}

  function renderEmpty(query) {{
    cardsContainer.innerHTML = `
      <div class="empty-state">
        No match for "${{query}}" yet. Try a BBQ classic like
        <span class="examples">Brisket</span> or
        <span class="examples">Buffalo Wings</span>, or a beer like
        <span class="examples">Modelo</span> or
        <span class="examples">Guinness</span>.
      </div>
    `;
  }}

  function doSearch(query) {{
    if (!query || !query.trim()) return;

    hero.classList.add('hidden');
    topbar.classList.remove('hidden');
    resultsSection.classList.remove('hidden');

    document.getElementById('searchInputTop').value = query;

    const foodMatch = findMatch(query, DATA.food_names);
    if (foodMatch) {{
      renderResults(DATA.food_to_beers[foodMatch], 'beer');
      return;
    }}

    const beerMatch = findMatch(query, DATA.beer_names);
    if (beerMatch) {{
      renderResults(DATA.beer_to_foods[beerMatch], 'food');
      return;
    }}

    renderEmpty(query);
  }}

  document.getElementById('searchBtnHero').addEventListener('click', () => {{
    doSearch(document.getElementById('searchInputHero').value);
  }});
  document.getElementById('searchInputHero').addEventListener('keydown', (e) => {{
    if (e.key === 'Enter') doSearch(e.target.value);
  }});

  document.getElementById('searchBtnTop').addEventListener('click', () => {{
    doSearch(document.getElementById('searchInputTop').value);
  }});
  document.getElementById('searchInputTop').addEventListener('keydown', (e) => {{
    if (e.key === 'Enter') doSearch(e.target.value);
  }});
</script>
</body>
</html>
"""


def _grill_bottle_icon(width, height):
    """The client's real logo mark: a beer bottle rising out of a
    kettle-grill silhouette."""
    with open("assets/logo.svg") as f:
        logo = f.read()
    # Swap in the requested display size while keeping the original
    # viewBox (so the art still scales/crops correctly)
    logo = logo.replace(
        "<svg viewBox=",
        f'<svg width="{width}" height="{height}" viewBox=',
    )
    return logo


def generate(output_path="index.html"):
    with open("pairings.json") as f:
        data = json.load(f)
    data = _attach_image_paths(data)

    html = TEMPLATE.format(
        data_json=json.dumps(data),
        grill_bottle_icon_sm=_grill_bottle_icon(23, 31),
        grill_bottle_icon_lg=_grill_bottle_icon(64, 87),
    )

    with open(output_path, "w") as f:
        f.write(html)

    print(f"Site written to {output_path}")
    return output_path


if __name__ == "__main__":
    generate()
