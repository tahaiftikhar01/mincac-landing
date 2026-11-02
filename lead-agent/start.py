#!/usr/bin/env python3
"""One command to check your Google key and build the Mincac call list + email targets.

    python3 start.py              # read key from clipboard, validate, confirm, run everything
    python3 start.py --check      # only validate the key and do one real test search
    python3 start.py --quick      # validate, then a small 40-request run to inspect the output first
    python3 start.py --yes        # skip the confirmation prompt
    python3 start.py --max-requests 1500

The key is read from your clipboard (or GOOGLE_PLACES_API_KEY if already set), is never printed or
written to disk, and is passed only to the child processes this script starts.
Runs are resumable: re-run the same command and finished searches are skipped.
"""
import argparse
import getpass
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("The 'requests' package is missing. Run:  python3 -m pip install --user requests")

HERE = Path(__file__).resolve().parent
URL = "https://places.googleapis.com/v1/places:searchText"
KEY_RE = re.compile(r"^AIza[0-9A-Za-z_\-]{35}$")
SERPER_RE = re.compile(r"^[0-9A-Za-z]{24,64}$")
PROVIDER = "google"


def read_clipboard():
    cmds = []
    if platform.system() == "Darwin":
        cmds = [["pbpaste"]]
    elif platform.system() == "Windows":
        cmds = [["powershell", "-NoProfile", "-Command", "Get-Clipboard"]]
    else:
        cmds = [["xclip", "-selection", "clipboard", "-o"], ["xsel", "--clipboard", "--output"],
                ["wl-paste"]]
    for c in cmds:
        if shutil.which(c[0]):
            try:
                out = subprocess.run(c, capture_output=True, text=True, timeout=10).stdout
                return out.strip().strip("\"'")
            except Exception:
                pass
    return ""


def get_key(ask=False):
    envname = "SERPER_API_KEY" if PROVIDER == "serper" else "GOOGLE_PLACES_API_KEY"
    kre = SERPER_RE if PROVIDER == "serper" else KEY_RE
    key = "" if ask else os.environ.get(envname, "").strip()
    src = f"the {envname} variable"
    if ask:
        key = getpass.getpass("Paste the key and press Enter (input is hidden): ").strip().strip("\"'")
        src = "the hidden prompt"
    elif not key:
        key, src = read_clipboard(), "your clipboard"
    if not kre.match(key) and sys.stdin.isatty():
        print("The clipboard does not hold an API key (you may have copied a command since).")
        key = getpass.getpass("Copy the key again, paste it here and press Enter (input is hidden): ").strip().strip("\"'")
        src = "the hidden prompt"
    if not key:
        sys.exit("Nothing found. Copy your API key (Google Cloud > APIs & Services > Credentials > Show key), "
                 "then run this again.")
    if not kre.match(key):
        why = []
        if PROVIDER == "google" and not key.startswith("AIza"):
            why.append("it does not start with 'AIza'")
        if PROVIDER == "google" and len(key) != 39:
            why.append(f"it is {len(key)} characters long (a Google API key is 39)")
        if PROVIDER == "serper" and not 24 <= len(key) <= 64:
            why.append(f"it is {len(key)} characters long (a Serper key is about 40 letters and numbers)")
        if re.search(r"\s", key):
            why.append("it contains spaces or line breaks (you may have copied more than the key)")
        sys.exit(f"The text in {src} does not look like a Google API key: " + "; ".join(why) +
                 ".\nCopy the key again and re-run.")
    return key, src


def check_key(key):
    """One real search. Returns (ok, message)."""
    try:
        r = requests.post(URL, timeout=30, json={"textQuery": "roofing contractor in Omaha, NE", "pageSize": 3},
                          headers={"X-Goog-Api-Key": key, "X-Goog-FieldMask": "places.id,places.displayName"})
    except requests.RequestException as e:
        return False, f"Could not reach Google ({e.__class__.__name__}). Check your internet connection."
    if r.status_code == 200:
        names = [p["displayName"]["text"] for p in r.json().get("places", [])]
        return True, f"Key works. Test search returned: {', '.join(names) or 'no results'}"
    try:
        err = r.json()["error"]
    except Exception:
        return False, f"Unexpected reply {r.status_code}: {r.text[:200]}"
    reason = next((d.get("reason") for d in err.get("details", []) if d.get("reason")), "")
    msg = err.get("message", "")
    fixes = {
        "API_KEY_INVALID": "Google says this key is invalid. Copy it again from Credentials > Show key.",
        "API_KEY_SERVICE_BLOCKED": "The key is restricted to other APIs. Edit the key > API restrictions > tick 'Places API (New)'.",
        "SERVICE_DISABLED": "Places API (New) is not enabled in the key's project. Enable it in APIs & Services > Library.",
        "API_KEY_HTTP_REFERRER_BLOCKED": "Key has a website restriction. Edit the key > Application restrictions > None.",
        "API_KEY_IP_ADDRESS_BLOCKED": "Key has an IP restriction. Edit the key > Application restrictions > None.",
        "BILLING_DISABLED": "Billing is not active on this project. Link a billing account under Billing.",
    }
    hint = fixes.get(reason) or ("Billing may not be linked to this project (Billing > check the project has an "
                                  "active billing account)." if r.status_code == 403 else "")
    return False, f"Google replied {r.status_code} {err.get('status', '')} {reason}: {msg}\n  Fix: {hint}"


def diagnose(key):
    """Send the same key to several Google APIs and print exact replies (key text is scrubbed)."""
    def scrub(t):
        return str(t).replace(key, "KEY")

    def show(label, r):
        try:
            j = r.json()
        except Exception:
            j = {"raw": r.text[:200]}
        e = j.get("error") if isinstance(j.get("error"), dict) else None
        if e:
            reasons = [d.get("reason") for d in e.get("details", []) if isinstance(d, dict) and d.get("reason")]
            out = f"{e.get('status')} {reasons or ''} | {e.get('message')}"
        else:
            out = f"{j.get('status', '')} | {j.get('error_message', '') or ('ok' if r.status_code == 200 else j)}"
        print(f"  {label:<34} HTTP {r.status_code}: {scrub(out)[:330]}")
        return r.status_code, scrub(out)

    print("\nDiagnosis (same key, different Google APIs):")
    res = {}
    body = {"textQuery": "roofing contractor in Omaha, NE", "pageSize": 1}
    hdr = {"X-Goog-FieldMask": "places.id"}
    res["places_header"] = show("Places (New), key in header", requests.post(URL, json=body, timeout=30, headers={**hdr, "X-Goog-Api-Key": key}))
    res["places_query"] = show("Places (New), key in URL", requests.post(URL, params={"key": key}, json=body, timeout=30, headers=hdr))
    res["geocode"] = show("Geocoding API", requests.get("https://maps.googleapis.com/maps/api/geocode/json", params={"address": "Omaha NE", "key": key}, timeout=30))
    res["places_legacy"] = show("Places legacy text search", requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json", params={"query": "roofing Omaha", "key": key}, timeout=30))
    msgs = " ".join(v[1].lower() for v in res.values())
    print("\nReading:")
    if "billing" in msgs:
        print("  Billing is the problem. Open console.cloud.google.com/billing, link an active billing account to the "
              "project that owns this key, wait 2 minutes and re-run.")
    elif res["geocode"][0] == 200 and "ok" in res["geocode"][1].lower()[:12] and res["places_header"][0] != 200:
        print("  The key works for other Google APIs but Places (New) rejects it. Edit the key: set API restrictions "
              "to 'Don't restrict key' and Application restrictions to None, save, wait 2 minutes, re-run. If it then "
              "works, re-restrict to Places API (New).")
    elif res["places_header"][0] == 403 and "caller does not have permission" in res["places_header"][1].lower():
        print("  The key is valid and reaches Google, but Google refuses it for Places (New) with no reason given.")
        print("  Check in this order, waiting 2 minutes and re-running after each change:")
        print("   1. Billing: console.cloud.google.com/billing > the project that owns this key must be listed under")
        print("      an ACTIVE billing account (not closed, not 'unlinked').")
        print("   2. Key settings: edit the key > API restrictions = 'Don't restrict key', Application restrictions = None.")
        print("   3. Try your other key: python3 start.py --ask --diagnose (paste the 'Maps Platform API Key').")
    elif "not authorized" in msgs or "has not been used" in msgs or "disabled" in msgs:
        print("  Places API (New) is not enabled in the project that owns this key. Open APIs & Services > Library, "
              "check the project name at the top is the one that created the key, and click Enable on Places API (New).")
    elif "invalid" in msgs:
        print("  Google says the key text is invalid. Copy it again from Credentials > Show key.")
    else:
        print("  No clear single cause. Send the four lines above to Claude.")


def run(args, env, label):
    print(f"\n=== {label} ===", flush=True)
    t = time.time()
    p = subprocess.run([sys.executable, "-m", "mincac_leads.cli", *args], cwd=HERE, env=env)
    if p.returncode != 0:
        sys.exit(f"Step '{label}' failed (exit {p.returncode}). Fix the error above and re-run: finished work is kept.")
    print(f"({time.time() - t:.0f}s)", flush=True)


def count(path):
    p = HERE / path
    return sum(1 for _ in open(p)) - 1 if p.exists() else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="validate the key only")
    ap.add_argument("--quick", action="store_true", help="40-request trial run")
    ap.add_argument("--diagnose", action="store_true", help="explain why Google rejects the key")
    ap.add_argument("--provider", choices=["google", "serper"], default="google")
    ap.add_argument("--ask", action="store_true", help="ignore the clipboard and type/paste the key at a hidden prompt")
    ap.add_argument("--yes", action="store_true", help="skip confirmation")
    ap.add_argument("--max-requests", type=int, default=2500)
    ap.add_argument("--tiers", default="tier1,tier2,tier3")
    a = ap.parse_args()
    global PROVIDER
    PROVIDER = a.provider

    key, src = get_key(a.ask)
    if PROVIDER == "serper":
        from_path = str(HERE)
        sys.path.insert(0, from_path)
        from mincac_leads import serper
        print(f"Read a key from {src} (...{key[-4:]}). Testing it with Serper...")
        ok, msg, credits = serper.check(key)
        print(("OK: " if ok else "FAILED: ") + msg)
        if ok and credits is not None:
            print(f"Credits used by that test: {credits}")
        if not ok:
            sys.exit(1)
    else:
        print(f"Read a key from {src} (AIza...{key[-4:]}). Testing it with Google...")
        ok, msg = check_key(key)
        print(("OK: " if ok else "FAILED: ") + msg)
        if not ok or a.diagnose:
            diagnose(key)
        if not ok:
            sys.exit(1)
    if a.check:
        return

    n = 40 if a.quick else a.max_requests
    if PROVIDER == "serper":
        print(f"\nPlan: up to {n} Serper search requests (each uses Serper credits; the free signup credits are "
              f"about 2,500), then check every website, then build the call list and email targets.")
    else:
        print(f"\nPlan: up to {n} Places searches (about ${n * 0.032:.0f} at list price), then check every website, "
              f"then build the call list and email targets.")
    if not a.yes and input("Start? [y/N] ").strip().lower() != "y":
        sys.exit("Cancelled. Nothing was spent.")

    (HERE / "data" / "raw").mkdir(parents=True, exist_ok=True)
    (HERE / "out").mkdir(exist_ok=True)
    env = {**os.environ, "SERPER_API_KEY" if PROVIDER == "serper" else "GOOGLE_PLACES_API_KEY": key}
    run(["storms", "90"], env, "1/6 NOAA storm reports (hail and wind, last 90 days)")
    run(["serper" if PROVIDER == "serper" else "places", str(n), a.tiers], env, f"2/6 Maps search (cap {n} requests)")
    run(["candidates", "out/places_candidates.csv"], env, "3/6 Clean, de-duplicate, drop franchises")
    run(["fingerprint", "out/places_candidates.csv"], env, "4/6 Check each website for chat, 24/7, ads (slowest step)")
    run(["calllist", "out/places_candidates.csv", "out/call_list.csv"], env, "5/6 Build call list")
    run(["emailtargets", "out/places_candidates.csv", "out/email_targets.csv", "4000"], env, "6/6 Build email targets")

    print("\nDone.")
    print(f"  Call list     : {HERE / 'out' / 'call_list.csv'}  ({count('out/call_list.csv')} rows)")
    print(f"  Email targets : {HERE / 'out' / 'email_targets.csv'}  ({count('out/email_targets.csv')} rows)")
    print("Before dialing: scrub the call list against the National Do Not Call registry and dial manually.")


if __name__ == "__main__":
    main()
