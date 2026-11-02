"""Build the two deliverables from Places discovery + fingerprints:

  call list  : looser filter, every operational small roofing/HVAC business with a phone,
               ranked by intent. Drops franchises, 24/7 answering, chat/AI receptionists, commercial-only.
  email list : strict ICP (qualify.py rubric, score >= 55) ranked by intent, for owner lookup + Clay Work Email.

Intent points (shown per row as tags):
  storm  +3  roofer in a county with >=1in hail / damaging wind / tornado in last 90 days (NOAA SPC)
  ads    +3  Google Ads tag, Meta Pixel, CallRail, LSA badge, Angi/HomeAdvisor/Thumbtack on site
  hours  +2  Google Business Profile hours end by 6pm, or closed weekends
  nochat +2  no chat, AI receptionist, text-back or online booking on site
  small  +1  15-160 Google reviews (owner-operator range)
  noweb  +1  no website: phone is the only lead channel (call list only)
"""
import csv
import json
import re
from pathlib import Path

from . import qualify, storms
from .cli import digits, domain_of, precheck, read, write, SEEN

ROOT = Path(__file__).resolve().parent.parent
TRADE = re.compile(r"roof|hvac|heat|air|cool|mechanical|comfort|climate|furnace|exterior|restoration|temperature|refrigeration", re.I)
OFFSET_TZ = {-300: "ET", -240: "ET", -360: "CT", -300.5: "CT", -420: "MT", -480: "PT", -540: "AK", -600: "HI"}
STATE_TZ = {"GA": "ET", "NC": "ET", "SC": "ET", "VA": "ET", "OH": "ET", "IN": "ET", "KY": "ET", "FL": "ET", "TN": "CT",
            "OK": "CT", "KS": "CT", "MO": "CT", "NE": "CT", "TX": "CT", "AL": "CT", "LA": "CT", "AR": "CT", "MS": "CT",
            "IA": "CT", "MN": "CT", "IL": "CT", "SD": "CT", "ND": "CT", "CO": "MT", "AZ": "MT", "UT": "MT", "NM": "MT",
            "NV": "PT"}


def _comp(p, kind):
    for c in p.get("addressComponents", []):
        if kind in c.get("types", []):
            return c.get("shortText") or c.get("longText")
    return ""


def places_to_candidates(out_path, raw=ROOT / "data" / "raw" / "places.jsonl"):
    seen_d, seen_p = set(), set()
    if SEEN.exists():
        for s in read(SEEN):
            seen_d.add(s["domain"]); seen_p.add(s["phone"])
    agg = storms.load()
    rows, drop = [], {}
    for line in open(raw):
        p = json.loads(line)
        name = (p.get("displayName") or {}).get("text", "")
        phone, site = p.get("nationalPhoneNumber"), p.get("websiteUri") or ""
        reason = None
        if p.get("businessStatus") not in (None, "OPERATIONAL"):
            reason = "not operational"
        elif not phone:
            reason = "no phone"
        elif not TRADE.search(name + " " + " ".join(p.get("types", []))):
            reason = "off-niche"
        elif precheck(name, site or name):
            reason = precheck(name, site or name)
        elif digits(phone) in seen_p or (site and domain_of(site) in seen_d):
            reason = "duplicate"
        if reason:
            drop[reason] = drop.get(reason, 0) + 1
            continue
        seen_p.add(digits(phone))
        if site:
            seen_d.add(domain_of(site))
        st = _comp(p, "administrative_area_level_1")
        county = _comp(p, "administrative_area_level_2")
        ind = p["_industry_query"]
        if "roof" in name.lower() or p.get("primaryType") == "roofing_contractor":
            ind = "Roofing"
        hours = " | ".join((p.get("regularOpeningHours") or {}).get("weekdayDescriptions", []))
        rows.append({
            "business_name": name, "website": re.sub(r"\?.*$", "", site), "phone": phone,
            "address": p.get("formattedAddress"), "city_state": f"{_comp(p, 'locality')}, {st}", "state": st,
            "county": county, "time_zone": STATE_TZ.get(st, "unknown"), "industry": ind,
            "google_rating": p.get("rating"), "google_reviews": p.get("userRatingCount") or 0,
            "gbp_hours": hours, "maps_url": p.get("googleMapsUri"), "place_id": p["id"], "tier": p.get("_tier"),
            "storm_signal": storms.signal(agg, st, county) if ind == "Roofing" else "",
        })
    write(out_path, rows)
    print(f"{len(rows)} candidates; dropped {drop}")


def _gbp_close(hours):
    return qualify._close_hour(hours) if hours else None


def intent(r, call_list=False):
    pts, tags = 0, []
    if r.get("storm_signal"):
        pts += 3; tags.append("storm")
    ads = r.get("fp_ad_signals", "none detected")
    if ads and ads != "none detected":
        pts += 3; tags.append("ads")
    hrs = r.get("gbp_hours", "")
    close = _gbp_close(hrs)
    if (close is not None and close <= 18) or re.search(r"(Saturday|Sunday): Closed", hrs):
        pts += 2; tags.append("hours")
    if r.get("fp_pages") and r.get("fp_chat_or_answering") == "none detected" and r.get("fp_booking") == "none detected":
        pts += 2; tags.append("nochat")
    n = int(float(r.get("google_reviews") or 0))
    if 15 <= n <= 160:
        pts += 1; tags.append("small")
    if call_list and not r.get("website"):
        pts += 1; tags.append("noweb")
    return pts, tags


def call_list(cands_path, out_path, max_reviews=300):
    rows, out, drop = read(cands_path), [], {}
    for r in rows:
        hrs = r.get("gbp_hours", "")
        why = None
        if "Open 24 hours" in hrs:
            why = "GBP hours: open 24 hours"
        elif int(float(r.get("google_reviews") or 0)) > max_reviews:
            why = f"over {max_reviews} reviews (likely >10 staff)"
        elif r.get("website") and r.get("fp_pages"):
            d = qualify.disqualify(r)
            if d and "score" not in d and "unreachable" not in d:
                why = d
        if why:
            drop[why.split(":")[0][:40]] = drop.get(why.split(":")[0][:40], 0) + 1
            continue
        pts, tags = intent(r, call_list=True)
        out.append({
            "intent_score": pts, "intent_tags": " ".join(tags), "business_name": r["business_name"],
            "phone": r["phone"], "industry": r["industry"], "city_state": r["city_state"], "county": r.get("county"),
            "time_zone": r["time_zone"], "gbp_hours": hrs or "not listed", "website": r.get("website") or "none",
            "google_rating": r.get("google_rating"), "google_reviews": r.get("google_reviews"),
            "storm_signal": r.get("storm_signal", ""), "ad_signals": r.get("fp_ad_signals", ""),
            "best_call_window": "7:00-8:30am or 4:30-6:00pm local (owners on job sites midday)",
            "compliance": "dial manually; scrub against National DNC before dialing",
            "tier": r.get("tier"), "maps_url": r.get("maps_url"),
        })
    out.sort(key=lambda x: (x["tier"] or "tier9", -x["intent_score"]))
    write(out_path, out)
    print(f"{len(out)} call leads; dropped {drop}")


def email_targets(cands_path, out_path, n=4000):
    """Strict ICP + intent ranking. Output feeds owner lookup then Clay Work Email."""
    rows, out = read(cands_path), []
    for r in rows:
        if not r.get("website") or qualify.disqualify(r) or "Open 24 hours" in r.get("gbp_hours", ""):
            continue
        if r.get("gbp_hours"):
            r["fp_hours"] = r["gbp_hours"]
        q = qualify.build(r, {})
        if q["score"] < 55:
            continue
        pts, tags = intent(r)
        q.update(intent_score=pts, intent_tags=" ".join(tags), storm_signal=r.get("storm_signal", ""),
                 tier=r.get("tier"), domain=domain_of(r["website"]))
        out.append(q)
    out.sort(key=lambda x: (-x["intent_score"], -x["score"]))
    write(out_path, out[:n])
    print(f"{len(out)} ICP-qualified; wrote top {min(n, len(out))}")
