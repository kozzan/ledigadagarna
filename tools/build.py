#!/usr/bin/env python3
"""Render the site into dist/.

    python3 tools/build.py

Two kinds of pages: hand-written ones in site/pages/** (with a <!--meta -->
block, same as hjärngympa) and generated ones from tools/holidays.py — the
year overview, klämdagar, skollov, month calendars and one page per named
day. Markup is deliberately plain: real <table>s, the answer in the first <p>,
FAQPage + Event JSON-LD. That is what gets a page quoted by Google's AI box.

ponytail: f-strings, no template engine. When the design handoff lands, only
the HTML fragments below and app.css change.
"""
import os, re, shutil, html as H, json, datetime as dt, sys
from string import Template

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools import holidays as hol

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE, DIST = os.path.join(ROOT, "site"), os.path.join(ROOT, "dist")
BASE_URL = os.environ.get("BASE_URL") or "https://ledigadagarna.se"
BASE_PATH = (os.environ.get("BASE_PATH") or "").rstrip("/")
CNAME = os.environ.get("CNAME") or "ledigadagarna.se"
SITE_NAME = "Lediga dagarna"
META_RE = re.compile(r"^<!--meta\s*(.*?)-->\s*", re.S)
OG_IMAGE = "/assets/og.png"
ADS_CLIENT = "ca-pub-2838730195714407"   # same AdSense account as hjärngympa
ADS_SLOT = "4551546102"                 # TODO: create a slot for this site
AD_RE = re.compile(r'<div class="ad ([^"]*)">[^<]*</div>')

TODAY = dt.date.today()
YEARS = [TODAY.year - 1, TODAY.year, TODAY.year + 1]
FIVE = list(range(TODAY.year, TODAY.year + 5))
SKOLLOV = json.load(open(os.path.join(SITE, "data/skollov.json"), encoding="utf-8"))

esc = H.escape
t = lambda d, **k: f'<time datetime="{d.isoformat()}">{hol.sv(d, **k)}</time>'


def mount_ads(page):
    return AD_RE.sub(lambda m: (
        f'<div class="ad {m.group(1)}"><ins class="adsbygoogle" style="display:block;width:100%;height:100%"'
        f' data-ad-client="{ADS_CLIENT}" data-ad-slot="{ADS_SLOT}" data-ad-format="auto"'
        f' data-full-width-responsive="true"></ins></div>'), page)


def jsonld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False, indent=1)}</script>'


def faq(pairs):
    return jsonld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]})


def days_until(d):
    n = (d - TODAY).days
    return "idag" if n == 0 else f"om {n} dagar" if n > 0 else f"för {-n} dagar sedan"


def year_switch(fmt):
    return '<nav class="seg" aria-label="År">' + "".join(
        f'<a href="{fmt.format(y)}"{" aria-current=page" if y == TODAY.year else ""}>{y}</a>' for y in YEARS) + "</nav>"


def red_table(y, klam):
    rows = "".join(
        f"<tr{' class=red' if h['red'] else ''}><td>{t(h['date'], with_year=False)}</td><td>v{hol.week(h['date'])}</td>"
        f"<td><a href=\"/{h['slug']}/\">{h['name']}</a></td>"
        f"<td>{'● röd dag' if h['red'] else 'ledig' if h['off'] else '—'}"
        f"{' · ◐ klämdag' if any(k['run'][0] <= h['date'] <= k['run'][1] for k in klam) and h['date'].weekday() < 5 else ''}</td></tr>"
        for h in hol.year(y))
    return ('<div class="tablewrap"><table><thead><tr><th>Datum</th><th>Vecka</th><th>Dag</th><th>Status</th></tr></thead>'
            f"<tbody>{rows}</tbody></table></div>")


# ------------------------------------------------------------------ pages
def page_year(y, is_home):
    days = hol.year(y); klam = hol.klamdagar(y)
    red = [h for h in days if h["red"]]
    weekday_red = [h for h in red if h["date"].weekday() < 5]
    nxt = next((h for h in days if h["off"] and h["date"] >= TODAY), None) if y == TODAY.year else None
    hero = (f'<section class="hero"><p class="mono">NÄSTA LEDIGA DAG · {days_until(nxt["date"]).upper()}</p>'
            f'<h2><a href="/{nxt["slug"]}/">{nxt["name"]}</a></h2><p class="date">{t(nxt["date"])}</p></section>') if nxt else ""
    body = f"""<div class="wrap cols"><div>
<div class="ad ad-320x100 mobile-ad">ANNONS 320×100</div>
<h1>Lediga dagar {y}</h1>
<p>Under {y} har Sverige {len(red)} röda dagar, varav {len(weekday_red)} infaller på en vardag.
Det finns {len(klam)} klämdagar. Nedan finns alla helgdagar, aftnar och märkesdagar med datum och veckonummer.</p>
{hero}
{year_switch("/{}/")}
<div class="ad ad-728x90 desktop-ad">ANNONS 728×90</div>
<h2>Alla röda dagar och helger {y}</h2>
{red_table(y, klam)}
<div class="ad ad-336x280">ANNONS 336×280</div>
<h2>Klämdagar {y}</h2>
<p>{"Ingen klämdag i år." if not klam else f'Ta {len(klam)} semesterdagar och få {sum(k["days"] for k in klam)} lediga dagar.'}
<a href="/klamdagar/{y}/">Se alla klämdagar {y} →</a></p>
<h2>Skollov {y}</h2>
<p>Sportlov, påsklov, sommarlov, höstlov och jullov per region. <a href="/skollov/{y}/">Se skollov {y} →</a></p>
<h2>Kalender {y}</h2>
<p class="months">{" · ".join(f'<a href="/kalender/{y}/{m+1}/">{hol.MONTHS[m]}</a>' for m in range(12))}</p>
</div><aside><div class="ad ad-300x600 desktop-ad">ANNONS 300×600</div></aside></div>"""
    return {"route": "/" if is_home else f"/{y}/", "title": f"Lediga dagar {y} – alla röda dagar, klämdagar och lov",
            "desc": f"Alla röda dagar {y} med veckonummer, klämdagar och skollov. {len(red)} helgdagar, {len(klam)} klämdagar.",
            "priority": "1.0" if is_home else "0.9", "body": body}


def page_klam(y):
    klam = hol.klamdagar(y)
    def strip(k):
        a, b = k["run"]; d = a - dt.timedelta(1); cells = []
        while d <= b + dt.timedelta(1):
            cls = "take" if d == k["date"] else "off" if a <= d <= b else "work"
            cells.append(f'<span class="tile {cls}" title="{hol.sv(d)}">{hol.WEEKDAYS[d.weekday()][:2]}</span>')
            d += dt.timedelta(1)
        return f'<div class="strip" aria-label="{hol.sv(a)} till {hol.sv(b)}">{"".join(cells)}</div>'
    rows = "".join(f'<tr><td>{t(k["date"])}</td><td>{strip(k)}</td><td>Ta 1 dag → {k["days"]} dagar lediga ({hol.sv(k["run"][0], with_year=False)}–{hol.sv(k["run"][1], with_year=False)})</td></tr>' for k in klam)
    body = f"""<div class="wrap cols"><div>
<div class="ad ad-320x100 mobile-ad">ANNONS 320×100</div>
<h1>Klämdagar {y}</h1>
<p>{f"Med {len(klam)} semesterdagar får du {sum(k['days'] for k in klam)} lediga dagar {y}." if klam else f"{y} har inga klämdagar."}
En klämdag är en vardag mellan en röd dag och en helg.</p>
{year_switch("/klamdagar/{}/")}
<div class="tablewrap"><table><thead><tr><th>Klämdag</th><th>Så blir det</th><th>Utfall</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class="ad ad-336x280">ANNONS 336×280</div>
<p><a href="/{y}/">Alla lediga dagar {y} →</a></p>
</div><aside><div class="ad ad-300x600 desktop-ad">ANNONS 300×600</div></aside></div>"""
    return {"route": f"/klamdagar/{y}/", "title": f"Klämdagar {y} – så får du flest lediga dagar",
            "desc": f"Alla klämdagar {y} och hur många lediga dagar varje semesterdag ger.", "priority": "0.9", "body": body}


def page_skollov(y):
    data = SKOLLOV.get(str(y))
    if not data: return None
    regions = SKOLLOV["regions"]; lov = ["sportlov", "pasklov", "sommarlov", "hostlov", "jullov"]
    names = {"sportlov": "Sportlov", "pasklov": "Påsklov", "sommarlov": "Sommarlov", "hostlov": "Höstlov", "jullov": "Jullov"}
    fmt = lambda v: f"v{v}" if isinstance(v, int) else v
    rows = "".join(f"<tr><th>{names[l]}</th>" + "".join(f"<td>{fmt(data[r][l])}</td>" for r in regions) + "</tr>" for l in lov)
    body = f"""<div class="wrap cols"><div>
<div class="ad ad-320x100 mobile-ad">ANNONS 320×100</div>
<h1>Skollov {y}</h1>
<p>Sportlov, påsklov, sommarlov, höstlov och jullov {y} per region, angivet i veckonummer.</p>
{year_switch("/skollov/{}/")}
<div class="tablewrap"><table><thead><tr><th>Lov</th>{"".join(f"<th>{n}</th>" for n in regions.values())}</tr></thead><tbody>{rows}</tbody></table></div>
<p class="small">Sportlov och höstlov följer länet. Påsklov och terminsgränser bestäms av varje kommun — kontrollera alltid mot din skolas läsårsplan.</p>
<div class="ad ad-336x280">ANNONS 336×280</div>
</div><aside><div class="ad ad-300x600 desktop-ad">ANNONS 300×600</div></aside></div>"""
    return {"route": f"/skollov/{y}/", "title": f"Skollov {y} – sportlov, påsklov, höstlov per region",
            "desc": f"Veckor för sportlov, påsklov, sommarlov, höstlov och jullov {y} i Stockholm, Göteborg, Skåne och övriga landet.",
            "priority": "0.8", "body": body}


def page_month(y, m):
    off = {h["date"]: h for h in hol.year(y)}; klam = {k["date"] for k in hol.klamdagar(y)}
    first = dt.date(y, m, 1); d = first - dt.timedelta(first.weekday()); rows = []
    while (d.year, d.month) <= (y, m):
        cells = [f'<th class="wk">v{hol.week(d)}</th>']
        for i in range(7):
            x = d + dt.timedelta(i); h = off.get(x) if x.month == m else None
            flags = [("other", x.month != m), ("red", bool(h and h["red"])), ("klam", x in klam),
                     ("today", x == TODAY), ("wknd", x.weekday() >= 5)]
            cls = " ".join(c for c, ok in flags if ok)
            label = f'<span class="label">{h["name"]}</span>' if h else ""
            cells.append(f'<td class="{cls}"><span class="n">{x.day}</span>{label}</td>')
        rows.append("<tr>" + "".join(cells) + "</tr>"); d += dt.timedelta(7)
    prev_m, next_m = (y, m - 1) if m > 1 else (y - 1, 12), (y, m + 1) if m < 12 else (y + 1, 1)
    body = f"""<div class="wrap cols"><div>
<div class="ad ad-320x100 mobile-ad">ANNONS 320×100</div>
<h1>Kalender {hol.MONTHS[m-1]} {y}</h1>
<p>Kalender för {hol.MONTHS[m-1]} {y} med veckonummer, röda dagar (●) och klämdagar (◐).</p>
<nav class="seg"><a href="/kalender/{prev_m[0]}/{prev_m[1]}/">‹ {hol.MONTHS[prev_m[1]-1]}</a><a href="/{y}/">{y}</a><a href="/kalender/{next_m[0]}/{next_m[1]}/">{hol.MONTHS[next_m[1]-1]} ›</a></nav>
<div class="tablewrap"><table class="cal"><thead><tr><th></th>{"".join(f"<th>{w[:3]}</th>" for w in hol.WEEKDAYS)}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>
<div class="ad ad-336x280">ANNONS 336×280</div>
</div><aside><div class="ad ad-300x600 desktop-ad">ANNONS 300×600</div></aside></div>"""
    return {"route": f"/kalender/{y}/{m}/", "title": f"Kalender {hol.MONTHS[m-1]} {y} med veckonummer och röda dagar",
            "desc": f"Månadskalender {hol.MONTHS[m-1]} {y}: veckonummer, helgdagar och klämdagar.", "priority": "0.5", "body": body}


def page_day(slug):
    name, red, fn = hol.DAYS[slug]; d = fn(TODAY.year); dn = fn(TODAY.year + 1)
    status = "en röd dag" if red else "ingen röd dag" + (" men ledig hos de flesta arbetsgivare" if slug in hol.DE_FACTO_OFF else "")
    answer = f"{name} {TODAY.year} infaller {hol.sv(d)} (vecka {hol.week(d)}) och är {status}."
    faqs = [(f"Är {name.lower()} en röd dag?", f"{name} är {status}."),
            (f"Vilken vecka är {name.lower()} {TODAY.year}?", f"Vecka {hol.week(d)}, {hol.sv(d)}."),
            (f"När är {name.lower()} {TODAY.year + 1}?", f"{hol.sv(dn).capitalize()}.")]
    rows = "".join(f"<tr><td>{y}</td><td>{t(fn(y))}</td><td>v{hol.week(fn(y))}</td></tr>" for y in FIVE)
    body = f"""<div class="wrap cols"><div>
<h1>{name} {TODAY.year}</h1>
<p>{answer}</p>
<div class="ad ad-320x100 mobile-ad">ANNONS 320×100</div>
<p class="mono">{days_until(d).upper()}</p>
<div class="tablewrap"><table><thead><tr><th>År</th><th>{name}</th><th>Vecka</th></tr></thead><tbody>{rows}</tbody></table></div>
{"".join(f"<h2>{q}</h2><p>{a}</p>" for q, a in faqs)}
<div class="ad ad-336x280">ANNONS 336×280</div>
<p><a href="/{TODAY.year}/">Alla lediga dagar {TODAY.year} →</a> · <a href="/klamdagar/{TODAY.year}/">Klämdagar →</a></p>
</div><aside><div class="ad ad-300x600 desktop-ad">ANNONS 300×600</div></aside></div>"""
    head = faq(faqs) + jsonld({"@context": "https://schema.org", "@type": "Event", "name": f"{name} {TODAY.year}",
                                "startDate": d.isoformat(), "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
                                "eventStatus": "https://schema.org/EventScheduled", "location": {"@type": "Country", "name": "Sverige"}})
    return {"route": f"/{slug}/", "title": f"{name} {TODAY.year} – datum, vecka och röd dag?", "desc": answer,
            "priority": "0.8", "body": body, "head": head}


def page_group(slug):
    name, members = hol.GROUPS[slug]
    def line(y):
        return ", ".join(f"{hol.DAYS[m][0].lower()} {hol.sv(hol.DAYS[m][2](y), with_year=False)}" for m in members)
    answer = f"{name} {TODAY.year}: {line(TODAY.year)}."
    faqs = [(f"När är {name.lower()} {TODAY.year}?", answer), (f"När är {name.lower()} {TODAY.year + 1}?", f"{name} {TODAY.year + 1}: {line(TODAY.year + 1)}.")]
    rows = "".join(f"<tr><td>{y}</td>" + "".join(f"<td>{t(hol.DAYS[m][2](y), with_year=False)}</td>" for m in members) + "</tr>" for y in FIVE)
    body = f"""<div class="wrap cols"><div>
<h1>{name} {TODAY.year}</h1>
<p>{answer}</p>
<div class="ad ad-320x100 mobile-ad">ANNONS 320×100</div>
<div class="tablewrap"><table><thead><tr><th>År</th>{"".join(f"<th>{hol.DAYS[m][0]}</th>" for m in members)}</tr></thead><tbody>{rows}</tbody></table></div>
{"".join(f"<h2>{q}</h2><p>{a}</p>" for q, a in faqs)}
<p>{" · ".join(f'<a href="/{m}/">{hol.DAYS[m][0]}</a>' for m in members)}</p>
<div class="ad ad-336x280">ANNONS 336×280</div>
<p><a href="/{TODAY.year}/">Alla lediga dagar {TODAY.year} →</a></p>
</div><aside><div class="ad ad-300x600 desktop-ad">ANNONS 300×600</div></aside></div>"""
    return {"route": f"/{slug}/", "title": f"{name} {TODAY.year} – alla datum", "desc": answer, "priority": "0.9", "body": body, "head": faq(faqs)}


def generated():
    pages = [page_year(TODAY.year, True)] + [page_year(y, False) for y in YEARS]
    pages += [page_klam(y) for y in YEARS] + [page_skollov(y) for y in YEARS]
    pages += [page_month(y, m) for y in YEARS for m in range(1, 13)]
    pages += [page_day(s) for s in hol.DAYS] + [page_group(s) for s in hol.GROUPS]
    return [p for p in pages if p]


def file_pages():
    base = os.path.join(SITE, "pages")
    for dirpath, _, files in os.walk(base):
        for fn in files:
            if not fn.endswith(".html"): continue
            raw = open(os.path.join(dirpath, fn), encoding="utf-8").read()
            m = META_RE.match(raw); meta = {}
            if m:
                meta = dict(l.split(":", 1) for l in m.group(1).strip().splitlines() if ":" in l)
                meta = {k.strip(): v.strip() for k, v in meta.items()}
            rel = os.path.dirname(os.path.relpath(os.path.join(dirpath, fn), base))
            yield {"route": "/" + (rel + "/" if rel else ""), "body": raw[m.end():] if m else raw, **meta}


def main():
    if not BASE_URL.startswith(("http://", "https://")):
        raise SystemExit(f"BASE_URL must be absolute, got {BASE_URL!r}")
    layout = Template(open(os.path.join(SITE, "_layout.html"), encoding="utf-8").read())
    if os.path.exists(DIST): shutil.rmtree(DIST)
    os.makedirs(DIST); routes = []
    for p in list(file_pages()) + generated():
        out = os.path.join(DIST, p["route"].strip("/"), "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        page = layout.safe_substitute(
            basepath=BASE_PATH, title=esc(p.get("title", SITE_NAME)), desc=esc(p.get("desc", "")),
            canonical=BASE_URL + BASE_PATH + p["route"], image=BASE_URL + BASE_PATH + p.get("image", OG_IMAGE),
            bodyclass=p.get("bodyclass", ""), head=p.get("head", ""), body=p["body"])
        page = mount_ads(page)
        if BASE_PATH:
            page = page.replace('href="/', f'href="{BASE_PATH}/').replace('src="/', f'src="{BASE_PATH}/')
        open(out, "w", encoding="utf-8").write(page)
        routes.append((p["route"], p.get("priority", "0.7")))
    shutil.copytree(os.path.join(SITE, "assets"), os.path.join(DIST, "assets"))
    if BASE_PATH:
        for dirpath, _, files in os.walk(os.path.join(DIST, "assets")):
            for fn in files:
                if fn.endswith(".css"):
                    f = os.path.join(dirpath, fn); css = open(f, encoding="utf-8").read()
                    open(f, "w", encoding="utf-8").write(css.replace("url(/assets/", f"url({BASE_PATH}/assets/"))
    today = TODAY.isoformat()
    open(os.path.join(DIST, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(f"  <url><loc>{BASE_URL}{BASE_PATH}{r}</loc><lastmod>{today}</lastmod><priority>{p}</priority></url>" for r, p in sorted(routes))
        + "\n</urlset>\n")
    open(os.path.join(DIST, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}{BASE_PATH}/sitemap.xml\n")
    open(os.path.join(DIST, "ads.txt"), "w").write(f"google.com, {ADS_CLIENT.replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n")
    open(os.path.join(DIST, ".nojekyll"), "w").close()
    if CNAME and not BASE_PATH: open(os.path.join(DIST, "CNAME"), "w").write(CNAME + "\n")
    print(f"built {len(routes)} pages -> {DIST}")


if __name__ == "__main__":
    main()
