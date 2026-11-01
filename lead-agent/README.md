# Mincac lead agent

Finds, verifies and ranks US roofing and HVAC companies (1 to 10 staff, $300K to $1M revenue) that lose jobs because
calls and leads are not answered fast enough. It uses public sources only and never contacts a business: no calls, no
form submissions, no emails sent.

## Pipeline

| Stage | What runs | Tool | Cost |
|---|---|---|---|
| 1. Discover | Maps search per metro and suburb, `"<trade> <city> <ST>"`, 20 results per page | Firecrawl `firecrawl-maps/businesses/search` | 10 credits/page |
| 2. Precheck | Drop franchises, national brands, suspect lead-gen domains, duplicates | `cli.py dedupe`, `icp.FRANCHISE_MARKERS` | free |
| 3. Fingerprint | Read homepage + /about + /contact source: chat, AI receptionist, booking, 24/7 claims, hours, Google Ads tag, Meta Pixel, CallRail, Angi/HomeAdvisor, Google Guaranteed | `cli.py fingerprint` | free |
| 4. Hours | Google Business Profile hours (website hours as fallback) | Bing `businesses/business` or Maps listing | 5 credits |
| 5. Reviews | 20 to 60 lowest-rated reviews, tagged missed_call / no_callback / slow_response / no_estimate / no_show, with quote and URL | Firecrawl `businesses/reviews` then `cli.py reviews` | 10 credits |
| 6. Owner | Name from site, then state license board and Secretary of State filing (also gives founding year), then BBB | Firecrawl scrape of public registries | 5 credits/page |
| 7. Owner email | **Guess `firstnamelastname@domain`, verify. Only if that fails, enrich (Clay or Vibe), then verify.** | `cli.py emails` | free until enrichment |
| 8. Firmographics | Headcount and revenue range, only for rows that pass stages 1 to 7 | Vibe Prospecting or Clay | 1 credit/row, approval first |
| 9. Score | Mincac rubric, one reason per point, confidence | `score.py` | free |
| 10. Output | CSV per batch in `out/`, ledger in `data/seen.csv` so batches never repeat | `cli.py dedupe` | free |

Firmographics overlay: `data/firmo.csv` (Clay company search by domain) feeds verified headcount, revenue bucket,
owner names and hard exclusions into `qualify`. `data/excluded.csv` holds manual exclusions that must persist across
batches. A revenue bucket of $5M+ excludes; a $1M-5M bucket scores 0 revenue points and is flagged.

Paid enrichment runs last, on survivors only. That keeps credit spend at roughly a third of enriching everything up front.

## Why passive detection beats AI test calls

Answering services, AI receptionists, chat and text-back tools all leave script tags or widgets in the page source
(Podium, Birdeye, Hatch, LeadConnector/GHL, Smith.ai, Ruby, Numa, Goodcall, ServiceTitan or Housecall Pro booking and
more in `fingerprint.py`). Reading the source finds them in under a second, at zero cost, without dialing anyone.
Robocalling business lines with an AI voice also carries TCPA exposure, because many owner lines are cell phones.

## Email rule

1. `firstnamelastname@domain`, for example `justinberry@berrygoodheatingandair.com`.
2. Verify with an API (`VERIFIER_PROVIDER` = millionverifier, zerobounce, neverbounce or reoon, plus `VERIFIER_API_KEY`)
   or an SMTP RCPT probe from a machine with outbound port 25. Catch-all domains are detected first and never marked valid.
3. Only rows still unverified go to Clay or Vibe enrichment, and the enriched address is verified again.

Freemail inboxes (gmail.com and similar) skip the pattern. Rows with only an owner first name skip it until stage 6
finds the surname.

## Run

```bash
cd lead-agent
python3 -m mincac_leads.cli discover out/batch3.csv        # merge Maps exports in data/raw/, drop seen + franchises
python3 -m mincac_leads.cli fingerprint out/batch3.csv     # 24 parallel workers, ~2 min per 300 sites
python3 -m mincac_leads.cli qualify out/batch3.csv         # writes _qualified.csv and _excluded.csv with reasons
VERIFIER_PROVIDER=millionverifier VERIFIER_API_KEY=... python3 -m mincac_leads.cli emails out/batch2.csv
```

Discovery, reviews and registry lookups run through the Firecrawl connector inside Claude Code; see
`.claude/skills/mincac-leads/SKILL.md`. `out/` and `data/` are git-ignored because they hold lead lists.
