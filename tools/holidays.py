"""Swedish red days, klämdagar and named days for any year. Stdlib only.

    python3 tools/holidays.py 2026     # prints the year as TSV

Every date on the site comes from here, so a wrong rule is wrong everywhere;
keep the rules readable and tested (tools/test.py).
"""
import datetime as dt
import sys

D = dt.date
WEEKDAYS = ["måndag", "tisdag", "onsdag", "torsdag", "fredag", "lördag", "söndag"]
MONTHS = ["januari", "februari", "mars", "april", "maj", "juni", "juli",
          "augusti", "september", "oktober", "november", "december"]


def easter(y):
    """Gregorian Easter Sunday (Anonymous/Meeus algorithm)."""
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = (h + l - 7 * m + 114) % 31 + 1
    return D(y, month, day)


def weekday_on_or_after(date, weekday):
    return date + dt.timedelta((weekday - date.weekday()) % 7)


def last_weekday_of_month(y, m, weekday):
    d = D(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(1)
    return d - dt.timedelta((d.weekday() - weekday) % 7)


def nth_weekday(y, m, weekday, n):
    return weekday_on_or_after(D(y, m, 1), weekday) + dt.timedelta(7 * (n - 1))


# slug -> (name, red day?, date function). Slug is the URL: /<slug>/.
# "red" = allmän helgdag under lag (1989:253). Aftnar are not red days but
# semesterlagen treats midsommarafton, julafton and nyårsafton as söndag.
DAYS = {
    "nyarsdagen":        ("Nyårsdagen",          True,  lambda y: D(y, 1, 1)),
    "trettondedag-jul":  ("Trettondedag jul",    True,  lambda y: D(y, 1, 6)),
    "langfredagen":      ("Långfredagen",        True,  lambda y: easter(y) - dt.timedelta(2)),
    "paskafton":         ("Påskafton",           False, lambda y: easter(y) - dt.timedelta(1)),
    "paskdagen":         ("Påskdagen",           True,  easter),
    "annandag-pask":     ("Annandag påsk",       True,  lambda y: easter(y) + dt.timedelta(1)),
    "valborg":           ("Valborgsmässoafton",  False, lambda y: D(y, 4, 30)),
    "forsta-maj":        ("Första maj",          True,  lambda y: D(y, 5, 1)),
    "kristi-himmelsfard":("Kristi himmelsfärdsdag", True, lambda y: easter(y) + dt.timedelta(39)),
    "mors-dag":          ("Mors dag",            False, lambda y: last_weekday_of_month(y, 5, 6)),
    "nationaldagen":     ("Sveriges nationaldag", True, lambda y: D(y, 6, 6)),
    "pingstdagen":       ("Pingstdagen",         True,  lambda y: easter(y) + dt.timedelta(49)),
    "midsommarafton":    ("Midsommarafton",      False, lambda y: weekday_on_or_after(D(y, 6, 19), 4)),
    "midsommardagen":    ("Midsommardagen",      True,  lambda y: weekday_on_or_after(D(y, 6, 20), 5)),
    "alla-helgons-dag":  ("Alla helgons dag",    True,  lambda y: weekday_on_or_after(D(y, 10, 31), 5)),
    "fars-dag":          ("Fars dag",            False, lambda y: nth_weekday(y, 11, 6, 2)),
    "lucia":             ("Lucia",               False, lambda y: D(y, 12, 13)),
    "julafton":          ("Julafton",            False, lambda y: D(y, 12, 24)),
    "juldagen":          ("Juldagen",            True,  lambda y: D(y, 12, 25)),
    "annandag-jul":      ("Annandag jul",        True,  lambda y: D(y, 12, 26)),
    "nyarsafton":        ("Nyårsafton",          False, lambda y: D(y, 12, 31)),
}
# Aftnar most employers give off; counted as "ledig" for klämdag purposes.
DE_FACTO_OFF = {"midsommarafton", "julafton", "nyarsafton"}
# Umbrella pages: one slug, several days.
GROUPS = {
    "pask": ("Påsk", ["langfredagen", "paskafton", "paskdagen", "annandag-pask"]),
    "midsommar": ("Midsommar", ["midsommarafton", "midsommardagen"]),
    "jul": ("Jul", ["julafton", "juldagen", "annandag-jul"]),
}


def year(y):
    """[{slug, name, date, red, off}] sorted by date."""
    out = []
    for slug, (name, red, fn) in DAYS.items():
        d = fn(y)
        out.append({"slug": slug, "name": name, "date": d, "red": red,
                    "off": red or slug in DE_FACTO_OFF})
    return sorted(out, key=lambda x: x["date"])


def off_days(y):
    """Set of dates nobody works: weekends + red days + de facto aftnar."""
    s = {h["date"] for h in year(y) if h["off"]}
    d = D(y, 1, 1)
    while d.year == y:
        if d.weekday() >= 5:
            s.add(d)
        d += dt.timedelta(1)
    return s


def klamdagar(y):
    """Workdays with a free day on both sides. Each -> {date, run:(start,end)}
    where run is the contiguous free stretch you get by taking the day off."""
    off = off_days(y) | off_days(y - 1) | off_days(y + 1)
    out = []
    d = D(y, 1, 1)
    one = dt.timedelta(1)
    while d.year == y:
        if d not in off and (d - one) in off and (d + one) in off:
            a, b = d - one, d + one
            while (a - one) in off: a -= one
            while (b + one) in off: b += one
            out.append({"date": d, "run": (a, b), "days": (b - a).days + 1})
        d += one
    return out


def sv(d, with_year=True):
    s = f"{WEEKDAYS[d.weekday()]} {d.day} {MONTHS[d.month - 1]}"
    return f"{s} {d.year}" if with_year else s


def week(d):
    return d.isocalendar()[1]


if __name__ == "__main__":
    y = int(sys.argv[1]) if len(sys.argv) > 1 else dt.date.today().year
    for h in year(y):
        print(f"{h['date']}\tv{week(h['date'])}\t{'röd' if h['red'] else '   '}\t{h['name']}")
    print("--- klämdagar")
    for k in klamdagar(y):
        print(f"{k['date']}\t{sv(k['date'])}\t-> {k['days']} dagar ({k['run'][0]}–{k['run'][1]})")
