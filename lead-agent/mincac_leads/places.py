"""Google Places API (New) discovery. Needs env GOOGLE_PLACES_API_KEY.

Text Search returns up to 20 places per request and up to 3 pages per query. Every request is
counted against --max-requests so spend is capped. Results append to data/raw/places.jsonl and are
de-duplicated by place id, so a run can be stopped and resumed.
"""
import json
import os
import time
from pathlib import Path

import requests

from .cities import TIERS

URL = "https://places.googleapis.com/v1/places:searchText"
FIELDS = ",".join("places." + f for f in [
    "id", "displayName", "formattedAddress", "addressComponents", "nationalPhoneNumber", "websiteUri",
    "rating", "userRatingCount", "regularOpeningHours.weekdayDescriptions", "businessStatus", "primaryType",
    "types", "googleMapsUri", "utcOffsetMinutes"]) + ",nextPageToken"
QUERIES = {"Roofing": "roofing contractor in {city}, {st}", "HVAC": "heating and air conditioning contractor in {city}, {st}"}
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "raw" / "places.jsonl"
DONE = ROOT / "data" / "raw" / "places_done.txt"


def _search(key, text, token=None):
    body = {"textQuery": text, "pageSize": 20, "regionCode": "US"}
    if token:
        body["pageToken"] = token
    r = requests.post(URL, json=body, timeout=30,
                      headers={"X-Goog-Api-Key": key, "X-Goog-FieldMask": FIELDS})
    if r.status_code == 429:
        time.sleep(5)
        return _search(key, text, token)
    r.raise_for_status()
    return r.json()


def run(tiers=("tier1", "tier2", "tier3"), max_requests=2500, pages=3):
    key = os.environ.get("GOOGLE_PLACES_API_KEY")
    if not key:
        raise SystemExit("GOOGLE_PLACES_API_KEY is not set in this environment")
    seen = set()
    if OUT.exists():
        seen = {json.loads(l)["id"] for l in OUT.open()}
    done = set(DONE.read_text().split("\n")) if DONE.exists() else set()
    used = 0
    with OUT.open("a") as out, DONE.open("a") as dlog:
        for tier in tiers:
            for st, cities in TIERS[tier].items():
                for city in cities:
                    for ind, q in QUERIES.items():
                        text = q.format(city=city, st=st)
                        if text in done:
                            continue
                        token, new = None, 0
                        for _ in range(pages):
                            if used >= max_requests:
                                print(f"request budget {max_requests} reached; {len(seen)} places stored")
                                return
                            j = _search(key, text, token)
                            used += 1
                            for p in j.get("places", []):
                                if p["id"] in seen:
                                    continue
                                seen.add(p["id"])
                                p["_industry_query"], p["_tier"], p["_query"] = ind, tier, text
                                out.write(json.dumps(p) + "\n")
                                new += 1
                            token = j.get("nextPageToken")
                            if not token:
                                break
                            time.sleep(1.5)
                        dlog.write(text + "\n")
                        dlog.flush()
                        out.flush()
                        print(f"[{used}] {text}: +{new} (total {len(seen)})")
    print(f"finished; {used} requests, {len(seen)} places stored")
