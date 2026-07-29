#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sama Sama Guides — Payhip homepage + per-city blocks.
Writes: Payhip-Homepage.html, Payhip-City-Blocks.html, ssg-logo-*.svg
When Payhip links arrive, fill LINKS below and re-run — everything regenerates."""
import json, urllib.parse

DEST   = json.load(open('data/all_destinations.json'))
COVERS = json.load(open('data/guide_covers.json'))
STATS  = json.load(open('data/guide_stats.json'))

GNAME = {"samui":"Koh Samui","kl":"Kuala Lumpur","sevilla":"Seville","miami":"Miami Beach","grancanaria":"Las Palmas","malaga":"Málaga"}
ORDER = ["bangkok","phuket","samui","pattaya","penang","kl","hanoi","danang","saigon","sanur","giliair","ubud","boracay","cebu","bohol","sevilla","madrid","fuengirola","malaga","miami","fortlauderdale","barcelona","mallorca","grancanaria","tenerife","alicante","valencia"]
FLAV = {
 "bangkok":"Street food, noodle shops, som tam stalls and Michelin-level dining.",
 "phuket":"Night-market noodles, southern curries and fresh-off-the-boat seafood.",
 "samui":"Beach barbecues, khao soi and the island's café scene.",
 "pattaya":"Seafood markets, street grills and the best-value Thai kitchens.",
 "penang":"Hawker legends of George Town — char kway teow, laksa and kopi.",
 "kl":"Hawker courts, banana-leaf lunches and rooftop dining.",
 "hanoi":"Phở at dawn, bún chả, egg coffee and Old Quarter street stalls.",
 "danang":"Mì quảng, fresh seafood and the beach-café scene.",
 "saigon":"Street phở, bánh mì counters and rooftop dining.",
 "sanur":"Warung classics, beachfront seafood and the smoothie-bowl scene.",
 "giliair":"Beach barbecues, warung nasi campur and island cafés.",
 "ubud":"Warungs, babi guling, healthy cafés and jungle fine dining.",
 "boracay":"Carinderia plates, D'Talipapa seafood and beachfront grills.",
 "cebu":"Lechon — the world's best roast pig — plus sutukil seafood.",
 "bohol":"Fresh seafood, carinderia comfort food and river-cruise lunches.",
 "sevilla":"Tapas crawls, abacería counters and Triana's market bars.",
 "madrid":"Menú del día, tapas, bocadillos de calamares and market halls.",
 "fuengirola":"Chiringuito espetos, tapas bars and the seafront paseo.",
 "malaga":"Espetos on the beach, tapas institutions and sweet Málaga wine.",
 "miami":"Cuban ventanitas, stone crab, ceviche and Ocean Drive dining.",
 "fortlauderdale":"Dockside fish houses, conch fritters and happy-hour raw bars.",
 "barcelona":"Pintxos, bombas, market counters and seafront paella.",
 "mallorca":"Ensaïmadas, market lunches and seaside fine dining.",
 "grancanaria":"Papas arrugadas, fresh fish and Vegueta's tapas lanes.",
 "tenerife":"Guachinches, papas con mojo and fresh Atlantic fish.",
 "alicante":"Arroces, tapas on the Explanada and market-hall counters.",
 "valencia":"The home of paella — plus horchata, tapas and market feasts.",
}
# ======= PASTE PAYHIP LINKS HERE, THEN RE-RUN =======
# LINKS["bangkok"] = {"product": "https://payhip.com/b/XXXX", "checkout": "https://payhip.com/buy?link=XXXX"}
LINKS = {cid: {"product": "", "checkout": ""} for cid in ORDER}
# ====================================================

def wm(fn, w=700):
    return "https://commons.wikimedia.org/wiki/Special:FilePath/" + urllib.parse.quote(fn) + f"?width={w}"

INK="#191817"; SAND="#cfa356"; PAPER="#faf9f6"; GREY="#6f6c66"; LINE="#e8e5de"

# ---------------- logo: Sama Sama Guides (neutral palette) ----------------
def badge(sz, ink=INK, sand=SAND, paper="#ffffff"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="{sz}" height="{sz}">
<circle cx="60" cy="60" r="55" fill="{paper}"/><circle cx="60" cy="60" r="55" fill="none" stroke="{ink}" stroke-width="5"/>
<g stroke="{sand}" stroke-width="5" stroke-linecap="round">
<line x1="60" y1="18" x2="60" y2="28"/><line x1="34" y1="29" x2="39.5" y2="38"/><line x1="86" y1="29" x2="80.5" y2="38"/>
<line x1="21" y1="49" x2="31" y2="52.5"/><line x1="99" y1="49" x2="89" y2="52.5"/></g>
<path d="M38 66 a22 22 0 0 1 44 0 Z" fill="{sand}"/>
<path d="M22 74 q9 -7 19 0 t19 0 t19 0 t19 0" fill="none" stroke="{ink}" stroke-width="5" stroke-linecap="round"/>
<path d="M30 88 q9 -7 19 0 t19 0" fill="none" stroke="{ink}" stroke-width="5" stroke-linecap="round" opacity=".5"/></svg>'''

def word(fill=INK):
    return f'<text x="0" y="0" font-family="Nunito,Inter,Arial,sans-serif" font-weight="900" font-size="44" letter-spacing="-1" fill="{fill}">sama<tspan fill="{SAND}">·</tspan>sama</text>'

LOGO_H=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 130" width="540" height="130">
<g transform="translate(5,5)">{badge(110)[badge(110).index('>')+1:-6]}</g>
<g transform="translate(136,74)">{word()}</g>
<text x="138" y="103" font-family="Inter,Arial,sans-serif" font-weight="700" font-size="15" letter-spacing="7" fill="{GREY}">G U I D E S</text></svg>'''
LOGO_S=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 280" width="360" height="280">
<g transform="translate(120,0)">{badge(120)[badge(120).index('>')+1:-6]}</g>
<g transform="translate(78,178)">{word()}</g>
<text x="180" y="212" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-weight="700" font-size="14" letter-spacing="7" fill="{GREY}">G U I D E S</text></svg>'''
open('ssg-logo-horizontal.svg','w').write(LOGO_H)
open('ssg-logo-stacked.svg','w').write(LOGO_S)
open('ssg-logo-icon.svg','w').write(badge(512))

def title(cid): return f"{GNAME.get(cid,DEST[cid]['name'])} — The Complete City Guide"

def card(cid):
    d=DEST[cid]; st=STATS[cid]; L=LINKS[cid]
    buy = L['checkout'] or '#'
    prod = L['product'] or '#'
    dis = '' if L['checkout'] else ' data-needs-link="1"'
    return f'''  <article class="ssg-card">
   <div class="ssg-cardimg"><img loading="lazy" src="{wm(COVERS[cid]['cover'],700)}" alt="{title(cid)}" onerror="this.style.display='none'"></div>
   <div class="ssg-cardbody">
    <div class="ssg-cardkick">{d['country'].upper()}</div>
    <h3>{title(cid)}</h3>
    <p>{d['hook']} {FLAV[cid]}</p>
    <div class="ssg-cardmeta">32 pages · A4 · {st['links']} live links · {st['prices']}+ real prices</div>
    <div class="ssg-cardbtns">
     <a class="ssg-btn ssg-btn-buy" href="{buy}"{dis}>Buy Now</a>
     <a class="ssg-btn ssg-btn-more" href="{prod}"{dis}>Full details →</a>
    </div>
   </div>
  </article>'''

CSS = f'''
.ssg *{{margin:0;padding:0;box-sizing:border-box}}
.ssg{{font-family:Inter,-apple-system,'Segoe UI',Arial,sans-serif;background:{PAPER};color:{INK};line-height:1.6}}
.ssg .wrap{{max-width:1080px;margin:0 auto;padding:0 22px}}
.ssg h1,.ssg h2,.ssg h3{{font-family:Nunito,Inter,Arial,sans-serif}}
.ssg-hero{{text-align:center;padding:64px 0 54px;border-bottom:1px solid {LINE};background:#fff}}
.ssg-hero h1{{font-size:clamp(30px,5vw,48px);font-weight:900;letter-spacing:-1.2px;max-width:760px;margin:26px auto 0}}
.ssg-hero p{{font-size:clamp(15px,2.2vw,18px);color:{GREY};max-width:620px;margin:16px auto 0}}
.ssg-hero .ssg-sup{{margin-top:20px;font-size:12.5px;letter-spacing:.6px;color:{GREY};font-weight:600}}
.ssg-sec{{padding:56px 0}}
.ssg-sec.alt{{background:#fff;border-top:1px solid {LINE};border-bottom:1px solid {LINE}}}
.ssg-sec h2{{font-size:clamp(23px,3.4vw,32px);font-weight:900;letter-spacing:-.8px;margin-bottom:12px}}
.ssg-sec .lead{{color:{GREY};max-width:720px;font-size:16px;margin-bottom:8px}}
.ssg-benefits{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin-top:22px}}
.ssg-benefits div{{background:#fff;border:1px solid {LINE};border-radius:16px;padding:18px 20px;font-size:14px;color:#4b4a45}}
.ssg-benefits b{{display:block;font-family:Nunito;font-weight:800;font-size:15px;color:{INK};margin-bottom:4px}}
.ssg-sec.alt .ssg-benefits div{{background:{PAPER}}}
.ssg-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:20px;margin-top:26px}}
.ssg-card{{background:#fff;border:1px solid {LINE};border-radius:18px;overflow:hidden;display:flex;flex-direction:column;transition:transform .15s,box-shadow .15s}}
.ssg-card:hover{{transform:translateY(-3px);box-shadow:0 14px 34px rgba(25,24,23,.1)}}
.ssg-cardimg{{height:170px;background:linear-gradient(120deg,#e9e2d2,#d8cdb4);overflow:hidden}}
.ssg-cardimg img{{width:100%;height:100%;object-fit:cover;display:block}}
.ssg-cardbody{{padding:18px 20px 20px;display:flex;flex-direction:column;gap:8px;flex:1}}
.ssg-cardkick{{font-size:10.5px;letter-spacing:1.8px;font-weight:800;color:{SAND}}}
.ssg-card h3{{font-size:18.5px;font-weight:900;letter-spacing:-.3px;line-height:1.25}}
.ssg-card p{{font-size:13px;color:{GREY};flex:1}}
.ssg-cardmeta{{font-size:11.5px;font-weight:700;color:#8b867c;border-top:1px dashed {LINE};padding-top:9px}}
.ssg-cardbtns{{display:flex;gap:9px;margin-top:4px}}
.ssg-btn{{display:inline-block;padding:11px 18px;border-radius:12px;font-weight:800;font-size:13.5px;font-family:Nunito;text-decoration:none;transition:transform .12s}}
.ssg-btn:hover{{transform:translateY(-1px)}}
.ssg-btn-buy{{background:{INK};color:#fff}}
.ssg-btn-more{{background:#fff;border:1.5px solid {LINE};color:{INK}}}
.ssg-foot{{background:{INK};color:#b9b5ac;text-align:center;padding:36px 20px;font-size:13px}}
.ssg-foot b{{color:#fff;font-family:Nunito;font-weight:900;font-size:16px}}
.ssg-foot .dot{{color:{SAND}}}
@media(max-width:620px){{.ssg-hero{{padding:44px 0 40px}}.ssg-grid{{grid-template-columns:1fr}}}}
'''

HOME = f'''<!-- ============================================================
 SAMA SAMA GUIDES — Payhip homepage
 Paste this whole block into Payhip → Page Builder → Code block.
 To activate buttons: fill LINKS in build_payhip.py and re-run,
 or replace href="#" on .ssg-btn-buy / .ssg-btn-more per guide.
============================================================= -->
<div class="ssg">
<style>{CSS}</style>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@800;900&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<section class="ssg-hero"><div class="wrap">
 {LOGO_S.replace('width="360" height="280"','width="280" height="218"')}
 <h1>Honest, everything-in-one-place city guides.</h1>
 <p>Real prices, curated venues, neighbourhood strategy and live Google Maps links — for travelers who want the truth, not the tourist traps.</p>
 <div class="ssg-sup">27 detailed premium guides · researched 2026 · instant download</div>
</div></section>
<section class="ssg-sec"><div class="wrap">
 <h2>About Sama Sama Guides</h2>
 <p class="lead">Sama Sama makes detailed premium city guides — researched on the ground, priced in euros, designed like magazines and built to be used. Every guide is 32 print-ready A4 pages: budgets, neighbourhoods, food, markets, stays, day plans and a Top 10, with live links on every venue. The name is Indonesian for “you're welcome” — learnt, with a smile, on Gili Air.</p>
 <p class="lead">We don't take sponsorships or paid placements. If it's in a guide, it's there because it's good.</p>
</div></section>
<section class="ssg-sec alt"><div class="wrap">
 <h2>Why these guides are different</h2>
 <div class="ssg-benefits">
  <div><b>Real prices</b>Every section uses current, researched prices in euros — from a dorm bed to a splurge dinner.</div>
  <div><b>One tap to navigate</b>Around a hundred Google Maps links per guide. You never type an address on holiday.</div>
  <div><b>Neighbourhood strategy</b>We help you choose a base, not just a hotel — with honest “best for” labels.</div>
  <div><b>Plan-it-for-me included</b>A ready three-day plan, a Top 10, and honest budgets at three levels.</div>
  <div><b>Zero sponsorships</b>Nobody paid to be included. Ever.</div>
 </div>
</div></section>
<section class="ssg-sec"><div class="wrap">
 <h2>The guides</h2>
 <p class="lead">27 cities and islands across Thailand, Malaysia, Vietnam, Indonesia, the Philippines, Spain and the USA.</p>
 <div class="ssg-grid">
{chr(10).join(card(c) for c in ORDER)}
 </div>
</div></section>
<footer class="ssg-foot">
 <b>sama<span class="dot">·</span>sama</b> &nbsp;guides<br>
 Honest, detailed premium city guides · researched 2026<br>
 <span style="font-size:11.5px;opacity:.8">Know it · Pick it · Go</span>
</footer>
</div>'''

open('Payhip-Homepage.html','w').write(HOME)

# ---------------- per-city mini blocks (inline styles, paste anywhere) ----------------
def block(cid):
    d=DEST[cid]; L=LINKS[cid]
    buy=L['checkout'] or '#'; prod=L['product'] or '#'
    return f'''<!-- ==================== {title(cid).upper()} — city-page block ==================== -->
<div style="font-family:Inter,Arial,sans-serif;max-width:640px;background:#fff;border:1px solid #e8e5de;border-radius:16px;overflow:hidden;display:flex;flex-wrap:wrap">
 <div style="flex:1 1 200px;min-height:160px;background:#e9e2d2">
  <img src="{wm(COVERS[cid]['cover'],520)}" alt="{title(cid)}" style="width:100%;height:100%;min-height:160px;object-fit:cover;display:block" onerror="this.style.display='none'">
 </div>
 <div style="flex:2 1 300px;padding:18px 20px">
  <div style="font-size:10.5px;letter-spacing:1.8px;font-weight:800;color:#cfa356">{d['country'].upper()}</div>
  <div style="font-family:Nunito,Arial,sans-serif;font-size:19px;font-weight:900;color:#191817;margin:2px 0 6px">{title(cid)}</div>
  <p style="font-size:13px;color:#6f6c66;margin:0 0 12px;line-height:1.5">{d['hook']} 32 print-ready A4 pages — budgets, neighbourhoods, food, stays, day plans and a Top 10, every venue one tap from Google Maps.</p>
  <a href="{buy}" style="display:inline-block;background:#191817;color:#fff;padding:10px 18px;border-radius:11px;font-weight:800;font-size:13px;text-decoration:none;font-family:Nunito,Arial,sans-serif">Buy Now</a>
  <a href="{prod}" style="display:inline-block;margin-left:8px;color:#191817;border:1.5px solid #e8e5de;padding:10px 16px;border-radius:11px;font-weight:800;font-size:13px;text-decoration:none;font-family:Nunito,Arial,sans-serif">Full guide →</a>
 </div>
</div>
'''

blocks = f'''<!-- SAMA SAMA GUIDES — per-city blocks. Copy the block you need under the matching city page.
     Buttons point to "#" until Payhip links are filled in build_payhip.py (then re-run). -->\n\n''' + "\n\n".join(block(c) for c in ORDER)
open('Payhip-City-Blocks.html','w').write(blocks)

filled=sum(1 for c in ORDER if LINKS[c]['checkout'])
print(f"wrote Payhip-Homepage.html ({len(HOME)//1024} KB), Payhip-City-Blocks.html ({len(blocks)//1024} KB), 3 logo SVGs | links filled: {filled}/27")
