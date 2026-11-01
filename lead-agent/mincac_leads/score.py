"""Apply the Mincac rubric to one lead record. Every point carries a reason string."""
from .icp import WEIGHTS as W, MIN_SCORE


def score(lead):
    """lead keys used:
    employees_verified (int|None), employees_estimated_small (bool),
    revenue_status ('verified'|'estimated'|'out_of_range'|None),
    aov_evidence (str), after_hours ('yes'|'unclear'|'weak'|'no'),
    speed ('yes'|'form_only'|'partial'|'no'), lead_spend_evidence (str), owner_name (str)
    """
    pts, why = 0, []

    def add(n, reason):
        nonlocal pts
        pts += n
        why.append(f"+{n} {reason}")

    e = lead.get("employees_verified")
    if e is not None and 1 <= e <= 5:
        add(W["team_1_5"], f"team {e} verified")
    elif e is not None and 6 <= e <= 10:
        add(W["team_6_10"], f"team {e} verified")
    elif lead.get("employees_estimated_small"):
        add(W["team_estimated_small"], "team <=10 estimated from proxies")

    rs = lead.get("revenue_status")
    if rs == "verified":
        add(W["revenue_verified"], "revenue verified in range")
    elif rs == "estimated":
        add(W["revenue_estimated"], "revenue estimated in range")

    if lead.get("aov_evidence"):
        add(W["aov"], "AOV > $1,000 evidence")

    ah = lead.get("after_hours")
    add({"yes": W["after_hours_yes"], "unclear": W["after_hours_unclear"], "weak": W["after_hours_weak"]}.get(ah, 0),
        f"after-hours gap: {ah}")

    sp = lead.get("speed")
    add({"yes": W["speed_yes"], "form_only": W["speed_form_only"], "partial": W["speed_partial"]}.get(sp, 0),
        f"speed-to-lead gap: {sp}")

    if lead.get("lead_spend_evidence") and lead["lead_spend_evidence"] != "none found":
        add(W["lead_spend"], "paid-lead evidence")
    if lead.get("owner_name") and lead["owner_name"] != "unknown":
        add(W["owner_contact"], "owner named")

    why = [w for w in why if not w.startswith("+0 ")]
    return {"score": pts, "qualifies": pts >= MIN_SCORE, "score_breakdown": "; ".join(why)}


def confidence(lead):
    """high: verified team or revenue AND owner AND cited pain review. low: key size facts unknown."""
    verified = lead.get("employees_verified") is not None or lead.get("revenue_status") == "verified"
    pain = bool(lead.get("review_evidence"))
    owner = lead.get("owner_name") not in (None, "", "unknown")
    if verified and owner and pain:
        return "high"
    if (owner or pain) and lead.get("after_hours") in ("yes", "unclear"):
        return "medium"
    return "low"
