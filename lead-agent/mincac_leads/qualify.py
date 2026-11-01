"""Turn fingerprint + review evidence into the Mincac output row, score it, and explain every decision."""
import json
import re
from pathlib import Path

from . import reviews as rv
from .score import score, confidence

NOT_A_NAME = re.compile(r"roof|heat|air|cool|hvac|llc|inc|company|operated|owned|family|service|construction|"
                        r"contract|home|local|veteran|licensed|insured|\b(the|our|and|we|you|your|customer|knowledge|"
                        r"first|approach|guides?|maintenance|corners?|peachtree|team|about|meet|contact|call|today|"
                        r"quality|best|trusted|years?|experience|business|owner|founder|president|videos?|talk|reviews?|blog|news|photos?|gallery)\b", re.I)
JOB_VALUE = {"Roofing": 10_000, "HVAC": 7_000}
JOB_WORD = {"Roofing": "roof", "HVAC": "system replacement"}


def _close_hour(hours_text):
    """Latest closing hour (24h) across the hours strings found, or None."""
    latest = None
    for m in re.finditer(r"(?:-|–|—|to)\s*(\d{1,2})(?::(\d{2}))?\s*(pm|p\.m\.|p)\b", hours_text or "", re.I):
        h = int(m.group(1)) % 12 + 12 + (int(m.group(2) or 0) / 60)
        latest = h if latest is None else max(latest, h)
    return latest


def _manual_exclusions():
    from pathlib import Path
    import csv
    f = Path(__file__).resolve().parent.parent / "data" / "excluded.csv"
    return {row["domain"]: row["reason"] for row in csv.DictReader(open(f))} if f.exists() else {}


MANUAL = _manual_exclusions()


def _firmo():
    from pathlib import Path
    import csv
    f = Path(__file__).resolve().parent.parent / "data" / "firmo.csv"
    return {row["domain"]: row for row in csv.DictReader(open(f))} if f.exists() else {}


FIRMO = _firmo()


def _dom(url):
    return re.sub(r"^(?:https?://)?(?:www\.)?([^/?#]+).*", r"\1", (url or "").lower())


def disqualify(r):
    d = re.sub(r"^(?:https?://)?(?:www\.)?([^/?#]+).*", r"\1", (r.get("website") or "").lower())
    if d in MANUAL:
        return MANUAL[d]
    if FIRMO.get(d, {}).get("exclude_reason"):
        return FIRMO[d]["exclude_reason"] + " (" + FIRMO[d]["source"] + ")"
    if r.get("precheck_exclude"):
        return r["precheck_exclude"]
    if not r.get("fp_pages"):
        return "website unreachable (no verifiable web presence)"
    chat = r.get("fp_chat_or_answering", "none detected")
    if chat != "none detected" and chat != "Facebook Messenger chat":
        return f"already has chat/answering tool: {chat}"
    if r.get("fp_live_answering_claim", "none") != "none":
        return f"advertises live answering: {r['fp_live_answering_claim']}"
    claims = r.get("fp_claims_24_7", "none").lower()
    if re.search(r"open 24|24 hours a day|24 hours,? 7 days", claims):
        return f"advertises 24/7 availability: {r['fp_claims_24_7']}"
    if r.get("fp_commercial_only") == "yes":
        return "commercial-only wording, no residential"
    m = re.search(r"(20\d{2})", r.get("fp_founded", ""))
    if m and int(m.group(1)) >= 2026:
        return f"under 1 year in business ({r['fp_founded']})"
    return None


def load_reviews(map_path):
    """map file: {"<raw reviews file>": ["feature_id", ...in call order]} -> {feature_id: tagged evidence}"""
    out = {}
    root = Path(map_path).parent
    for fname, fids in json.loads(Path(map_path).read_text()).items():
        blocks = json.loads((root / fname).read_text())["data"]["alexandria"]
        for fid, b in zip(fids, blocks):
            out[fid] = rv.tag_reviews((b.get("data") or {}).get("reviews", []))
    return out


def build(r, review_ev):
    ind = r.get("industry") or "Roofing"
    ev = review_ev.get(r.get("feature_id"), [])
    tags = {t for e in ev for t in e["tags"]}
    claims = r.get("fp_claims_24_7", "none")
    close = _close_hour(r.get("fp_hours"))

    # after-hours gap
    if claims != "none":
        ah, ah_txt = "unclear", f"office hours {r.get('fp_hours')}; site claims '{claims}' (emergency, not live answering)"
    elif close is None:
        ah, ah_txt = "unclear", "no hours published on website; no 24/7 claim"
    elif close <= 18:
        ah, ah_txt = "yes", f"hours end by {int(close) - 12}pm ({r['fp_hours']}); no 24/7 or emergency line on site"
    elif close <= 20:
        ah, ah_txt = "unclear", f"hours run to {int(close) - 12}pm ({r['fp_hours']})"
    else:
        ah, ah_txt = "weak", f"hours run late ({r['fp_hours']})"
    if ah != "yes" and tags & {"missed_call", "after_hours"} and claims == "none":
        ah, ah_txt = "yes", ah_txt + "; reviews cite missed or after-hours calls"

    # speed-to-lead gap
    has_booking = r.get("fp_booking", "none detected") != "none detected"
    has_text = r.get("fp_text_us") == "yes"
    pain = tags & {"missed_call", "no_callback", "slow_response", "no_estimate", "no_show"}
    if pain:
        sp = "yes"
        sp_txt = "reviews cite " + ", ".join(sorted(pain)).replace("_", " ")
    elif not has_booking and not has_text:
        sp, sp_txt = "form_only", ("contact form only" if r.get("fp_contact_form") == "yes" else "phone/email only") + \
            "; no chat, text-back or online booking detected"
    else:
        sp, sp_txt = "partial", f"no chat; booking={r.get('fp_booking')}; text option={'yes' if has_text else 'no'}"

    owners = [o for o in (r.get("fp_owner_mentions") or "").split(", ") if o and o != "none found" and not NOT_A_NAME.search(o)]
    owner = owners[0] if owners else "unknown"
    f = FIRMO.get(_dom(r.get("website")), {})
    if owner == "unknown" and f.get("owner_name"):
        owner = f["owner_name"]
    emp = int(f["employees"]) if f.get("employees") and "conflict" not in f.get("source", "") else None
    rev_bucket = f.get("revenue_bucket", "")
    aov = r.get("fp_install_evidence") or ""
    ads = r.get("fp_ad_signals", "none detected")
    lead_spend = "none found" if ads == "none detected" else f"{ads} detected on site" + (
        f" ({r['fp_ad_ids']})" if r.get("fp_ad_ids") else "")

    lead = {"employees_verified": emp, "employees_estimated_small": True,
            "revenue_status": "out_of_range" if rev_bucket and rev_bucket not in ("0-500K", "500K-1M") else "estimated",
            "aov_evidence": aov, "after_hours": ah, "speed": sp, "lead_spend_evidence": lead_spend.replace("CallRail (call tracking)", "CallRail call tracking (usually measures paid-ad calls)"),
            "owner_name": owner, "review_evidence": ev}
    sc = score(lead)

    # offer + leak math
    v, w = JOB_VALUE[ind], JOB_WORD[ind]
    if "no_estimate" in tags and ind == "Roofing":
        offer, math = "estimate follow-up", f"If 6 estimates a month stall with no follow-up at ${v:,} a {w} and 1 in 4 would have signed, that is about ${6 * v // 4:,} a month."
    elif ah == "yes":
        offer, math = "after-hours call answering", f"If 6 calls a month go unanswered after hours at ${v:,} a {w} and 1 in 5 would have booked, that is about ${6 * v // 5:,} a month."
    elif tags & {"missed_call", "no_callback"}:
        offer, math = "missed-call text-back", f"If 8 calls a month ring out with no callback at ${v:,} a {w} and 1 in 5 would have booked, that is about ${8 * v // 5:,} a month."
    elif sp in ("yes", "form_only"):
        offer, math = "60-second lead follow-up", f"If 5 web leads a month wait hours for a reply at ${v:,} a {w} and 1 in 5 would have closed, that is about ${v:,} a month."
    else:
        offer, math = "missed-call text-back", f"If 6 calls a month are missed on job sites at ${v:,} a {w} and 1 in 5 would have booked, that is about ${6 * v // 5:,} a month."

    domain_emails = [e for e in (r.get("fp_emails") or "").split(", ") if "@" in e]
    srcs = [r.get("website"), r.get("maps_url")] + (r.get("fp_pages") or "").split(" ; ") + [e["url"] for e in ev[:3]]
    return {
        "business_name": r["business_name"], "website": r["website"], "phone": r.get("phone"),
        "city_state": r.get("city_state"), "time_zone": r.get("time_zone"), "industry": ind,
        "employee_count": (f"{emp} ({f['source']})" if emp is not None else
                           f"unknown (estimated <=10: {r.get('google_reviews')} Google reviews, single listing"
                           + (f"; {f['source']} bucket {f['size_bucket']}" if f.get("size_bucket") else "") + ")"),
        "revenue": (f"{rev_bucket} per {f['source']}: modeled, may exceed the $1M cap; scored 0" if rev_bucket and rev_bucket not in ("0-500K", "500K-1M")
                    else "estimated $300K-$1M from proxies (review volume, single location); not verified"),
        "aov_evidence": f"site: {aov}" if aov else "none found on site",
        "owner_name": owner, "owner_title": "per website mention, title unverified" if owner != "unknown" else "unknown",
        "owner_linkedin": "unknown", "owner_email": "unknown",
        "email_status": "pending guess/verify" if owner != "unknown" else "owner unknown",
        "general_email": ", ".join(domain_emails[:2]) or "unknown",
        "business_hours": r.get("fp_hours") or "none found",
        "after_hours_gap": f"{ah if ah != 'weak' else 'no'}: {ah_txt}",
        "speed_to_lead_gap": f"{'yes' if sp == 'yes' else 'unclear' if sp != 'no' else 'no'}: {sp_txt}",
        "review_evidence": " || ".join(f"{e['rating']}* {e['when']}: \"{e['quote'][:160]}\"" for e in ev[:2]) or "none found",
        "lead_spend_evidence": lead_spend.replace("CallRail (call tracking)", "CallRail call tracking (usually measures paid-ad calls)"), "best_offer_fit": offer, "leak_math_line": math,
        "score": sc["score"], "score_breakdown": sc["score_breakdown"], "confidence": confidence(lead),
        "google_rating": r.get("google_rating"), "google_reviews": r.get("google_reviews"),
        "source_urls": " ; ".join(dict.fromkeys(s for s in srcs if s)),
    }
