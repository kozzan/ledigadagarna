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
from tools import copy as C

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
    """Fill sized placeholders with fixed-size <ins>. Fixed, not data-ad-format=auto:
    auto lets AdSense grow the slot to 280px and shift the page."""
    def rep(m):
        size = re.search(r"ad-(\d+)x(\d+)", m.group(1))
        w, h = size.groups()
        return (f'<div class="ad {m.group(1)}"><ins class="adsbygoogle" style="display:inline-block;width:{w}px;height:{h}px"'
                f' data-ad-client="{ADS_CLIENT}" data-ad-slot="{ADS_SLOT}"></ins></div>')
    return AD_RE.sub(rep, page)


def jsonld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False, indent=1)}</script>'


def faq(pairs):
    return jsonld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]})


def days_until(d):
    n = (d - TODAY).days
    return "idag" if n == 0 else f"om {n} dagar" if n > 0 else f"för {-n} dagar sedan"


def year_switch(fmt, y):
    return '<nav class="seg" aria-label="År">' + "".join(
        f'<a href="{fmt.format(x)}"{" aria-current=page" if x == y else ""}>{x}</a>' for x in YEARS) + "</nav>"


def caption(txt):
    return f'<caption class="vh">{txt}</caption>'


def dot(h):
    return '<span class="rod" aria-hidden="true">●</span> ' if h["red"] else ""


def red_table(y, klam):
    bridge_days = {d for k in klam for d in k["take"]}
    def klam_for(h):
        nxt = h["date"] + dt.timedelta(1); prv = h["date"] - dt.timedelta(1)
        if nxt in bridge_days: return f"◐ Klämdag {hol.WEEKDAYS[nxt.weekday()][:3]}"
        if prv in bridge_days: return f"◐ Klämdag {hol.WEEKDAYS[prv.weekday()][:3]}"
        return ""
    rows = []
    for h in hol.year(y):
        d = h["date"]; k = klam_for(h)
        status = "Röd dag" if h["red"] else "Ledig" if h["off"] else "Märkesdag"
        sub = " · ".join(x for x in [hol.WEEKDAYS[d.weekday()].capitalize(), f"V. {hol.week(d)}", k] if x)
        rows.append(
            f'<tr><td><a class="name" href="/{h["slug"]}/">{h["name"]}</a><span class="sub meta m">{sub}</span></td>'
            f'<td class="d">{hol.WEEKDAYS[d.weekday()].capitalize()}</td>'
            f'<td class="datum">{dot(h)}<time datetime="{d.isoformat()}">{d.day} {hol.MONTHS[d.month-1][:3]}</time></td>'
            f'<td class="d">V. {hol.week(d)}</td><td class="d">{status}</td>'
            f'<td class="d">{f"<span class=pill>{k}</span>" if k else "<span class=none>—</span>"}</td></tr>')
    return (f'<table>{caption(f"Röda dagar och helger {y}")}<thead><tr><th scope="col">Helgdag</th><th scope="col" class="d">Veckodag</th>'
            f'<th scope="col" class="datum">Datum</th><th scope="col" class="d">Vecka</th><th scope="col" class="d">Typ</th><th scope="col" class="d">Klämdag</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table>')


def sidebar(y, extra="", ads=True):
    ad = '<div class="ad ad-300x600 desktop-ad">Annons 300×600</div>' if ads else ""
    return (f'<aside><div class="sticky">{ad}'
            f'<div class="quick"><p class="meta">Snabblänkar</p><a href="/klamdagar/{y}/">Klämdagar {y}</a>'
            f'<a href="/kalender/{y}/{max(TODAY.month if y == TODAY.year else 1, 1)}/">Kalender {hol.MONTHS[(TODAY.month if y == TODAY.year else 1) - 1]} {y}</a>'
            f'<a href="/{y + 1}/">Röda dagar {y + 1}</a><a href="/skollov/{y}/">Skollov {y}</a>{extra}</div></div></aside>')


def stats(red, weekday_red, klam, cls=""):
    return (f'<div class="stats {cls}"><div><b>{len(red)}</b><span>Röda dagar</span></div><div><b>{len(weekday_red)}</b><span>På vardagar</span></div>'
            f'<div><b>{len(klam)}</b><span>Klämdagar</span></div></div>')


def named_list(y):
    return '<div class="list2">' + "".join(f'<a href="/{h["slug"]}/">{h["name"]}</a>' for h in hol.year(y)) + "</div>"


# ------------------------------------------------------------------ pages
def page_year(y):
    days = hol.year(y); klam = hol.klamdagar(y)
    red = [h for h in days if h["red"]]; weekday_red = [h for h in red if h["date"].weekday() < 5]
    nxt = next((h for h in days if h["red"] and h["date"] >= TODAY), None) if y == TODAY.year else (red[0] if y > TODAY.year else None)
    hero = ""
    if nxt:
        d = nxt["date"]
        hero = (f'<section class="hero"><div class="num" aria-hidden="true">{d.day}</div><div>'
                f'<p class="meta">Nästa röda dag <span class="rod">●</span></p><p class="name"><a href="/{nxt["slug"]}/">{nxt["name"]}</a></p>'
                f'<p class="meta"><time datetime="{d.isoformat()}">{hol.WEEKDAYS[d.weekday()]} {d.day} {hol.MONTHS[d.month-1]}</time><br>'
                f'V. {hol.week(d)} · <span data-countdown="{d.isoformat()}">{days_until(d)}</span></p></div>{stats(red, weekday_red, klam)}</section>')
    body = f"""<div class="wrap cols"><div>
<h1>Lediga dagar {y}</h1>
<p>Under {y} har Sverige {len(red)} röda dagar, varav {len(weekday_red)} infaller på en vardag. Med rätt {len(klam)} klämdagar blir det betydligt fler lediga dagar. Alla datum nedan, med veckonummer.</p>
<div class="ad ad-728x90 desktop-ad">Annons 728×90</div>
{hero}
<div class="ad ad-320x100 mobile-ad">Annons 320×100</div>
{year_switch("/{}/", y)}
<h2>Alla röda dagar {y}</h2>
<div class="tablewrap">{red_table(y, klam)}</div>
{stats(red, weekday_red, klam, "mobile")}
<div class="ad ad-336x280 desktop-ad">Annons 336×280</div>
<h2>Klämdagar {y}</h2>
<p>{f'Ta {sum(len(k["take"]) for k in klam)} semesterdagar och få {sum(k["days"] for k in klam)} lediga dagar.' if klam else "Inga klämdagar i år."} <a href="/klamdagar/{y}/">Se alla klämdagar {y} →</a></p>
<h2>Skollov {y}</h2>
<p>Sportlov, påsklov, sommarlov, höstlov och jullov. <a href="/skollov/{y}/">Se alla lov för din region →</a></p>
{C.HUB["year"].format(y=y)}
<div class="ad ad-300x250 mobile-ad">Annons 300×250</div>
<h2>Namngivna dagar {y}</h2>
{named_list(y)}
<h2>Kalender {y}</h2>
{months_grid(y)}
</div>{sidebar(y)}</div>"""
    return {"route": f"/{y}/", "title": f"Lediga dagar {y} – alla röda dagar, klämdagar och lov",
            "desc": f"Alla röda dagar {y} med veckonummer, klämdagar och skollov. {len(red)} helgdagar, {len(klam)} klämdagar.",
            "priority": "0.9", "body": body}


def page_home():
    """Its own page, not a copy of /<year>/: what's next from today. Rebuilt daily by the deploy cron."""
    y = TODAY.year
    ahead = [h for yy in (y, y + 1) for h in hol.year(yy) if h["off"] and h["date"] >= TODAY][:8]
    nxt_red = next(h for yy in (y, y + 1) for h in hol.year(yy) if h["red"] and h["date"] >= TODAY)
    klam = next((k for yy in (y, y + 1) for k in hol.klamdagar(yy) if k["take"][0] >= TODAY), None)
    d = nxt_red["date"]; hv = SKOLLOV["hostlov"]
    rows = "".join(
        f'<tr><td><a class="name" href="/{h["slug"]}/">{h["name"]}</a></td>'
        f'<td class="datum">{dot(h)}<time datetime="{h["date"].isoformat()}">{hol.WEEKDAYS[h["date"].weekday()][:3]} {h["date"].day} {hol.MONTHS[h["date"].month-1][:3]} {h["date"].year}</time></td>'
        f'<td class="d">V. {hol.week(h["date"])}</td><td class="d"><span data-countdown="{h["date"].isoformat()}">{days_until(h["date"])}</span></td></tr>'
        for h in ahead)
    if klam:
        takes = " + ".join(f"{hol.WEEKDAYS[x.weekday()]} {x.day} {hol.MONTHS[x.month-1]}" for x in klam["take"])
        klam_p = (f'<p>Nästa klämdag: ta ledigt {takes} {klam["take"][0].year} (vecka {hol.week(klam["take"][0])}) och få '
                  f'{klam["days"]} lediga dagar i rad för {len(klam["take"])} semesterdag{"ar" if len(klam["take"]) > 1 else ""}. '
                  f'<a href="/klamdagar/{klam["take"][0].year}/">Alla klämdagar {klam["take"][0].year} →</a></p>')
    else:
        klam_p = ""
    hl_end = week_range(y, hv)[1]
    lov_p = (f'<p>Höstlovet {y} är vecka {hv}, {wk(y, hv)}, i hela landet. Därefter kommer jullovet och sportlovet {y + 1}, '
             f'som ligger vecka 7–10 beroende på län. <a href="/skollov/{y}/">Skollov {y} per län →</a></p>' if TODAY <= hl_end else
             f'<p>Nästa lov med fast vecka är sportlovet {y + 1}, vecka 7–10 beroende på län. Höstlovet {y + 1} är vecka {hv}. '
             f'<a href="/skollov/{y + 1}/">Skollov {y + 1} per län →</a></p>')
    def yr(x):
        red = [h for h in hol.year(x) if h["red"]]; k = hol.klamdagar(x)
        return (f'<tr><th scope="row"><a href="/{x}/">{x}</a></th><td class="datum">{len(red)}</td>'
                f'<td class="d">{sum(h["date"].weekday() < 5 for h in red)}</td><td class="d"><a href="/klamdagar/{x}/">{len(k)}</a></td></tr>')
    body = f"""<div class="wrap cols"><div>
<h1>När är jag ledig nästa gång?</h1>
<p>Nästa röda dag är {nxt_red["name"].lower()}, {t(d)} (vecka {hol.week(d)}), <span data-countdown="{d.isoformat()}">{days_until(d)}</span>. Just nu är det vecka {hol.week(TODAY)}.</p>
<div class="ad ad-728x90 desktop-ad">Annons 728×90</div>
<div class="ad ad-320x100 mobile-ad">Annons 320×100</div>
<h2>Kommande lediga dagar</h2>
<div class="tablewrap"><table>{caption("De närmaste lediga dagarna")}<thead><tr><th scope="col">Dag</th><th scope="col" class="datum">Datum</th><th scope="col" class="d">Vecka</th><th scope="col" class="d">När</th></tr></thead><tbody>{rows}</tbody></table></div>
<h2>Nästa klämdag</h2>
{klam_p}
<h2>Nästa skollov</h2>
{lov_p}
<div class="ad ad-336x280 desktop-ad">Annons 336×280</div>
<div class="ad ad-300x250 mobile-ad">Annons 300×250</div>
<h2>År för år</h2>
<div class="tablewrap"><table>{caption("Röda dagar och klämdagar per år")}<thead><tr><th scope="col">År</th><th scope="col" class="datum">Röda dagar</th><th scope="col" class="d">På vardagar</th><th scope="col" class="d">Klämdagar</th></tr></thead><tbody>{"".join(yr(x) for x in YEARS)}</tbody></table></div>
{C.HOME.format(y=y)}
</div>{sidebar(y)}</div>"""
    return {"route": "/", "title": "Lediga dagar – nästa röda dag, klämdag och lov",
            "desc": f"Nästa röda dag är {nxt_red['name'].lower()} {hol.sv(d)}. Kommande lediga dagar, nästa klämdag och nästa skollov, alltid räknat från idag.",
            "priority": "1.0", "body": body}


def tile(d, y_off, take, red_dates, klam_dates):
    cls = "tagen" if d in take else "rod" if d in red_dates else "klam" if d in klam_dates else "helg" if d in y_off else ""
    glyph = {"tagen": " ◑", "rod": " ●", "klam": " ◐"}.get(cls, "")
    return f'<span class="dag {cls}" title="{hol.sv(d)}"><i>{hol.WEEKDAYS[d.weekday()][0].upper()}{glyph}</i><b>{d.day}</b></span>'


def page_klam(y):
    klam = hol.klamdagar(y); off = hol.off_days(y - 1) | hol.off_days(y) | hol.off_days(y + 1)
    red_dates = {h["date"] for yy in (y - 1, y, y + 1) for h in hol.year(yy) if h["red"]}
    afton = {h["date"] for yy in (y - 1, y, y + 1) for h in hol.year(yy) if h["off"] and not h["red"]}
    names = {h["date"]: h["name"] for yy in (y - 1, y, y + 1) for h in hol.year(yy)}
    def row(k):
        a, b = k["run"]; n = (b - a).days + 1
        holiday = next((names[x] for x in sorted(names) if a <= x <= b and x in names and (x in red_dates or x in afton)), "")
        cells = "".join(tile(a + dt.timedelta(i), off, set(k["take"]), red_dates, set()) for i in range(n))
        takes = " + ".join(f"{hol.WEEKDAYS[t.weekday()][:3]} {t.day} {hol.MONTHS[t.month-1][:3]}" for t in k["take"])
        return (f'<article class="bridge"><p class="meta">{takes} · V. {hol.week(k["date"])}{" · " + holiday if holiday else ""}</p>'
                f'<p class="pay">Ta {len(k["take"])} dag{"ar" if len(k["take"]) > 1 else ""} ledigt <span class="arr">→</span> {k["days"]} dagar lediga</p>'
                f'<div class="strip n{n}" style="grid-template-columns:repeat({n},1fr)">{cells}</div>'
                f'<p class="meta">{hol.WEEKDAYS[a.weekday()][:3]} {a.day} {hol.MONTHS[a.month-1][:3]} – {hol.WEEKDAYS[b.weekday()][:3]} {b.day} {hol.MONTHS[b.month-1][:3]}</p></article>')
    take_n, free_n = sum(len(k["take"]) for k in klam), sum(k["days"] for k in klam)
    body = f"""<div class="wrap cols"><div>
<h1>Klämdagar {y}</h1>
<p>En klämdag är en vardag inklämd mellan en röd dag och en helg. Här är varje tillfälle {y} och exakt hur många lediga dagar du får för varje semesterdag du tar.</p>
<div class="ad ad-728x90 desktop-ad">Annons 728×90</div>
<section class="hero"><div class="total"><div><b>{take_n}</b><span>Semesterdagar</span></div><span class="arr">→</span><div><b>{free_n}</b><span>Lediga dagar</span></div></div></section>
<div class="ad ad-320x100 mobile-ad">Annons 320×100</div>
{year_switch("/klamdagar/{}/", y)}
<div class="legend"><span><span class="sw rod"></span>● Röd dag</span><span><span class="sw klam"></span>◐ Klämdag</span><span><span class="sw helg"></span>Ledig</span><span><span class="sw"></span>Arbetsdag</span><span><span class="sw tagen"></span>◑ Dagen du tar ledigt</span></div>
{"".join(row(k) for k in klam) if klam else "<p>Inga klämdagar detta år.</p>"}
{C.HUB["klamdagar"]}
<div class="ad ad-336x280 desktop-ad">Annons 336×280</div>
<div class="ad ad-300x250 mobile-ad">Annons 300×250</div>
<div class="links"><a href="/{y}/">Alla lediga dagar {y} →</a><a href="/skollov/{y}/">Skollov {y} →</a></div>
</div>{sidebar(y)}</div>"""
    return {"route": f"/klamdagar/{y}/", "title": f"Klämdagar {y} – så får du flest lediga dagar",
            "desc": f"Alla klämdagar {y}: ta {take_n} semesterdagar och få {free_n} lediga dagar. Datum, veckor och exakt utfall.", "priority": "0.9", "body": body}


def week_range(y, w):
    """ISO week w of year y -> (monday, sunday)."""
    mon = dt.date.fromisocalendar(y, w, 1)
    return mon, mon + dt.timedelta(6)


def wk(y, w):
    a, b = week_range(y, w)
    return f'<time datetime="{a.isoformat()}">{a.day} {hol.MONTHS[a.month-1][:3]}</time>–<time datetime="{b.isoformat()}">{b.day} {hol.MONTHS[b.month-1][:3]}</time>'


def lov_faq_note():
    return ('<p class="small">Sportlov och höstlov är fasta veckor per län. Påsklov, sommarlov och jullov '
            'bestäms av varje kommun — de datumen hittar du i din skolas läsårsplan.</p>')


def page_skollov(y):
    L = SKOLLOV["lan"]; hv = SKOLLOV["hostlov"]
    rows = "".join(
        f'<tr id="{k}"><th scope="row"><span class="name">{v["namn"]}</span><span class="sub meta m">Höstlov v. {hv}</span>'
        f'{f"""<span class="sub meta">{v['not']}</span>""" if v.get("not") else ""}</th>'
        f'<td class="datum">V. {v["sportlov"]}</td><td class="d">{wk(y, v["sportlov"])}</td><td class="d">V. {hv}</td><td class="d">{wk(y, hv)}</td></tr>'
        for k, v in sorted(L.items(), key=lambda kv: (kv[1]["sportlov"], kv[1]["namn"])))
    by_week = {}
    for v in L.values(): by_week.setdefault(v["sportlov"], []).append(v["namn"])
    summary = " ".join(f"Vecka {w}: {', '.join(sorted(ns))}." for w, ns in sorted(by_week.items()))
    span = lambda yy, w: f"{hol.sv(week_range(yy, w)[0])} – {hol.sv(week_range(yy, w)[1])}"
    faqs = [(f"Vilken vecka är höstlovet {y}?", f"Vecka {hv}, {span(y, hv)}, i hela landet.")]
    faqs += [(f"Vilka län har sportlov vecka {w} {y}?", f"{', '.join(sorted(ns))}: {span(y, w)}.") for w, ns in sorted(by_week.items())]
    faqs += [(f"När är sportlovet {y} i Stockholm?", f"Vecka {L['stockholm']['sportlov']}, {span(y, L['stockholm']['sportlov'])}.")]
    body = f"""<div class="wrap cols"><div>
<h1>Skollov {y}</h1>
<p>Sportlovet {y} infaller vecka 7–10 beroende på län. {summary} Höstlovet är vecka {hv} i hela landet ({span(y, hv)}).</p>
<div class="ad ad-728x90 desktop-ad">Annons 728×90</div>
<div class="ad ad-320x100 mobile-ad">Annons 320×100</div>
{year_switch("/skollov/{}/", y)}
<div class="tablewrap"><table>{caption(f"Sportlov och höstlov {y} per län")}<thead><tr><th scope="col">Län</th><th scope="col" class="datum">Sportlov</th><th scope="col" class="d">Datum</th><th scope="col" class="d">Höstlov</th><th scope="col" class="d">Datum</th></tr></thead><tbody>{rows}</tbody></table></div>
{lov_faq_note()}
{C.HUB["skollov"].format(y=y)}
<div class="ad ad-336x280 desktop-ad">Annons 336×280</div>
<div class="ad ad-300x250 mobile-ad">Annons 300×250</div>
<div class="faq">{"".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in faqs)}</div>
<div class="links"><a href="/{y}/">Alla lediga dagar {y} →</a><a href="/klamdagar/{y}/">Klämdagar {y} →</a></div>
</div>{sidebar(y)}</div>"""
    return {"route": f"/skollov/{y}/", "title": f"Sportlov och höstlov {y} – vecka och datum för alla län",
            "desc": f"Sportlov {y} vecka för vecka i alla 21 län, och höstlov vecka {hv}. Datum och veckonummer.", "priority": "0.8",
            "body": body, "head": faq(faqs)}


def moved(route, to):
    """ponytail: GitHub Pages has no 301s; an instant meta refresh + canonical is what Google treats as one."""
    return {"route": route, "redirect": to}


def day_state(x, m, y, names, klam_dates):
    h = names.get(x)
    if x.month != m: return "utanfor"
    if (h and h["red"]) or x.weekday() == 6: return "rod"
    if x in klam_dates: return "klam"
    if x.weekday() == 5 or (h and h["off"]): return "helg"
    return ""


def month_cells(y, m, names, klam_dates, mini=False):
    first = dt.date(y, m, 1); d = first - dt.timedelta(first.weekday()); out = []
    while (d.year, d.month) <= (y, m):
        if not mini:
            out.append(f'<div class="wk{" now" if hol.week(d) == hol.week(TODAY) and y == TODAY.year else ""}">{hol.week(d)}</div>')
        for i in range(7):
            x = d + dt.timedelta(i); st = day_state(x, m, y, names, klam_dates); h = names.get(x) if x.month == m else None
            if mini:
                out.append(f'<span class="{st or ""}{" e" if st == "utanfor" else ""}">{x.day if x.month == m else ""}</span>')
            else:
                glyph = " ●" if st == "rod" and h else " ◐" if st == "klam" else ""
                out.append(f'<div class="{st}" data-date="{x.isoformat()}"><span class="n">{x.day}{glyph}</span>'
                           f'{f"<span class=label>{h[chr(110)+chr(97)+chr(109)+chr(101)]}</span>" if h and x.month == m else ""}</div>')
        d += dt.timedelta(7)
    return "".join(out)


def months_grid(y):
    names = {h["date"]: h for h in hol.year(y)}; klam_dates = {d for k in hol.klamdagar(y) for d in k["take"]}
    return '<div class="months">' + "".join(
        f'<a class="mini" href="/kalender/{y}/{m}/"><div class="t">{hol.MONTHS[m-1].capitalize()}</div><div class="g">{month_cells(y, m, names, klam_dates, mini=True)}</div></a>'
        for m in range(1, 13)) + "</div>"


def page_month(y, m):
    names = {h["date"]: h for h in hol.year(y)}; klam_dates = {d for k in hol.klamdagar(y) for d in k["take"]}
    prev_m, next_m = ((y, m - 1) if m > 1 else (y - 1, 12)), ((y, m + 1) if m < 12 else (y + 1, 1))
    heads = '<div class="h"></div>' + "".join(f'<div class="h">{w[:3]}</div>' for w in hol.WEEKDAYS)
    in_month = [h for h in hol.year(y) if h["date"].month == m]
    body = f"""<div class="wrap cols"><div>
<h1>Kalender {hol.MONTHS[m-1]} {y}</h1>
<p>Månadskalender för {hol.MONTHS[m-1]} {y} med veckonummer, röda dagar (●) och klämdagar (◐).{" " + "; ".join(f"{h['name']} {hol.WEEKDAYS[h['date'].weekday()]} {h['date'].day} {hol.MONTHS[m-1]}" for h in in_month) + "." if in_month else ""}</p>
<nav class="monthnav" aria-label="Månad"><a href="/kalender/{prev_m[0]}/{prev_m[1]}/">← {hol.MONTHS[prev_m[1]-1].capitalize()}</a><a href="/{y}/">Hela {y}</a><a href="/kalender/{next_m[0]}/{next_m[1]}/">{hol.MONTHS[next_m[1]-1].capitalize()} →</a></nav>
<div class="kal" role="grid" aria-label="{hol.MONTHS[m-1]} {y}">{heads}{month_cells(y, m, names, klam_dates)}</div>
<p class="small"><a href="javascript:print()">⎙ Skriv ut</a></p>
<h2>Hela {y}</h2>
{months_grid(y)}
</div>{sidebar(y, ads=False)}</div>"""
    # ponytail: no ads, no sitemap entry, noindex -- AdSense flagged these as "screens without
    # publisher content" and Google left them "crawled, not indexed". They are for printing.
    return {"route": f"/kalender/{y}/{m}/", "title": f"Kalender {hol.MONTHS[m-1]} {y} med veckonummer och röda dagar",
            "desc": f"Månadskalender {hol.MONTHS[m-1]} {y}: veckonummer, helgdagar och klämdagar. Utskriftsvänlig.", "priority": "0.5", "body": body, "sitemap": False,
            "head": '<meta name="robots" content="noindex, follow">'}


def named_common(slug, name, answer, faqs, table, target, extra):
    y = TODAY.year
    body = f"""<div class="wrap cols"><div>
<p class="meta crumb"><a href="/">Lediga dagar</a> · <a href="/{y}/">{y}</a> · {name}</p>
<h1>{name} {y}</h1>
<p>{answer}</p>
<div class="ad ad-728x90 desktop-ad">Annons 728×90</div>
<div class="ad ad-320x100 mobile-ad">Annons 320×100</div>
<div class="tablewrap">{table}</div>
<div class="count"><b data-countdown="{target.isoformat()}">{days_until(target)}</b><span class="meta">Till {name.lower()} {target.year}</span></div>
{extra}
<div class="faq">{"".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in faqs)}</div>
<div class="links"><a href="/{y}/">Alla lediga dagar {y} →</a><a href="/klamdagar/{y}/">Klämdagar {y} →</a></div>
</div>{sidebar(y)}</div>"""
    return body


def page_day(slug):
    name, red, fn = hol.DAYS[slug]; d = fn(TODAY.year); dn = fn(TODAY.year + 1)
    status = "en röd dag" if red else "ingen röd dag" + (" men ledig hos de flesta arbetsgivare" if slug in hol.DE_FACTO_OFF else "")
    answer = f"{name} {TODAY.year} infaller {hol.sv(d)} (vecka {hol.week(d)}) och är {status}."
    why = (f"Ja. {name} är en allmän helgdag enligt lag (1989:253) om allmänna helgdagar och därmed en röd dag i hela Sverige." if red
           else f"Nej. {name} är inte en allmän helgdag, men de flesta arbetsplatser har stängt och semesterlagen jämställer dagen med söndag, så den kostar ingen semesterdag." if slug in hol.DE_FACTO_OFF
           else f"Nej. {name} är ingen allmän helgdag utan en vanlig arbetsdag när den infaller på en vardag.")
    faqs = [(f"Är {name.lower()} en röd dag?", why),
            (f"Vilken vecka är {name.lower()} {TODAY.year}?", f"Vecka {hol.week(d)}, {hol.sv(d)}."),
            (f"När är {name.lower()} {TODAY.year + 1}?", f"{hol.sv(dn).capitalize()}.")]
    rows = "".join(f'<tr><th scope="row">{y}</th><td class="datum">{"<span class=rod aria-hidden=true>●</span> " if red else ""}<time datetime="{fn(y).isoformat()}">{hol.sv(fn(y), with_year=False)}</time></td><td class="d">V. {hol.week(fn(y))}</td></tr>' for y in FIVE)
    table = f'<table>{caption(f"{name} de närmaste fem åren")}<thead><tr><th scope="col">År</th><th scope="col" class="datum">{name}</th><th scope="col" class="d">Vecka</th></tr></thead><tbody>{rows}</tbody></table>'
    target = d if d >= TODAY else dn
    head = faq(faqs) + jsonld({"@context": "https://schema.org", "@type": "Event", "name": f"{name} {TODAY.year}", "startDate": d.isoformat(),
                                "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode", "eventStatus": "https://schema.org/EventScheduled",
                                "location": {"@type": "Country", "name": "Sverige"}})
    return {"route": f"/{slug}/", "title": f"{name} {TODAY.year} – datum, vecka och röd dag?", "desc": answer, "priority": "0.8",
            "body": named_common(slug, name, answer, faqs, table, target, C.DAYS[slug].format(y=TODAY.year)), "head": head}


def page_group(slug):
    name, members = hol.GROUPS[slug]
    line = lambda y: ", ".join(f"{hol.DAYS[m][0].lower()} {hol.sv(hol.DAYS[m][2](y), with_year=False)}" for m in members)
    answer = f"{name} {TODAY.year}: {line(TODAY.year)}. " + " ".join(f"{hol.DAYS[m][0]} är en röd dag." for m in members if hol.DAYS[m][1])
    faqs = [(f"När är {name.lower()} {TODAY.year}?", f"{name} {TODAY.year}: {line(TODAY.year)}."),
            (f"När är {name.lower()} {TODAY.year + 1}?", f"{name} {TODAY.year + 1}: {line(TODAY.year + 1)}."),
            (f"Vilka dagar är röda under {name.lower()}?", ", ".join(hol.DAYS[m][0] for m in members if hol.DAYS[m][1]) + ".")]
    rows = "".join(f'<tr><th scope="row">{y}</th>' + "".join(
        f'<td class="{"datum" if i == 0 else "d"}">{"<span class=rod aria-hidden=true>●</span> " if hol.DAYS[m][1] else ""}<time datetime="{hol.DAYS[m][2](y).isoformat()}">{hol.sv(hol.DAYS[m][2](y), with_year=False)}</time></td>'
        for i, m in enumerate(members)) + "</tr>" for y in FIVE)
    table = f'<table>{caption(f"{name} de närmaste fem åren")}<thead><tr><th scope="col">År</th>' + "".join(f'<th scope="col" class="{"datum" if i == 0 else "d"}">{hol.DAYS[m][0]}</th>' for i, m in enumerate(members)) + f"</tr></thead><tbody>{rows}</tbody></table>"
    d0 = hol.DAYS[members[0]][2](TODAY.year); target = d0 if d0 >= TODAY else hol.DAYS[members[0]][2](TODAY.year + 1)
    body = named_common(slug, name, answer, faqs, table, target, C.GROUPS[slug].format(y=TODAY.year)).replace('<div class="faq">', '<p>' + " · ".join(f'<a href="/{m}/">{hol.DAYS[m][0]}</a>' for m in members) + '</p><div class="faq">')
    return {"route": f"/{slug}/", "title": f"{name} {TODAY.year} – alla datum", "desc": answer, "priority": "0.9", "body": body, "head": faq(faqs)}


def generated():
    pages = [page_home()] + [page_year(y) for y in YEARS]
    pages += [page_klam(y) for y in YEARS] + [page_skollov(y) for y in YEARS]
    # län pages were thin near-duplicates and got dropped from Google (Sep 2026); folded into the hub
    pages += [moved(f"/skollov/{y}/{lan}/", f"/skollov/{y}/#{lan}") for y in YEARS for lan in SKOLLOV["lan"]]
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
        if p.get("redirect"):
            to = BASE_PATH + p["redirect"]
            open(out, "w", encoding="utf-8").write(
                f'<!doctype html><meta charset="utf-8"><title>{SITE_NAME}</title>'
                f'<link rel="canonical" href="{BASE_URL}{to.split("#")[0]}"><meta http-equiv="refresh" content="0; url={to}">'
                f'<a href="{to}">{BASE_URL}{to}</a>\n')
            continue
        page = layout.safe_substitute(
            basepath=BASE_PATH, title=esc(p.get("title", SITE_NAME)), desc=esc(p.get("desc", "")),
            canonical=BASE_URL + BASE_PATH + p["route"], image=BASE_URL + BASE_PATH + p.get("image", OG_IMAGE),
            bodyclass=p.get("bodyclass", ""), head=p.get("head", ""), body=p["body"],
            year=TODAY.year, month=TODAY.month, updated=f"{TODAY.day} {hol.MONTHS[TODAY.month-1]} {TODAY.year}")
        page = mount_ads(page)
        if BASE_PATH:
            page = page.replace('href="/', f'href="{BASE_PATH}/').replace('src="/', f'src="{BASE_PATH}/')
        open(out, "w", encoding="utf-8").write(page)
        if p.get("sitemap", True): routes.append((p["route"], p.get("priority", "0.7")))
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
