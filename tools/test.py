"""python3 -m unittest -q tools.test — the checks that fail if a date rule breaks."""
import unittest, datetime as dt, os, subprocess, sys
from tools import holidays as H

D = dt.date


class Dates(unittest.TestCase):
    def test_easter_known_years(self):
        for y, d in {2024: D(2024, 3, 31), 2025: D(2025, 4, 20), 2026: D(2026, 4, 5),
                     2027: D(2027, 3, 28), 2028: D(2028, 4, 16)}.items():
            self.assertEqual(H.easter(y), d)

    def test_midsommar_2026(self):
        y = {h["slug"]: h["date"] for h in H.year(2026)}
        self.assertEqual(y["midsommarafton"], D(2026, 6, 19))
        self.assertEqual(y["midsommardagen"], D(2026, 6, 20))
        self.assertEqual(y["alla-helgons-dag"], D(2026, 10, 31))
        self.assertEqual(y["mors-dag"], D(2026, 5, 31))
        self.assertEqual(y["fars-dag"], D(2026, 11, 8))
        self.assertEqual(y["kristi-himmelsfard"], D(2026, 5, 14))
        self.assertEqual(y["pingstdagen"], D(2026, 5, 24))

    def test_thirteen_red_days(self):
        for y in (2025, 2026, 2027):
            self.assertEqual(sum(h["red"] for h in H.year(y)), 13)

    def test_bridges_2026(self):
        k = {x["date"]: x for x in H.klamdagar(2026)}
        self.assertEqual(k[D(2026, 5, 15)]["days"], 4)           # fre efter Kristi himmelsfärd
        self.assertEqual(k[D(2026, 1, 2)]["take"], [D(2026, 1, 2), D(2026, 1, 5)])  # merged pair
        self.assertEqual(k[D(2026, 12, 28)]["days"], 11)         # mellandagarna
        self.assertIn(D(2026, 4, 2), k)                           # skärtorsdag
        self.assertFalse(any(d.weekday() >= 5 for x in k.values() for d in x["take"]))
        for x in k.values():
            self.assertGreaterEqual(x["days"] - len(x["take"]), 3)

    def test_copy_covers_every_page(self):
        from tools import copy as C
        self.assertEqual(set(C.DAYS), set(H.DAYS))
        self.assertEqual(set(C.GROUPS), set(H.GROUPS))
        self.assertEqual(set(C.HUB), {"year", "klamdagar", "skollov"})

    def test_month_pages_carry_no_ads(self):
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        subprocess.run([sys.executable, "tools/build.py"], cwd=root, check=True, capture_output=True)
        page = open(os.path.join(root, "dist/kalender/2026/8/index.html"), encoding="utf-8").read()
        self.assertNotIn("adsbygoogle\"", page)
        self.assertNotIn("/kalender/", open(os.path.join(root, "dist/sitemap.xml")).read())

    def test_skollov_lan_folded_into_hub(self):
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        subprocess.run([sys.executable, "tools/build.py"], cwd=root, check=True, capture_output=True)
        hub = open(os.path.join(root, "dist/skollov/2026/index.html"), encoding="utf-8").read()
        self.assertIn('<tr id="skane">', hub)
        self.assertIn("Vecka 8: Blekinge", hub)
        self.assertIn("Kungsbacka följer Göteborg", hub)
        self.assertIn('"@type": "FAQPage"', hub)
        stub = open(os.path.join(root, "dist/skollov/2026/skane/index.html"), encoding="utf-8").read()
        self.assertIn('url=/skollov/2026/#skane"', stub)
        self.assertIn('rel="canonical" href="https://ledigadagarna.se/skollov/2026/"', stub)
        self.assertNotIn("/skollov/2026/skane/", open(os.path.join(root, "dist/sitemap.xml")).read())

    def test_home_is_not_the_year_page(self):
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        subprocess.run([sys.executable, "tools/build.py"], cwd=root, check=True, capture_output=True)
        home = open(os.path.join(root, "dist/index.html"), encoding="utf-8").read()
        self.assertIn("<h1>När är jag ledig nästa gång?</h1>", home)
        self.assertNotIn("<h1>Lediga dagar", home)
        kal = open(os.path.join(root, "dist/kalender/2026/8/index.html"), encoding="utf-8").read()
        self.assertIn('<meta name="robots" content="noindex, follow">', kal)

    def test_build_runs(self):
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        r = subprocess.run([sys.executable, "tools/build.py"], cwd=root, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        html = open(os.path.join(root, "dist/nationaldagen/index.html"), encoding="utf-8").read()
        self.assertIn("Sveriges nationaldag 2026 infaller lördag 6 juni 2026", html)
        self.assertIn('"@type": "FAQPage"', html)
        self.assertIn("<h1>", html)
        self.assertNotIn("$", html, "unfilled template var")
        home = open(os.path.join(root, "dist/index.html"), encoding="utf-8").read()
        self.assertIn("<table>", home); self.assertNotIn("Newsreader", home)
        self.assertIn('data-countdown=', home)
        self.assertTrue(os.path.exists(os.path.join(root, "dist/ads.txt")))


def built(path):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(root, "dist", path), encoding="utf-8") as f:
        return f.read()


class Site64(unittest.TestCase):
    """SITE-64: pages with something the calendar sites don't have, and no thin near-duplicates."""

    @classmethod
    def setUpClass(cls):
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        subprocess.run([sys.executable, "tools/build.py"], cwd=root, check=True, capture_output=True)

    def test_best_breaks_2027(self):
        b = H.best_breaks(2027, 4)
        self.assertEqual(b[0]["run"], (D(2026, 12, 31), D(2027, 1, 10)))
        self.assertEqual(b[0]["take"], [D(2027, 1, 4), D(2027, 1, 5), D(2027, 1, 7), D(2027, 1, 8)])  # 6 jan is red
        self.assertEqual(b[0]["days"], 11)
        self.assertEqual(b[1]["run"], (D(2027, 3, 20), D(2027, 3, 29)))                            # påsk: 10 for 4
        for n in (1, 3, 5, 10, 20):
            bs = H.best_breaks(2027, n)
            self.assertEqual(len(bs), 3)
            off = H.off_days(2026) | H.off_days(2027) | H.off_days(2028)
            for x in bs:
                self.assertEqual(len(x["take"]), n)
                self.assertTrue(all(d.year == 2027 and d not in off for d in x["take"]))
                self.assertEqual(x["days"], (x["run"][1] - x["run"][0]).days + 1)
            runs = sorted(x["run"] for x in bs)
            self.assertTrue(all(a[1] < b[0] for a, b in zip(runs, runs[1:])), "breaks overlap")

    def test_best_breaks_filters(self):
        mid = H.DAYS["midsommarafton"][2](2027)
        self.assertEqual(H.best_breaks(2027, 1, 1, around=mid)[0]["take"], [D(2027, 6, 24)])
        self.assertEqual(H.best_breaks(2027, 1, 1, around=mid)[0]["days"], 4)
        s = H.best_breaks(2027, 10, 1, months={6, 7, 8})[0]
        self.assertTrue(all(d.month in (6, 7, 8) for d in s["take"]))

    def test_workdays_2027(self):
        # 261 weekdays, minus 8 weekday holidays/aftnar (1/1, 6/1, långfre, annandag påsk, Kristi hf, midsommarafton, 24/12, 31/12)
        self.assertEqual(sum(w for _, w in H.workdays_by_month(2027)), 253)
        self.assertEqual(dict(H.workdays_by_month(2027))[1], 19)

    def test_planner_on_klamdagar_and_year(self):
        y = H.D.today().year + 1
        k = built(f"klamdagar/{y}/index.html")
        self.assertIn('id="planera"', k)
        self.assertEqual(k.count('<tr><th scope="row">'), 8)  # 1, 2, 3, 4, 5, 10, 15, 20 days
        self.assertIn("Bäst på sommaren", k)
        self.assertIn('"@type": "FAQPage"', k)
        yr = built(f"{y}/index.html")
        self.assertIn(f"<title>Röda dagar {y}", yr)
        self.assertIn(f'id="arbetsdagar"', yr)
        self.assertIn(f"{y} har {sum(w for _, w in H.workdays_by_month(y))} arbetsdagar", yr)

    def test_group_pages_absorb_their_days(self):
        stub = built("midsommarafton/index.html")
        self.assertIn('url=/midsommar/#midsommarafton"', stub)
        self.assertIn('rel="canonical" href="https://ledigadagarna.se/midsommar/"', stub)
        for slug in ("paskafton", "langfredagen", "julafton", "annandag-jul", "midsommardagen"):
            self.assertIn('http-equiv="refresh"', built(f"{slug}/index.html"))
        mid = built("midsommar/index.html")
        self.assertIn('<h2 id="midsommarafton">', mid)
        self.assertIn("lag-1989253-om-allmanna-helgdagar", mid)
        self.assertIn("nordiskamuseet.se/aretsdagar/midsommar", mid)
        self.assertIn('id="ledigt"', mid)
        self.assertNotIn('href="/midsommarafton/"', built("index.html"))  # links skip the redirect

    def test_group_focus_year_is_the_next_one(self):
        from tools import build as B
        saved = B.TODAY
        try:
            B.TODAY = D(2026, 11, 27)
            self.assertEqual(B.page_group("midsommar")["title"], "Midsommar 2027 – midsommarafton fredag 25 juni")
            self.assertEqual(B.page_group("jul")["title"], "Jul 2026 – julafton torsdag 24 december")
            B.TODAY = D(2026, 6, 1)
            self.assertEqual(B.page_group("midsommar")["title"], "Midsommar 2026 – midsommarafton fredag 19 juni")
        finally:
            B.TODAY = saved

    def test_thin_and_past_pages_leave_the_index(self):
        sitemap = built("sitemap.xml")
        past = H.D.today().year - 1
        for path in ("nationaldagen/", "lucia/", f"{past}/", f"klamdagar/{past}/", f"skollov/{past}/"):
            self.assertIn('<meta name="robots" content="noindex, follow">', built(path + "index.html"), path)
            self.assertNotIn(f"ledigadagarna.se/{path}<", sitemap, path)
        for path in ("midsommar/", "pask/", "jul/", "semesterlon/", "semesterlagen/", f"klamdagar/{past + 2}/"):
            self.assertIn(f"ledigadagarna.se/{path}<", sitemap, path)
            self.assertNotIn("noindex", built(path + "index.html"), path)

    def test_semester_pages_answer_without_js(self):
        lon = built("semesterlon/index.html")
        self.assertIn('id="semesterersattning"', lon)
        for p in ("28 §", "29 §", "29 a §", "30 §"):
            self.assertIn(p, lon)
        self.assertIn("<b>645 kr</b>", lon)        # 0,43 % × 30 000 × 5, default in the calculator
        self.assertIn("<b>21 600 kr</b>", lon)     # 12 % × 180 000
        lag = built("semesterlagen/index.html")
        self.assertIn('id="betalda"', lag)
        self.assertIn("182 / 365 × 25 = 12,47", lag)
        self.assertIn("senast 31 mars 2032", lag)


if __name__ == "__main__":
    unittest.main()
