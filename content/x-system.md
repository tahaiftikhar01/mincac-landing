# X (Twitter) Content System — Taha / MinCac

Companion to `instagram-system.md`. Same assets, same positioning, completely different mechanics — treating X like a text version of Instagram is the most common way technical founders waste a year there.

---

## 1. What makes X different

Three things change how you play:

**Distribution is conversational, not algorithmic-first.** On Instagram the algorithm decides who sees you. On X, *other accounts* decide — through quote tweets and replies. This means for the first 3–6 months, replying is more valuable than posting. Your reach comes from being visible in other people's comment sections, not from your own timeline.

**There is no ramp.** A single post can reach 100k people on a two-week-old account. Instagram almost never does that. The tail risk is worth farming — which means posting more, and posting things you're not sure about.

**Text is the native form.** Video and images work, but the default unit is a sentence someone can screenshot. Your Instagram content is *shown*; your X content is *said*.

**Consequence for you:** X is where the AI/automation/build-in-public crowd actually lives — n8n, LangChain, indie hackers, agency operators. That audience is technical, allergic to marketing language, and buys from people who post specifics. It's a much better fit for your real work than Instagram, and a much worse fit for polished agency copy.

---

## 2. Positioning on X

Same person, sharper edge:

> Automation engineer. I build the systems companies hire people to do by hand. I post the builds, the numbers, and the things that broke.

On Instagram you're teaching a business owner. On X you're talking to peers who will call you out — which is exactly what makes it credible when they don't.

**Profile:**
- **Name:** `Taha` (add `| automations` if you want the keyword; the bio does more work here)
- **Bio:** what you build + one proof number + the offer. e.g. *"I build AI agents & automations. Killed 80+ hrs/mo of manual work for one client. Free build for 5 businesses a month →"*
- **Link:** mincac.com/audit
- **Pinned:** your best build thread with the workflow screenshot. Replace it whenever something outperforms it.
- **Header image:** an actual n8n canvas. It signals "builder" before anyone reads a word.

---

## 3. The daily rhythm

This is the whole system. It takes about 45 minutes a day.

**Replies: 10–20/day.** Non-negotiable, and the highest-leverage thing on this list. Build a list of 30–50 accounts in AI automation, agency ops, and indie SaaS. Reply early — within 10 minutes of their post — with something that adds a specific detail, not "great post." One good reply on a large account outperforms most original posts in your first months.

**Original posts: 2–3/day.** Spread out. Mix from the pillars below.

**One thread or long post: 2–3/week.** This is what gets bookmarked and followed.

**Quote-tweet with a take: 2–3/week.** Not agreement — a genuine addition or disagreement. Quote tweets borrow reach.

---

## 4. Content pillars

### Pillar 1 — Build logs [daily]
Short, specific, present-tense. What you shipped or broke today.

> Client's invoices were being typed into QuickBooks by hand. 6 hrs/week.
>
> Built it in n8n: email trigger → Claude extracts the fields → validation → QuickBooks API → Slack confirmation.
>
> 11 nodes. Runs in 4 seconds. She found out today it had been running since Tuesday.

This is your bread and butter and you generate the raw material every working day. Screenshot of the canvas attached whenever possible.

### Pillar 2 — Teardowns [2–3/week]
Take one automation and explain the architecture properly. This is where the technical audience decides whether you're real.

Your existing builds, each worth a thread:
- The audit bot — 22 nodes, Claude Sonnet, scores the lead, routes hot to Calendly, cold gets a system prompt and a polite close. The lead-scoring logic alone is a thread.
- Shopify + Meta Ads + DailyFulfill → one source of truth. Three n8n workflows, four data sources, 80+ hours.
- The LinkedIn lead engine — scrape, enrich, personalize, log to HubSpot, 300 leads/month.
- The Instagram DM responder — qualifies, answers FAQs, routes to Slack.

Include what was hard. "The Meta Ads API rate-limited me and here's the queue I built" is worth more than a clean summary.

### Pillar 3 — Takes [1–2/day]
The pillar that grows the account. Short, declarative, arguable. You have real ones:

- Most "AI agents" are a workflow with an LLM at one decision point. That's fine — but it's not an agent, and the pricing shouldn't pretend otherwise.
- Automate before you hire. Most $60K roles are 6 hours of judgment and 34 hours of copy-paste.
- The bottleneck in AI consulting was never the model. It's that clients can't describe their own process.
- RAG is mostly a data-cleaning job wearing an AI costume.

Rule: post takes you'd defend in a reply thread. If you wouldn't argue it, it's not a take, it's a platitude — and platitudes are what everyone else is posting.

### Pillar 4 — Numbers & receipts [2/week]
Screenshots. Upwork reviews, the client message, the dashboard, the Slack alert firing at 3am. Minimal caption. On X, the artifact carries the post.

Your verified proof: the Upwork profitability review, Eberly & Collard, Tauseef Rehman (VP, Systems Limited), Shayan Malik (Meta). Post them one at a time, with the story of what you actually built.

### Pillar 5 — Building the business in public [2–3/week]
Client count, pricing decisions, what you charged and whether it was wrong, hiring, the free-build funnel and whether it's converting. The agency-operator audience on X is large and starved of honest numbers.

This is also the pillar where being based in Pakistan serving US and EU clients is genuinely interesting content rather than a footnote — the logistics, the timezone reality, the pricing dynamics. Almost nobody is writing it well.

---

## 5. Format rules

- **One idea per post.** If it needs a "2/", it's a thread, not a post.
- **No hashtags.** They do nothing on X and read as marketing.
- **Line breaks between every 1–2 sentences.** Mobile readability is most of the game.
- **Threads: hook post must stand alone.** It has to be worth reading even if nobody expands it.
- **Links kill reach.** Put the link in a reply, never the main post.
- **Never open with "Let me tell you why..."** or any other engagement-bait scaffolding. Just say the thing.

---

## 6. The three-platform pipeline

You now have LinkedIn (established), Instagram (launching), and X (launching). One piece of work, three outputs — but the *order* matters, and it's the opposite of what most people do.

**Draft on X first.** It's the cheapest place to test an idea, feedback is fastest and most honest, and a post takes two minutes. Let X tell you which ideas have legs.

Then:
- **X post that lands → LinkedIn post.** Expand it, soften the edge slightly, add the business framing.
- **X thread that lands → Instagram Reel.** The thread is already a script. Read it to camera over the screen recording.
- **Instagram build video → X post.** Same clip, tighter caption, workflow screenshot.
- **LinkedIn long-form → X thread.** Break it at the natural paragraph breaks.

The compounding version: one build per week becomes an X build log on day one, an X teardown thread on day two, an Instagram Reel on day three, and a LinkedIn post on day four. Four pieces, one afternoon of actual work.

---

## 7. CTA on X

Softer than Instagram. This audience punishes selling and rewards patience.

- **Default:** no CTA at all. The bio and the pinned post do the work. Most of your posts should just be the content.
- **Weekly:** the free build, stated plainly. *"I build one automation free for 5 businesses a month. Reply with your worst manual process."* Replies are public, which makes this post double as a lead magnet and a content generator — every reply is a future build log.
- **Occasional:** "DMs open" at the end of a strong teardown.

Ratio: roughly 15:1 value to pitch. Tighter than Instagram because X notices.

---

## 8. First 30 days

**Week 1 — presence over posting.** Set up the profile properly. Build the 40-account reply list. Do 15 replies/day, 2 posts/day. Do not expect anything. The only goal is being seen in comment sections.

**Week 2 — first teardowns.** Keep replying. Add two threads: the audit bot architecture, and the Shopify profitability system. Pin the better one.

**Week 3 — takes.** Introduce Pillar 3 properly, one take per day. This is when the follower count usually starts moving. Post the first free-build offer.

**Week 4 — receipts and business.** Testimonials as stories, first build-in-public numbers post. Review which posts got replies rather than likes — replies tell you what to write more of.

**Expectations, honestly:** X is slower to start than Instagram and faster to compound. Expect near-silence for three weeks. The accounts that quit, quit in week three.

---

## 9. Rules

- **Reply more than you post.** For six months, at minimum.
- **Never argue with bad faith.** Mute and move on. It costs reach and it costs your day.
- **Never post a build you didn't do.** This audience checks, and being caught once on X follows you permanently.
- **Screenshot everything as you work.** The canvas, the error, the Slack alert, the client message. You cannot reconstruct these later, and they are the whole content supply.
- **Don't automate your own posting.** The irony would be fair, but the reason is practical: X's reach favours native, timely, conversational posting, and scheduled content reads as scheduled. Automate the *capture* (screenshots, drafts, a notes inbox), never the posting or the replies.
