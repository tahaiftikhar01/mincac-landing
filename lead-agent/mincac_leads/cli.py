"""Command line for the deterministic steps of the pipeline.

  python -m mincac_leads.cli fingerprint out/batch.csv      # add tech/ads/hours evidence
  python -m mincac_leads.cli emails out/batch.csv           # guess firstnamelastname@domain, verify
  python -m mincac_leads.cli reviews raw_reviews.json       # tag pain quotes from Maps reviews export
  python -m mincac_leads.cli dedupe out/batch.csv           # drop rows already in data/seen.csv, then record them
"""
import csv
import json
import re
import sys
from pathlib import Path

from . import emails, fingerprint, reviews
from .icp import FRANCHISE_MARKERS, SUSPECT_TLDS

ROOT = Path(__file__).resolve().parent.parent
SEEN = ROOT / "data" / "seen.csv"


def domain_of(url):
    m = re.match(r"(?:https?://)?(?:www\.)?([^/?#]+)", (url or "").strip().lower())
    return m.group(1) if m else ""


def digits(phone):
    d = re.sub(r"\D", "", phone or "")
    return d[-10:] if len(d) >= 10 else d


def read(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def write(path, rows):
    cols = list(dict.fromkeys(k for r in rows for k in r))
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def precheck(name, url):
    """Cheap disqualifiers before spending any credits."""
    n, d = (name or "").lower(), domain_of(url)
    if any(m in n or m.replace(" ", "") in d for m in FRANCHISE_MARKERS):
        return "franchise/national brand"
    if d.endswith(SUSPECT_TLDS):
        return "suspect lead-gen domain"
    return None


def _industry(cats):
    c = " ".join(cats or []).lower()
    first = (cats or [""])[0].lower()
    if "roof" in first:
        return "Roofing"
    if any(k in first for k in ("hvac", "air conditioning", "heating", "furnace")):
        return "HVAC"
    if "roof" in c:
        return "Roofing"
    if any(k in c for k in ("hvac", "air conditioning contractor", "heating contractor")):
        return "HVAC"
    return None


def cmd_discover(out_path, raw_glob="data/raw/*.json", min_reviews=15, max_reviews=160):
    """Merge Maps search exports into a candidate CSV. Drops seen, franchise, suspect and off-trade rows."""
    from .icp import TIMEZONES
    seen_d, seen_p = set(), set()
    if SEEN.exists():
        for s in read(SEEN):
            seen_d.add(s["domain"]); seen_p.add(s["phone"])
    rows, dropped = [], {}
    for f in sorted(ROOT.glob(raw_glob)):
        try:
            blocks = json.loads(f.read_text()).get("data", {}).get("alexandria", [])
        except Exception:
            continue
        for b in blocks:
            for p in (b.get("data") or {}).get("results", []) or []:
                name, site, phone = p.get("name"), p.get("website"), p.get("phone")
                d, ph = domain_of(site), digits(phone)
                rc = p.get("review_count") or 0
                reason = None
                if not site:
                    reason = "no website"
                elif not (min_reviews <= rc <= max_reviews):
                    reason = "review count outside 15-160"
                elif not _industry(p.get("categories")):
                    reason = "not roofing/HVAC"
                elif precheck(name, site):
                    reason = precheck(name, site)
                elif d in seen_d or (ph and ph in seen_p):
                    reason = "duplicate"
                if reason:
                    dropped[reason] = dropped.get(reason, 0) + 1
                    continue
                seen_d.add(d); seen_p.add(ph)
                addr = p.get("address") or ""
                m = re.search(r",\s*([^,]+),\s*([A-Z]{2})\s*\d{5}", addr)
                rows.append({
                    "business_name": name, "website": re.sub(r"\?.*$", "", site), "phone": phone,
                    "city_state": f"{m.group(1)}, {m.group(2)}" if m else addr,
                    "time_zone": TIMEZONES.get(p.get("timezone"), p.get("timezone") or "unknown"),
                    "industry": _industry(p.get("categories")), "google_rating": p.get("rating"),
                    "google_reviews": rc, "feature_id": p.get("feature_id"), "maps_url": p.get("maps_url"),
                })
    write(out_path, rows)
    print(f"{len(rows)} candidates; dropped {dropped}", file=sys.stderr)


def _fp_row(r):
    why = precheck(r.get("business_name"), r.get("website"))
    if why:
        r["precheck_exclude"] = why
        return r
    fp = fingerprint.fingerprint(r["website"])
    r["fp_chat_or_answering"] = ", ".join(fp["chat_or_answering_tools"]) or "none detected"
    r["fp_booking"] = ", ".join(fp["booking_tools"]) or "none detected"
    r["fp_ad_signals"] = ", ".join(fp["ad_and_lead_signals"]) or "none detected"
    r["fp_ad_ids"] = ", ".join(fp.get("ad_ids", [])) or ""
    r["fp_claims_24_7"] = " | ".join(fp["claims_24_7"]) or "none"
    r["fp_live_answering_claim"] = " | ".join(fp["claims_live_answering"]) or "none"
    r["fp_text_us"] = "yes" if fp["text_us_option"] else "no"
    r["fp_contact_form"] = "yes" if fp["contact_form"] else "no"
    r["fp_hours"] = " | ".join(fp["hours_found"]) or "none found"
    r["fp_emails"] = ", ".join(fp["emails"]) or "none found"
    r["fp_owner_mentions"] = ", ".join(fp["owner_mentions"]) or "none found"
    r["fp_install_evidence"] = fp.get("install_evidence", "")
    r["fp_commercial_only"] = "yes" if fp.get("commercial_only") else "no"
    r["fp_founded"] = fp.get("founded", "")
    r["fp_pages"] = " ; ".join(fp["pages_read"])
    r["fp_errors"] = " ; ".join(fp["errors"])
    return r


def cmd_fingerprint(path, workers=24):
    from concurrent.futures import ThreadPoolExecutor
    rows = read(path)
    todo = [r for r in rows if not r.get("fp_pages")]
    with ThreadPoolExecutor(workers) as ex:
        for r in ex.map(_fp_row, todo):
            print(f"{r.get('business_name')}: chat={r.get('fp_chat_or_answering')} | ads={r.get('fp_ad_signals')}",
                  file=sys.stderr)
    write(path, rows)


def cmd_emails(path):
    rows = read(path)
    for r in rows:
        name = (r.get("owner_name") or "").strip()
        parts = [p for p in re.split(r"\s+", re.sub(r"\(.*?\)", "", name)) if p.isalpha()]
        first, last = (parts[0], parts[-1]) if len(parts) >= 2 else (parts[0] if parts else None, None)
        res = emails.resolve_owner_email(first, last, domain_of(r.get("website")))
        r["email_guess"] = res["guess"] or ""
        r["email_guess_status"] = res["guess_status"] or ""
        if res["owner_email"] != "unknown":
            r["owner_email"] = res["owner_email"]
        r["email_status"] = res["email_status"]
        r["needs_enrichment"] = "yes" if res["owner_email"] == "unknown" else "no"
        print(f"{r.get('business_name')}: {res['guess']} -> {res['email_status']}", file=sys.stderr)
    write(path, rows)


def cmd_reviews(path):
    data = json.loads(Path(path).read_text())
    blocks = data.get("data", {}).get("alexandria", data if isinstance(data, list) else [])
    out = []
    for b in blocks:
        tagged = reviews.tag_reviews(b.get("data", {}).get("reviews", []))
        out.append({"feature_id": (b.get("options") or {}).get("feature_id"), "summary": reviews.summarize(tagged),
                    "evidence": tagged})
    print(json.dumps(out, indent=1))


def cmd_dedupe(path):
    rows = read(path)
    seen_d, seen_p = set(), set()
    if SEEN.exists():
        for s in read(SEEN):
            seen_d.add(s["domain"])
            seen_p.add(s["phone"])
    keep, new = [], []
    for r in rows:
        d, p = domain_of(r.get("website")), digits(r.get("phone"))
        if (d and d in seen_d) or (p and p in seen_p):
            print(f"duplicate dropped: {r.get('business_name')}", file=sys.stderr)
            continue
        seen_d.add(d)
        seen_p.add(p)
        keep.append(r)
        new.append({"domain": d, "phone": p, "business_name": r.get("business_name"), "batch": Path(path).name})
    write(path, keep)
    exists = SEEN.exists()
    with open(SEEN, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["domain", "phone", "business_name", "batch"])
        if not exists:
            w.writeheader()
        w.writerows(new)
    print(f"{len(keep)} kept, {len(rows) - len(keep)} duplicates", file=sys.stderr)


def cmd_qualify(path, reviews_map="data/raw/reviews_map.json"):
    """Writes <batch>_qualified.csv (score >= MIN_SCORE) and <batch>_excluded.csv with reasons."""
    from . import qualify
    from .icp import MIN_SCORE
    rows = read(path)
    rmap = ROOT / reviews_map
    ev = qualify.load_reviews(rmap) if rmap.exists() else {}
    good, bad = [], []
    for r in rows:
        why = qualify.disqualify(r)
        if why:
            bad.append({"business_name": r["business_name"], "website": r.get("website"), "reason": why})
            continue
        q = qualify.build(r, ev)
        if q["score"] < MIN_SCORE:
            bad.append({"business_name": r["business_name"], "website": r.get("website"),
                        "reason": f"score {q['score']} < {MIN_SCORE} ({q['score_breakdown']})"})
        else:
            good.append(q)
    good.sort(key=lambda q: -q["score"])
    stem = path[:-4] if path.endswith(".csv") else path
    write(stem + "_qualified.csv", good)
    write(stem + "_excluded.csv", bad)
    c = {k: sum(1 for g in good if g["confidence"] == k) for k in ("high", "medium", "low")}
    print(f"{len(good)} qualified, {len(bad)} excluded; confidence {c}", file=sys.stderr)


def cmd_places(max_requests="2500", tiers="tier1,tier2,tier3"):
    from . import places
    places.run(tuple(tiers.split(",")), int(max_requests))


def cmd_storms(days="90"):
    from . import storms
    print(len(storms.build(int(days))), "counties with storm reports")


def cmd_candidates(out_path):
    from . import leadlists
    leadlists.places_to_candidates(out_path)


def cmd_calllist(cands_path, out_path="out/call_list.csv"):
    from . import leadlists
    leadlists.call_list(cands_path, out_path)


def cmd_emailtargets(cands_path, out_path="out/email_targets.csv", n="4000"):
    from . import leadlists
    leadlists.email_targets(cands_path, out_path, int(n))


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in {"fingerprint", "emails", "reviews", "dedupe", "discover", "qualify", "places", "storms", "candidates", "calllist", "emailtargets"}:
        print(__doc__)
        sys.exit(1)
    globals()[f"cmd_{sys.argv[1]}"](*sys.argv[2:])


if __name__ == "__main__":
    main()
