"""Serper.dev Google Maps discovery (no Google billing needed). Needs a Serper API key.

POST https://google.serper.dev/maps  {"q": "...", "page": n}  header X-API-KEY.
Each result is converted to the same record shape places.py writes, so candidates, fingerprint,
call list and email targets work unchanged. County (for the NOAA storm signal) comes from the free
FCC Area API using the result's coordinates, cached by rounded location.
"""
import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

from .cities import TIERS

URL = "https://google.serper.dev/maps"
FCC = "https://geo.fcc.gov/api/census/area"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "raw" / "places.jsonl"
DONE = ROOT / "data" / "raw" / "serper_done.txt"
QUERIES = {"Roofing": "roofing contractor in {city}, {st}", "HVAC": "heating and air conditioning contractor in {city}, {st}"}
ADDR = re.compile(r",\s*([^,]+),\s*([A-Z]{2})(?:\s+\d{5})?(?:,|$)")
_county_cache = {}


def _post(key, q, page, ll=None):
    body = {"q": q, "page": page, "gl": "us", "hl": "en"}
    if ll:
        body["ll"] = ll  # pages after the first require GPS, e.g. "@41.25,-96.0,12z"
    r = requests.post(URL, json=body, timeout=30, headers={"X-API-KEY": key, "Content-Type": "application/json"})
    if r.status_code == 429:
        time.sleep(5)
        return _post(key, q, page, ll)
    return r


def check(key):
    """Returns (ok, message, credits_left_or_None)."""
    try:
        r = _post(key, "roofing contractor in Omaha, NE", 1)
    except requests.RequestException as e:
        return False, f"Could not reach Serper ({e.__class__.__name__}). Check your internet connection.", None
    if r.status_code == 200:
        j = r.json()
        names = [p.get("title") for p in j.get("places", [])[:3]]
        return True, "Key works. Test search returned: " + (", ".join(n for n in names if n) or "no results") + \
            f" (keys in a result: {sorted((j.get('places') or [{}])[0].keys())})", j.get("credits")
    if r.status_code in (401, 403):
        return False, "Serper rejected the key (" + r.text[:160] + "). Copy it again from serper.dev > API key.", None
    if r.status_code == 400 and "credit" in r.text.lower():
        return False, "Serper says you are out of credits: " + r.text[:160], None
    return False, f"Serper replied {r.status_code}: {r.text[:200]}", None


def _county(lat, lon):
    k = (round(lat, 2), round(lon, 2))
    if k not in _county_cache:
        try:
            j = requests.get(FCC, params={"lat": lat, "lon": lon, "format": "json"}, timeout=15).json()
            _county_cache[k] = (j.get("results") or [{}])[0].get("county_name", "")
        except Exception:
            _county_cache[k] = ""
    return _county_cache[k]


def _convert(p, industry, tier, query):
    addr = p.get("address") or ""
    m = ADDR.search(addr) or ADDR.search(addr + ",")
    if not m:
        return None
    city, st = m.group(1).strip(), m.group(2)
    cid = str(p.get("cid") or p.get("placeId") or p.get("place_id") or "")
    if not cid:
        return None
    lat, lon = p.get("latitude"), p.get("longitude")
    comps = [{"shortText": city, "types": ["locality"]}, {"shortText": st, "types": ["administrative_area_level_1"]}]
    cat = p.get("category") or p.get("type") or ""
    oh, lines = p.get("openingHours"), []
    if isinstance(oh, dict):
        lines = [f"{d}: {v}" for d, v in oh.items() if v]
    elif isinstance(oh, list):
        for it in oh:
            if isinstance(it, str):
                lines.append(it)
            elif isinstance(it, dict):
                day, hrs = it.get("day") or it.get("name"), it.get("hours") or it.get("time")
                if day and hrs:
                    lines.append(f"{day}: {hrs}")
    rec = {
        "id": "serper:" + cid, "displayName": {"text": p.get("title") or ""}, "formattedAddress": addr,
        "addressComponents": comps, "nationalPhoneNumber": p.get("phoneNumber") or p.get("phone") or "",
        "websiteUri": p.get("website") or "", "rating": p.get("rating"),
        "userRatingCount": p.get("ratingCount") or p.get("reviews") or 0, "businessStatus": "OPERATIONAL",
        "primaryType": "roofing_contractor" if "roof" in cat.lower() else "", "types": [cat.lower().replace(" ", "_")],
        "googleMapsUri": f"https://www.google.com/maps?cid={cid}", "_lat": lat, "_lon": lon,
        "_industry_query": industry, "_tier": tier, "_query": query,
    }
    if lines:
        rec["regularOpeningHours"] = {"weekdayDescriptions": lines}
    return rec


def run(tiers=("tier1", "tier2", "tier3"), max_requests=2000, pages=3):
    key = os.environ.get("SERPER_API_KEY")
    if not key:
        raise SystemExit("SERPER_API_KEY is not set")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    seen = {json.loads(l)["id"] for l in OUT.open()} if OUT.exists() else set()
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
                        new, ll = [], None
                        for page in range(1, pages + 1):
                            if used >= max_requests:
                                print(f"request budget {max_requests} reached; {len(seen)} places stored")
                                return
                            r = _post(key, text, page, ll)
                            used += 1
                            if r.status_code != 200:
                                if page > 1 and r.status_code == 400:
                                    break  # no further pages for this query
                                raise SystemExit(f"Serper error {r.status_code}: {r.text[:200]}. "
                                                 f"Progress is saved; re-run to resume.")
                            places = r.json().get("places", [])
                            if not places:
                                break
                            if ll is None:
                                pts = [(x["latitude"], x["longitude"]) for x in places
                                       if x.get("latitude") is not None and x.get("longitude") is not None]
                                if pts:
                                    ll = "@%.6f,%.6f,12z" % (sum(a for a, _ in pts) / len(pts),
                                                             sum(b for _, b in pts) / len(pts))
                            added = 0
                            for p in places:
                                rec = _convert(p, ind, tier, text)
                                if rec and rec["id"] not in seen:
                                    seen.add(rec["id"])
                                    new.append(rec)
                                    added += 1
                            if len(places) < 15 or ll is None or added < 5:
                                break  # last page, or diminishing returns: do not spend more credits here
                        roofers = [x for x in new if x["_industry_query"] == "Roofing" and x.get("_lat") is not None]
                        if roofers:
                            with ThreadPoolExecutor(8) as ex:
                                for rec, county in zip(roofers, ex.map(lambda x: _county(x["_lat"], x["_lon"]), roofers)):
                                    if county:
                                        rec["addressComponents"].append(
                                            {"shortText": county, "types": ["administrative_area_level_2"]})
                        for rec in new:
                            out.write(json.dumps(rec) + "\n")
                        dlog.write(text + "\n")
                        dlog.flush()
                        out.flush()
                        print(f"[{used}] {text}: +{len(new)} (total {len(seen)})", flush=True)
    print(f"finished; {used} requests, {len(seen)} places stored")
