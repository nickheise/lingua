# Reference critiques — build targets, not documentation

**These files are not documentation of how `brand-name-critic` behaves. They are the
specification of how it must behave.** They were written by hand, at full quality, *before* any
part of the skill existed — before SKILL.md, before the reference files, before the template.

That order is the method, and it comes from PRD §8:

> **Method note:** build this one by reverse-engineering. Write three or four ideal critique
> outputs by hand first (one venture name, one feature name, one deliberately bad name), then
> build the skill that produces them, then have a fresh-context subagent run the skill blind and
> compare. Iterate until the blind output resembles the target. Naming critique is subjective
> enough that specifying the output first is the only reliable way to know the skill works.

---

## The three targets

| File | Name | Profile | Why this case exists |
|---|---|---|---|
| [`venture-scout.md`](venture-scout.md) | **Scout** | venture / product | The PRD's own worked example. A split verdict: exceptional world, badly crowded namespace. Tests that `flag, never block` actually works — that ownability reports a severity and takes no veto. |
| [`feature-balance.md`](feature-balance.md) | **Balance** | feature / UI | Built on the real Apple case in PRD §4.5. Must come out **approving a boring name**, and must show the feature profile inverting the venture profile's priorities — distinctiveness down, spellability and sibling consistency up. Carries the sibling-consistency check and the Microsoft Copilot cautionary tale. |
| [`bad-xzrq.md`](bad-xzrq.md) | **Xzrq** | venture / product | A deliberately bad name that fails for **articulable** reasons. Where PRD §3.3 earns its keep: Xerox and Xzrq both open with X, and the rubric must say precisely why one works and the other does not — `rare letters, common sounds`. Also proves a disastrous name still gets an argued read, not a sneer. |

Between them the three cover every structural property the skill must exhibit:

- all three layers producing **three different shapes** of output — a measurement, an argument, a
  fact sheet — and **never a composite** (Xzrq is the proof case: ergonomics 34, brandability
  zero, practicality perfectly clean);
- every leading word used **verbatim**, in the places BUILD-MAP §1 assigns them;
- both context profiles producing visibly different readings of the same dimensions (`Balance`
  says distinctiveness 60 is close to the requirement; `Scout` says distinctiveness is the whole
  conversation);
- a counter-argument attached to every brandability position, including the ones that are
  obviously right;
- a recommendation that is argued rather than decided — **never a verdict** — with an explicit
  "what would change this read."

---

## The acceptance test

From PRD §8, restated as a procedure:

1. A **fresh-context subagent** — no visibility into this build session, no sight of these files —
   is given the skill and one of the three candidate names, with its profile.
2. It runs `brand-name-critic` blind and produces a critique.
3. That output is compared against the corresponding target in this directory.

**Pass condition: the blind output *resembles* the target.** Not word-for-word — these are argued
documents and two competent critics will phrase the argument differently. What must match is
structural and substantive:

| Must match | Check |
|---|---|
| Headline shape | Three separate verdicts, no composite number anywhere |
| Layer 1 | Six dimensions, script-derived, with the profile re-weighting done in prose rather than by recomputing the number |
| Layer 2 | Five criteria, each with a position **and** its strongest counter-argument |
| Layer 3 | Flags with severity, and an explicit statement that this never gives clearance |
| Leading words | Present verbatim, not paraphrased |
| Ending | An argued recommendation and a "what would change this" — not a verdict |
| Substance | The load-bearing findings are reached. Scout's namespace crowding. Balance beating Spending Power on sibling consistency. Xzrq's distinctiveness 81 being worthless. |

---

## The rule that makes this work

**If the blind output does not resemble the target, the skill is wrong — not the target.**

Say it plainly, because the failure mode is obvious and tempting: an agent comparing its own
output to a target will find reasons the target should be relaxed. That is backwards. These files
were written first, deliberately, so that they could not be adjusted to whatever the skill happened
to produce. A target that is edited to match a disappointing run has stopped being a target.

The permitted repairs, in order of preference:

1. **Strengthen the reference files.** The usual cause of a weak blind run is that
   `01-ergonomics.md`, `02-brandability.md` or `03-practicality.md` describes a step without
   giving a procedure for it.
2. **Strengthen `assets/critique-template.md`.** If the shape came out wrong, the template did not
   pin the shape.
3. **Strengthen the leading words in SKILL.md.** If the phrases are missing from the reasoning
   trace, the steering failed (BUILD-MAP §1) and the words need to be more consistent or more
   prominent — not softer.
4. **Only then, and only with a written note in `docs/DECISIONS.md`, revise a target** — and only
   if the target itself is *wrong on the substance*, e.g. it asserts a fact that turns out to be
   false. Never because it is inconveniently demanding.

---

## Two things these files are honest about

**The ergonomics numbers were provisional, and have since been reconciled.**
`scripts/phonetics.py` was written in parallel with these targets, against the contract pinned in
BUILD-MAP §3, so no target could be produced by running it at the time. Each ergonomics block
carried the marker:

```html
<!-- PROVISIONAL: reconcile against real phonetics.py output -->
```

Once the script landed, reconciliation ran per ADR-008: the script's output is authoritative, and
every hand-estimated number was replaced with the script's real one, with the interpreting prose
rewritten wherever a number moved enough to change the argument built on it (most notably Balance's
spellability, which moved from an estimated 89 to a real 66, and every one of Xzrq's six
dimensions). The `PROVISIONAL` markers are gone from all three critiques; this file's code fence
above is now the only place that string appears, kept as the historical record of what the marker
looked like.

`bad-xzrq.md` still carries a caveat in its Layer 1 comment: the name is not in CMUdict, so its
transcription is a low-confidence g2p estimate. The script does not return a syllable count of
zero for a name with no vowel — it returns `syllables.count: 1` with an all-consonant structure and
`stress.shape: "no vowel nucleus"`, plus a matching entry in `warnings`. The target keys on those
fields rather than on a count of zero, and says out loud that the exact ARPABET string is the
least reliable part of the document even though the no-nucleus finding itself holds under any
plausible transcription.

**One number in the PRD does not match one number in the build map — and this is resolved, not
open.** PRD §4.1 illustrates the headline with `Ergonomics 89 · Brandability: exceptional world,
crowded namespace · Practicality: 2 flags`, while the worked Scout JSON in BUILD-MAP §3 yields
`ergonomics_score: 85` from its own six dimension scores. Running the real script settles it: it
also returns **85** for Scout, from the same six dimensions the build map's worked example carries.
So the contract's worked example was right, and the PRD's `89` was exactly what ADR-008 says it
was — an illustration, not a specification. `venture-scout.md` reports 85, matching the script.
`assets/critique-template.md` no longer keeps `89` attached to Scout either, for the same reason:
see the note in that file. Both facts are recorded here rather than left as a live discrepancy.
