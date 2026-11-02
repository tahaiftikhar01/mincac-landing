"""Storm intent for roofers: NOAA SPC filtered hail and wind reports for the last N days, by county.

Source: https://www.spc.noaa.gov/climo/reports/YYMMDD_rpts_filtered_{hail,wind,torn}.csv (public domain).
A roofer whose county had hail >= 1.00 inch or damaging wind recently has storm-damage call volume now.
"""
import csv
import datetime as dt
import io
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "raw" / "storms_by_county.json"
SPC = "https://www.spc.noaa.gov/climo/reports/{d}_rpts_filtered_{k}.csv"


def _day(d):
    out = []
    for k in ("hail", "wind", "torn"):
        try:
            r = requests.get(SPC.format(d=d.strftime("%y%m%d"), k=k), timeout=20)
            if r.status_code != 200:
                continue
            for row in csv.DictReader(io.StringIO(r.text)):
                if not row.get("State") or not row.get("County"):
                    continue
                size = row.get("Size") or ""
                out.append((row["State"].upper(), row["County"].strip().lower(), k, size, d.isoformat()))
        except requests.RequestException:
            pass
    return out


def build(days=90):
    today = dt.date.today()
    dates = [today - dt.timedelta(days=i) for i in range(1, days + 1)]
    agg = {}
    with ThreadPoolExecutor(12) as ex:
        for rows in ex.map(_day, dates):
            for st, county, kind, size, date in rows:
                a = agg.setdefault(f"{st}|{county}", {"hail": 0, "big_hail": 0, "wind": 0, "torn": 0,
                                                      "max_hail_in": 0.0, "last": ""})
                a[kind] += 1
                if kind == "hail" and size.isdigit():
                    inch = int(size) / 100
                    a["max_hail_in"] = max(a["max_hail_in"], inch)
                    if inch >= 1.0:
                        a["big_hail"] += 1
                a["last"] = max(a["last"], date)
    CACHE.write_text(json.dumps(agg))
    return agg


def load():
    return json.loads(CACHE.read_text()) if CACHE.exists() else {}


def signal(agg, st, county):
    """Return a short evidence string or '' for a lead's state + county."""
    if not (st and county):
        return ""
    c = county.lower().replace(" county", "").replace(" parish", "").strip()
    a = agg.get(f"{st.upper()}|{c}")
    if not a or not (a["big_hail"] or a["wind"] >= 3 or a["torn"]):
        return ""
    parts = []
    if a["big_hail"]:
        parts.append(f"{a['big_hail']} hail reports >=1in (max {a['max_hail_in']:.2f}in)")
    if a["wind"]:
        parts.append(f"{a['wind']} damaging-wind reports")
    if a["torn"]:
        parts.append(f"{a['torn']} tornado reports")
    return f"NOAA SPC last 90 days in {county}: " + ", ".join(parts) + f"; latest {a['last']}"
