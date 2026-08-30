# CLAUDE.md

**ledigadagarna.se** — Swedish "when am I off?" site. Röda dagar, klämdagar,
skollov, calendars, named-day pages. Funded by AdSense. Static HTML, stdlib
Python build, GitHub Pages. Swedish copy; English code and commits.

## Why it looks the way it does
Every target query has a Google AI Overview on top. The site earns by (a) being
the source that box cites and (b) serving what the box can't: the whole-year
table, the klämdag planner, printable calendars. So: answer sentence in the
first `<p>` after the H1, real `<table>` on every breakpoint (never cards),
`<time datetime>` on every date, FAQPage + Event JSON-LD. Don't prettify that
away.

## Commands
```bash
python3 -m unittest -q tools.test
python3 tools/build.py
```

## Layout
- `tools/holidays.py` — the only source of dates. `DAYS` table + Easter
  computus. Add a day there, it appears everywhere.
- `tools/build.py` — renders `site/pages/**` (hand-written, `<!--meta -->`
  block) plus generated pages: `/`, `/<year>/`, `/klamdagar/<y>/`,
  `/skollov/<y>/`, `/kalender/<y>/<m>/`, `/<day-slug>/`, `/pask/`, `/midsommar/`, `/jul/`.
- `site/data/skollov.json` — per-region lov weeks. Municipal, must be verified by hand each year.
- `site/_layout.html`, `site/assets/app.js` — consent (Consent Mode v2 before
  the AdSense tag), theme toggle, one-push-per-slot ad mounting. Copied from
  hjarngympa; same rules apply: never push an ad into a zero-width slot, ads
  are sized placeholders `<div class="ad ad-336x280">` that build.py fills.

## Rules
- Dates are computed, never typed. If a date is wrong, fix the rule and add a test.
- Ads never sit between the H1 and the answer sentence, never inside a table, never on print.
- Colour is never the only signal: red days get ●, klämdagar ◐, today an outline.
