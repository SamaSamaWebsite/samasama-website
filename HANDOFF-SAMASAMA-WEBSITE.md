# Sama Sama — Website v2 — Handoff Note

Paste this into a new chat and attach the files from this zip (at minimum `build_website2.py`, the whole `data/` folder and the whole `img/prev/` folder). This note explains what the website is, how it's built, and what's still pending.

## What it is

**`samasama-v2.html`** — the complete Sama Sama website in ONE HTML file (~483 KB, plus a 2.7 MB `img/prev/` folder of guide-preview images; see "Files you must upload" below). It replaced the old compiled React app and integrates:

- The **full 123-destination travel database** (extracted losslessly from the old app): per-city transit, stays, groceries, eating out, things to do (kids/grown-ups), 12-month climate (air/sea/rain), flights, traveller tips — plus per-country ATM, health & safety, dietary and visa info, and a **47-currency converter** (EUR default, persisted in localStorage).
- The **28 detailed premium guides** integrated as products: gold "PREMIUM GUIDE" badges, buy banners, previews, promo boxes with real per-guide stats.
- The rebuild-brief pages: Home (photo hero), Destinations, City Guides, Where to Buy (+FAQ), About (minimal Ko-fi), Contact (trip-planning offer from the guides' closing page).

### Files you must upload

```
index.html          ← samasama-v2.html, renamed
img/prev/           ← 112 files: <guideid>-460.webp/.avif and <guideid>-920.webp/.avif
```

That's it. `data/` and `build_website2.py` are build-time only — never upload them. Photos of destinations load from Wikimedia Commons in the visitor's browser (sandboxes/offline show branded gradient fallbacks — this is expected, NOT a bug); only the 28 guide previews are self-hosted, because they're screenshots of your own product.

If you want ONE fully portable file with no folder next to it, set `"inline_previews": true` in `data/site.json` and rebuild — the previews go back to base64 inside the HTML and the file becomes ~1 MB. External is the default because it's roughly half the download and the previews then load lazily per city instead of all 28 up front.

## How it's built

`python3 build_website2.py` → writes `samasama-v2.html`. The script holds **page templates only** — no hand-typed facts, no hardcoded counts. Everything factual lives in `data/`:

| file | contents |
|---|---|
| `data/guides.json` | **THE file to edit when adding a guide.** An ordered list of `{id, name?, flav}` — `name` only where the display name differs from the destination name, `flav` is the one-line food/vibe blurb. This single list drives guide-ness, ordering, names and blurbs everywhere. |
| `data/site.json` | brand (name, legal, tagline, copyright year, research year), contact email, buy `{live, tooltip}`, `stats.facts_tracked`, the four shops (name + url + blurb), which shop is the support shop, and `images.{inline_previews, prev_dir}` |
| `data/countries.json` | `flags` (country → emoji) and `schengen` (the list that picks which visa text a country gets) |
| `data/all_destinations.json` | the 123-city database (id, name, country, region, vibes, hook, tiers s/c/f in USD-base, rides, transit, stays, market, eat, kids, nokids, climate, fly, tips) |
| `data/country_info.json` | per-country atm {fee,lim,best,tip}, health {vax,health,water,safe,er}, diet {v,g,t}, visa {general,schengen} |
| `data/rates.json` | 47 currencies {r (per USD), pre, post} |
| `data/dest_photos.json` | profile photo (Commons filename) for EVERY destination |
| `data/guide_covers.json` | each guide's cover (+`place`) photo — used on guide cards & preview covers |
| `data/guide_stats.json` | real per-guide numbers: links, maps, photos, prices, pages (recomputed from the FINAL upgraded HTMLs; page count includes cover & back) |
| `data/gprev_dims.json` | intrinsic width/height of each preview image (all 460×651) — emitted as `width`/`height` so pages don't jump while images load |
| `data/gprev_by_id.json` | base64 WebP of each guide's closing brand page — only embedded when `inline_previews` is true |
| `logo2-*.svg` | the logo: badge (sun over waves in a ring), horizontal, stacked |

### Counts are derived, never typed

`123 destinations`, `60 countries`, `6 continents`, `28 guides` and `38 pages` are all computed at build time from the data (`38` is the modal value of `guide_stats.json`, since the set runs 37–39). The only number that is stored rather than derived is **"115,734 facts tracked"** in `site.json`, because it counts research inputs rather than JSON leaves.

**So adding a 29th guide is now: append one object to `data/guides.json`, add its entry to `guide_stats.json` / `guide_covers.json` / `gprev_dims.json`, drop its four preview files into `img/prev/`, rebuild.** The old "change 28 to 29 in ten places" sweep is gone.

## Photo rules (the owner is STRICT about these)
1. Every destination has a profile photo, shown on its card AND as the hero when opened.
2. A guide city's **profile photo ≠ its guide cover** (cover appears on guide cards/preview).
3. The three homepage spots (photo strip / database featured / guides teaser) must feature **all-different cities**. Currently: strip = Bangkok, Boracay, Madrid, Miami Beach, Ubud · featured = Tokyo, Prague, Rio, Cusco, Sydney, Dubrovnik · teaser = Seville, Phuket, Fort Lauderdale, Hanoi. Hero background = Santorini blue domes (Santorini's own page uses a different Oia night photo).
4. All photo filenames must be VERIFIED-real Commons files (never guessed) — check `File:` pages exist via web search before adding.

## Design system
Deep green `#14312a` + gold `#e0a63c` + cream `#faf8f3` (matches the PDF guides). Nunito 800/900 display + Inter body (Google Fonts). Region colours: SE Asia amber, Europe green, Americas terracotta, Asia violet, Oceania sea-blue, Africa bronze. "Detailed premium guide" wording is deliberately insisted on sitewide.

## Key decisions already made by the owner
- ONE single HTML file (not multi-page), Ko-fi minimal (footer line + About section only), database app superseded by this site, contact email **sama.sama.trave@protonmail.com** (spelling as given — "trave" — flagged as possible typo, owner hasn't corrected), socials = plain text "COMING SOON" (no links), guide previews show cover + contents + brand page (NO content pages — owner rejected showing the day-plans page as it gives info away), preview order: cover → covers-list → brand page, no "Where to buy" button in promo boxes.

## PENDING (the important part)
1. **Wire real shop links.** Owner sells via **Payhip** (guides already hosted there) + will open Etsy/Ko-fi/Gumroad shops. The four platform URLs now live in ONE place — `shops[].url` in `data/site.json` — and feed the guidebar buttons, Where-to-Buy cards, footer and About automatically. Still to do in the builder: the per-city `.payhip-buy` buttons (each has `data-city="<id>"`) are `href="#"` until per-guide product URLs exist; flip `buy.live` to `true` in `site.json` when they do. This is the jump from score 8.9 → 9.2+.
2. Real **email-list service** (signup bar currently opens a mailto).
3. **Testimonials** section once buyers exist.
4. Optional next projects: multi-page SEO version, МК/multilingual UI (the old app was bilingual; this one is EN-only), updating the email inside the 28 guide PDFs (they still show hello@sama-sama.travel).

## Related files
The 28 guides live as `Sama-Sama-<City>-Guide.html` (37–39-page A4, fully upgraded Jul 2026: booking strips, hostels, arrival pages, verified links, print via Brave: A4 / Margins None / Background graphics ON). Guide system handoff: `HANDOFF-README.md` in the guides handoff zip. Photo-uniqueness registry for the GUIDES (not the website): `global_avoid.json` (1,725 filenames — never reuse a photo inside guides).

## Verify after any change
`python3 build_website2.py`, then `node verify_refactor.js`. That script walks all 129 routes (6 static + 123 cities) in headless Chromium and compares rendered text, link lists, dead/nested anchors and image attributes against a snapshot of the previous build (`_site_before.html`), plus checks every referenced `img/prev/` file exists, every preview carries width/height, there are no JS console errors, and there's no horizontal overflow at 390×844. To re-baseline after an intentional change, copy the accepted build over `_site_before.html`.

Expected non-zero result: 2 `[HREF#]` per guide city — those are the placeholder Buy Now buttons (`href="#" onclick="return false"`), pending item 1 below.

## Addendum — Mauritius added (July 2026)

The 28th guide is integrated as a product exactly like the other 27; nothing new was invented for it. What changed:

- `build_website2.py`: `"mauritius"` appended to `GUIDE_IDS`, a `FLAV["mauritius"]` food line added, and every hardcoded guide count moved 27 → 28 (home hero, stat bar, home guides section, `/guides` view, where-to-buy bundle line, both meta descriptions).
- `guide_stats.json`, `guide_covers.json`, `gprev_by_id.json`: one Mauritius entry each. Stats are counted from `Sama-Sama-Mauritius-Guide.html` with the same method as the other 27 (`href="http"`, `google.com/maps`, `Special:FilePath`, `&euro;`/`€`, `<div class="page`) → **38 pages · 229 links · 113 maps · 50 photos · 239 prices**. Cover photo `Aerial_view_of_the_underwater_waterfall_in_Mauritius_(53697770576).jpg`, place photo `Port_Louis_Skyline.JPG`. The preview JPEG is the second-to-last page captured at 820×1200 with `regen_gprev.js`, resized to 460 px wide and saved at JPEG quality 58 — the same recipe as the other 27.
- No new destination data was needed: `all_destinations.json`, `dest_photos.json` and `country_info.json` (atm / health / diet) already carried Mauritius, and `FLAGS` already had 🇲🇺. The buy button, guide bar and preview section are all driven by `d.guide = cid in GUIDE_IDS`, so they appeared automatically.
- Fixed while in there: the guide bar and guide cards claimed a hardcoded "32 pages"; they now read `GSTATS[id].pages` (38 for almost every guide, 37–39 across the set). The same stale "32-page" claim was corrected in the home guides blurb, the `/guides` lead, the where-to-buy FAQ and the `/guides` meta description.

## Addendum — data split + image optimisation (July 2026)

Two refactors, done together, verified together. No visible design change: all 129 routes render byte-identical copy and identical link sets versus the previous build, apart from one deliberate wording change noted at the end.

### 1. Data moved out of the builder

Seven JSON files moved from the top level into `data/`, and five new ones joined them (`guides.json`, `site.json`, `countries.json`, `gprev_dims.json`, and the regenerated `gprev_by_id.json`). `build_website2.py` now opens everything through one loader and contains no hand-typed facts: the guide list, flavour lines, display names, country flags, Schengen list, shop names/URLs/blurbs, email, tagline, brand strings and every count are all read or derived. About 25 hardcoded literals became `${N.dest}` / `${N.guides}` / `${N.pages}` / `${SITE.contact.email}` and friends.

`build_payhip.py` was updated to the new `data/` paths at the same time — it reads `all_destinations.json`, `guide_covers.json` and `guide_stats.json`.

### 2. Images

- **Guide previews**: recaptured from the 28 guide HTMLs at 2× device scale (`shot_all_2x.js`, viewport 820×1200, Commons requests aborted, `.page` index n−2), then encoded to four files each — `-460.webp` q80, `-920.webp` q72, `-460.avif` q60, `-920.avif` q52 — in `img/prev/`. Served through `<picture>` with AVIF first, WebP fallback, `sizes="(max-width:700px) 62vw, 300px"`, explicit `width`/`height` from `gprev_dims.json`. Sharper than the old JPEG q58 inline previews, and they now load only for the city you're looking at.
- **Commons photos** (destination cards, guide covers, heroes): `srcset` at 320/460/640/900/1300/1800 px with per-context `sizes`, using Commons' own `?width=` resizer. **Format conversion is impossible for these** — `Special:FilePath` resizes but has no format parameter, so WebP/AVIF would require self-hosting ~180 files. Not done; say the word if you want it.
- `loading="lazy"` was already on every non-critical image; added `decoding="async"` everywhere, `fetchpriority="high"` on the home hero and on the city hero (which is the largest-paint element of a city page and was previously lazy).

**Result: `samasama-v2.html` went from 1,086,999 bytes to ~495,000 — 54% smaller — while the previews got sharper.** Total upload including `img/prev/` is ~3.2 MB, but a visitor downloads ~495 KB plus the one preview set for the city they open.

### One deliberate wording change

The Where-to-Buy refund line used to read "(Etsy, Ko-fi, Gumroad or Payhip)" — a hand-typed order that matched nothing else on the site. It's now generated from `site.json` like every other shop mention, so it reads "(Payhip, Etsy, Ko-fi or Gumroad)". Reorder `shops` in `site.json` if you'd rather have a different order — it will change consistently everywhere.
