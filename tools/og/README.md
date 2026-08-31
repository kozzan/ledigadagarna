# Social card source

`card.html` renders the 1200×630 og.png. Regenerate (new year or new stats):

1. Update the year, the stat numbers (from `python3 tools/holidays.py <year>`:
   bridges / sum take / sum days) and the January tile strip in card.html.
2. `google-chrome --headless=new --hide-scrollbars --window-size=1200,800 --screenshot=tall.png card.html`
   (800 tall: the shot at exactly 630 can fire before the Archivo webfont loads)
3. Crop to 1200×630 and save as `site/assets/og.png`.
