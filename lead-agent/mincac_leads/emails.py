"""Owner email: guess first, verify, enrich only on failure.

Order (per Mincac lead-gen playbook):
  1. Guess firstnamelastname@domain  (e.g. justinberry@berrygoodheatingandair.com)
  2. Verify the guess.
  3. Only if the guess is not "valid": enrich from a paid source (Clay / Vibe), then verify that.

Verification backends, tried in order:
  - "api": an email-verification API if VERIFIER_PROVIDER + VERIFIER_API_KEY are set
           (millionverifier | zerobounce | neverbounce | reoon)
  - "smtp": direct RCPT TO probe on port 25 (works from a VPS / your own machine;
            blocked in most cloud sandboxes). Detects catch-all domains first.
  - fallback: MX check only -> status "unverified_mx_ok" (NOT counted as valid).

A domain on a freemail host (gmail.com etc.) cannot use the pattern; it is skipped.
No email is ever sent. RCPT probes end with QUIT before DATA.
"""
import os
import random
import re
import smtplib
import socket
import string
import unicodedata

import requests

from .icp import FREEMAIL


def _clean(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z]", "", s.lower())


def guess(first, last, domain):
    """Primary pattern only: firstnamelastname@domain."""
    if not (first and last and domain):
        return None
    domain = domain.lower().removeprefix("www.")
    if domain in FREEMAIL:
        return None
    f, l = _clean(first), _clean(last)
    return f"{f}{l}@{domain}" if f and l else None


def mx_hosts(domain):
    r = requests.get("https://dns.google/resolve", params={"name": domain, "type": "MX"}, timeout=10)
    ans = r.json().get("Answer", [])
    hosts = sorted((int(a["data"].split()[0]), a["data"].split()[1].rstrip(".")) for a in ans if a.get("type") == 15)
    return [h for _, h in hosts]


def _smtp_rcpt(host, addr, helo="verify.mincac.local", sender="postmaster@mincac.com"):
    s = smtplib.SMTP(host, 25, timeout=15)
    try:
        s.ehlo(helo)
        if s.has_extn("starttls"):
            s.starttls()
            s.ehlo(helo)
        s.mail(sender)
        code, _ = s.rcpt(addr)
        return code
    finally:
        try:
            s.quit()
        except Exception:
            pass


_PORT25 = None


def _port25_open():
    global _PORT25
    if _PORT25 is None:
        try:
            socket.create_connection(("gmail-smtp-in.l.google.com", 25), timeout=6).close()
            _PORT25 = True
        except OSError:
            _PORT25 = False
    return _PORT25


def verify_smtp(addr):
    domain = addr.split("@")[1]
    if not _port25_open():
        hosts = mx_hosts(domain)
        return {"status": "unverified_mx_ok" if hosts else "invalid", "reason": "port 25 blocked; MX " +
                (hosts[0] if hosts else "missing"), "method": "dns", "mx": hosts[0] if hosts else None}
    hosts = mx_hosts(domain)
    if not hosts:
        return {"status": "invalid", "reason": "no MX", "method": "dns"}
    junk = "".join(random.choices(string.ascii_lowercase, k=14)) + "@" + domain
    try:
        if _smtp_rcpt(hosts[0], junk) == 250:
            return {"status": "catch_all", "reason": "domain accepts any address", "method": "smtp", "mx": hosts[0]}
        code = _smtp_rcpt(hosts[0], addr)
    except (socket.timeout, OSError, smtplib.SMTPException) as e:
        return {"status": "unverified_mx_ok", "reason": f"smtp unreachable: {e.__class__.__name__}", "method": "dns",
                "mx": hosts[0]}
    status = "valid" if code == 250 else "invalid" if code in (550, 551, 553) else "unknown"
    return {"status": status, "reason": f"RCPT {code}", "method": "smtp", "mx": hosts[0]}


def verify_api(addr):
    p, key = os.environ.get("VERIFIER_PROVIDER", "").lower(), os.environ.get("VERIFIER_API_KEY")
    if not (p and key):
        return None
    if p == "millionverifier":
        j = requests.get("https://api.millionverifier.com/api/v3/", params={"api": key, "email": addr}, timeout=30).json()
        raw = j.get("result")
        m = {"ok": "valid", "invalid": "invalid", "catch_all": "catch_all", "disposable": "invalid"}
    elif p == "zerobounce":
        j = requests.get("https://api.zerobounce.net/v2/validate", params={"api_key": key, "email": addr}, timeout=30).json()
        raw = j.get("status")
        m = {"valid": "valid", "invalid": "invalid", "catch-all": "catch_all", "spamtrap": "invalid", "abuse": "invalid"}
    elif p == "neverbounce":
        j = requests.get("https://api.neverbounce.com/v4/single/check", params={"key": key, "email": addr}, timeout=30).json()
        raw = j.get("result")
        m = {"valid": "valid", "invalid": "invalid", "catchall": "catch_all", "disposable": "invalid"}
    elif p == "reoon":
        j = requests.get("https://emailverifier.reoon.com/api/v1/verify",
                         params={"email": addr, "key": key, "mode": "power"}, timeout=60).json()
        raw = j.get("status")
        m = {"safe": "valid", "valid": "valid", "invalid": "invalid", "catch_all": "catch_all", "disposable": "invalid"}
    else:
        return {"status": "unknown", "reason": f"unsupported provider {p}", "method": "api"}
    return {"status": m.get(raw, "unknown"), "reason": f"{p}: {raw}", "method": "api"}


def verify(addr):
    return verify_api(addr) or verify_smtp(addr)


def resolve_owner_email(first, last, domain, enrich_fn=None):
    """Guess -> verify -> (only on failure) enrich -> verify. Returns a dict for the output row."""
    g = guess(first, last, domain)
    out = {"guess": g, "guess_status": None, "owner_email": "unknown", "email_status": "not attempted",
           "enriched": False}
    if not g:
        out["email_status"] = ("skipped: freemail domain" if domain and domain.lower() in FREEMAIL
                               else "skipped: owner first and last name required")
        return out
    v = verify(g)
    out["guess_status"] = v["status"]
    if v["status"] == "valid":
        out.update(owner_email=g, email_status=f"verified ({v['method']}: {v['reason']})")
        return out
    if v["status"] == "catch_all":
        out["email_status"] = "catch-all domain: guess unverifiable"
    elif v["status"] == "unverified_mx_ok":
        out["email_status"] = f"guess not verified ({v['reason']}); needs verifier API or port 25"
    else:
        out["email_status"] = f"guess failed ({v['reason']})"
    if enrich_fn:
        found = enrich_fn(first, last, domain)
        if found:
            v2 = verify(found)
            out.update(owner_email=found, enriched=True,
                       email_status=f"enriched, {v2['status']} ({v2['method']}: {v2['reason']})")
    return out
