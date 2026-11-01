"""Passive website fingerprinting.

Answers, without contacting the business:
  - is there live chat / AI receptionist / instant text-back already installed?
  - is there online booking?
  - does the site claim 24/7 answering?
  - are Google Ads or Meta ad pixels installed (evidence of paid lead spend)?
  - published hours, emails, owner mentions.

This replaces "AI test calls": the tools that answer phones and chats leave
script tags and widgets in the page source.
"""
import re
import requests

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0 Safari/537.36"}

# name -> regex over raw HTML. Keep patterns specific to script hosts / widget ids.
CHAT_AND_ANSWERING = {
    "Podium": r"podium\.com|podiumwebchat",
    "Birdeye": r"birdeye\.com",
    "Hatch": r"usehatchapp\.com|hatchapp",
    "LiveChat": r"livechatinc\.com|cdn\.livechat",
    "Intercom": r"widget\.intercom\.io|intercomcdn",
    "Drift": r"js\.driftt\.com|drift\.com/",
    "Tidio": r"tidio\.co|tidiochat",
    "Tawk": r"embed\.tawk\.to",
    "Zendesk Chat": r"zopim|static\.zdassets\.com",
    "HubSpot Chat": r"js\.usemessages\.com|hs-scripts",
    "GoHighLevel/LeadConnector": r"leadconnectorhq\.com|msgsndr\.com|widgets\.leadconnector",
    "Smith.ai": r"smith\.ai",
    "Ruby": r"ruby\.com/|callruby",
    "AnswerConnect": r"answerconnect",
    "Numa": r"numa\.com",
    "Goodcall": r"goodcall\.com",
    "Rosie": r"heyrosie\.com",
    "Avoca": r"avoca\.ai",
    "Signpost": r"signpost\.com",
    "Kenect": r"kenect\.com",
    "Facebook Messenger chat": r"fb-customerchat|customerchat\.js",
    "Weave": r"getweave\.com|weave\.com/",
}
BOOKING = {
    "ServiceTitan scheduler": r"servicetitan|scheduler\.servicetitan",
    "Housecall Pro booking": r"housecallpro\.com|book\.housecallpro",
    "Jobber request form": r"getjobber\.com|clienthub\.getjobber",
    "Workiz": r"workiz\.com",
    "Calendly": r"calendly\.com",
    "Acuity": r"acuityscheduling\.com",
    "Square Appointments": r"squareup\.com/appointments",
    "Service Fusion": r"servicefusion",
    "FieldEdge": r"fieldedge",
}
AD_PIXELS = {
    "Google Ads conversion tag": r"AW-\d{6,}",
    "Google Ads call tracking": r"googleadservices\.com|_googWcmGet",
    "Meta Pixel": r"connect\.facebook\.net/[^\"']*/fbevents\.js|fbq\(['\"]init",
    "CallRail (call tracking)": r"callrail\.com|cdn\.callrail",
    "Angi/HomeAdvisor profile": r"angi\.com/companylist|homeadvisor\.com/(rated|ratings|sp/)",
    "Thumbtack badge": r"thumbtack\.com",
    "Google Guaranteed / LSA": r"google[ _-]?guaranteed|ads\.google\.com/local-services",
    "Nextdoor pixel": r"ads\.nextdoor\.com",
}
CLAIM_247 = re.compile(r"24\s*/\s*7|24\s*hours? a day|open 24|24[- ]hour (?:emergency|service|availability)|"
                       r"around the clock|24 hours,? 7 days", re.I)
INSTALL = re.compile(r"(?:roof|system|ac|a/c|air conditioner|air conditioning|furnace|heat pump|hvac|unit|equipment)s?\s+"
                     r"(?:replacements?|installations?|installs?|replace)|(?:replacement|new) (?:roofs?|systems?|furnaces?|ac\b|"
                     r"air conditioners?|heat pumps?)|re-?roof(?:ing)?|\binstallations?\b|\breplacements?\b", re.I)
COMMERCIAL = re.compile(r"commercial|industrial", re.I)
RESIDENTIAL = re.compile(r"residential|homeowner|your home|home ?owners", re.I)
FOUNDED = re.compile(r"(?:since|established|est\.?|founded(?: in)?)\s+((?:19|20)\d{2})|(\d{1,2})\+?\s+years? (?:of )?(?:experience|in business|serving)", re.I)
AD_ID = re.compile(r"AW-\d{6,}|fbq\(['\"]init['\"],\s*['\"](\d{8,})")
LIVE_ANSWER = re.compile(r"(live|real) (person|human)s? answer|answering service|call center|never miss a call", re.I)
HOURS = re.compile(
    r"((?:mon(?:day)?|tue(?:s(?:day)?)?|wed(?:nesday)?|thu(?:rs(?:day)?)?|fri(?:day)?|sat(?:urday)?|sun(?:day)?)\.?"
    r"(?:\s*(?:-|–|—|to|through|thru)\s*(?:mon|tue|wed|thu|fri|sat|sun)[a-z]*\.?)?[\s,:]*"
    r"\d{1,2}(?::\d{2})?\s*(?:am|a\.m\.|a)\s*(?:-|–|—|to)\s*\d{1,2}(?::\d{2})?\s*(?:pm|p\.m\.|p)\b)", re.I)
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_NM = r"[A-Z][a-z]+(?:\s(?:Mc|Mac|O')?[A-Z][a-z]+)+"
OWNER = re.compile(r"(?:owner|founder|president|ceo|proprietor)[,:\s-]+(?:is\s+)?(" + _NM + r")"
                   r"|(" + _NM + r")[,\s-]+(?:owner|founder|president)", re.M)
TEXT_US = re.compile(r"text us|sms:|text (?:or call|\(?\d{3})", re.I)


def fetch(url, timeout=20):
    r = requests.get(url, headers=UA, timeout=timeout, allow_redirects=True)
    r.raise_for_status()
    return r.url, r.text


def _hits(table, html):
    return sorted(name for name, pat in table.items() if re.search(pat, html, re.I))


def _visible_text(html):
    html = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", html)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))


def fingerprint(url, extra_paths=("/about", "/about-us", "/contact", "/contact-us")):
    """Fetch homepage plus a few subpages and return evidence dict. Never submits forms."""
    pages, errors = {}, []
    try:
        final, html = fetch(url)
        pages[final] = html
        base = re.match(r"https?://[^/]+", final).group(0)
        for p in extra_paths:
            try:
                u, h = fetch(base + p, timeout=12)
                if u not in pages:
                    pages[u] = h
            except Exception:
                pass
    except Exception as e:
        errors.append(f"{url}: {e}")
    raw = "\n".join(pages.values())
    text = _visible_text(raw)
    emails = sorted({e.lower() for e in EMAIL.findall(text)
                     if not e.lower().endswith((".png", ".jpg", ".webp", ".svg", "sentry.io", "wixpress.com"))})
    owners = sorted({(a or b).strip() for a, b in OWNER.findall(text)})
    return {
        "pages_read": list(pages),
        "errors": errors,
        "chat_or_answering_tools": _hits(CHAT_AND_ANSWERING, raw),
        "booking_tools": _hits(BOOKING, raw),
        "ad_and_lead_signals": _hits(AD_PIXELS, raw),
        "claims_24_7": sorted({m.group(0) for m in CLAIM_247.finditer(text)})[:5],
        "claims_live_answering": sorted({m.group(0) for m in LIVE_ANSWER.finditer(text)})[:3],
        "text_us_option": bool(TEXT_US.search(raw)),
        "contact_form": bool(re.search(r"<form", raw, re.I)),
        "hours_found": sorted({m.strip() for m in HOURS.findall(text)})[:6],
        "emails": emails[:10],
        "owner_mentions": owners[:5],
        "install_evidence": " | ".join(sorted({m.group(0).lower() for m in INSTALL.finditer(text)})[:4]),
        "commercial_only": bool(COMMERCIAL.search(text)) and not RESIDENTIAL.search(text),
        "founded": next((m.group(0) for m in FOUNDED.finditer(text)), ""),
        "ad_ids": sorted({m.group(0) if m.group(0).startswith("AW-") else "MetaPixel " + m.group(1)
                          for m in AD_ID.finditer(raw)})[:4],
    }
