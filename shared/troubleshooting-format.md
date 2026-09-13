# Troubleshooting log — format and pruning discipline

**Purpose.** Per PRD §5.6, each skill ends every run with a reflection step: examine any friction
encountered during that run, and update the skill's own `references/troubleshooting.md`. The
point is that a skill which has seen fifty real runs should behave better than one that hasn't —
the log is where that experience accumulates, in a form the next run can actually read and act on.

## Entry format

Every entry follows the same three-part shape, dated, plus a status:

```
### YYYY-MM-DD — short symptom title
**Symptom:** what went wrong, observed in an actual run.
**Cause:** why it happened.
**Fix:** what changed as a result — a rule added to a reference file, a phrasing change, a new
check. If the fix belongs in one of this skill's own reference or asset files, make the edit
there and say so in this entry.
**Status:** anticipated | observed | resolved-into-docs
```

`anticipated` entries are seeded before the skill has been run, based on failure modes the build
process could foresee. They are not evidence the skill has failed this way — they exist so the
reflection step has a checklist of known risks to watch for on the first real runs, and so anyone
reading the log can tell foreseen risk apart from observed fact. Keep these short: a watchlist
note (what to watch for, why it matters, what it would mean if it actually shows up) rather than a
full Symptom/Cause/Fix entry — there is no real symptom yet to write one about. Upgrade a watchlist
note to a full entry, with real evidence, the first time it is actually observed.

`observed` entries are the real thing: friction that actually happened in a run, written up in
full. `resolved-into-docs` entries record a fix that already landed — the failure mode is gone
because a reference or asset file was rewritten, not because the log remembers it. These are a
changelog of what got caught and fixed, not sediment, and they stay.

## Pruning discipline — read this before adding an entry

This log is in tension with the pruning rules by design: logs are exactly how skills accumulate
sediment (PRD §5.6). The mitigation is structural, not optional:

1. **The reflection step edits this file; it does not append to it indefinitely.** Before adding
   a new entry, read every existing entry.
2. **Apply the deletion test to each existing entry:** would removing it change a future run's
   output? If the fix has already been folded into one of this skill's own reference or asset
   files — so the failure mode structurally can't recur — mark it `resolved-into-docs` and delete
   the entry on the *next* pruning pass. The fix lives in the doc now; the log doesn't need to
   remember it too.
3. **Merge near-duplicates.** Two entries describing the same underlying friction become one.
4. **Add a new entry only for genuinely novel friction** — not a restatement of something already
   logged, and not a restatement of a rule a reference file already states once, clearly. An
   anticipated entry that just re-describes an existing rule as a hypothesis about itself doesn't
   need a second home; one that names a genuinely non-obvious risk the reference files don't
   already flag — a specific leak surface, a specific way a written rule fails to self-enforce —
   earns its place.
5. **A full pruning pass is mandatory at every phase boundary** (per BUILD-MAP.md §4), regardless
   of whether new entries were added during that phase. Treat that as non-negotiable, not as one
   option among several.

Whoever (or whatever) runs the reflection step next should treat rules 1–5 above as the actual
instruction, not this paragraph of framing around them.
