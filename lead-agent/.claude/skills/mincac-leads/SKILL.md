---
name: mincac-leads
description: Build a batch of Mincac roofing/HVAC leads (missed-call and slow-lead pain) using the lead-agent pipeline. Use when asked for a new lead batch, more leads, or to enrich/score leads.
---

# Mincac lead batch

Follow the stages in `lead-agent/README.md` in order. Rules that never bend:

- Public sources only. Never call, text, email or submit a form for any business.
- Never invent an owner name, email, revenue or headcount. Write `unknown` and lower confidence.
- Every row cites source URLs. Every score point has a reason (`score.py`).
- Batches of 100, deduplicated against `data/seen.csv` by domain and phone.
- Paid enrichment (Clay, Vibe) only after stages 1 to 7, and only after the user approves the quoted credit cost.

## Stage notes

1. **Discover**: `firecrawl_scrape` with up to 7 `firecrawl-maps/businesses/search` calls per request; results over the
   token limit land in a file, so parse with `jq`. Keep 15 to 160 reviews as a small-business proxy. Skip franchises and
   `.homes/.best/.sbs/.site` domains.
2. Write candidates to `lead-agent/out/batchN.csv` with columns business_name, website, phone, city_state, time_zone,
   industry, feature_id. Run `cli.py dedupe` then `cli.py fingerprint`.
3. Disqualify on `fp_live_answering_claim`, a 24/7 answering claim, or chat/answering tools detected.
   "24/7 emergency service" alone is `after_hours_gap: unclear`, not a disqualifier.
4. **Reviews**: `firecrawl-maps/businesses/reviews` with `sort: lowest`, `count: 20`, 10 businesses per call, then
   `cli.py reviews <file>`.
5. **Owner**: site About page, then the state license board and Secretary of State business search (OK CIB roofing
   registry, NC Licensing Board for General Contractors, TN Board for Licensing Contractors, CO SOS, KS SOS, MO SOS,
   NE SOS, GA SOS). Record the registered principal and formation year.
6. **Email**: `cli.py emails`. It guesses `firstnamelastname@domain` and verifies the guess. Only rows marked
   `needs_enrichment=yes` go to Clay or Vibe.
7. **Score** with the rubric in `mincac_leads/icp.py`, keep 55+, and end the reply with high, medium and low counts.

## Volume lists (call list + email list)

Source is the Google Places API (env `GOOGLE_PLACES_API_KEY`), not Firecrawl. Run `lead-agent/run_lists.sh 2500`
(2,500 Text Search requests is about $50-90 after Google's free monthly allowance). It writes:

- `out/call_list.csv`: looser filter, ranked by tier then intent (storm, ads, hours, nochat, small, noweb).
- `out/email_targets.csv`: strict ICP (score 55+) ranked by intent, top 4,000.

Email step for `email_targets.csv`, in this order:
1. Owner name from the site (`fp_owner_mentions`), else Clay `search-contacts` with up to 10 domains per call and
   `select from people where experiences.any(is_current = true and job_title is_similar_to ("owner", "founder", "president")) limit 1 by clay_company_id`.
2. Guess `firstnamelastname@domain` (`cli.py emails`). Verification here needs port 25 or a verifier key.
3. Unverified guesses go to Clay `run_subroutine_direct` "Work Email" (Full Name + Company Domain, up to 1,000 per call;
   charges only when found). Confirm the Clay credit cap with the user before each run.
4. Keep only Clay-verified addresses in the final 1,600.
