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

## Round 8 — first image upload attempt, none usable yet

You pushed 4 "thumbnail.png" files and 3 "logo.md" files to `main`
(`skoopless-thumbnail.png`, `navo-thumbnail.png`,
`golden-artist-colors-thumbnail.png`, `pupproven-thumbnail.png`,
`IBA.md`, `Nust logo.md`, `DMCR logo.md`). None of the 7 contain real
image data, GitHub's "Create new file" editor doesn't commit a pasted
image, it commits a markdown `<img>` tag pointing at a
`github.com/user-attachments/assets/...` CDN link (one, `pupproven`,
didn't even finish uploading before the file was saved). This session's
network policy blocks that CDN domain outright, so those links aren't
fetchable from here either way. Real fix: re-upload via "Add file →
Upload files" on the repo's file browser, that path commits the actual
binary.

Confirmed via AskUserQuestion while sorting out the filenames:
- `skoopless-thumbnail` is the **Scoop Plus** portfolio screenshot.
- `DMCR` is a **third institution logo**, alongside NUST and IBA (needs
  the actual logo file, plus institution strip CSS currently only
  supports the two text wordmarks, will need updating for 3 logos as
  real image files, sizing included).
- `pupproven` is a **new, 11th portfolio case study**, not previously
  scoped anywhere in this project. Still need: what MinCac actually built
  for it, and any real metrics/description, alongside the real screenshot.
- **Golden Artist stays skipped**, confirmed again, not going on the site.

Updated open-items list (supersedes items 1 and 2 above):
1. Real screenshots, as actual uploaded binaries: Scoop Plus (skoopless),
   Approvent, Navo, Augmented Squad, plus pupproven once its project
   details are known.
2. Real logo files, as actual uploaded binaries: NUST, IBA, DMCR.
3. Pupproven's project description, MinCac's actual work on it, any real
   metrics, for its portfolio card copy.

**Shipped from this round**: added `DMCR` as a third text wordmark next to
NUST and IBA in the `.inst-strip` section, that part didn't need a real
image file, matches the existing NUST/IBA styling. Still a placeholder
wordmark, not a real logo, item 2 above still stands, now for the logo
files themselves rather than the missing third entry.

## Round 9 — real screenshots land, Scoop Plus and Navo wired in

First upload attempt via GitHub's "Create new file" editor (round 8)
produced text wrappers around a CDN link, not real images. The user tried
again the same way for `navo-thumbnail.png` and it got worse, editing it
through the web editor emptied it to 1 byte. Explained the actual
mechanism (that editor can't carry binary content through any path,
period) and walked through the correct one, "Add file → Upload files."

That worked: commit `a99ccfe` added `golden-artist-colors-upwork-
thumbnail.png`, `navo-upwork-thumbnail.png`, and `skoopless-upwork-
thumbnail.png` as real 1600x1200 PNGs (confirmed with `file`, not just
extension). Wired the Scoop Plus and Navo portfolio cards to their real
screenshots (`f07f35e`), replacing the gradient placeholders. Both images
are polished marketing thumbnails (big title, tagline, feature pills,
layered app screenshot) rather than plain product screenshots, so a
straight `object-fit: cover` crop was cutting through the title text.
Added a `.thumb-crop` class (`object-position: center 60%`) that biases
the crop toward the actual app screenshot instead, since the title is
already repeated in the card's own `<h3>` right below the image.

Also used the real copy visible in those thumbnails to sharpen both card
descriptions in the previous round (`15ddaeb`): Scoop Plus is specifically
a custom supplement *builder* (mix your own pre/post-workout blends, live
nutrition facts and pricing), not just a generic ordering flow; Navo's
dashboard rolls up duty exposure and landed cost from BOMs and import
history.

Golden Artist's thumbnail also arrived in that same upload but stays off
the site, per the standing "skip it" decision, confirmed twice now.

Updated open-items list (supersedes the previous one):
1. Real screenshots still needed: Approvent, Augmented Squad, plus
   pupproven once its project details are known.
2. Real logo files still needed: NUST, IBA, DMCR.
3. Pupproven's project description and any real metrics, still nothing
   confirmed for it beyond the name.

## Round 10 — real institution logos land, all four wired in

Another proper upload via "Add file → Upload files" (commit `57e7040` on
`main`) landed `NUST logo.png`, `IBA Logo.png`, `DMCR logo.png`, and a
new one not previously scoped anywhere in this project, `BNU logo.png`
(Beaconhouse National University). Confirmed via AskUserQuestion that BNU
should join the strip as a fourth institution, same footing as the other
three.

Replaced all three text wordmarks with the real logo images
(`81c8001`). The four logos have very different aspect ratios and brand
colors (NUST's blue circular seal, IBA's maroon square mark, BNU's black
line art, DMCR's teal/gray wordmark), so they're shown at a fixed height,
in grayscale by default with a hover-to-color reveal, for a clean, unified
"trusted by" strip instead of four clashing brand colors side by side.

Updated open-items list (supersedes the previous one):
1. Real screenshots still needed: Approvent, Augmented Squad, plus
   pupproven once its project details are known.
2. Institution logos: done, all four real.
3. Pupproven's project description and any real metrics, still nothing
   confirmed for it beyond the name.

## Round 11 — Augmented Squad logo, PupProven ships, Industries expands

Another proper upload (commit `c4d218e` on `main`) landed the Augmented
Squad brand logo and a completed `pupproven-upwork-thumbnail.png` (the
earlier attempt never finished). Wired both in (`9eff18e`):

- **Augmented Squad**: since this case study is services/outbound work,
  not a built product UI, used the client logo on a plain white card
  instead of the usual full-bleed screenshot crop. The uploaded logo
  itself had a "transparency preview" checkerboard flattened into solid
  opaque pixels (confirmed via alpha channel, uniformly 255, no real
  transparency), an export artifact, not something that would disappear
  in a browser. Thresholded the light checker tones to true white in
  place before using it.
- **PupProven**: shipped as an 11th portfolio card (previously confirmed
  as "add it," not skipped). Real copy used from its own thumbnail: "Pet
  Supplement Storefront," a subscription bundle-builder for a pet
  supplement brand. Updated the "systems shipped" stat and work-section
  copy from ten to eleven.

Separately, the user pasted techjays.com's full site copy and said "we do
everything that techjays does." Two of techjays' claims are business
claims, not just copy, so checked both before touching anything:

- **Outcome-based pricing** ("you pay for results, if we don't deliver
  you don't pay"): confirmed this is **not** MinCac's actual model, free
  scoping/consultation calls, but build work is paid regardless of
  outcome. Not added, the current site already doesn't claim this.
- **Industries list**: confirmed expand to match techjays even without
  matching portfolio evidence, since this is a positioning choice, not a
  claim about specific past client work. Added Manufacturing, Field
  Services, Distribution & Logistics, Financial Services, and PE
  Portfolio Companies (13 industries total now), in both the Industries
  section grid and the nav dropdown (widened to 3 columns). New icons:
  factory, truck, upward trend chart. `4c93101`.

Still declining to copy techjays' own tagline ("The AI Reimagination
Company") verbatim, consistent with the round-4 decision not to copy
their proprietary positioning language, structural/stylistic inspiration
only.

Updated open-items list (supersedes the previous one):
1. Real screenshots still needed: Approvent, plus pupproven's project
   description would sharpen its card further (shipped with only the
   thumbnail's own visible copy so far).
2. That's it, everything else from prior rounds is done.

## Round 12 — institution logo transparency fix

User reported the live NUST, IBA, BNU, and DMCR logos "are not coloured,
and dont even have the transparent logo... dont blend into the Background."
Diagnosed: all four PNGs had zero real alpha transparency (confirmed via
`alpha.getextrema()` returning `(255, 255)`), with a flat near-white
background baked into fully opaque pixels, the same class of export bug
as the Augmented Squad logo fixed in Round 11, just not caught for these
four at upload time.

DMCR had a second, sneakier version of the same bug: a checkerboard
"transparent" preview pattern from the design tool was flattened into
literal opaque pixels, including inside enclosed shapes like the "D"
counter, where a plain border-flood-fill can't reach it (the counter
isn't connected to the image's outer edge). Fixed with a two-pass approach:
a border-connected flood-fill for the real outer background, plus a
second pass that finds connected components matching the checkerboard's
two-color signature (roughly balanced mix of the two colors, not a
solid fill) and clears those too, wherever they sit. This deliberately
leaves NUST's white ring/lettering, IBA's white icon, and BNU's white
accent lines untouched, since those are uniform solid fills, not
alternating checker noise, verified pixel-by-pixel and via rendered
comparisons on both the light and dark theme backgrounds.

Also removed the `filter: grayscale(1); opacity: 0.65;` on
`.inst-logo-img` (and its hover override) added back in Round 10, since
that was actively fighting the "not coloured" complaint. Logos now show
their real brand colors at all times, full opacity on hover.

Note: BNU's own logo is solid black, so on the (non-default) dark theme
toggle it reads faint against the dark strip. That's the real logo's own
color, not a bug worth "fixing" by recoloring their mark.

Pushed as `444d017` on a freshly-restarted `claude/mincac-revamp-xori1l`
(PR #1 had already merged, so the branch was reset to `origin/main` first
per the standard "treat a merged branch as done" rule, then this commit
added on top).

## Round 13 — new brand mark

User uploaded a new "Mincac logo" PNG directly to `main` via GitHub's
Add file → Upload files flow (the correct method this time, confirmed a
real 1.5MB binary with genuine alpha transparency, not the fake-checker
bug seen in earlier rounds). It's a redesigned mark: a more dimensional
teal/white "M" built from two overlapping shapes (one reading as a
stylized pen nib), white "mincac" wordmark underneath, same white/teal
palette family as the outgoing mark, meant for a dark background exactly
like the one it replaces.

Cropped its transparent margin and saved it in place as
`mincac-logo-transparent.png`, the exact filename already referenced by
the nav logo, footer logo, and favicon link on every page (`index.html`,
`audit/index.html`, `scorecard.html`, `free-build.html`), so the swap
takes effect everywhere with no HTML changes. Removed the stray
no-extension "Mincac logo" upload artifact now that its content lives in
the proper file. Left `mincac-logo-web.png` and `audit/mincac-logo.png`
(a separate avatar image) alone, out of scope for this swap.

## Round 14 — Artifact approved, real implementation: testimonials, services, industry pages

User said "Continue" after reviewing the updated Artifact (testimonials cleanup,
Work-section n8n/MinCac removal, widened Services rows, Law Firms template).
Same reading as Round 7's "Continue": approval to move from the Artifact
review loop into real implementation. Applied everything to `index.html`
directly:

- **Testimonials**: removed the "Verified Upwork Review" / "LinkedIn
  Recommendation" badges and all 5 generic review chips (rodrigoarajoei,
  selizal, stanleyoltin, omerrehman) from both the primary and duplicate
  slider sets. Renamed Tauseef Rehman &rarr; Augmented Squad (avatar "AG")
  and Shayan Malik &rarr; Dial Zero, Authorized Meta Partner (avatar "DZ"),
  keeping their exact quotes. Removed the now-dead `.testimonial-badge` and
  `.review-chip` CSS.
- **Work section**: removed the "MinCac Automation Audit Bot" (n8n) card
  from both slider copies, dropping the portfolio count from 11 to 10.
  Updated the stat bar ("11" &rarr; "10" Systems Shipped) and the section's
  own copy ("Eleven systems" &rarr; "Ten systems") to match.
- **Services widened** (the CVision-inspired capability breadth, in
  MinCac's own words, no client or project named): Data Intelligence now
  explicitly mentions legacy data modernization, Custom AI Agents &amp; RAG
  now explicitly mentions voice and conversational agents (replacing the
  never-confirmed "Brief &rarr; Spec Automation" tag), Lead Generation &amp;
  Enrichment now explicitly mentions AI-driven outreach agents. Same
  positioning move as the Round-11 Industries expansion: a capability claim,
  not a specific client outcome.
- **13 industry pages, for real**: built `industries/*.html` (clinics,
  law-firms, e-commerce, marketing-agencies, construction, b2b-saas,
  real-estate, consultants, manufacturing, field-services,
  distribution-logistics, financial-services, pe-portfolio), each a
  self-contained static page (matching the site's existing pattern of
  `audit/index.html`, `scorecard.html`, `free-build.html` each carrying
  their own trimmed CSS rather than importing a shared stylesheet). Every
  page reuses the homepage's real nav (working theme toggle, industries
  dropdown, mobile menu), the same dark frozen hero treatment, a 4-item
  Problem list, 3 software-only Capability cards, an explicitly-labeled
  "Illustrative example, not a specific client result" stat bar, an
  explicitly-labeled "Illustrative, not an actual client" scenario box, a
  4-item FAQ, a CTA linking straight to Calendly, and the real footer.
  Every claim stays software/AI/data work only, no on-site or physical-work
  claims anywhere (explicit FAQ answers on the physical-adjacent industries,
  Construction/Manufacturing/Field Services, say so directly). Generated via
  a small local Python templating script (not committed) to keep the 13
  pages' shared chrome byte-identical and reduce copy-paste drift; the
  per-page content itself is hand-written, not templated.
- **Homepage wiring**: the nav's Industries dropdown and the homepage's own
  Industries grid tiles (`industry-tile`, previously plain `<div>`s) now
  link to their real page instead of the `#industries` anchor. `.industry-tile`
  got `text-decoration:none; color:inherit; display:block;` to work as an
  anchor.
- **Verified**: served the site locally, clicked an Industries tile through
  to its real page, toggled dark mode on an industry page (matches the
  homepage's palette exactly), scrolled through stat bar / scenario / FAQ /
  CTA / footer, confirmed the homepage's Services and Testimonials sections
  render the updated copy correctly. Grepped for leftover em dashes, the old
  n8n Automation Audit Bot references, and the stale "11"/"Eleven" stat
  copy, all clean, across `index.html` and all 13 new pages.

## Round 15 — Approvent removed

Approvent's real screenshot never arrived across 4+ rounds of asking. User
decided to drop it rather than keep waiting: removed the Approvent card
(both slider copies) along with the now-dead `.portfolio-placeholder` CSS
it was the only user of. Portfolio count updates from 10 to 9 (stat bar and
the section's own "systems we've shipped" copy, "five of them brand new"
now "four," since Approvent was one of the five). Open-items list is now
empty, nothing else is waiting on a real asset.
