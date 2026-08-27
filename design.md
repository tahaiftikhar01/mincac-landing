# MinCac.com Revamp — Design Spec

Status: draft for review. Nothing in this repo outside this file has been
touched yet. See the companion Artifact for a visual mockup of everything
below.

## Design direction

Reference: beew.studio (screenshot supplied). Borrowing the structural/
editorial cues, not the light color scheme: hairline-divider numbered lists
instead of heavy bordered card grids, borderless pill badges, bold centered
statement breaks, tighter more confident type. Keeping MinCac's existing dark
theme and brand colors as-is:

- Background: `#06010f` / `#0a0613`
- Purple: `#9b87f5`
- Teal: `#00E5B0`
- Fonts: Sora (headings), Inter (body), JetBrains Mono (labels/tags)

Sections NOT called out below are unchanged from the current live site
(Problem, AI/LLM Solutions, Industries, How It Works, Free Build form, Footer)
— light polish only (e.g. slightly softer borders to match the less-boxy
feel), no structural rebuild.

## Nav

- Remove the "Quote Estimation Calculator" button (was linking to
  `scorecard.html`). `scorecard.html` stays live in the repo, just unlinked
  from the main nav.
- Fix the "Book a Call" link to `https://calendly.com/tahaiftikhar1991/30min`
  (was `taha-mincac`, a stale duplicate). Same fix applied on `/audit`.
- Logo, "Work" / "Problems" links stay. "Fit Check" link removed (section is
  being removed, see below).

## Hero

- Remove the border on the "AI Agents & Automation · Always On" badge pill —
  keep the soft background blur, drop `border: 1px solid var(--border)`.
- Replace the headline. Three options, no em dashes in any of them:

  **A.** "Built to replace the busywork, not the people who matter."
  **B.** "Your team does the thinking. We build what does the rest."
  **C.** "The work that shouldn't need a human anymore, automated."

  Artifact mockup uses **Option A** as the working default — swap freely.
  The CTA-section headline near the bottom of the page gets a matching
  update so it doesn't still say "robot work":

  **CTA update:** "Ready to get the busywork off your plate?"

- Everything else in the hero (sub-copy, stat row, both CTA buttons, orbs/
  grid background) stays as-is.

## Services (heaviest beew influence)

Replace the 6-card grid with a numbered, hairline-divider list, matching
beew's "01 / 02 / 03..." services pattern — same 6 services, same copy,
new presentation:

```
01   Workflow Automation         n8n · Make · Zapier          [icon]
02   Data Dashboards             Power BI · Tableau · Looker   [icon]
03   Custom AI Tools             OpenAI · LangChain · RAG      [icon]
04   CRM Automation              HubSpot · Salesforce          [icon]
05   Excel Automation            VBA · Apps Script · Python    [icon]
06   Data Pipeline Engineering   PostgreSQL · Snowflake · dbt  [icon]
```

Each row: large index number (mono font, dim), service name (Sora, bold),
one-line description beneath on hover/expand or always-visible on desktop,
tool tags trailing right, thin `var(--border)` divider between rows, no card
background/border. Section header copy unchanged.

## Portfolio ("Our Work") — 9 cards total

Keep the existing 6 cards exactly as they are (same images, copy, metrics).
Append 3 new cards in the same `.portfolio-card` format:

**7. Scoop Plus** — scoopplus.ca
Tag: `Web Development`
"Built the kiosk-facing interface for Scoop Plus's supplement vending
machines, the ordering and payment flow customers use directly at the
machine."
Metrics: `Live` / Kiosk Deployment, `Vending` / Hardware-Integrated

**8. Approvent**
Tag: `Shopify · E-Commerce`
"Shopify storefront built on Liquid. Focused on the subscription models and
discount logic that let Approvent run recurring orders and promotions
without manual setup per customer."
Metrics: `Shopify` / Platform, `Subscriptions` / Core Build

**9. Navo Intelligence Dashboard**
Tag: `Data Dashboard`
"Add a part, see every tariff that applies to it. A lookup dashboard that
turns tariff research from a manual search into an instant answer."
Metrics: `Instant` / Tariff Lookup, `Parts Database` / Core Feature

**Pending from you:** real screenshots for all three. The Artifact uses
labeled placeholder blocks in the exact card dimensions; final `index.html`
implementation swaps in the real images once you send them (same treatment
as the other 6 — `object-fit: cover`, same aspect ratio).

## Testimonials — interactive slider

Convert from the static 2x2 grid into a continuously auto-scrolling,
left-to-right slider (pauses on hover, same mechanism already powering the
tools marquee at the top of the page). Two kinds of cards ride the same
track:

1. **4 existing full testimonials** — unchanged text/attribution (Shopify
   Profitability Dashboard client, Eberly & Collard PR, Tauseef Rehman,
   Shayan Malik).
2. **5 verified review chips** (compact format: name, country, star rating,
   recency, quote only where given):
   - rodrigoarajoei — Portugal — ★★★★★ — 2 years ago — $50 project, 1 day
     delivery
   - selizal — United States — ★★★★★ — 3 years ago — "Patient and helpful.
     Will come back again."
   - stanleyoltin — United States — ★★★★★ — 3 years ago
   - omerrehman — United States — ★★★★★ — 3 years ago

**Not included — needs your input before it can go live:** the 5 "DRAFT 1-5"
template quotes from the brief (general / documentation / technical depth /
short and punchy / responsiveness). They still carry literal
`[Name]`, `[Role]`, `[Company]` placeholders — no real client was attached to
any of them, so publishing them as real testimonials isn't something I'll do
on my own. Send real attribution for any of these you want live and they can
be added to the slider in the same pass as the new portfolio screenshots.

## Fit Check — removed

The "Is this right for you?" section (`#fit`) and its nav link are removed
entirely, per your instruction that it's not important.

## Quote Estimation Calculator — removed from nav

Nav button removed. `scorecard.html` itself stays in the repo (not deleted),
just no longer linked from the main nav.

## Unchanged, kept exactly as-is

- "Try Our AI" floating chat button + panel
- Logo (nav + footer)
- Footer links: `hello@mincac.com`, LinkedIn, Book a Call
- Copyright line
- Free Build form section (offer, form fields, success state)
- Marquee tool strip

## Copy rule applied throughout

No em dashes in any new or touched copy — commas, periods, or parentheses
instead. Existing `&mdash;` / `—` occurrences already in `index.html` body
copy get swept to match in the implementation pass.

## Open items for you

1. Real screenshots for Scoop Plus, Approvent, Navo (portfolio cards 7-9).
2. Real name / role / company for any of the 5 draft testimonials you want
   published.
3. Pick a hero headline (A/B/C above, or a variant) during Artifact review.
