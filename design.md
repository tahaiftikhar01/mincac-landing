# MinCac.com Revamp — Design Spec (v2)

Status: draft for review, round 2. Nothing in this repo outside this file has
been touched yet. See the companion Artifact for a visual mockup of
everything below.

## Design direction

Reference: beew.studio (screenshot supplied). Borrowing the structural/
editorial cues, not the light color scheme: hairline-divider numbered lists
instead of heavy bordered card grids, borderless pill badges, bold centered
statement breaks, tighter more confident type. Keeping MinCac's existing dark
theme and brand colors as the default, now paired with a real light mode too
(see Theme toggle below):

- Background: `#06010f` / `#0a0613` (dark) / off-white (light, see below)
- Purple: `#9b87f5`
- Teal: `#00E5B0`
- Fonts: Sora (headings), Inter (body), JetBrains Mono (labels/tags)

**No emoji anywhere on the site.** Every icon (services, industries, AI/LLM
cards, problem list, chat widget, star ratings, theme toggle) is a custom
inline-SVG line icon, single stroke, rounded caps, colored via `currentColor`
so it inherits purple/teal per context. The tools marquee drops its per-item
icon chip entirely, clean mono-font text only.

Sections not called out below are unchanged in content from the current live
site (Problem, Industries, How It Works) — they get the icon swap and light/
dark tokens applied like everything else, no structural rebuild.

## Nav

- Remove the "Quote Estimation Calculator" button (was linking to
  `scorecard.html`). `scorecard.html` stays live in the repo, just unlinked
  from the main nav.
- Fix the "Book a Call" link to `https://calendly.com/tahaiftikhar1991/30min`
  (was `taha-mincac`, a stale duplicate). Same fix applied on `/audit`.
- Add a light/dark theme toggle (sun/moon SVG icon button), see Theme toggle
  section.
- Logo, "Work" / "Problems" links stay. "Fit Check" link removed (section is
  being removed, see below).

## Hero

- Remove the border on the "AI Agents & Automation · Always On" badge pill,
  keep the soft background blur, drop `border: 1px solid var(--border)`.
- Replace the headline. Three options, no em dashes in any of them:

  **A.** "Built to replace the busywork, not the people who matter."
  **B.** "Your team does the thinking. We build what does the rest."
  **C.** "The work that shouldn't need a human anymore, automated."

  Artifact mockup uses **Option A** as the working default, swap freely.

- **Primary CTA becomes "Book a Call"**, linking straight to Calendly,
  replacing "Get a Free AI Audit" in the hero's top slot. This puts the main
  conversion action at the top of the page instead of only appearing in the
  final CTA section. The AI audit chatbot isn't going away, it's still one
  click away via the "Try Our AI" floating widget and reachable from the
  nav. Secondary hero button stays "See Our Work".
- "I build the AI agents..." sub-copy becomes "We build the AI agents...",
  see the We voice section below.
- The final CTA section near the bottom of the page gets a matching update
  so it isn't the only place a real Book a Call ask lives, and drops "free":
  **CTA update:** "Ready to get the busywork off your plate?" / "Book a
  30-minute strategy call."

## Never say "free"

Every instance reworded, it reads as a discount/cheap signal rather than a
premium one:

- Hero CTA: "Get a Free AI Audit" → folded into the "Book a Call" change
  above; the audit funnel keeps its own copy on the `/audit` page and the
  chat widget, reworded there too ("Start Your AI Audit", no "free").
- The "Free Build" offer section is reframed entirely, see next section.
- Final CTA: "Book a free 30-minute strategy call" → "Book a 30-minute
  strategy call."
- Success-state and footnote copy: "No credit card, no commitment, you keep
  the build regardless" → replaced, see next section.

## "Free Build" section → "Let's Talk" consultation section

The lead-capture form itself stays (name, email, company, industry, tools,
process, hours, it's genuinely useful pipeline data), but the entire
framing around it changes from a giveaway to a consultation ask:

- Section label: "Special Offer" → "Get Started"
- Header: "We'll build your first automation for free" → "Let's talk about
  your first automation"
- Sub-copy: "Tell us your most annoying manual process..." → "Tell us your
  biggest bottleneck. We'll show you exactly how to automate it, no
  obligation."
- Form header: "Request your free build" → "Tell us what's slowing you down"
- Submit button: "Request Your Free Build →" → "Request a Consultation →"
- Footer note: "No credit card · No commitment · You keep the build
  regardless" → "No pressure · No sales pitch · Just a real conversation"
- Success state: "You're in. We're on it." stays (doesn't reference "free"),
  its next-steps copy swaps "build" language for "automation plan" /
  "consultation" language where it currently says "build."

## Services (heaviest beew influence)

Replace the 6-card grid with a numbered, hairline-divider list, matching
beew's "01 / 02 / 03..." services pattern, same 6 services and copy, new
presentation, each row an SVG line icon instead of an emoji:

```
01   Workflow Automation         n8n · Make · Zapier           [svg icon]
02   Data Dashboards             Power BI · Tableau · Looker    [svg icon]
03   Custom AI Tools             OpenAI · LangChain · RAG       [svg icon]
04   CRM Automation              HubSpot · Salesforce           [svg icon]
05   Excel Automation            VBA · Apps Script · Python     [svg icon]
06   Data Pipeline Engineering   PostgreSQL · Snowflake · dbt   [svg icon]
```

Large index number (mono font, dim), service name (Sora, bold), one-line
description, tool tags trailing right, thin `var(--border)` divider between
rows, no card background/border.

## Team

New section, placed after Services and before AI/LLM Solutions. Three
initials-avatar cards (same visual language as the existing testimonial
avatars) with name, role, and LinkedIn link:

- **Founding Engineer** — linkedin.com/in/mfbadev
- **Managing Partner** — linkedin.com/in/taha12
- **Automation Expert** — linkedin.com/in/moiz-imran-821a0b285

This is also where the existing unused `team-photo.png` asset gets used
(group photo alongside or behind the three cards).

## AI & LLM Solutions — adds Computer Vision

The existing 4 cards (Custom GPTs & AI Agents, RAG Systems, AI-Powered
Workflows, Fine-Tuning & Integration) stay as-is, plus a 5th:

**Computer Vision** — object detection, OCR/document extraction, and visual
quality inspection built on your own footage or images. Use-case tags:
`Object Detection`, `OCR & Document Extraction`, `Visual Inspection`.

"Etc" in the brief is scoped to Computer Vision only for now, more
capabilities can be added once named.

## Portfolio ("Our Work") — 9 cards, now a slider

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

**Pending from you (push to the repo):** real screenshots for all three.
Placeholder cards use a clean solid brand-gradient panel with just the
project name, no "pending" callout, no camera icon, reads as intentional
rather than unfinished.

**Now a slider**, same auto-scroll/pause-on-hover mechanism as testimonials,
moving **right to left** (testimonials move left to right, see below, this
is the opposite direction on purpose). Portfolio images zoom in slightly on
card hover (`transform: scale(1.08)` on the image, `overflow: hidden` on its
container), applied to all 9 cards.

## Testimonials — interactive slider, left to right

Static 2x2 grid becomes a continuously auto-scrolling, **left-to-right**
slider (pauses on hover, same mechanism powering the tools marquee).
Correcting a bug from the first mockup: that version's track actually
animated right-to-left despite the original ask, this version genuinely
flows left to right, opposite of the portfolio slider above. Two kinds of
cards ride the same track:

1. **4 existing full testimonials** — unchanged text/attribution (Shopify
   Profitability Dashboard client, Eberly & Collard PR, Tauseef Rehman,
   Shayan Malik).
2. **5 verified review chips** (compact format: name, country, star rating,
   recency, quote only where given, star icons are SVG not emoji):
   - rodrigoarajoei — Portugal — 5 stars — 2 years ago — $50 project, 1 day
     delivery
   - selizal — United States — 5 stars — 3 years ago — "Patient and helpful.
     Will come back again."
   - stanleyoltin — United States — 5 stars — 3 years ago
   - omerrehman — United States — 5 stars — 3 years ago

**Not included, needs your input before it can go live:** the 5 "DRAFT 1-5"
template quotes from the brief (general / documentation / technical depth /
short and punchy / responsiveness). They still carry literal
`[Name]`, `[Role]`, `[Company]` placeholders, no real client was attached to
any of them, so publishing them as real testimonials isn't something done on
my own. Send real attribution for any of these you want live and they can be
added to the slider in the same pass as the new portfolio screenshots.

## Institutions we've worked with

New logo strip (name/positioning similar to the tools marquee, but for
institutions, not tools), crediting NUST and IBA since several final-year
projects were built with them. **Pending from you (push to the repo):** the
actual logo files, images pasted directly into chat don't land as files this
session can read from disk. Placeholder uses text wordmarks ("NUST",
"IBA") in the same slot until the real logos arrive.

## Theme toggle (dark/light, real feature)

Nav gets a sun/moon SVG icon button. Preference stored in `localStorage`,
defaults to the visitor's OS `prefers-color-scheme` if nothing is stored.
Full light-mode palette designed alongside the existing dark one:

- Light background: warm off-white (`#FAF9F7`) rather than pure white
- Light surface/card: `#FFFFFF` with a soft `rgba(0,0,0,0.06)` border
- Light text: near-black (`#171321`) primary, muted grey-purple secondary
- Purple and teal accents stay the same hex values in both themes, verified
  for contrast against both grounds (teal in particular needs a slightly
  deeper shade on light backgrounds to stay legible, `#00A382` rather than
  `#00E5B0` for text/icon use on light surfaces, the brighter teal stays for
  large fills/gradients)

Every color in the CSS moves onto tokens (`--bg`, `--surface`, `--text-1`,
`--text-2`, `--border`, etc.) so light and dark are just two value sets for
the same tokens, not two parallel stylesheets.

## Fit Check — removed

The "Is this right for you?" section (`#fit`) and its nav link are removed
entirely, per your instruction that it's not important.

## Quote Estimation Calculator — removed from nav

Nav button removed. `scorecard.html` itself stays in the repo (not deleted),
just no longer linked from the main nav.

## We, not I

Sweeping every first-person-singular reference to first-person-plural,
consistent with now having a named 3-person team on the page: hero sub-copy
("I build the AI agents..." → "We build the AI agents..."), and anywhere
else "I" shows up as the site's voice.

## Unchanged, kept exactly as-is

- "Try Our AI" floating chat button + panel
- Logo (nav + footer)
- Footer links: `hello@mincac.com`, LinkedIn, Book a Call
- Copyright line
- Marquee tool strip content (icons removed, see Design direction)

## Copy rules applied throughout

- No em dashes in any new or touched copy, commas, periods, or parentheses
  instead. Existing `&mdash;` / `—` occurrences already in `index.html` body
  copy get swept to match in the implementation pass.
- No emoji anywhere, see Design direction.
- No "free," see above.
- First person plural ("we"), not singular ("I").

## Open items for you

1. Real screenshots for Scoop Plus, Approvent, Navo (portfolio cards 7-9),
   push into the repo (agreed approach).
2. Real NUST and IBA logo files, push into the repo (agreed approach).
3. Real name / role / company for any of the 5 draft testimonials you want
   published.
4. Pick a hero headline (A/B/C above, or a variant) during Artifact review.
5. Confirm the "Book a Call" hero-primary interpretation is what you meant
   by "top instead of last page," this was inferred from a terse note.
