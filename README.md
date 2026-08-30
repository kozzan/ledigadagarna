# ledigadagarna.se

Swedish holiday site — röda dagar, klämdagar, skollov, month calendars and one
page per named day. Static HTML, stdlib-only Python build, GitHub Pages, AdSense.
Sister site of hjarngympa.se (same plumbing, no games).

```bash
python3 -m unittest -q tools.test   # date rules + build smoke test
python3 tools/build.py              # site/** + tools/holidays.py -> dist/
python3 tools/holidays.py 2027      # eyeball a year
cd dist && python3 -m http.server 8765
```

Deploy: push to `main` → Actions builds and publishes. Repo variables
`BASE_URL` / `BASE_PATH` for a github.io preview; empty for the real domain.

## Before launch
- [ ] Register `ledigadagarna.se`, point DNS at GitHub Pages, enable Pages on the repo
- [ ] Replace `site/assets/app.css` with the Claude Design handoff
- [ ] Verify `site/data/skollov.json` against municipal läsårsplaner, set `_verified: true`
- [ ] Create an AdSense ad unit for this site and set `ADS_SLOT` in `tools/build.py`; add site in AdSense
- [ ] `site/assets/og.png` (1200×630)
- [ ] Search Console: add property, submit `/sitemap.xml`
