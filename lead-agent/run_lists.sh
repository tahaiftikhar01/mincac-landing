#!/usr/bin/env bash
# Build the call list and email targets. Needs Places auth: Network secret (X-Goog-Api-Key) or GOOGLE_PLACES_API_KEY.
# Usage: ./run_lists.sh [max_places_requests]
set -euo pipefail
cd "$(dirname "$0")"
MAX=${1:-2500}
python3 start.py --yes  # preferred: checks your clipboard key, then runs every step below
python3 -m mincac_leads.cli storms 90
python3 -m mincac_leads.cli places "$MAX" tier1,tier2,tier3
python3 -m mincac_leads.cli candidates out/places_candidates.csv
python3 -m mincac_leads.cli fingerprint out/places_candidates.csv 2> data/fp_places_log.txt
python3 -m mincac_leads.cli calllist out/places_candidates.csv out/call_list.csv
python3 -m mincac_leads.cli emailtargets out/places_candidates.csv out/email_targets.csv 4000
