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

**New leak surface as of the velocity change: the handoff block.** Step 4 now ends by naming
`/lingua:brand-name-generator`. Naming the next *command* is not naming the product, but it puts
the word "generator" in the agent's mouth at exactly the moment the guard is holding back a
candidate, and the obvious slip is a bridging sentence — "the cartography world would generate
something like…", or a `Needs:` line that names a survivor *and* a word it suggests. Watch for a
leak specifically **between** the guard and the handoff block, and in the `Needs:` line. The
structural mitigation is that the block is copied verbatim (template rule 5) and contains no
free-text slot; if a leak lands there anyway, the fix is removing the free text around it, not
removing the handoff — a run that strands the user is a different failure, not a safer one.
**Status:** anticipated — this is the highest-priority thing to watch on the first real run.

### 2026-08-24 — Path C extraction silently swallows the competitive-alternatives gap
**Symptom (anticipated):** a run on a PRD or design doc extracts most of the brief, reports
confidently that the document was used, and proposes worlds in Step 2 without ever asking what the
product replaces — or asks nothing because the document had a section that *looked* like it
covered this ("Alternatives considered," "Prior art") and it was really about implementation
choices, not about what a user does today instead.
**Cause (anticipated):** extraction feels like coverage. Path A's licence to ask nothing is
attached to a canvas, which genuinely has a Competitive alternatives section; Path C inherits the
*feeling* of that licence without the field. And competitive alternatives is the one field where a
plausible-looking heading is most likely to be a false positive, because project documents really
do discuss alternatives — just the wrong kind.
**Fix (anticipated):** `01-brief.md` Path C §3 names this as the gap to press hardest on and says
to ask even when the document appears to cover it, and §2's extraction test requires a citable
passage that also survives the Step 3 vagueness check. If this is observed anyway, the fix is
making it mechanical rather than emphatic: no Path C run proceeds to Step 2 until the competitive
alternatives field is either answered by the user or written into the brief's Assumptions block as
an explicit stated guess. Silence is the failure; a marked assumption is not.
**Status:** anticipated.

### 2026-08-24 — the follow-up round becomes an unbounded interview
**Symptom (anticipated):** Path B's four questions get answered, one answer is vague, the
follow-up round fires — and then a second round fires on the follow-up's answer, or Path C's gap
questions arrive in three separate messages, or the run keeps asking because each answer opens a
new interesting thread. The user came for worlds and is on message five of an intake form.
**Cause (anticipated):** the constraint that used to prevent this ("do not expand this into a
longer discovery interview") was removed on purpose — the user said they would rather be grilled
than hand-held — and the replacement bound is a rule the agent has to hold rather than a wall.
Removing a ceiling invites drift toward the opposite anti-pattern (`velocity.md` §5, "the
interview that never converges"). Curiosity also reads as diligence from the inside.
**Cause, second half:** every additional question feels individually justified. The failure is
never one bad question; it is the absence of a stopping rule being enforced.
**Fix (anticipated):** the bounds are already written — Path B gets exactly one follow-up round,
batched into one message, only on answers that fail the stated vagueness test; Path C gets one gap
message; both then proceed on stated assumptions. If drift is observed, the fix is a visible
counter rather than a firmer instruction: state the round number in the message itself ("one
follow-up round, then I proceed on assumptions"), which makes a second round conspicuous to the
user as well as to the agent. Do **not** fix this by reinstating the old four-questions-only
ceiling — that produced the thin briefs this change exists to end.
**Status:** anticipated.

### 2026-08-24 — the step ledger leaks the chain's goal
**Symptom (anticipated):** a response opens with `Step 3 of 4 · toward a shortlist of names`, or
`· toward naming the product`, instead of `· toward 2-3 stress-tested worlds`.
**Cause (anticipated):** the ledger asks for a destination, and the honest-feeling destination is
the one the user actually wants. `velocity.md` §2 is explicit that this is the wrong answer here:
an agent that can see "names" as the goal while running the fidelity test will rush the fidelity
test to get there — the same pressure as the leak entry above, arriving one line earlier.
**Fix (anticipated):** `SKILL.md` states the ledger string literally and says why the chain's
outcome must not enter it; template rule 6 repeats the constraint at the output. If a leak is
observed, check whether it correlates with a thinner fidelity test in that same run — that
correlation is the thing worth knowing, and it would justify treating the ledger string as
copy-verbatim rather than composed.
**Status:** anticipated.

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
