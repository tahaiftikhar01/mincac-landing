"""Tag review text with the pains Mincac sells against. Keeps the quote and URL as evidence."""
import re

TAGS = {
    "missed_call": r"(never|didn'?t|did not|wouldn'?t|won'?t|no one) (answer|pick(ed)? up)|went (straight )?to voicemail|"
                   r"voicemail|voice mail|never answered my calls|unanswered|no answer",
    "no_callback": r"(never|didn'?t|did not|wouldn'?t|no one) (call(ed)?|got) (me )?back|never returned|"
                   r"didn'?t return (my )?call|no call ?back|still waiting (for|on) a call",
    "slow_response": r"did not receive a response until|took (\d+|several|a few) (days|weeks) to (respond|call)|"
                     r"slow to respond|hard to reach|hard to get a ?hold|couldn'?t (reach|get a ?hold)|"
                     r"no response|lack of response|unresponsive|ghost(ed)?",
    "no_estimate": r"never (got|received|had) (an |the |my )?(estimate|quote|bid)|estimate never|quote never|"
                   r"call(ed)? .{0,40} to see when I would receive the quote",
    "no_show": r"no[- ]show|never showed|stood me up|didn'?t show|did not show|did not even show",
    "after_hours": r"after hours|weekend|sunday|saturday|at night|evening|emergency line",
}
COMPILED = {k: re.compile(v, re.I) for k, v in TAGS.items()}


def tag_reviews(reviews, max_rating=3):
    """reviews: iterable of dicts with text, rating, review_url, relative_time."""
    out = []
    for r in reviews:
        t = (r.get("text") or "").replace("<br>", " ")
        if not t or (r.get("rating") or 5) > max_rating:
            continue
        tags = [k for k, rx in COMPILED.items() if rx.search(t)]
        if tags and tags != ["after_hours"]:
            out.append({"tags": tags, "rating": r.get("rating"), "when": r.get("relative_time"),
                        "quote": t[:240], "url": r.get("review_url")})
    return out


def summarize(tagged):
    s = {k: 0 for k in TAGS}
    for t in tagged:
        for k in t["tags"]:
            s[k] += 1
    return s
