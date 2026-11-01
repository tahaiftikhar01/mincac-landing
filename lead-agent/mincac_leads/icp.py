"""Mincac ICP rules and scoring rubric. Edit weights here, nowhere else."""

WEIGHTS = {
    "team_1_5": 20,
    "team_6_10": 12,
    "team_estimated_small": 12,   # proxies say <=10 but no verified headcount
    "revenue_verified": 15,
    "revenue_estimated": 8,
    "aov": 15,
    "after_hours_yes": 20,
    "after_hours_unclear": 10,
    "after_hours_weak": 5,        # hours run late (after 8pm)
    "speed_yes": 15,
    "speed_form_only": 8,
    "speed_partial": 5,           # has booking or text, but no instant reply
    "lead_spend": 10,
    "owner_contact": 5,
}
MIN_SCORE = 55
MAX_EMPLOYEES = 10
REVENUE_MIN, REVENUE_MAX = 300_000, 1_000_000

# Brands, franchises and roll-ups to drop on sight (lowercase substrings of name or domain).
FRANCHISE_MARKERS = [
    "mighty dog", "bumble roofing", "priority roofing", "premier roofing", "mr. roof", "mr roof",
    "one hour heating", "onehourheatandair", "aire serv", "service experts", "ars rescue", "rescue rooter",
    "shamrock roofing", "bone dry roofing", "elite roof and solar", "the cool roofing company",
    "roofing by mccann", "home pride", "pyramid contractors", "benjamin franklin", "mister sparky",
    "bluefrog", "five star roof", "storm guard", "dryer vent wizard", "goettl", "lennox stores",
    "sears home", "power home remodeling", "window nation", "leaffilter",
]

# Rank-and-rent / lead-gen sites with no verifiable operator.
SUSPECT_TLDS = (".homes", ".best", ".sbs", ".lovable.app", ".site")

FREEMAIL = {"gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "aol.com", "icloud.com",
            "live.com", "msn.com", "comcast.net", "att.net", "sbcglobal.net", "bellsouth.net"}

TIMEZONES = {"America/New_York": "ET", "America/Detroit": "ET", "America/Chicago": "CT",
             "America/Denver": "MT", "America/Phoenix": "MT", "America/Boise": "MT",
             "America/Los_Angeles": "PT"}
