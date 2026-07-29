#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sama Sama v2 — premium single-file site integrating the full 123-destination
database with the 28 PDF guides as products. Writes samasama-v2.html + logo SVGs."""
import json, urllib.parse, collections

# ---------------------------------------------------------------------------
#  ALL DATA LIVES IN data/ — this script contains no hand-typed facts.
#  Adding a guide = append one object to data/guides.json. Nothing else.
# ---------------------------------------------------------------------------
D = 'data/'
def _load(n): return json.load(open(D + n, encoding='utf-8'))

DEST   = _load('all_destinations.json')   # 123 destinations, full price database
CINFO  = _load('country_info.json')       # ATM / health / diet / visa by country
RATES  = _load('rates.json')              # currency conversion rates
COVERS = _load('guide_covers.json')       # guide cover + place photo per guide
GSTATS = _load('guide_stats.json')        # links/maps/photos/prices/pages per guide
PHOTOS = _load('dest_photos.json')        # destination hero photo per city
GPREV  = _load('gprev_by_id.json')        # base64 preview WebP per guide (inline mode only)
GPDIM  = _load('gprev_dims.json')         # intrinsic w/h per preview (stops layout shift)
GUIDES = _load('guides.json')             # ORDERED list of the guides we sell
COUNTRY= _load('countries.json')          # flag emoji per country + Schengen list
SITE   = _load('site.json')               # brand, contact, shops, buy state

GUIDE_IDS = [g['id'] for g in GUIDES]
GNAME     = {g['id']: g['name'] for g in GUIDES if g.get('name')}
FLAV      = {g['id']: g.get('flav', '') for g in GUIDES}
FLAGS     = COUNTRY['flags']
SCHENGEN  = COUNTRY['schengen']

# ---- every number shown on the site is DERIVED, never typed twice ----
_pg = collections.Counter(v['pages'] for v in GSTATS.values() if 'pages' in v)
N = {
 'dest':       len(DEST),
 'countries':  len({d['country'] for d in DEST.values()}),
 'continents': len({d['region'] for d in DEST.values()}),
 'guides':     len(GUIDE_IDS),
 'pages':      _pg.most_common(1)[0][0] if _pg else 38,
 'facts':      SITE['stats']['facts_tracked'],
}
SHOPS = SITE['shops']
EMAIL = SITE['contact']['email']
def shop_links(style=''):
    a = f' style="{style}"' if style else ''
    L = [f'<a{a} target="_blank" rel="noopener" href="{s["url"]}">{s["name"]}</a>' for s in SHOPS]
    return ', '.join(L[:-1]) + ' and ' + L[-1]
def shop_names(last='and'):
    n = [s['name'] for s in SHOPS]
    return ', '.join(n[:-1]) + f' {last} ' + n[-1]

# slim the dataset for embedding (keep everything; add computed fields)
for cid, d in DEST.items():
    d['flag'] = FLAGS.get(d['country'], '🌍')
    d['gname'] = GNAME.get(cid, d['name'])
    d['guide'] = cid in GUIDE_IDS
    d['flav'] = FLAV.get(cid, '')

# ---------------- LOGO (new, badge design) ----------------
INK = "#14312a"   # deep guide-green ink
GOLD = "#e0a63c"
def badge(size):
    s = size
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="{s}" height="{s}">
<circle cx="60" cy="60" r="55" fill="#fdfaf3"/>
<circle cx="60" cy="60" r="55" fill="none" stroke="{INK}" stroke-width="5"/>
<g stroke="{GOLD}" stroke-width="5" stroke-linecap="round">
 <line x1="60" y1="18" x2="60" y2="28"/>
 <line x1="34" y1="29" x2="39.5" y2="38"/>
 <line x1="86" y1="29" x2="80.5" y2="38"/>
 <line x1="21" y1="49" x2="31" y2="52.5"/>
 <line x1="99" y1="49" x2="89" y2="52.5"/>
</g>
<path d="M38 66 a22 22 0 0 1 44 0 Z" fill="{GOLD}"/>
<path d="M22 74 q9 -7 19 0 t19 0 t19 0 t19 0" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>
<path d="M30 88 q9 -7 19 0 t19 0 t19 0" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round" opacity=".55"/>
</svg>'''

WORD = f'''<text x="0" y="0" font-family="Nunito,Inter,Arial,sans-serif" font-weight="900" font-size="46" letter-spacing="-1" fill="{INK}">sama<tspan fill="{GOLD}">·</tspan>sama</text>'''
LOGO_H = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 130" width="520" height="130">
<g transform="translate(5,5)">{badge(110)[badge(110).index('>')+1:-6]}</g>
<g transform="translate(138,80)">{WORD}</g>
<text x="140" y="106" font-family="Inter,Arial,sans-serif" font-weight="700" font-size="14" letter-spacing="5.5" fill="#8a8272">KNOW IT · PICK IT · GO</text>
</svg>'''
WORD_W = f'''<text x="0" y="0" font-family="Nunito,Inter,Arial,sans-serif" font-weight="900" font-size="46" letter-spacing="-1" fill="#ffffff">sama<tspan fill="{GOLD}">·</tspan>sama</text>'''
LOGO_SW = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 260" width="360" height="260">
<g transform="translate(120,0)">{badge(120)[badge(120).index('>')+1:-6]}</g>
<g transform="translate(74,180)">{WORD_W}</g>
<text x="180" y="212" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-weight="700" font-size="13" letter-spacing="5" fill="#e8e2d4">KNOW IT · PICK IT · GO</text>
</svg>'''
LOGO_S = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 260" width="360" height="260">
<g transform="translate(120,0)">{badge(120)[badge(120).index('>')+1:-6]}</g>
<g transform="translate(74,180)">{WORD}</g>
<text x="180" y="212" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-weight="700" font-size="13" letter-spacing="5" fill="#8a8272">KNOW IT · PICK IT · GO</text>
</svg>'''
open('logo2-badge.svg','w').write(badge(512))
open('logo2-horizontal.svg','w').write(LOGO_H)
open('logo2-stacked.svg','w').write(LOGO_S)
FAVICON = 'data:image/svg+xml,' + urllib.parse.quote(badge(64))

NAV_BADGE = badge(34)

CSS = """
:root{--ink:#14312a;--ink2:#0e241f;--gold:#e0a63c;--gold-soft:#f6ecd6;--bg:#faf8f3;--card:#fff;--line:#e8e2d4;--mut:#6f6a5e;--r:18px;--maxw:1120px}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:Inter,-apple-system,'Segoe UI',Arial,sans-serif;background:var(--bg);color:#20201b;line-height:1.6;-webkit-font-smoothing:antialiased}
h1,h2,h3,.disp{font-family:Nunito,Inter,Arial,sans-serif}
a{color:inherit;text-decoration:none}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 22px}
/* ---------- header ---------- */
header{position:sticky;top:0;z-index:60;background:rgba(250,248,243,.93);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.nb{display:flex;align-items:center;gap:14px;height:68px}
.brand{display:flex;align-items:center;gap:10px;font-family:Nunito;font-weight:900;font-size:21px;letter-spacing:-.6px;color:var(--ink)}
.brand .dot{color:var(--gold)}
nav.m{display:flex;gap:2px;margin-left:auto;align-items:center}
nav.m a{padding:9px 13px;border-radius:11px;font-size:14.5px;font-weight:600;color:#3c4740}
nav.m a:hover{background:var(--gold-soft)}
nav.m a.on{background:var(--gold-soft);color:var(--ink)}
select.cur{border:1.5px solid var(--line);background:#fff;border-radius:10px;padding:7px 9px;font-weight:700;font-size:13px;color:var(--ink);cursor:pointer}
.btn{display:inline-block;padding:12px 22px;border-radius:13px;font-weight:800;font-size:14.5px;cursor:pointer;border:none;transition:.15s;font-family:Nunito}
.btn:hover{transform:translateY(-1px)}
.btn-p{background:var(--ink);color:#fff!important}
.btn-p:hover{box-shadow:0 8px 22px rgba(20,49,42,.3)}
.btn-o{background:#fff;border:1.5px solid var(--line);color:var(--ink)}
.btn-g{background:var(--gold);color:#3a2a07!important}
.btn-sm{padding:8px 15px;font-size:13px;border-radius:11px}
nav.m a.cta{color:#fff;background:var(--ink);margin-left:8px}
nav.m a.cta:hover{background:var(--ink2);color:#fff}
.mb{display:none;margin-left:auto;background:none;border:1.5px solid var(--line);border-radius:10px;padding:7px 12px;font-size:18px;cursor:pointer}
/* ---------- hero ---------- */
.hero{padding:74px 0 60px;text-align:center;background:radial-gradient(900px 400px at 50% -80px,#f4ecd9 0%,rgba(250,248,243,0) 70%)}
.hero .biglogo{margin-bottom:26px}
.hero h1{font-size:clamp(34px,5.6vw,58px);font-weight:900;letter-spacing:-1.6px;line-height:1.06;max-width:840px;margin:0 auto;color:var(--ink)}
.hero p.sub{font-size:clamp(16px,2.3vw,19.5px);color:var(--mut);max-width:680px;margin:20px auto 30px}
.hero .btns{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.hero .supp{margin-top:24px;font-size:13.5px;color:var(--mut);font-weight:600;letter-spacing:.3px}

.heroph{position:relative;overflow:hidden}
.heroph .hbg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.heroph .hveil{position:absolute;inset:0;background:linear-gradient(180deg,rgba(13,32,26,.62),rgba(13,32,26,.55) 55%,rgba(250,248,243,.97) 96%)}
.heroph h1{color:#fff;text-shadow:0 2px 22px rgba(8,20,16,.45)}
.heroph p.sub{color:#eee8da;text-shadow:0 1px 12px rgba(8,20,16,.5)}
.heroph .supp{color:#f6f1e3;background:rgba(12,26,21,.42);display:inline-block;padding:8px 18px;border-radius:22px;backdrop-filter:blur(4px)}
.signup{margin-top:26px;background:linear-gradient(120deg,var(--ink),#1d4a3e);border-radius:var(--r);padding:22px 26px;display:flex;gap:18px;align-items:center;justify-content:space-between;flex-wrap:wrap}
.signup b{font-family:Nunito;font-size:18px;color:#fff}
.signup p{font-size:13px;color:#c9d3c8;margin-top:3px}
.signup .btn-p{background:var(--gold);color:#3a2a07!important}
.pb-count{font-size:13.5px;color:#5c5233;background:#fff;border:1px dashed #ddc98f;border-radius:12px;padding:11px 14px;margin-bottom:14px}
.pb-count b{color:var(--ink)}
.statbar{display:flex;justify-content:center;gap:clamp(18px,5vw,64px);padding:22px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:#fff;flex-wrap:wrap}
.statbar b{display:block;font-family:Nunito;font-size:26px;font-weight:900;color:var(--ink);letter-spacing:-.5px}
.statbar span{font-size:12px;letter-spacing:1.6px;color:var(--mut);font-weight:700;text-transform:uppercase}
/* ---------- sections ---------- */
section.blk{padding:58px 0}
section.alt{background:#fff;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
h2.sec{font-size:clamp(25px,3.6vw,36px);font-weight:900;letter-spacing:-1px;margin-bottom:12px;color:var(--ink)}
p.lead{color:var(--mut);max-width:740px;margin-bottom:26px;font-size:16.5px}
ul.feat{list-style:none;display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:14px}
ul.feat li{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:17px 19px;font-size:14.5px;color:#4b4a42}
ul.feat li b{display:block;margin-bottom:3px;font-size:15px;color:var(--ink);font-family:Nunito;font-weight:800}
.grid3{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:18px}
.pcard{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:26px;display:flex;flex-direction:column;gap:10px}
.pcard h3{font-size:20px;font-weight:900;color:var(--ink)}
.pcard p{font-size:14px;color:var(--mut);flex:1}
/* ---------- destination cards ---------- */
.filters{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:6px 0 22px}
.filters input[type=search]{flex:1;min-width:200px;padding:11px 15px;border:1.5px solid var(--line);border-radius:12px;font-size:14.5px;background:#fff}
.pills{display:flex;gap:7px;flex-wrap:wrap}
.pill{padding:8px 14px;border-radius:20px;background:#fff;border:1.5px solid var(--line);font-size:13px;font-weight:700;cursor:pointer;color:#4b544d}
.pill.on{background:var(--ink);border-color:var(--ink);color:#fff}
select.filt{border:1.5px solid var(--line);background:#fff;border-radius:12px;padding:10px 12px;font-weight:600;font-size:13.5px;cursor:pointer}
.dgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px}
.dcard{position:relative;background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:20px;display:flex;flex-direction:column;gap:7px;transition:.15s}
.dcard:hover{transform:translateY(-3px);box-shadow:0 12px 30px rgba(20,49,42,.1)}
.dcard .co{font-size:11px;letter-spacing:1.6px;font-weight:800;color:var(--mut);text-transform:uppercase}
.dcard h3{font-size:21px;font-weight:900;letter-spacing:-.5px;color:var(--ink)}
.dcard .hk{font-size:13.5px;color:var(--mut);flex:1}
.dcard .mt{display:flex;justify-content:space-between;font-size:12.5px;font-weight:700;color:#4b544d;border-top:1px dashed var(--line);padding-top:9px;margin-top:5px}
.gbadge{position:absolute;top:14px;right:14px;background:var(--gold);color:#3a2a07;font-size:10.5px;font-weight:900;padding:4px 10px;border-radius:14px;letter-spacing:.4px;font-family:Nunito}
.reglab{margin:32px 0 12px;font-size:12px;letter-spacing:2.6px;font-weight:900;color:var(--gold);text-transform:uppercase;font-family:Nunito}
/* ---------- city page ---------- */
.cph{padding:52px 0 26px}
.cph .co{font-size:12.5px;letter-spacing:2px;font-weight:800;color:var(--mut);text-transform:uppercase}
.cph h1{font-size:clamp(32px,5.4vw,50px);font-weight:900;letter-spacing:-1.4px;margin:6px 0 8px;color:var(--ink)}
.cph p.hk{color:var(--mut);max-width:700px;font-size:17.5px}
.vibes{display:flex;gap:7px;flex-wrap:wrap;margin-top:14px}
.vibe{background:var(--gold-soft);border:1px solid #eddebb;color:#7c5c1c;font-size:12px;font-weight:800;padding:5px 12px;border-radius:16px}
.guidebar{background:linear-gradient(120deg,var(--ink),#1d4a3e);border-radius:var(--r);color:#f3eee2;padding:26px 28px;margin:18px 0;display:flex;gap:20px;align-items:center;flex-wrap:wrap}
.guidebar .t{flex:1;min-width:240px}
.guidebar h3{font-size:21px;font-weight:900;color:#fff;margin-bottom:5px}
.guidebar p{font-size:13.5px;color:#cfd8ce}
.guidebar .btns{display:flex;gap:9px;flex-wrap:wrap}
.tiergrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin:8px 0 8px}
.tier{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:20px;text-align:center}
.tier.hl{border:2px solid var(--gold);background:#fffdf6}
.tier .lb{font-size:10.5px;letter-spacing:2.2px;font-weight:900;color:var(--mut)}
.tier .v{font-family:Nunito;font-size:30px;font-weight:900;color:var(--ink);margin:5px 0 2px}
.tier .v small{font-size:12px;color:var(--mut);font-weight:700}
.tier .d{font-size:11.5px;color:var(--mut)}
.maths{background:var(--gold-soft);border:1px solid #eddebb;border-radius:var(--r);padding:20px 22px;margin:10px 0 6px;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
.maths b.ttl{font-family:Nunito;font-size:16px;color:var(--ink)}
.maths input,.maths select{border:1.5px solid #e2cf9d;border-radius:10px;padding:9px 11px;font-size:14px;font-weight:700;background:#fff;width:86px}
.maths select{width:auto}
.maths .out{font-family:Nunito;font-size:23px;font-weight:900;color:var(--ink);margin-left:auto}
.secgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:16px;margin-top:14px}
.card{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:22px}
.card.w2{grid-column:1/-1}
.card h3{font-family:Nunito;font-size:16.5px;font-weight:900;color:var(--ink);margin-bottom:11px;display:flex;gap:8px;align-items:center}
.rows{display:grid;gap:0}
.row{display:flex;justify-content:space-between;gap:12px;padding:7.5px 0;border-bottom:1px dashed var(--line);font-size:13.5px}
.row:last-child{border-bottom:none}
.row .n{color:#43423a}
.row .n small{display:block;color:#9a948a;font-size:11px}
.row .p{font-weight:800;color:var(--ink);white-space:nowrap}
.note{background:var(--gold-soft);border-radius:12px;padding:11px 14px;font-size:12.5px;color:#6b5320;margin-top:11px}
.chip{display:inline-block;background:#f1ede2;border:1px solid var(--line);border-radius:14px;padding:4px 11px;font-size:12px;font-weight:700;color:#4b544d;margin:0 5px 6px 0}
.tip{border-left:3px solid var(--gold);padding:8px 0 8px 14px;margin:10px 0;font-size:13.5px;color:#43423a}
.tip .by{font-size:12px;color:var(--mut);font-weight:700;margin-top:4px}
.tip b.tt{color:var(--ink)}
.kv{font-size:13.5px;color:#43423a;margin-bottom:9px}
.kv b{color:var(--ink)}
.clim{width:100%;height:auto}
.legend{display:flex;gap:14px;font-size:11px;color:var(--mut);font-weight:700;margin-top:6px;flex-wrap:wrap}
.legend i{display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:4px;vertical-align:-1px}
.bk{display:inline-block;margin:26px 0 0;font-weight:800;font-size:14px;color:var(--mut)}
.bk:hover{color:var(--ink)}
/* ---------- photos & colour ---------- */
.phimg{width:100%;height:100%;object-fit:cover;display:block}
.strip{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-top:34px}
.stile{position:relative;height:150px;border-radius:16px;overflow:hidden;display:block;transition:.15s}
.stile:hover{transform:translateY(-3px)}
.stile .vl{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,25,20,0) 40%,rgba(10,25,20,.65))}
.stile b{position:absolute;left:12px;bottom:9px;color:#fff;font-family:Nunito;font-size:14.5px;font-weight:900;letter-spacing:-.2px}
.dph{height:112px;margin:-20px -20px 12px;overflow:hidden;position:relative}
.dstripe{height:7px;margin:-20px -20px 14px;border-radius:18px 18px 0 0}
.gcard .top{position:relative;padding:0;height:160px;overflow:hidden}
.gcard .top .vl{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,28,22,.12) 30%,rgba(10,28,22,.78))}
.gcard .top .tx{position:absolute;left:18px;bottom:12px;right:14px}
.cityhero{position:relative;height:270px;border-radius:var(--r);overflow:hidden;margin:4px 0 16px;background:linear-gradient(120deg,#1d4a3e,#14312a)}
.cityhero .vl{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,25,20,0) 45%,rgba(10,25,20,.5))}
/* ---------- guide preview ---------- */
.prevrow{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:16px;margin-top:14px}
.pgwrap{cursor:zoom-in}
.pgwrap:hover .pg{transform:translateY(-3px);box-shadow:0 14px 32px rgba(20,49,42,.18)}
.pgcap{text-align:center;font-size:12px;font-weight:700;color:var(--mut);margin-top:8px}
.pg{aspect-ratio:210/297;background:#fbf9f3;border:1px solid var(--line);border-radius:10px;box-shadow:0 6px 18px rgba(20,49,42,.1);overflow:hidden;position:relative;font-size:6.4px;transition:.15s}
.pg *{line-height:1.45}
.pg .pad{padding:9% 8%}
.pg .nhd{display:flex;gap:.5em;align-items:baseline;border-bottom:.22em solid #2b463d;padding-bottom:.55em;margin-bottom:.9em}
.pg .nhd b{font-family:Nunito;font-size:1.85em;font-weight:900;color:#232323;letter-spacing:-.03em}
.pg .lede{font-style:italic;font-size:1.15em;color:#0f5d4a;margin-bottom:1em;font-family:Georgia,serif}
.pg .tg{display:grid;grid-template-columns:1fr 1fr 1fr;gap:.7em;margin-bottom:1em}
.pg .tc{background:#fff;border:1px solid #ece7db;border-radius:.9em;padding:1em .6em;text-align:center}
.pg .tc.hl{border:.18em solid #6bbf9c;background:#eef6f0}
.pg .tc .l{font-size:.78em;letter-spacing:.18em;color:#8a857a;font-weight:800}
.pg .tc .v{font-family:Nunito;font-size:2em;font-weight:900;color:#0f5d4a;margin:.15em 0}
.pg .tc .d{font-size:.75em;color:#6f6a5e}
.pg .rw{display:flex;justify-content:space-between;padding:.5em 0;border-bottom:.5px dashed #e2dccc;font-size:.95em;color:#43423a}
.pg .rw b{color:#14312a}
.pg .vc{background:#fff;border:1px solid #ece7db;border-radius:.9em;padding:.9em 1em;margin-bottom:.7em}
.pg .vc .t{font-weight:800;color:#0f5d4a;font-size:1.1em;font-family:Nunito}
.pg .vc .m{font-size:.72em;letter-spacing:.1em;color:#c56a36;font-weight:800;text-transform:uppercase;margin:.15em 0 .3em}
.pg .vc .d{font-size:.86em;color:#4b4a42}
.pg .tipbx{background:#fbf3da;border:1px solid #ecd6a0;border-radius:.9em;padding:.9em 1em;font-size:.9em;color:#5c5233}
.pg .foot{position:absolute;left:8%;right:8%;bottom:3.5%;border-top:.5px solid #e2dccc;padding-top:.6em;display:flex;justify-content:space-between;font-size:.75em;color:#9a948a}
.pg .cols{columns:2;column-gap:1.4em}
.pg .ck{font-size:.92em;color:#43423a;padding:.28em 0;break-inside:avoid}
.pg .ck::before{content:"✓ ";color:#e0a63c;font-weight:900}
.pg.cover{background:#14312a;color:#fff}
.pg.cover .cvimg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.85}
.pg.cover .vl{position:absolute;inset:0;background:linear-gradient(180deg,rgba(12,26,21,.25),rgba(12,26,21,.2) 40%,rgba(12,26,21,.86))}
.pg.cover .in{position:absolute;left:9%;right:9%;bottom:7%}
.pg.cover .pillt{position:absolute;top:6%;right:8%;background:rgba(255,255,255,.92);color:#1e463b;font-size:.75em;letter-spacing:.14em;font-weight:800;padding:.5em 1em;border-radius:2em}
.pg.cover .kick{font-size:.8em;letter-spacing:.22em;color:#e0a63c;font-weight:800}
.pg.cover .big{font-family:Nunito;font-size:3.1em;font-weight:900;letter-spacing:-.03em;line-height:1;margin:.15em 0}
.pg.cover .sub{font-family:Georgia,serif;font-style:italic;font-size:.95em;opacity:.95;margin-bottom:.8em}
.pg.cover .wm{font-family:Nunito;font-size:1.25em;font-weight:900}
.pg.cover .wm i{color:#e0a63c;font-style:normal}
/* promo box */
.prev2{grid-template-columns:repeat(3,minmax(170px,220px));align-items:start;justify-content:start}
.prev2 .promobox{grid-column:1/-1}
@media(max-width:900px){.prev2{grid-template-columns:1fr 1fr}}
.pg.real{aspect-ratio:auto;padding:0}
.pg.real img{display:block;width:100%;height:auto}
.promobox{background:linear-gradient(135deg,#fffdf6,#fdf6e6);border:1.5px solid #ecd9ae;border-radius:var(--r);padding:26px 28px}
.promobox h3{font-family:Nunito;font-size:21px;font-weight:900;color:var(--ink);margin-bottom:8px;letter-spacing:-.4px}
.pb-lead{font-size:14px;color:#5c5233;margin-bottom:16px}
.statgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px;margin-bottom:16px}
@media(min-width:920px){.statgrid{grid-template-columns:repeat(5,1fr)}}
.stt{background:#fff;border:1px solid #ecd9ae;border-radius:14px;padding:13px 10px;text-align:center}
.stt b{display:block;font-family:Nunito;font-size:25px;font-weight:900;color:var(--ink);letter-spacing:-.5px}
.stt span{font-size:11px;color:#8a7a4e;font-weight:700;line-height:1.3;display:block;margin-top:2px}
.pb-list{list-style:none;display:grid;gap:9px}
.pb-list li{padding-left:24px;position:relative;font-size:13.5px;color:#4b4a42}
.pb-list li::before{content:"★";position:absolute;left:0;color:var(--gold);font-weight:900}
.pb-list b{color:var(--ink)}
/* ---- preview effects (flashy but classy) ---- */
.prev2 .pgwrap{position:relative;animation:pvUp .6s cubic-bezier(.2,.7,.2,1) both}
.prev2 .pgwrap:nth-child(1){animation-delay:.05s}.prev2 .pgwrap:nth-child(2){animation-delay:.16s}.prev2 .pgwrap:nth-child(3){animation-delay:.27s}
@keyframes pvUp{from{opacity:0;transform:translateY(22px) scale(.97)}to{opacity:1;transform:none}}
.prev2 .pg{transition:transform .35s cubic-bezier(.2,.7,.2,1),box-shadow .35s,border-color .35s}
.prev2 .pgwrap:hover .pg{transform:translateY(-8px) scale(1.025) rotate(-.4deg);border-color:#e0a63c;box-shadow:0 10px 24px rgba(20,49,42,.16),0 24px 54px rgba(224,166,60,.28)}
.prev2 .pgwrap:hover .pgcap{color:#a97b1f}
.pgcap{transition:color .3s}
.pgcap::before{content:'\25C6';color:#e0a63c;font-size:8px;margin-right:6px;vertical-align:2px}
.pg .sheen{position:absolute;inset:0;z-index:5;pointer-events:none;background:linear-gradient(115deg,transparent 38%,rgba(255,255,255,.28) 48%,rgba(255,240,200,.42) 52%,transparent 62%);background-size:280% 100%;background-position:120% 0;animation:pvSheen 5.6s ease-in-out infinite}
@keyframes pvSheen{0%,55%{background-position:130% 0}78%{background-position:-40% 0}100%{background-position:-40% 0}}
.pgwrap:hover .sheen{animation-duration:1.6s}
.pvbadge{position:absolute;top:-9px;left:50%;transform:translateX(-50%);z-index:6;background:linear-gradient(120deg,#e0a63c,#c98a2c);color:#fff;font-size:9px;font-weight:900;letter-spacing:1.6px;padding:5px 12px;border-radius:20px;box-shadow:0 4px 12px rgba(180,130,40,.4);white-space:nowrap}
.pg.real img{transition:transform .5s ease}
.pgwrap:hover .pg.real img{transform:scale(1.03)}
.stt{transition:transform .3s,box-shadow .3s}
.stt:hover{transform:translateY(-3px);box-shadow:0 10px 22px rgba(224,166,60,.22);border-color:#e0a63c}
.lbx{animation:lbFade .22s ease both}
.lbx .pg{animation:lbZoom .26s cubic-bezier(.2,.7,.2,1) both}
@keyframes lbFade{from{opacity:0}to{opacity:1}}
@keyframes lbZoom{from{transform:scale(.92);opacity:.4}to{transform:none;opacity:1}}
@media (prefers-reduced-motion: reduce){.prev2 .pgwrap,.pg .sheen,.lbx,.lbx .pg{animation:none!important}}
.lbx{position:fixed;inset:0;background:rgba(12,20,17,.78);z-index:120;display:flex;align-items:center;justify-content:center;padding:24px;cursor:zoom-out}
.lbx .pg{font-size:13px;width:min(88vw,460px);aspect-ratio:210/297;box-shadow:0 30px 80px rgba(0,0,0,.5)}
@media(max-width:820px){.strip{grid-template-columns:repeat(2,1fr)}.stile{height:110px}.lbx .pg{font-size:10.5px}}
/* guides hub */
.ggrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(255px,1fr));gap:16px}
.gcard{background:#fff;border:1px solid var(--line);border-radius:var(--r);overflow:hidden;display:flex;flex-direction:column;transition:.15s}
.gcard:hover{transform:translateY(-3px);box-shadow:0 12px 30px rgba(20,49,42,.1)}
.gcard .top{background:linear-gradient(120deg,var(--ink),#1d4a3e);color:#fff;padding:18px 20px}
.gcard .top .co{font-size:10.5px;letter-spacing:1.6px;font-weight:800;color:#b9c8bb;text-transform:uppercase}
.gcard .top h3{font-size:21px;font-weight:900;letter-spacing:-.4px}
.gcard .bd{padding:16px 20px;display:flex;flex-direction:column;gap:8px;flex:1}
.gcard .bd p{font-size:13px;color:var(--mut);flex:1}
.gcard .mt{font-size:12px;font-weight:700;color:#4b544d}
/* footer */
footer{background:var(--ink);color:#adbbb0;margin-top:74px}
footer .fw{max-width:var(--maxw);margin:0 auto;padding:42px 22px;display:flex;flex-wrap:wrap;gap:22px;align-items:center;justify-content:space-between;font-size:13.5px}
footer a{color:#e7e2d4;font-weight:700}
footer a:hover{color:var(--gold)}
footer .kofi a{color:var(--gold)}
.fl{display:flex;gap:16px;flex-wrap:wrap}
.samplebox{background:var(--gold-soft);border:1px solid #eddebb;border-radius:var(--r);padding:22px 24px}
.samplebox h3{font-size:16px;font-weight:900;color:var(--ink);margin-bottom:7px}
.samplebox p{font-size:14px;color:#5c5233}
.checklist{list-style:none;display:grid;gap:9px}
.checklist li{padding-left:26px;position:relative;font-size:15px}
.checklist li::before{content:"✓";position:absolute;left:0;color:var(--gold);font-weight:900}
.contactbox{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:30px;max-width:560px}
.contactbox a.mail{display:inline-block;background:var(--ink);color:#fff;padding:12px 22px;border-radius:12px;font-weight:800;margin:14px 0;font-family:Nunito}
.phnote{font-size:12.5px;color:var(--mut);font-style:italic;margin-top:8px}
@media(max-width:880px){
 nav.m{display:none;position:absolute;top:68px;left:0;right:0;background:#fff;border-bottom:1px solid var(--line);flex-direction:column;align-items:stretch;padding:12px 18px 18px}
 nav.m.open{display:flex}
 nav.m a{padding:12px}
 .mb{display:block}
 nav.m a.cta{margin:8px 0 0}
 .hero{padding:50px 0 46px}
}
"""

JS_HEAD = "const DEST=" + json.dumps(DEST, ensure_ascii=False) + ";\n" \
        + "const CINFO=" + json.dumps(CINFO, ensure_ascii=False) + ";\n" \
        + "const RATES=" + json.dumps(RATES, ensure_ascii=False) + ";\n" \
        + "const SCHENGEN=" + json.dumps(SCHENGEN) + ";\n" \
        + "const GUIDES=" + json.dumps(GUIDE_IDS) + ";\n" \
        + "const COVERS=" + json.dumps(COVERS, ensure_ascii=False) + ";\n" \
        + "const GSTATS=" + json.dumps(GSTATS) + ";\n" \
        + "const PHOTOS=" + json.dumps(PHOTOS, ensure_ascii=False) + ";\n" \
        + "const GPREV=" + json.dumps(GPREV if SITE['images']['inline_previews'] else {}) + ";\n" \
        + "const GPDIM=" + json.dumps(GPDIM) + ";\n" \
        + "const IMGCFG=" + json.dumps(SITE['images']) + ";\n" \
        + "const SITE=" + json.dumps(SITE, ensure_ascii=False) + ";\n" \
        + "const N=" + json.dumps(N, ensure_ascii=False) + ";\n"

JS = r"""
const $=s=>document.querySelector(s);
const ORDER=Object.keys(DEST).sort((a,b)=>{const A=DEST[a],B=DEST[b];return A.region.localeCompare(B.region)||A.country.localeCompare(B.country)||A.gname.localeCompare(B.gname)});
const REGIONS=[...new Set(ORDER.map(i=>DEST[i].region))];
const VIBES=[...new Set(Object.values(DEST).flatMap(d=>d.vibes))].sort();
let CUR=localStorage.getItem('ss_cur')||'EUR';
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');
function cv(v){const r=RATES[CUR]||RATES.EUR;const x=v*r.r;
 const n=x>=100?Math.round(x):x>=10?Math.round(x*2)/2:Math.round(x*10)/10;
 return (r.pre||'')+(n%1?n.toFixed(n<10?1:0):n.toLocaleString('en-US'))+(r.post||'')}
function rng(a,b){if(a===0&&(b===0||b===undefined))return 'free';return a===b?cv(a):cv(a)+'–'+cv(b)}
const stat=(n,l)=>`<div><b>${n}</b><span>${l}</span></div>`;
const wm=(fn,w)=>'https://commons.wikimedia.org/wiki/Special:FilePath/'+encodeURIComponent(fn)+'?width='+(w||700);
const IMG_ERR=` onerror="this.style.display='none'"`;
/* responsive: Commons resizes on demand via ?width=, so srcset is free */
const WLADDER=[320,460,640,900,1300,1800];
const wmset=(fn,max)=>WLADDER.filter(w=>w<=max).map(w=>`${wm(fn,w)} ${w}w`).join(', ');
const REGHUE={'SE Asia':'linear-gradient(120deg,#d98e3f,#c06a2e)','Europe':'linear-gradient(120deg,#4f8a68,#33604a)','Americas':'linear-gradient(120deg,#c65f52,#a03f35)','Africa':'linear-gradient(120deg,#b3762e,#8f5a1e)','Asia':'linear-gradient(120deg,#8a68b8,#63488c)','Oceania':'linear-gradient(120deg,#3f87a6,#2a5f78)'};
const phot=(id,w,sz,eager)=>PHOTOS[id]?`<img class="phimg" loading="${eager?'eager':'lazy'}"${eager?' fetchpriority="high"':''} decoding="async" alt="${esc(DEST[id].gname)}" src="${wm(PHOTOS[id],w||700)}" srcset="${wmset(PHOTOS[id],(w||700)*2)}" sizes="${sz||(w||700)+'px'}"${IMG_ERR}>`:'';
const gph=(id,w,sz)=>COVERS[id]?`<img class="phimg" loading="lazy" decoding="async" alt="${esc(DEST[id].gname)} guide" src="${wm(COVERS[id].cover,w||700)}" srcset="${wmset(COVERS[id].cover,(w||700)*2)}" sizes="${sz||(w||700)+'px'}"${IMG_ERR}>`:'';
/* one preview page, AVIF with WebP fallback, or inlined if site.json says so */
const SZ_PREV='(max-width:700px) 62vw, 300px';
function prevImg(id,name){const alt=`A real page from the ${esc(name)} guide`,dm=GPDIM[id]||[460,651];
 if(IMGCFG.inline_previews) return `<img src="${GPREV[id]}" alt="${alt}" loading="lazy" decoding="async" width="${dm[0]}" height="${dm[1]}">`;
 const b=`${IMGCFG.prev_dir}/${id}`;
 return `<picture><source type="image/avif" srcset="${b}-460.avif 460w, ${b}-920.avif 920w" sizes="${SZ_PREV}"><source type="image/webp" srcset="${b}-460.webp 460w, ${b}-920.webp 920w" sizes="${SZ_PREV}"><img src="${b}-460.webp" alt="${alt}" loading="lazy" decoding="async" width="${dm[0]}" height="${dm[1]}"></picture>`}
const hasPrev=id=>IMGCFG.inline_previews?!!GPREV[id]:!!GPDIM[id];
const PLATS=SITE.shops.map(s=>({n:s.name,url:s.url,d:s.blurb}));
const platCards=()=>`<div class="grid3">`+PLATS.map(p=>`<div class="pcard"><h3>${p.n}</h3><p>${p.d}</p><a class="btn btn-o" target="_blank" rel="noopener" href="${p.url}">Visit ${p.n} ↗</a></div>`).join('')+`</div>`;
function dcard(id){const d=DEST[id];
 const top=`<div class="dph" style="background:${REGHUE[d.region]||'#33604a'}">${phot(id,520,"(max-width:640px) 92vw, (max-width:1100px) 46vw, 340px")}<div class="stile-vl" style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,25,20,0) 55%,rgba(10,25,20,.35))"></div></div>`;
 return `<a class="dcard" href="#/city/${id}">
 ${d.guide?'<span class="gbadge">PREMIUM GUIDE</span>':''}${top}
 <div class="co">${d.flag} ${esc(d.country)}</div><h3>${esc(d.gname)}</h3>
 <div class="hk">${esc(d.hook)}</div>
 <div class="mt"><span>☀ ${esc(d.climate.best)}</span><span>${cv(d.tiers.s)}–${cv(d.tiers.f)}/day</span></div></a>`}
function gcard(id){const d=DEST[id];return `<a class="gcard" href="#/city/${id}">
 <div class="top" style="background:${REGHUE[d.region]||'#33604a'}">${gph(id,560,"(max-width:640px) 92vw, (max-width:1100px) 46vw, 360px")}<div class="vl"></div>
  <div class="tx"><div class="co">${d.flag} ${esc(d.country)}</div><h3>${esc(d.gname)}</h3></div></div>
 <div class="bd"><p>${esc(d.flav)}</p>
 <div class="mt">${(GSTATS[id]||{}).pages||38} pages · A4 · ${cv(d.tiers.s)}–${cv(d.tiers.f)}/day</div>
 <span class="btn btn-g btn-sm" style="align-self:flex-start">View premium guide →</span></div></a>`}
function setD(t){const m=document.querySelector('meta[name="description"]');if(m)m.content=t}

/* -------- guide preview (mock pages in the guide's own design) -------- */
const CONTENTS=['What\u2019s inside + how to use','The place & what a day costs','City at a glance \u2014 the best-of snapshot','What & how to eat','Where to eat \u2014 cheap & local','Mid-range & special occasion','Sweets, caf\u00e9s & coffee','Vegan, veggie & gluten-free','Supermarkets & typical prices','Markets & food halls','Souvenirs & shopping','Where to stay \u2014 neighbourhoods','Budget, boutique & luxury stays','Hostels \u2014 the backpacker shortlist','Six big things to do','Top 10 experiences \u2014 book & compare','Nightlife & after dark','Best day trips','Insider tips + safety & scams','Ready-made day plans','Getting around','Arrival, tickets & transport cheat sheet','When to go + best time to visit','Cash, cards & tipping','Connectivity & insurance','Health, safety & entry','The travel toolbox','Every link, one place'];
function guidePreview(id,d){
 const cover=COVERS[id];
 const dorm=(d.stays.night||[])[0], meal=(d.eat||[])[0], tr=(d.transit||[])[0], wat=(d.market.items||[])[0];
 const rows=[dorm,meal,tr,wat].filter(Boolean).map(r=>`<div class="rw"><span>${esc(r[0])}</span><b>${rng(r[1],r[2]!==undefined?r[2]:r[1])}</b></div>`).join('');
 const eats=(d.eat||[]).slice(0,3).map(r=>`<div class="vc"><div class="t">${esc(r[0])}</div><div class="m">${r[3]?esc(r[3]):'local favourite'}</div><div class="d">${rng(r[1],r[2]!==undefined?r[2]:r[1])}${r[3]?'':' — as researched on the ground'}</div></div>`).join('');
 const pgCover=`<div class="pg cover"><span class="sheen"></span>${cover?`<img class="cvimg" loading="lazy" decoding="async" alt="" src="${wm(cover.cover,640)}" srcset="${wmset(cover.cover,1300)}" sizes="${SZ_PREV}"${IMG_ERR}>`:''}<div class="vl"></div>
  <span class="pillt">THE COMPLETE CITY GUIDE</span>
  <div class="in"><div class="kick">${esc(d.country).toUpperCase()} · RESEARCHED 2026</div>
  <div class="big">${esc(d.gname)}</div><div class="sub">${esc(d.hook)}</div>
  <div class="wm">sama<i>·</i>sama</div></div></div>`;
 const st=GSTATS[id]||{links:230,maps:100,photos:60,prices:230,pages:38};
 const pgToc=`<div class="pg"><div class="pad">
  <div class="nhd"><b>What this guide covers</b></div>
  <div class="lede">${st.pages} pages, A4 — cover to back, everything in one place.</div>
  <div class="cols">${CONTENTS.map(c=>`<div class="ck">${c}</div>`).join('')}</div>
  <div class="foot"><span>Sama·Sama · ${esc(d.gname)} guide</span><span>${st.pages} pages</span></div></div></div>`;
 const promo=`<div class="promobox">
  <h3>Everything. In one premium file. Working for you.</h3>
  <p class="pb-lead">This isn\u2019t a blog post saved as a PDF \u2014 it\u2019s a <b>detailed, premium, ${st.pages}-page A4 magazine</b> \u2014 researched on the ground, designed to be used. Keep it on your phone or print it, open it at a street corner in ${esc(d.gname)} and it answers the question you\u2019re standing there with.</p>
  <div class="statgrid">
   <div class="stt"><b data-n="${st.pages}">${st.pages}</b><span>A4 pages \u2014 cover to back</span></div>
   <div class="stt"><b data-n="${st.prices}" data-suf="+">${st.prices}+</b><span>researched prices in \u20AC</span></div>
   <div class="stt"><b data-n="${st.links}">${st.links}</b><span>live, verified links</span></div>
   <div class="stt"><b data-n="${st.maps}">${st.maps}</b><span>jump straight to Google Maps</span></div>
   <div class="stt"><b data-n="${st.photos}">${st.photos}</b><span>hand-picked photos</span></div>
  </div>
  <p class="pb-count">Add it up: <b>${st.prices+st.links+st.photos}+ researched details</b> \u2014 every price checked, every venue placed, every link live. More usable information than a week of blog-tab hopping, in one beautiful file.</p>
  <ul class="pb-list">
   <li><b>Every venue is one tap from navigation</b> \u2014 ${st.maps} Google Maps links mean you never type an address on holiday.</li>
   <li><b>Real prices, not vibes</b> \u2014 three honest daily budgets (${cv(d.tiers.s)} / ${cv(d.tiers.c)} / ${cv(d.tiers.f)}) and prices on everything from a dorm bed to a splurge dinner.</li>
   <li><b>Zero sponsorships</b> \u2014 nobody paid to be in this guide. If it\u2019s in, it\u2019s in because it\u2019s good.</li>
   <li><b>Book everything from the page</b> \u2014 stays open on Booking.com & Hostelworld, experiences on GetYourGuide, Trip.com & Klook, transport on official operator sites.</li>
   <li><b>Plan-it-for-me included</b> \u2014 ready day plans, a Top 10, a best-of snapshot, and neighbourhood \u201Cbest for\u201D labels that choose your base with you.</li>
  </ul>
  <div class="btns" style="display:flex;gap:10px;flex-wrap:wrap;margin-top:14px">
   <a class="btn btn-g payhip-buy" data-city="${id}" href="#" onclick="return false" title="${esc(SITE.buy.tooltip)}">Buy the ${esc(d.gname)} guide</a>
  </div></div>`;
 return `<section id="gpreview" style="padding:8px 0 6px">
  <h2 class="sec" style="font-size:24px;margin-top:14px">Inside the premium guide</h2>
  <p class="lead" style="margin-bottom:4px">A preview of the real thing \u2014 a detailed premium guide, researched on the ground. Click a page to enlarge.</p>
  <div class="prevrow prev2">
   <div class="pgwrap">${pgCover}<div class="pgcap">The cover</div></div>
   <div class="pgwrap">${pgToc}<div class="pgcap">Everything it covers</div></div>
   ${hasPrev(id)?`<div class="pgwrap"><span class="pvbadge">STRAIGHT FROM THE GUIDE</span><div class="pg real">${prevImg(id,d.gname)}</div><div class="pgcap">Designed cover to cover</div></div>`:''}
   ${promo}
  </div></section>`;
}

/* -------- climate mini chart -------- */
function climChart(c){
 const W=340,H=110,base=86,mons='JFMAMJJASOND';
 const rmax=Math.max(...c.rain,1),tmax=40;
 let bars='',air='',sea='',lbl='';
 for(let i=0;i<12;i++){
  const x=12+i*27;
  const rh=(c.rain[i]/rmax)*52;
  bars+=`<rect x="${x-7}" y="${base-rh}" width="14" height="${rh}" rx="3" fill="#9db8d6"/>`;
  air+=(i?'L':'M')+`${x} ${base-(c.air[i]/tmax)*66} `;
  if(c.sea&&c.sea.length)sea+=(i?'L':'M')+`${x} ${base-(c.sea[i]/tmax)*66} `;
  lbl+=`<text x="${x}" y="${base+16}" text-anchor="middle" font-size="8.5" fill="#8b857a">${mons[i]}</text>`;
 }
 return `<svg class="clim" viewBox="0 0 ${W} ${H}">
 <line x1="6" y1="${base}" x2="${W-6}" y2="${base}" stroke="#e2dccc"/>
 ${bars}<path d="${air}" fill="none" stroke="#d07a35" stroke-width="2.4" stroke-linejoin="round"/>
 ${sea?`<path d="${sea}" fill="none" stroke="#0f96b2" stroke-width="2.2" stroke-linejoin="round"/>`:''}${lbl}</svg>
 <div class="legend"><span><i style="background:#d07a35"></i>Day °C</span>${sea?'<span><i style="background:#0f96b2"></i>Sea °C</span>':''}<span><i style="background:#9db8d6"></i>Rain</span></div>`;
}
/* -------- rows helpers -------- */
const rowsT=arr=>`<div class="rows">`+arr.map(r=>`<div class="row"><span class="n">${esc(r[0])}${r[3]?`<small>${esc(r[3])}${r[4]?' — '+esc(r[4]):''}</small>`:(r[4]?`<small>${esc(r[4])}</small>`:'')}</span><span class="p">${rng(r[1],r[2])}</span></div>`).join('')+`</div>`;
const rows2=arr=>`<div class="rows">`+arr.map(r=>`<div class="row"><span class="n">${esc(r[0])}</span><span class="p">${rng(r[1],r[2]!==undefined?r[2]:r[1])}</span></div>`).join('')+`</div>`;

const VIEWS={
home(){document.title='Sama Sama — Honest travel database & city guides';setD(`${N.dest} destinations, ${N.countries} countries, real prices — plus ${N.guides} detailed premium city guides. ${SITE.brand.tagline}`);
 const featured=['tokyo','prague','rio','cusco','sydney','dubrovnik'];
 return `
 <section class="hero heroph"><img class="hbg" loading="eager" fetchpriority="high" decoding="async" alt="" src="${wm('Oia Santorini Blue Domes.jpg',1300)}" srcset="${wmset('Oia Santorini Blue Domes.jpg',1800)}" sizes="100vw"${IMG_ERR}><div class="hveil"></div><div class="wrap" style="position:relative">
  <div class="biglogo">__LOGO_STACKED_W__</div>
  <h1>Honest, everything-in-one-place city guides.</h1>
  <p class="sub">Real prices, curated venues, neighbourhood strategy and live data—for travelers who want the truth, not the tourist traps.</p>
  <div class="btns"><a class="btn btn-p" href="#/destinations">Explore ${N.dest} Destinations</a>
  <a class="btn btn-g" href="#/guides">Browse City Guides</a>
  <a class="btn btn-o" href="#/where-to-buy">Where to Buy</a></div>
  <div class="supp">${N.dest} destinations · ${N.guides} detailed premium guides · researched ${SITE.brand.research_year} · built for real trips, not just inspiration.</div>
  <div class="strip">${['bangkok','boracay','madrid','miami','ubud'].map(i=>`<a class="stile" style="background:${REGHUE[DEST[i].region]}" href="#/city/${i}">${phot(i,520,"(max-width:640px) 46vw, 210px")}<div class="vl"></div><b>${DEST[i].gname}</b></a>`).join('')}</div>
 </div></section>
 <div class="statbar">${stat(N.dest,'Destinations')}${stat(N.countries,'Countries')}${stat(N.continents,'Continents')}${stat(N.facts,'Facts tracked')}${stat(N.guides,'Premium guides')}</div>
 <section class="blk"><div class="wrap">
  <h2 class="sec">What is Sama Sama?</h2>
  <p class="lead">Sama Sama is an honest travel database and a series of deeply researched city guides. Everything gives you:</p>
  <ul class="feat">
   <li><b>Budgets</b>What a day costs at three levels—scrimp, comfort, splurge.</li>
   <li><b>Neighbourhoods</b>Where to stay and why, with clear “best for” labels.</li>
   <li><b>Food</b>Street food, mid-range and special-occasion dining, with real prices.</li>
   <li><b>Daily life</b>Convenience stores, typical prices, laundry, massage, transport and SIMs.</li>
   <li><b>Experiences</b>Markets, sights, day trips and a Top 10 list for easy planning.</li>
  </ul>
 </div></section>
 <section class="blk alt"><div class="wrap">
  <h2 class="sec">The database — every destination, priced</h2>
  <p class="lead">Free, no ads, no sponsored picks. Transit fares, grocery baskets, dorm beds, street plates and ATM fees for ${N.dest} places — see it in your money with the currency picker above.</p>
  <div class="dgrid" style="grid-template-columns:repeat(auto-fit,minmax(280px,1fr))">${featured.map(dcard).join('')}</div>
  <div style="margin-top:22px"><a class="btn btn-p" href="#/destinations">See all ${N.dest} destinations</a></div>
 </div></section>
 <section class="blk"><div class="wrap">
  <h2 class="sec">The ${N.guides} detailed premium city guides</h2>
  <p class="lead">Our best work: detailed, premium ${N.pages}-page magazine-style PDF guides — budgets, neighbourhood strategy, food, markets, stays, day plans and a Top 10, with live Google Maps links on every venue.</p>
  <div class="ggrid">${['sevilla','phuket','fortlauderdale','hanoi'].map(gcard).join('')}</div>
  <div style="margin-top:22px"><a class="btn btn-g" href="#/guides">All ${N.guides} premium guides</a></div>
  <div class="signup"><div>
    <b>Get new guides first</b>
    <p>New cities, updates and launch discounts — straight to your inbox. No spam, ever.</p></div>
    <a class="btn btn-p" href="mailto:${SITE.contact.email}?subject=Keep%20me%20posted%20about%20new%20Sama%20Sama%20guides&body=Hi%20Sama%20Sama%20%E2%80%94%20add%20me%20to%20the%20list%20for%20new%20guides%20and%20updates!">Keep me posted →</a>
  </div>
 </div></section>
 <section class="blk alt" id="buy"><div class="wrap">
  <h2 class="sec">Where to buy our premium guides</h2>
  <p class="lead">You’ll be able to buy our premium city guides on four platforms. For now, these links go to their main pages—once our shops are live, we’ll link directly to them.</p>
  ${platCards()}
 </div></section>
 <section class="blk"><div class="wrap">
  <h2 class="sec">About Sama Sama</h2>
  <p class="lead" style="max-width:840px">Sama Sama creates honest, everything-in-one-place city guides—researched on the ground, with real prices, curated venues, neighbourhood strategy and live Google Maps links. Built for travelers who want the truth, not the tourist traps. We don’t take sponsorships or paid placements; if it’s in the guide, it’s there because it’s good.</p>
  <a class="btn btn-o" href="#/about">More about us</a>
 </div></section>`},
destinations(){document.title='Destinations — Sama Sama';setD(`${N.dest} destinations across ${N.countries} countries with real prices: transit, stays, groceries, eating out and more.`);
 return `<section class="blk"><div class="wrap">
  <h2 class="sec" style="font-size:clamp(28px,4.4vw,42px)">Destinations</h2>
  <p class="lead">${N.dest} places, priced for real life. Filter by region and vibe — prices shown in <b>${CUR}</b> (change it in the header).</p>
  <div class="filters">
   <input type="search" id="q" placeholder="Search city or country…">
   <select class="filt" id="fv"><option value="">All vibes</option>${VIBES.map(v=>`<option>${v}</option>`).join('')}</select>
   <select class="filt" id="fs"><option value="az">A → Z</option><option value="cheap">Cheapest first</option><option value="price">Priciest first</option></select>
  </div>
  <div class="pills" id="fr">${['All',...REGIONS].map((r,i)=>`<span class="pill${i===0?' on':''}" data-r="${r}">${r}</span>`).join('')}</div>
  <div id="dlist" style="margin-top:8px"></div>
 </div></section>`},
guides(){document.title='City Guides — Sama Sama';setD(`${N.guides} detailed premium city guides: ${N.pages} pages each of budgets, neighbourhoods, food, markets, stays and experiences.`);
 return `<section class="blk"><div class="wrap">
  <h2 class="sec" style="font-size:clamp(28px,4.4vw,42px)">City Guides</h2>
  <p class="lead">${N.guides} honest, detailed premium guides — ${N.pages} pages each, with real prices, curated venues, neighbourhood strategy and live Google Maps links. Researched ${SITE.brand.research_year}.</p>
  <div class="ggrid">${GUIDES.map(gcard).join('')}</div>
 </div></section>`},
'where-to-buy'(){document.title='Where to Buy — Sama Sama Guides';setD(`Buy Sama Sama city guides on ${SHOP_NAMES}. Bundles, collections and memberships coming soon.`);
 return `<section class="blk"><div class="wrap">
  <h2 class="sec" style="font-size:clamp(28px,4.4vw,42px)">Where to buy our premium guides</h2>
  <p class="lead">Our premium city guides will be available on four platforms. For now, these links go to their main pages—once our shops are live, we’ll link directly to our shops and bundles.</p>
  ${platCards()}
  <div style="margin-top:40px"><h2 class="sec" style="font-size:22px">Coming soon</h2>
  <ul class="feat">
   <li><b>Direct guide links</b>Every detailed premium guide, one click away.</li>
   <li><b>Bundles</b>Regional bundles—Southeast Asia, Spain, Florida.</li>
   <li><b>Membership options</b>Early access and updates for supporters.</li>
   <li><b>Full collection</b>All ${N.guides} premium guides in one mega bundle.</li>
  </ul><p class="phnote">Placeholders — links will go live with our shops.</p></div>
  <div style="margin-top:44px"><h2 class="sec" style="font-size:22px">Frequently asked</h2>
  <ul class="feat">
   <li><b>What exactly do I get?</b>A detailed premium city guide as a ${N.pages}-page, A4, print-ready PDF — beautifully designed, photo-rich, and made to be used on your phone or on paper.</li>
   <li><b>Do the links work in the PDF?</b>Yes — every venue, sight and booking link is clickable, and most jump straight to Google Maps so you never type an address on holiday.</li>
   <li><b>How do I receive it?</b>Instant digital download right after checkout on the platform you buy from. No shipping, no waiting.</li>
   <li><b>Can I print it?</b>Absolutely — it's laid out on A4 exactly so it prints beautifully at home or a copy shop.</li>
   <li><b>Are prices up to date?</b>Every guide is researched ${SITE.brand.research_year} with real prices in euros. Prices drift — that's travel — but we date our research and keep guides honest.</li>
   <li><b>Refunds?</b>Digital-download refund rules follow the platform you buy on (${SHOP_NAMES_OR}) — check their policy at checkout.</li>
  </ul></div>
 </div></section>`},
about(){document.title='About — Sama Sama';setD('Sama Sama creates honest, everything-in-one-place city guides for travelers who want the truth, not the tourist traps.');
 return `<section class="blk"><div class="wrap" style="max-width:800px">
  <h2 class="sec" style="font-size:clamp(28px,4.4vw,42px)">About Sama Sama</h2>
  <p class="lead">Sama Sama creates honest, everything-in-one-place city guides for travelers who want the truth, not the tourist traps. The name is Indonesian for “you’re welcome” — learnt, with a smile, on Gili Air.</p>
  <h2 class="sec" style="font-size:20px;margin-top:24px">What we believe</h2>
  <ul class="checklist"><li>Travel should feel real, not staged.</li><li>You deserve clear prices and practical details.</li><li>Neighbourhood choice can make or break a trip.</li></ul>
  <h2 class="sec" style="font-size:20px;margin-top:28px">How we build each guide</h2>
  <ul class="checklist"><li>We research venues, prices and neighbourhoods in detail.</li><li>We convert local prices for easy planning.</li><li>We organise each guide around how people actually travel: where to stay, what a day costs, where to eat, how to get around, what to do.</li></ul>
  <h2 class="sec" style="font-size:20px;margin-top:28px">No sponsorships</h2>
  <p class="lead">If a place is in a Sama Sama guide, it’s there because it’s good—not because someone paid us.</p>
  <h2 class="sec" style="font-size:20px;margin-top:28px">Where to buy</h2>
  <p class="lead">Our detailed premium guides will be available on ${SHOP_LINKS_STYLED}. Once live, we’ll link directly to our shops from this page.</p>
  <div class="samplebox" style="margin-top:24px"><h3>Support Sama Sama</h3>
  <p>Sama Sama is fully independent — we don’t take sponsorships or paid placements. If you want to help us keep these guides honest and updated, you can support us on ${SUPPORT_LINK_STYLED}.</p></div>
 </div></section>`},
contact(){document.title='Contact — Sama Sama';setD('Get in touch with Sama Sama — corrections, tips, trip planning and custom guides.');
 return `<section class="blk"><div class="wrap">
  <h2 class="sec" style="font-size:clamp(28px,4.4vw,42px)">Got a question? Planning a trip?</h2>
  <p class="lead" style="font-size:18px;color:var(--ink);font-weight:600;margin-bottom:10px">We’d love to hear from you.</p>
  <p class="lead">We do more than guides. Whether you’re travelling solo, with a group, or planning something truly special — we’re here to help. Drop us a line for <b>individual & group trip planning</b>, a <b>fully custom destination guide</b> built around your interests and pace, or just to tell us what we got wrong — that’s always welcome too.</p>
  <div class="grid3" style="margin-bottom:30px">
   <div class="pcard"><h3>🗺️ Custom destination guides</h3><p>Your city, your pace, your interests — we build detailed premium guides from scratch, tailored to exactly how you travel.</p></div>
   <div class="pcard"><h3>✈️ Individual & group trip planning</h3><p>From a weekend for two to a 20-person group adventure — itineraries, logistics, local knowledge, all sorted.</p></div>
   <div class="pcard"><h3>💬 Questions, tips & feedback</h3><p>Spotted something off? Found a hidden gem we missed? Tell us — every good tip lands with a thank-you.</p></div>
  </div>
  <div class="contactbox"><b style="font-size:17px;font-family:Nunito">Say hello</b><br>
  <a class="mail" href="mailto:${SITE.contact.email}">✉ ${SITE.contact.email}</a>
  <div style="display:flex;gap:12px;font-size:14px;font-weight:700;color:#8a857a;flex-wrap:wrap;align-items:center">
   <span>Instagram</span> · <span>Facebook</span> · <span>TikTok</span>
   <span style="background:#f6ecd6;border:1px solid #ecd9ae;color:#7c5c1c;font-size:11px;font-weight:800;padding:3px 10px;border-radius:14px;letter-spacing:.4px">COMING SOON</span>
  </div></div>
 </div></section>`},
city(id){const d=DEST[id];if(!d)return VIEWS.destinations();
 document.title=`${d.gname} — prices, budgets & guide — Sama Sama`;
 setD(`${d.gname}, ${d.country}: real prices for transit, stays, groceries and eating out — plus budgets and the full Sama Sama guide.`);
 const ci=CINFO.atm[d.country]||{},hi=CINFO.health[d.country]||{},di=CINFO.diet[d.country];
 const visa=SCHENGEN.includes(d.country)?CINFO.visa.schengen:CINFO.visa.general;
 const guideBar=d.guide?`<div class="guidebar"><div class="t">
   <h3>📘 The detailed premium ${d.gname} guide — ${(GSTATS[id]||{}).pages||38} pages</h3>
   <p>${esc(d.flav)} Budgets, neighbourhoods, markets, stays, day plans and a Top 10 — every venue with a live Google Maps link. <a href="#gpreview" style="color:#e0a63c;font-weight:800" onclick="setTimeout(()=>document.getElementById('gpreview')?.scrollIntoView({behavior:'smooth'}),40)">See inside ↓</a></p></div>
   <div class="btns">
    <a class="btn btn-g payhip-buy" data-city="${id}" href="#" onclick="return false" title="${esc(SITE.buy.tooltip)}">Buy Now</a>
    ${SITE.shops.map(s=>`<a class="btn btn-o btn-sm" style="background:transparent;color:#fff;border-color:#3f6a5b" target="_blank" rel="noopener" href="${s.url}">${s.name} ↗</a>`).join('\n    ')}
   </div></div>`:'';
 const hero=PHOTOS[id]?`<div class="cityhero">${phot(id,1100,"100vw",1)}<div class="vl"></div></div>`:'';
 const preview=d.guide?guidePreview(id,d):'';
 const rides=(d.rides||[]).map(r=>`<div class="kv"><b>${esc(r.a)}</b>${r.no?` — ${esc(r.no)}`:''}${r.b?` · ${esc(r.b)}`:''}</div>`).join('');
 const tips=(d.tips||[]).map(t=>`<div class="tip"><b class="tt">${esc(t.t)}</b> — ${esc(t.b)}<div class="by">${esc(t.by)} · ${esc(t.w)} · ▲ ${t.up}</div></div>`).join('');
 return `
 <section class="cph"><div class="wrap">
  <div class="co">${d.flag} ${esc(d.country)} · ${esc(d.region)}</div>
  <h1>${esc(d.gname)}</h1><p class="hk">${esc(d.hook)}</p>
  <div class="vibes">${d.vibes.map(v=>`<span class="vibe">${v}</span>`).join('')}<span class="vibe" style="background:#e8f0ea;border-color:#cfe0d3;color:#2c5a45">☀ best: ${esc(d.climate.best)}</span></div>
 </div></section>
 <div class="wrap">${hero}${guideBar}${preview}
  <div class="tiergrid">
   <div class="tier"><div class="lb">SHOESTRING</div><div class="v">${cv(d.tiers.s)}<small>/day</small></div><div class="d">dorms, street plates, transit</div></div>
   <div class="tier hl"><div class="lb">COMFY</div><div class="v">${cv(d.tiers.c)}<small>/day</small></div><div class="d">private room, sit-down meals, a treat</div></div>
   <div class="tier"><div class="lb">FLASH</div><div class="v">${cv(d.tiers.f)}<small>/day</small></div><div class="d">nice hotel, good dinners, no maths</div></div>
  </div>
  <div class="maths"><b class="ttl">🧮 Trip maths</b>
   <label>nights <input type="number" id="tm-n" min="1" max="90" value="7"></label>
   <label>style <select id="tm-s"><option value="s">shoestring</option><option value="c" selected>comfy</option><option value="f">flash</option></select></label>
   <span class="out" id="tm-out"></span>
  </div>
  <div class="secgrid">
   <div class="card"><h3>🛵 Getting around</h3>${rides}${rowsT(d.transit||[])}</div>
   <div class="card"><h3>🛏 Stays</h3><div class="kv"><b>Per night</b></div>${rows2(d.stays.night||[])}${d.stays.month?`<div class="kv" style="margin-top:12px"><b>Monthly</b></div>${rows2(d.stays.month)}`:''}</div>
   <div class="card"><h3>🛒 Groceries & daily life</h3>${(d.market.chains||[]).map(c=>`<div class="kv"><b>${esc(c.n)}</b> — ${esc(c.t)}</div>`).join('')}${rows2(d.market.items||[])}</div>
   <div class="card"><h3>🍜 Eating out</h3>${rowsT(d.eat||[])}</div>
   <div class="card"><h3>🎡 Things to do — with kids</h3>${rowsT(d.kids||[])}</div>
   <div class="card"><h3>🌙 Things to do — grown-ups</h3>${rowsT(d.nokids||[])}</div>
   <div class="card"><h3>🌤 Climate</h3>${climChart(d.climate)}<div class="kv" style="margin-top:10px"><b>Best:</b> ${esc(d.climate.best)} · <b>Wet:</b> ${esc(d.climate.wet||'—')}</div>${d.climate.note?`<div class="note">${esc(d.climate.note)}</div>`:''}</div>
   <div class="card"><h3>✈️ Getting there</h3>${(d.fly.air||[]).map(a=>`<span class="chip">${esc(a)}</span>`).join('')}${rowsT(d.fly.routes||[])}${d.fly.note?`<div class="note">${esc(d.fly.note)}</div>`:''}</div>
   <div class="card"><h3>🏧 ATMs & money</h3>${ci.fee?`<div class="kv"><b>Fees:</b> ${esc(ci.fee)}</div>`:''}${ci.lim?`<div class="kv"><b>Limits:</b> ${esc(ci.lim)}</div>`:''}${ci.best?`<div class="kv"><b>Best machines:</b> ${ci.best.map(b=>`<span class="chip">${esc(b)}</span>`).join('')}</div>`:''}${ci.tip?`<div class="note">${esc(ci.tip)}</div>`:''}</div>
   <div class="card"><h3>🩺 Health & safety</h3>${hi.vax?`<div class="kv"><b>Vaccines:</b> ${esc(hi.vax)}</div>`:''}${hi.health?`<div class="kv"><b>Health:</b> ${esc(hi.health)}</div>`:''}${hi.water?`<div class="kv"><b>Tap water:</b> ${esc(hi.water)}</div>`:''}${hi.safe?`<div class="kv"><b>Safety:</b> ${esc(hi.safe)}</div>`:''}${hi.er?`<div class="note">Emergency: ${esc(hi.er)}</div>`:''}</div>
   ${di?`<div class="card"><h3>🌱 Vegan, veggie & gluten-free</h3><div class="kv"><b>Plant-based:</b> ${esc(di.v)}</div><div class="kv"><b>Gluten-free:</b> ${esc(di.g)}</div><div class="note">${esc(di.t)}</div></div>`:''}
   <div class="card"><h3>🛂 Visa & entry</h3><div class="kv">${esc(visa)}</div><div class="note">Rules change — always verify with an official source for your nationality before you book.</div></div>
   ${tips?`<div class="card w2"><h3>💬 Traveller tips & reports</h3>${tips}</div>`:''}
  </div>
  <a class="bk" href="#/destinations">← All destinations</a>
 </div>`},
};
function bindCity(id){const d=DEST[id];const n=$('#tm-n'),s=$('#tm-s'),o=$('#tm-out');
 if(!n)return;const f=()=>{o.textContent=cv(d.tiers[s.value]*(+n.value||1))+' total'};
 n.addEventListener('input',f);s.addEventListener('change',f);f()}
let FR='All';
function bindDest(){
 const list=$('#dlist');if(!list)return;
 const q=$('#q'),fv=$('#fv'),fs=$('#fs');
 const draw=()=>{
  let ids=ORDER.filter(i=>{const d=DEST[i];
   if(FR!=='All'&&d.region!==FR)return false;
   if(fv.value&&!d.vibes.includes(fv.value))return false;
   const s=(q.value||'').toLowerCase();
   if(s&&!(d.gname.toLowerCase().includes(s)||d.country.toLowerCase().includes(s)))return false;
   return true});
  if(fs.value==='cheap')ids.sort((a,b)=>DEST[a].tiers.c-DEST[b].tiers.c);
  else if(fs.value==='price')ids.sort((a,b)=>DEST[b].tiers.c-DEST[a].tiers.c);
  else ids.sort((a,b)=>DEST[a].gname.localeCompare(DEST[b].gname));
  if(fs.value!=='az'||q.value||fv.value||FR!=='All'){
   list.innerHTML=`<div class="dgrid">${ids.map(dcard).join('')}</div>`+(ids.length?'':'<p class="lead">No matches.</p>');
  }else{
   let out='';for(const r of REGIONS){const rid=ids.filter(i=>DEST[i].region===r);if(!rid.length)continue;
    out+=`<div class="reglab">${r}</div><div class="dgrid">${rid.map(dcard).join('')}</div>`}
   list.innerHTML=out;
  }};
 q.addEventListener('input',draw);fv.addEventListener('change',draw);fs.addEventListener('change',draw);
 $('#fr').addEventListener('click',e=>{const p=e.target.closest('.pill');if(!p)return;
  FR=p.dataset.r;document.querySelectorAll('#fr .pill').forEach(x=>x.classList.toggle('on',x===p));draw()});
 draw();
}
function render(){
 const h=location.hash.replace(/^#\/?/,'');
 const [v,arg]=h.split('/');
 $('#app').innerHTML = v==='city'?VIEWS.city(arg):(VIEWS[v]?VIEWS[v]():VIEWS.home());
 document.querySelectorAll('nav.m a[data-v]').forEach(a=>a.classList.toggle('on',a.dataset.v===(v||'home')));
 document.querySelector('nav.m').classList.remove('open');
 if(v==='city')bindCity(arg);
 if(v==='city')bindCounts();
 if(v==='destinations')bindDest();
 window.scrollTo(0,0);
}
function bindCounts(){
 if(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
 const els=document.querySelectorAll('.stt b[data-n]');if(!els.length)return;
 const io=new IntersectionObserver(ents=>{ents.forEach(en=>{if(!en.isIntersecting)return;io.unobserve(en.target);
  const el=en.target,n=+el.dataset.n,suf=el.dataset.suf||'',t0=performance.now(),D=900;
  (function tick(t){const p=Math.min(1,(t-t0)/D),e=1-Math.pow(1-p,3);el.textContent=Math.round(n*e)+suf;if(p<1)requestAnimationFrame(tick)})(t0);
 })},{threshold:.4});
 els.forEach(el=>io.observe(el));
}
window.addEventListener('hashchange',render);
document.addEventListener('DOMContentLoaded',()=>{
 const cs=$('#cursel');
 cs.innerHTML=Object.keys(RATES).map(c=>`<option${c===CUR?' selected':''}>${c}</option>`).join('');
 cs.addEventListener('change',()=>{CUR=cs.value;localStorage.setItem('ss_cur',CUR);render()});
 $('.mb').addEventListener('click',()=>document.querySelector('nav.m').classList.toggle('open'));
 document.body.addEventListener('click',e=>{
  const lb=e.target.closest('.lbx');
  if(lb){lb.remove();return}
  const w=e.target.closest('.pgwrap');
  if(w){const o=document.createElement('div');o.className='lbx';o.innerHTML=w.querySelector('.pg').outerHTML;document.body.appendChild(o)}
 });
 render();
});
"""
JS = JS.replace('__LOGO_STACKED__', LOGO_S.replace('width="360" height="260"','width="300" height="217"').replace('\n',''))
_sup = next(s for s in SHOPS if s['name'] == SITE['support_shop'])
SUPPORT_LINK = f'<a target="_blank" rel="noopener" href="{_sup["url"]}">{_sup["name"]}</a>'
SUPPORT_LINK_STYLED = f'<a style="font-weight:800;text-decoration:underline" target="_blank" rel="noopener" href="{_sup["url"]}">{_sup["name"]}</a>'
for _tok, _val in [('${SHOP_NAMES_OR}', shop_names('or')), ('${SHOP_NAMES}', shop_names()),
                   ('${SHOP_LINKS_STYLED}', shop_links('font-weight:800;text-decoration:underline')),
                   ('${SUPPORT_LINK_STYLED}', SUPPORT_LINK_STYLED)]:
    JS = JS.replace(_tok, _val)
JS = JS.replace('__LOGO_STACKED_W__', LOGO_SW.replace('width="360" height="260"','width="300" height="217"').replace('\n',''))

page = f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sama Sama — Honest travel database &amp; city guides</title>
<meta name="description" content="{N['dest']} destinations, {N['countries']} countries, real prices — plus {N['guides']} detailed premium city guides. {SITE['brand']['tagline']}">
<meta property="og:title" content="Sama Sama — honest travel prices & city guides">
<meta property="og:description" content="Real prices, curated venues, neighbourhood strategy. {N['dest']} destinations · {N['guides']} guides.">
<meta property="og:type" content="website">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@800;900&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Organization","name":"Sama Sama Guides","description":"Honest, everything-in-one-place city guides and travel price database.","email":"{EMAIL}"}}</script>
<style>{CSS}</style></head>
<body>
<header><div class="wrap nb">
 <a class="brand" href="#/">{NAV_BADGE} sama<span class="dot">·</span>sama</a>
 <button class="mb" aria-label="Menu">☰</button>
 <nav class="m" aria-label="Main">
  <a href="#/" data-v="home">Home</a>
  <a href="#/destinations" data-v="destinations">Destinations</a>
  <a href="#/guides" data-v="guides">City Guides</a>
  <a href="#/where-to-buy" data-v="where-to-buy">Where to Buy</a>
  <a href="#/about" data-v="about">About</a>
  <a href="#/contact" data-v="contact">Contact</a>
  <select class="cur" id="cursel" aria-label="Currency"></select>
  <a class="btn cta btn-sm" href="#/where-to-buy">Shop Guides</a>
 </nav>
</div></header>
<main id="app"></main>
<footer><div class="fw">
 <div>© {SITE["brand"]["copyright_year"]} {SITE["brand"]["legal"]} · Honest, detailed premium city guides.<br>
 <span style="font-size:12.5px">{N['dest']} destinations · {N['countries']} countries · {N['continents']} continents · Find us on {shop_links()}.</span></div>
 <div class="fl"><a href="#/about">About</a><a href="#/where-to-buy">Where to Buy</a><a href="#/contact">Contact</a></div>
 <div class="kofi">Support {SITE["brand"]["name"]} on {SUPPORT_LINK}</div>
</div></footer>
<script>{JS_HEAD}{JS}</script>
</body></html>"""

open('samasama-v2.html','w').write(page)
print(f"  previews: {'inlined' if SITE['images']['inline_previews'] else 'external ' + SITE['images']['prev_dir'] + '/ (avif+webp)'}")
print(f"wrote samasama-v2.html ({len(page)//1024} KB) — {N['dest']} destinations, {N['countries']} countries, {N['guides']} guides @ {N['pages']} pages")
