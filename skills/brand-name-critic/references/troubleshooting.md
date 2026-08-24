# Troubleshooting Log

**Purpose.** Per PRD §5.6, `brand-name-critic` ends each run with a reflection step: examine any
friction encountered during that run, and update this file. The point is that a skill which has
seen fifty real runs should behave better than one that hasn't — this file is where that
experience accumulates, in a form the next run can actually read and act on.

## Entry format

Every entry follows the same three-part shape, dated, plus a status:

```
### YYYY-MM-DD — short symptom title
**Symptom:** what went wrong, observed in an actual run.
**Cause:** why it happened.
**Fix:** what changed as a result — a rule added to a reference file, a phrasing change, a new
check. If the fix belongs in `01-ergonomics.md`, `02-brandability.md`, `03-practicality.md`, a
profile file, or `myths-blocklist.md`, make the edit there and say so here.
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
2. **Apply the deletion test to each existing entry:** would removing it change a future critique's
   output? If the fix has already been folded into `01-ergonomics.md`, `02-brandability.md`,
   `03-practicality.md`, a profile file, or `myths-blocklist.md` — so the failure mode structurally
   can't recur — mark it `resolved-into-docs` and delete the entry on the *next* pruning pass. The
   fix lives in the doc now; the log doesn't need to remember it too.
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

### 2026-08-24 — g2p fallback presented as a measurement
**Symptom (anticipated):** a coined name outside CMUdict coverage returns `pronunciation.source:
"g2p"` and `confidence: "low"` from `phonetics.py`, but the critique's prose states the syllable
count, stress pattern, or phoneme sequence as flatly as it would for a dictionary hit — no hedge,
no mention that this is an estimate.
**Cause (anticipated):** the JSON contract already carries the confidence signal
(`pronunciation.confidence`, `warnings`), but nothing forces the reasoning layer to surface it in
the argued brandability/practicality prose rather than just the raw ergonomics numbers.
**Fix (anticipated, to verify on first real coined-name run):** the critic must echo
`confidence: low` and any `warnings` entry into the verdict text itself whenever present, in
language the user will actually read — not just leave it sitting in a JSON blob the user never
sees directly. If this recurs after that check is added to `01-ergonomics.md`, tighten the
instruction there rather than logging it here again.
**Status:** anticipated.

### 2026-08-24 — context profile not stated, skill guesses instead of asking
**Symptom (anticipated):** the user floats a name mid-conversation (this skill is model-invoked)
without saying whether it's a venture, feature, or codename candidate, and the critic silently
picks a profile based on conversational context instead of asking.
**Cause (anticipated):** critics are model-invoked and fire fast by design (PRD §5.1) — the same
speed that makes critique cheap and welcome also creates pressure to skip a clarifying question
and just proceed.
**Fix (anticipated):** every profile file already states "ask, briefly" as step 1 — the risk is
that instruction getting skipped under time pressure rather than the instruction being missing.
Watch specifically for this on the first several real runs; if it recurs, the fix is a stronger,
more visible flag in `SKILL.md` itself rather than in a profile file the skill may not have loaded
yet at the point the question should be asked.
**Status:** anticipated.

### 2026-08-24 — a name whose lore has no ending to read
**Symptom (anticipated):** `read the ending` is a leading word the brandability layer is supposed
to apply to any name with mythological or literary weight — but a candidate that is a plain
coinage, an acronym, or a name from a source with no real narrative resolution (no clear "how does
this story end") gets forced through the check anyway, producing a strained or invented reading
where there isn't a real one.
**Cause (anticipated):** the leading word is powerful precisely because it's meant to be applied
consistently — which creates pressure to apply it even where the premise (a story worth reading to
the end) doesn't hold.
**Fix (anticipated):** the correct output in this case is an explicit "no lore to read — this name
has no narrative source" finding, not a fabricated one. If this recurs, add that exact
fallback line to `02-brandability.md`'s lore-integrity section.
**Status:** anticipated.
