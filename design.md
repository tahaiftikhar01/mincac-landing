# MinCac.com Revamp — Design Spec (v4)

Status: draft for review, round 4. Nothing in this repo outside this file has
been touched yet. See the companion Artifact for a visual mockup of
everything below.

## Design direction

Two references now. beew.studio (round 1) set the structural/editorial cues:
hairline-divider numbered lists instead of heavy bordered card grids,
borderless pill badges, bold centered statement breaks. techjays.com (round
4, a direct competitor in the same industries, 5 screenshots supplied) set a
higher bar: full-bleed photographic hero, a stat bar, a short philosophy
statement section, and a numbered services list at capability altitude
("Conversational AI," "Data Intelligence"...) rather than tool altitude,
with light pill tags and small abstract graphics instead of colored icon
chips. Round 4 pulls the site toward techjays' polish and positioning using
MinCac's own real capabilities and copy, not techjays' words verbatim.
Keeping MinCac's existing dark theme and brand colors as the default, now
paired with a real light mode too (see Theme toggle below):

- Background: `#06010f` / `#0a0613` (dark) / off-white (light, see below)
- Purple: `#9b87f5`
- Teal: `#00E5B0`
- Fonts: Sora (headings), Inter (body), JetBrains Mono (labels/tags)

**No emoji anywhere on the site.** Every icon is a custom inline-SVG line
icon, single stroke, rounded caps, colored via `currentColor`. The tools
marquee drops its per-item icon chip entirely, clean mono-font text only.

**Honesty constraint on the techjays-style hero**: techjays uses real
photography (people at a desk). Nothing like that exists in this repo, and
inventing a fake "team at work" photo would be dishonest. The hero instead
gets a substantially richer CSS-only treatment (layered mesh gradient plus a
subtle grain texture) rather than the flatter gradient orbs from round 1. If
real photography becomes available, swapping it in later is a small change.

Sections not called out below are unchanged in content from the current live
site (Industries, How It Works) — they get the icon swap and light/dark
tokens applied like everything else, no structural rebuild.

## Problem section (round 4 restyle)

Content unchanged (same 4 pain points), but the per-item treatment loses
the individually bordered, rounded-box-with-colored-icon-circle look you
flagged as reading like a generic SaaS template. Restyled as a simpler
stacked list with thin hairline top borders between items (the same visual
language as the Services rows), icon shown small and muted rather than in
a colored circle badge.

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
- **Round 4 visual upgrade:** richer full-bleed background (layered mesh
  gradient, subtle grain texture, no flat orbs), taller hero, headline set
  larger and heavier, closer to techjays' scale and confidence. Nav becomes
  transparent/overlaid on the hero rather than an immediate solid bar,
  matching the reference. Content stays centered rather than techjays'
  lower-left anchor, a safer structural choice given there's no real photo
  to anchor text against.

## Stat Bar (new, round 4)

A full-width 4-column strip directly after the hero, techjays-style: big
bold numbers, small caps label beneath, thin vertical dividers between
columns, no card backgrounds or borders. Using only numbers already true on
the current site, never inventing figures like techjays' "1B+ people
touched":

```
80+          24/7          5.0          10
Hours Saved  Uptime        Star Rating  Systems Shipped
```

"Systems Shipped" is the current portfolio count. This absorbs the small
stat row that used to live inside the hero, the hero keeps its badge,
headline, sub-copy, and CTAs only.

## Approach Statement (round 6: two-column, moved after Services)

Round 4 had this as a short centered statement between the Stat Bar and the
Marquee. Round 6 replaces that with a two-column layout matching a
screenshot the user sent of techjays' own second statement section
("BUILT FOR YOUR CONTEXT"), moved to sit right after the Services section
(where techjays places their equivalent, directly following their numbered
capability list):

- Left column: small square-bullet eyebrow ("■ Our Approach") above a bold
  headline: **"Built around how your business actually runs, not a
  template."**
- Right column: two short supporting paragraphs, MinCac's own words (not
  techjays' sentences): opens with a "no two operations run the same way"
  framing, explains the approach (scope properly, build it right, hand
  over documentation the client's team can extend).

Plain background (`--bg-primary`), no card or border, generous padding,
matching the reference's restraint.

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

## Services — rebuilt at capability altitude (round 4)

Round 1-3 kept this as a tool-level list (Workflow Automation, Data
Dashboards, Excel Automation...) styled as a beew-style numbered list.
Round 4 explicitly drops that framing (your instruction: remove "Data
Dashboards, Excel Automation, etc.") and rebuilds it at the same
capability/outcome altitude as techjays' own list, using MinCac's real work,
not techjays' category names verbatim. This also **absorbs the old separate
"AI & LLM Solutions" section**, which was creating redundant AI-buzzword
duplication between two sections lower on the page, likely part of what
read as generic. There is now one unified 6-row list:

```
01  Workflow & Process Automation
02  Data Intelligence
03  Custom AI Agents & RAG
04  AI-Powered Workflows
05  Computer Vision
06  Lead Generation & Enrichment
```

Presentation, per row: index number (mono, dim), service name (Sora, bold),
one-line description, then a row of light gray capability-phrase pill tags
underneath (not brand/tool names, matching techjays' abstraction level), and
a small muted abstract line-art graphic at the row's right edge instead of
a colored icon-in-circle chip. Thin `var(--border)` divider between rows.

**01 Workflow & Process Automation** (merges the old Workflow Automation +
CRM Automation) — end-to-end automation across your stack and your CRM,
from lead capture to invoice generation, follow-ups and hygiene included.
Tags: `Cross-Platform Sync`, `CRM Hygiene`, `Follow-Up Automation`

**02 Data Intelligence** (merges the old Data Dashboards + Data Pipeline
Engineering) — real-time dashboards and the pipelines behind them, every
metric live, no more waiting on a report.
Tags: `Real-Time Dashboards`, `Automated Reporting`, `Data Pipelines`

**03 Custom AI Agents & RAG** (merges the old Custom AI Tools service with
the old Custom GPTs/RAG Systems cards) — purpose-built AI agents and
retrieval systems trained on your SOPs and documents, answering questions
like your best employee.
Tags: `Internal Q&A Bots`, `Sales Copilots`, `Document Search`,
`Brief → Spec Automation` (see note below)

**04 AI-Powered Workflows** (the old AI-Powered Workflows + Fine-Tuning &
Integration cards) — LLMs at the decision points in your workflow, triaging
email, extracting invoice data, routing tasks without a human in the loop.
Tags: `Email Triage`, `Invoice Processing`, `Model Integration`

**05 Computer Vision** (unchanged content from round 2) — object detection,
OCR/document extraction, and visual quality inspection built on your own
footage or images.
Tags: `Object Detection`, `OCR & Document Extraction`, `Visual Inspection`

**06 Lead Generation & Enrichment** (unchanged content from round 3, stays
its own row rather than getting folded in, it's a real differentiator tied
to an actual case study) — sourced and enriched targeted lead lists, then
automated the SDR workflow around them and the outbound infrastructure
itself.
Tags: `Lead Sourcing`, `Enrichment`, `Outbound Infra`

"Brief → Spec Automation" references the "brief to spec" skill from your
message, still unverified in this session (see Open items), inferred label
pending your confirmation. Excel Automation is dropped per your explicit
instruction. "VBA," "Apps Script," and other tool/vendor names no longer
appear on this list, capability pills replace them throughout, matching
techjays' more enterprise/premium abstraction level.

## Team

New section (round 2), placed after Services. Three initials-avatar cards
(same visual language as the existing testimonial avatars) with name, role,
and LinkedIn link:

- **Founding Engineer** — linkedin.com/in/mfbadev
- **Managing Partner** — linkedin.com/in/taha12
- **Automation Expert** — linkedin.com/in/moiz-imran-821a0b285

This is also where the existing unused `team-photo.png` asset gets used
(group photo alongside or behind the three cards).

## AI & LLM Solutions — removed as a standalone section (round 4)

This section (round 1-3: Custom GPTs & AI Agents, RAG Systems, AI-Powered
Workflows, Fine-Tuning & Integration, plus Computer Vision added in round
2) is gone as its own section. Its content now lives inside the unified
Services list above (rows 03-05), removing the redundant AI-buzzword
duplication between two separate sections that was part of what read as
generic/templated.

## Portfolio ("Our Work") — 10 cards, now a slider

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

**10. Lead Generation & Outbound Infrastructure — Augmented Squad**
Tag: `Lead Generation`
"Built and enriched lead lists, automated the SDR workflow around them, and
generated and configured the outbound inboxes Augmented Squad (and MinCac
itself) send from." This is the case study behind the existing Tauseef
Rehman testimonial ("ran outbound campaigns using Sales Navigator"), which
previously had no matching portfolio card.
Metrics: `Multi-Company` / Inbox Infrastructure, `SDR` / Workflow Automated
(qualitative, no invented numbers)

**Pending from you (push to the repo):** real screenshots for Scoop Plus,
Approvent, and Navo (card 10 doesn't need one, it's process/infrastructure
work, uses the same clean placeholder treatment). Placeholder cards use a
solid brand-gradient panel with just the project name, no "pending"
callout, no camera icon, reads as intentional rather than unfinished.

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

## Round 5 — light by default, hero copy, dot pattern, Industries dropdown

Direct feedback on the round 4 artifact: "that services structure works,
keep it. the reviews and portfolio look good" (no changes there), "I dont
want the black theme anymore, looks really unprofessional," the hero
headline/subhead read as "very mehh nothing impressive," a request for the
dot pattern from a reference screenshot, and an "Industries" nav dropdown
like techjays'.

**On the tech stack worry** ("Idk if all of this is even possible in html,
go in node.js or next.js"): everything asked for here, dropdowns, dot
patterns, sliders, theme toggles, is plain CSS and vanilla JavaScript. None
of it needs a framework or rewrite. Moving to Next.js would mean new build
tooling, a new hosting setup, and weeks of migration for zero visual
difference, not something to take on for this.

- **Light is now the default theme everywhere**, ignoring OS dark-mode
  preference (the earlier `prefers-color-scheme` auto-detection is
  removed, a deliberate choice given "I don't want the black theme
  anymore" was unambiguous). The dark/light toggle from round 2 still
  exists for anyone who wants dark, it's just no longer what greets a
  first-time visitor.
- **Hero and nav are the one deliberate exception**, frozen permanently
  dark regardless of the toggle, matching techjays' own pattern (their
  hero is a dark photo, their content sections below are white). This
  keeps the dramatic "moment" the mesh gradient and grain were built for
  in round 4, without the rest of the site reading as "black theme."
- **New hero headline and subhead**, the old sentence-length copy read
  flat: **"Automation that never sleeps."** / "AI agents and workflows that
  answer every call, book every appointment, and sync to your CRM. Live in
  5 to 7 days, running 24/7." ("Live in 5 to 7 days" is real copy already
  on the current live site's meta description, not a new claim.)
- **Halftone dot-grid pattern** added to the hero, layered over the mesh
  gradient, masked so it concentrates toward one side rather than covering
  the whole hero uniformly, matching the reference screenshot.
- **Industries dropdown in the nav**, hover (and tap, for touch devices)
  reveals the 8 industries as a two-column panel, each linking to the
  existing Industries section further down the page (there aren't
  separate per-industry pages on a single-page site, so this deep-links to
  the same section rather than fragmenting into subpages).

## Copy direction: techjays.com

You named techjays.com as a close competitor whose copy you like and want
this site to move toward. Couldn't fetch it directly, blocked by this
sandbox's network policy (same issue as beew.studio). Since reading a pasted
screenshot doesn't need file access (only vision), the same route that
worked for the beew.studio design reference works here for copy, paste
screenshots of the techjays.com sections/copy you specifically like and this
gets refined against them directly. In the meantime, this pass tightens
copy generally toward shorter, more confident, outcome-led sentences,
concrete verbs, less hedging, applied lightly across section intros rather
than rewriting everything blind.

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
6. Which tools/platforms to credit on the new Lead Generation & Enrichment
   service tag (Apollo, Clay, Instantly, Sales Navigator, something else).
7. Confirm or correct what the "brief to spec" skill actually does, it
   couldn't be found in this session to verify.
8. Screenshots of the techjays.com copy/sections you specifically like, so
   the writing pass can be matched to them directly rather than a general
   tightening guess. (Partially addressed: round 4 got structural/visual
   screenshots, still no specific copy call-outs.)
9. Real photography, if you have any (team at work, office), so the hero
   can use a real image instead of the CSS-only treatment.
10. Confirm the new 6-row Services structure (merging Services with the old
    AI/LLM section, dropping tool-brand tags for capability pills) actually
    matches how you want MinCac positioned, this is the biggest content
    judgment call in round 4.

## Round 7 — shipped to index.html

Your reply after six rounds of Artifact review was "Continue," read as
sign-off to move from the Artifact-review loop into the real implementation
step. `index.html` and `audit/index.html` now match the round-6 Artifact:
light-default theme with the hero and nav frozen dark, new hero copy and
dot pattern, Stat Bar, Services rebuilt as the 6-row capability list, the
two-column Approach Statement after Services, Team section (using
`team-photo.png`), Institutions strip, Industries nav dropdown, Fit Check
section and the Quote Estimation Calculator nav button removed, every
Calendly link fixed to `tahaiftikhar1991`, the portfolio grid as a 10-card
right-to-left slider (6 real screenshots plus 4 new placeholder cards),
testimonials as a left-to-right slider, the "Free Build" form reframed to
the "Let's Talk" consultation section with its original validation/submit
logic intact, and the theme toggle, Industries dropdown, and both slider
tracks wired up in JS. The Artifact's review-only scaffolding (preview
ribbon, dashed review-note boxes) didn't ship, obviously.

Verified locally with a headless browser: nav (desktop and mobile,
including the Industries submenu on both), the theme toggle, both sliders,
the consultation form's validation path, and the chat widget. One real bug
turned up and got fixed in the process: the mobile Industries submenu
inherited the desktop dropdown's `transform: translateX(-50%)` (a
higher-specificity selector than the mobile override), which pushed the
whole submenu off-screen to the left, invisible, on phones. Also swept the
file for leftover em dashes, `#fit` references, emoji, and stale Calendly
links, all clean.

Open items 1, 2, 3, 6, 7, and 9 above are still genuinely open (real
portfolio screenshots, real NUST/IBA logos, real draft-testimonial
attribution, lead-gen tool credits, brief-to-spec confirmation, real
photography), items 4-5 and 10 were effectively settled by rounds 3-6's
review and this implementation pass; item 8 (techjays copy screenshots) got
partially addressed in round 4 and folded into the copy throughout.
