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

    def test_klamdag_2026_kristi_himmelsfard(self):
        # Thu 14 May is red -> Fri 15 May is a klämdag giving Thu–Sun = 4 days.
        k = {x["date"]: x for x in H.klamdagar(2026)}
        self.assertIn(D(2026, 5, 15), k)
        self.assertEqual(k[D(2026, 5, 15)]["days"], 4)
        # A weekend is never a klämdag.
        self.assertFalse(any(d.weekday() >= 5 for d in k))

    def test_build_runs(self):
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        r = subprocess.run([sys.executable, "tools/build.py"], cwd=root, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        html = open(os.path.join(root, "dist/midsommarafton/index.html"), encoding="utf-8").read()
        self.assertIn("Midsommarafton 2026 infaller fredag 19 juni 2026", html)
        self.assertIn('"@type": "FAQPage"', html)
        self.assertIn("<h1>", html)
        self.assertNotIn("$", html.split("<main")[1].split("</main")[0], "unfilled template var")
        self.assertTrue(os.path.exists(os.path.join(root, "dist/ads.txt")))


if __name__ == "__main__":
    unittest.main()
