# Comparison mode — head-to-head, not two critiques stapled together

Two critiques run side by side and diffed by eye is not a comparison, it is homework left for the
reader. This mode produces a genuinely different artifact: one ergonomics table, deltas argued
instead of restated, and a single recommendation — never a ranking.

**No composite scores, anywhere, ever.** This file exists because a comparison table is the most
tempting place in the whole rubric to resurrect the composite the architecture was built to kill.
Every rule below is there to stop that.

---

## 1 · Profile and positioning — asked once, for all candidates

Run Step 1 of `SKILL.md` exactly once. One profile, one positioning answer, applied to every
candidate. Asking per-candidate is the ping-pong `earn the question` forbids, and it also breaks
the comparison: the whole point is reading every candidate against the *same* weights.

## 2 · Ergonomics — the script runs once

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/phonetics.py "<name-1>" "<name-2>" ["<name-3>" ...]
```

One call, one JSON array, one element per name, in input order. Never loop the script per
candidate — the array is the contract precisely so this mode doesn't run it N times.

Build the side-by-side table immediately: candidates as columns, the six dimensions as rows, plus
an `ergonomics_score` row. Every cell still comes straight from the JSON, unmodified, exactly as
in a solo critique — comparison mode changes the *shape* of Layer 1's report, not its numbers.

## 3 · Compare only where they differ

**This is a rule, not a suggestion.** For each dimension, before writing a word of prose, ask: does
this gap change anything a reader would decide differently? A five-point gap on two names both in
the 90s is noise. Mark it, in the table or just after it, as **equivalent** — one word — and move
on. Do not write a paragraph per candidate per dimension; that is two critiques stapled together
with extra steps, exactly what this mode exists to replace.

Spend the prose on the dimensions that actually separate the candidates. A 40-point spread earns
real discussion — what causes it, and what it costs or buys under the active profile. A 6-point
spread does not, no matter how tempting the table makes it look.

## 4 · The decisive-dimension rule

Before writing the recommendation, name which **one or two** dimensions actually separate these
candidates *under the active profile's weights* — not the largest raw gap, the largest gap after
the profile's own re-weighting (same prose re-weighting Step 2 of `SKILL.md` already does, applied
comparatively). Lead the write-up with those. Everything else in the table is context.

This is why the same table produces a different comparison under a different profile: a 40-point
distinctiveness spread is the whole story under venture, where distinctiveness is weighted way up,
and barely worth a sentence under feature, where it is weighted down. State which dimension is
decisive and why the profile makes it so — that sentence is the one a reader most needs.

## 5 · Brandability stays argued, stays separate, never tabled

Run Layer 2 (`02-brandability.md`) in full for each candidate, exactly as a solo critique would —
`world, not word`, the `six-siblings test`, `read the ending`, `flag, never block`, all five
criteria, position and counter-argument. Present the two reads as separate blocks, one per
candidate, never merged into the ergonomics table.

**Generativity, lore, and the world each name opens are not commensurable across candidates.** A
name with an exceptional world and a crowded namespace and a name with a plain world and a clean
one are not "better" and "worse" — they are different bets. Say what each bet is: what you're
buying, what you're giving up, in one or two sentences per candidate. A table forces a false
equivalence here that prose does not.

## 6 · Practicality — flags, juxtaposed, still not scored

Run Layer 3 per candidate; a short table of headline flag counts side by side is fine (`<n> flags`
per candidate is a count, not a score) — but per §3, only narrate the checks where the candidates'
findings actually diverge. Two names that are both clean on trademark tier don't need two
paragraphs saying so.

## 7 · The recommendation — a pick, not a ranking

Close with:

1. **Which candidate you would pick**, stated plainly.
2. **The single strongest argument for the other one** — not a list of its merits, the one that
   would actually change a reasonable person's mind.
3. **What would flip it** — the specific fact, positioning answer, or constraint that reverses the
   recommendation.

**Never a numeric ranking. Never a composite. Never "Name A: 87, Name B: 74."** If a sentence in
the draft could be replaced by two numbers and a greater-than sign, rewrite it — that sentence is
the composite in disguise.

## 8 · Ties are a real answer

If the decisive dimension(s) from §4 come out equivalent and brandability's bets are genuinely
comparable in size, **say so directly** — do not manufacture a preference to avoid an unsatisfying
ending. Hand the decision back with the actual tie-breaker named: usually ownability (`flag, never
block` — whichever namespace is less crowded) or, when one candidate already has siblings in an
existing product family, that consistency. A named tie-breaker is a real answer; an invented
preference is not.

Either way, comparison mode still ends at a verdict — `names or a verdict` — not a longer document
about the two names. A tie plus a named tie-breaker *is* the verdict; it hands the decision back
with a reason attached rather than deferring it.
