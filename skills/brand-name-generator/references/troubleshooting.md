# Troubleshooting Log

**Purpose.** Per PRD §5.6, `brand-name-generator` ends each run with a reflection step: examine
any friction encountered during that run, and update this file. The point is that a skill which
has seen fifty real runs should behave better than one that hasn't — this file is where that
experience accumulates, in a form the next run can actually read and act on.

## Entry format

Every entry follows the same three-part shape, dated, plus a status:

```
### YYYY-MM-DD — short symptom title
**Symptom:** what went wrong, observed in an actual run.
**Cause:** why it happened.
**Fix:** what changed as a result — a rule added to a reference file, a phrasing change, a new
check. If the fix belongs in `01-operators.md`, `02-converge.md`, or `assets/shortlist-template.md`,
make the edit there and say so here.
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
   output? If the fix has already been folded into `01-operators.md`, `02-converge.md`, or
   `assets/shortlist-template.md` — so the failure mode structurally can't recur — mark it
   `resolved-into-docs` and delete the entry on the *next* pruning pass. The fix lives in the doc
   now; the log doesn't need to remember it too.
3. **Merge near-duplicates.** Two entries describing the same underlying friction become one.
4. **Add a new entry only for genuinely novel friction** — not a restatement of something already
   logged.
5. **A full pruning pass is mandatory at every phase boundary** (per BUILD-MAP.md §4), regardless
   of whether new entries were added during that phase. Phase 3 explicitly calls for pruning this
   log — treat that as non-negotiable, not as one option among several.

Whoever (or whatever) runs the reflection step next should treat rules 1–5 above as the actual
instruction, not this paragraph of framing around them.

---

## Anticipated entries (seeded pre-launch — not yet observed)

### 2026-08-24 — diverge stops short and calls forty candidates done
**Symptom (anticipated):** Step 1 produces something like thirty to forty candidates, clustering
and convergence proceed anyway, and the run never notices it fell well short of the 80–100
target.
**Cause (anticipated):** the operator list in `01-operators.md` is reference material, and
reference material is exactly the kind of thing a run under time pressure treats as optional
background rather than a quota to actually work through — especially once a handful of operators
have produced names that already feel good enough.
**Fix (anticipated, to verify on first real runs):** the per-operator quota table in
`01-operators.md` is designed to make partial coverage visible (a blank "Generated" cell in
`assets/shortlist-template.md`'s operator-coverage table is not silently skippable the way a
vague "brainstorm more" instruction would be). If this recurs after that, the fix is to make
Step 1 in `SKILL.md` state the total explicitly as a gate before Step 2 begins, not just a
description of the target.
**Status:** anticipated.

### 2026-08-24 — the sibling gate gets waved through with weak siblings
**Symptom (anticipated):** a candidate reaches the shortlist with three sibling names listed, but
each one needed a sentence of justification to read as belonging to the world — the gate is
technically satisfied (three names present) while the actual test (`breadth × fidelity` holding
without a shrug) has failed.
**Cause (anticipated):** "produce three siblings" is easy to satisfy as a word-count requirement
and easy to fail as a quality bar, and the two get conflated under time pressure — especially for
a candidate the run has already grown attached to after surviving Step 1 and Step 2.
**Fix (anticipated):** `02-converge.md` names "weak siblings" as an explicit second failure mode
of the same gate, not a lesser problem than "too few." If this recurs, tighten that section with
a concrete test: could each sibling be presented to someone who has never seen the candidate name,
without the explanation attached, and still land? If not, it needed the shrug and the gate should
have failed.
**Status:** anticipated.

### 2026-08-24 — the QA subagent gets handed generation context by accident
**Symptom (anticipated):** the Step 4 subagent prompt includes something beyond the alphabetized
name list and the context profile — the world's name slips in because it's sitting right there in
the shortlist draft, or the candidates get pasted in generation order instead of alphabetized, or
a rationale line gets copied in "for context."
**Cause (anticipated):** the shortlist artifact being built through Steps 1–3 already contains the
world, the clusters, and the rationale in one place, so the path of least resistance when
assembling the Step 4 prompt is to copy from it directly rather than construct the withheld-down
prompt deliberately — and a leak here is invisible from the outside, because the subagent will
still return a plausible-looking critique either way.
**Fix (anticipated):** `SKILL.md` Step 4 spells out the prompt's contents as an explicit
allow-list (names, alphabetized; profile) rather than describing what to omit, specifically
because an omission-framed instruction is what a rushed run skips first. If this recurs, the
fix is a literal template string in Step 4 to copy rather than compose freely, so there's no
authoring step where a leak could get introduced.
**Status:** anticipated.

### 2026-08-24 — the step ledger states the chain's goal instead of this skill's
**Symptom (anticipated):** the opening `Step N of M · toward …` line names "names," "a verdict,"
or some other downstream/upstream artifact instead of *this run's own* deliverable, "a critiqued
shortlist of ~12 candidates" — plausible here because this skill's whole job is to hand off to a
critic and receive critiques back, so both neighboring artifacts are constantly in view.
**Cause (anticipated):** `shared/velocity.md` §2 names this exact failure as goal leakage — an
agent that can see the chain's finish line while doing its own leg rushes the leg to get there.
`brand-name-generator` sits in the middle of the three-skill chain, the position most exposed to
it, with a named upstream deliverable (worlds) and downstream one (critiques) on either side.
**Fix (anticipated):** `SKILL.md`'s ledger line is already fixed text — "toward a critiqued
shortlist of ~12 candidates" — so there is nothing to compose per-run. If this recurs, check the
line was copied verbatim rather than paraphrased from whichever neighboring artifact is more
salient in the moment, not reworded.
**Status:** anticipated.
