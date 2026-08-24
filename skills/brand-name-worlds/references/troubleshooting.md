# Troubleshooting Log

**Purpose.** Per PRD §5.6, `brand-name-worlds` ends each run with a reflection step: examine any
friction encountered during that run, and update this file. A skill that has seen fifty real runs
should behave better than one that hasn't — this file is where that experience accumulates, in a
form the next run can actually read and act on.

## Entry format

Every entry follows the same three-part shape, dated, plus a status:

```
### YYYY-MM-DD — short symptom title
**Symptom:** what went wrong, observed in an actual run.
**Cause:** why it happened.
**Fix:** what changed as a result — a rule added to a reference file, a phrasing change, a new
check. If the fix belongs in `01-brief.md`, `02-world-sourcing.md`, `03-fidelity-test.md`, or
`assets/world-brief-template.md`, make the edit there and say so here.
**Status:** anticipated | observed | resolved-into-docs
```

`anticipated` entries are seeded before the skill has been run, based on failure modes the build
process could foresee. They are not evidence the skill has failed this way — they exist so the
reflection step has a checklist of known risks to watch for on the first real runs, and so anyone
reading this file can tell foreseen risk apart from observed fact.

## Pruning discipline — read this before adding an entry

This log is in tension with the pruning rules by design: logs are exactly how skills accumulate
sediment (PRD §5.6). The mitigation is structural, not optional:

1. **The reflection step edits this file; it does not append to it indefinitely.** Before adding
   a new entry, read every existing entry.
2. **Apply the deletion test to each existing entry:** would removing it change a future run's
   output? If the fix has already been folded into `01-brief.md`, `02-world-sourcing.md`,
   `03-fidelity-test.md`, or `assets/world-brief-template.md` — so the failure mode structurally
   can't recur — mark it `resolved-into-docs` and delete the entry on the *next* pruning pass. The
   fix lives in the doc now; the log doesn't need to remember it too.
3. **Merge near-duplicates.** Two entries describing the same underlying friction become one.
4. **Add a new entry only for genuinely novel friction** — not a restatement of something already
   logged.
5. **A full pruning pass is mandatory at every phase boundary** (per BUILD-MAP.md §4), regardless
   of whether new entries were added during that phase.

Whoever (or whatever) runs the reflection step next should treat rules 1-5 above as the actual
instruction, not this paragraph of framing around them.

---

## Anticipated entries (seeded pre-launch — not yet observed)

### 2026-08-24 — a name leaks despite the Step 4 guard
**Symptom (anticipated):** the run reaches Step 4, converges on survivors, and somewhere in the
output — the survivors' argument, a parenthetical, the closing summary — a candidate word for the
product appears. This is the specific failure this skill was split out of a combined
worlds-and-names skill to prevent (PRD §5.2, BUILD-MAP §4 exit criterion): "if it leaks names, the
split has failed and needs stronger steering."
**Cause (anticipated):** a chosen world genuinely does suggest a word — that's what a good fidelity
result feels like from the inside — and saying the word out loud reads as helpful in the moment.
The pressure is structurally identical to the plan-mode failure the PRD names: the model can see
what the "real" next step would be and wants to shortcut to it.
**Fix (anticipated, to verify on first real runs):** the Step 4 guard in `SKILL.md` already tells
the agent to notice the pull and not act on it, and `assets/world-brief-template.md` states the
no-names rule as an explicit line in the output shape itself, not just in the instructions. If a
leak is observed anyway, the fix is not a longer warning — long warnings get skimmed under the
same pressure that caused the leak — it's checking whether the leak happened in the survivors'
argument specifically (rewrite that section's instructions to require citing evidence already
written above it, which structurally leaves no room for a fresh word) or in a different section
(diagnose from there). Log the actual leak location here before editing.
**Status:** anticipated — this is the highest-priority thing to watch on the first real run.

### 2026-08-24 — fidelity test gets rushed on the favorite world
**Symptom (anticipated):** a world that felt obviously right after Step 2 gets a thinner
five-concept test than the others — fewer real concepts, more benefit-of-the-doubt shrugs counted
as mapped, or the breaking-point probes skipped "because it clearly works."
**Cause (anticipated):** `03-fidelity-test.md` is explicit that this is the step most likely to be
rushed, precisely because it's the step where a favorite can die — the same asymmetry that makes
breadth-without-fidelity dangerous (PRD §3.2) makes rigor on the favorite feel unnecessary.
**Fix (anticipated):** the fixed five-concepts-across-every-world rule already exists to prevent
per-world cherry-picking; if uneven rigor is observed anyway, the fix is making the template's
five-concept table impossible to leave thin — e.g. requiring the "why it's true" column filled for
every mapped term, no exceptions, which removes the option to wave a mapping through without
writing the justification.
**Status:** anticipated.

### 2026-08-24 — gardening (or another vivid-but-shallow domain) survives on charm
**Symptom (anticipated):** gardening, or a domain like it — vivid imagery, instant six-sibling
recall — passes the breadth check and gets carried into the fidelity test, then the shrug count
gets rounded down ("well, three of these are *sort of* mapped") instead of triggering the discard.
**Cause (anticipated):** `02-world-sourcing.md` names this exact trap for gardening specifically,
but the same charm applies to any domain with strong pre-drawn imagery — the visual payoff arrives
before the fidelity check does, and by the time the check runs there's already an attachment to
defend.
**Fix (anticipated):** the 3-of-5 threshold in `03-fidelity-test.md` is written as mechanical and
non-negotiable for exactly this reason. If rounding is observed anyway, the fix is likely
tightening the shrug definition itself (e.g., a mapped term that required more than one clause of
justification counts as a shrug) rather than restating "be strict" louder.
**Status:** anticipated.
