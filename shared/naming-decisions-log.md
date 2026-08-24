# Naming decisions log

## Purpose

This is the taste log from PRD §5.6 — the record of names proposed, chosen, rejected, and why,
across every naming session run through this plugin. It is not the engineering ADR log (that is
`docs/DECISIONS.md`; see ADR-006 for why they're split). No amount of research supplies this
input — it accumulates the user's actual judgment, over time, and a skill that has read fifty of
these entries reasons about a new name better than one that hasn't.

---

## Entry format

One entry per naming decision. Keep every field, in this order. The **why** is the load-bearing
field — a rejection with a real "why" is worth more than ten entries that only record the outcome.

```
### NNN — YYYY-MM-DD — <short label>

- **Context profile:** venture | feature | codename
- **Proposed:** name1, name2, name3, ... (every candidate seriously considered)
- **Chosen:** name (or "none — deferred")
- **Rejected:** name — reason; name — reason (one reason per rejected name, not a shared blob)
- **Why:** the actual reasoning behind the choice, in the user's own terms. This is the field
  that has to generalise — a rule of thumb, a gut reaction explained, a trade-off that was made
  consciously. Not a restatement of the rubric scores; the rubric already lives in
  `brand-name-critic`. This field records what the rubric *didn't* capture.
- **Status:** provisional | settled | superseded by entry NNN
```

---

## The pruning discipline

Read this before adding or editing an entry.

**This log is edited, not appended to indefinitely.** PRD §5.6 is explicit that a taste log is
exactly how a skill accumulates sediment over time, and that risk is real here specifically
because the log's whole value is in being read in full by a naming session — an unpruned log
eventually costs more context than the taste it encodes is worth.

**The rule:** the reflection step at the end of a naming session **edits this file** rather than
only appending to it. Every phase boundary (PRD §8, BUILD-MAP §4) gets a dedicated pruning pass
over the whole log, not just the newest entry.

**What gets pruned first:**
- Entries fully superseded by a later, related decision — mark `superseded by entry NNN` and
  compress the superseded entry to one line pointing at its successor, rather than deleting it
  outright (the fact that a name was tried and abandoned is sometimes itself the useful signal).
- Entries whose **why** turned out not to generalise — logged as a rule of thumb that a later
  entry directly contradicted, and never invoked again since. If the reasoning didn't hold up
  across more than one decision, it isn't taste, it was a one-off, and it should be cut rather
  than carried forward as if it were a standing preference.
- Duplicate rejections of the same name for the same reason across multiple sessions — keep the
  first occurrence, drop the repeats.

**What gets preserved even under pruning pressure:**
- A rejection whose reasoning still bites — i.e., a "why" that a later session actually re-applied
  to a new candidate. That's the log doing its job; don't cut it to save space.
- Entry 001, permanently, as the seed case (below) — it documents the method itself, not just
  one outcome.
- Any entry still marked `provisional` — it hasn't finished being useful yet.

**Deletion test applies here too:** before pruning, ask whether removing the entry would change
a future critique's reasoning. If no, cut it. If the answer is unclear, compress rather than
delete — a one-line superseded pointer costs almost nothing and preserves the option to check.

---

## Entries

This log ships **seeded, not empty** — two entries drawn directly from PRD §7.2, not invented.
Everything past entry 002 is real usage; do not fabricate additional entries to make the log look
more populated than it is. **It is correct for this log to be nearly empty at v1.**

### 001 — 2026-08-24 — "Lingua" (the module's own name)

- **Context profile:** venture (module/product-level naming, not a feature inside something else)
- **Proposed:** Lingua
- **Chosen:** Lingua (provisionally — see status)
- **Rejected:** — (no alternatives were generated; this is a critique of the existing name, not a
  bake-off)
- **Why:**
  - Ergonomically strong: two syllables, DA-da stress, clean CVC-CV structure, unambiguous
    spelling. No complaint at the ergonomics layer.
  - Brandability weak: descriptive-suggestive Latin for "tongue" — the first word anyone reaches
    for in this exact space, sitting in a dense namespace with Linguee, Lingua Franca, and
    Lingua.ly already occupying it. Low generativity: the vocabulary it supplies — tongue, Babel,
    Rosetta, grammar — is thin, academic, and doesn't map onto anything actually being built. It
    tells you the domain (language) but nothing about the point of view, and the point of view is
    the actually interesting part: this is not "language," it's *ergonomics applied to language*.
    A name that only names the category and not the angle is doing half the job.
  - Practicality: irrelevant by design. Personal toolkit, no trademark exposure, no domain to
    register, no SEO to compete for. Which is exactly why it wasn't worth spending more than five
    minutes on — the practicality layer has nothing at stake here, so it can't rescue a weak
    brandability read.
- **Status:** **provisional, expected to be replaced.** The module name deliberately appears
  nowhere in the skill names or skill bodies (BUILD-MAP §0, §6) — only in `plugin.json`,
  `marketplace.json`, the README, and the invocation prefix — specifically so that renaming it
  later is cheap. This entry is the honest prior work that should seed the plugin's first real
  run on itself, per BUILD-MAP §6.

### 002 — 2026-08-24 — the unnamed umbrella (OPEN)

- **Context profile:** venture
- **Proposed:** none yet — this entry records an open naming gap, not a candidate list
- **Chosen:** none
- **Rejected:** "Lingua" — considered and set aside for this purpose specifically, because it's
  semantically too narrow: positioning, naming, content, and pitch together are not "language."
  Lingua names one module inside the umbrella, not the umbrella itself.
- **Why:** PRD §7.2 identifies the gap directly — the suite covering positioning + naming +
  content + pitch (§7.1's four-skill grid) has no name at all yet, and using "Lingua" for it would
  misdescribe three-quarters of what it covers. Naming it is called out as the fitting first real
  job for the finished plugin (BUILD-MAP §6): run `brand-name-worlds` → `brand-name-generator` →
  `brand-name-critic` on the umbrella itself once all three skills exist.
- **Constraint to carry into that session:** whatever candidate is proposed must pass the
  `six-siblings test` — it has to generate sibling names for positioning, naming, content, and
  pitch as a family, not just describe naming (Lingua's own failure mode) or describe the
  category generically ("Brand Suite," "Toolkit").
- **Status:** open. Not resolvable from research — this is exactly the kind of decision only the
  user makes, and fabricating a resolution here would violate the log's own purpose.
