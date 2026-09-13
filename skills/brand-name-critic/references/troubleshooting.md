# Troubleshooting Log

Format and pruning discipline: `${CLAUDE_PLUGIN_ROOT}/shared/troubleshooting-format.md` — read it
before adding an entry.

## Watchlist (anticipated — not yet observed)

- **The step ledger states the chain's goal instead of this skill's.** Watch the opening
  `Step N of M · toward …` line for naming "a shortlist of candidates" or some other
  downstream/upstream artifact instead of this run's own deliverable, "an argued recommendation" —
  most likely when the critic is invoked mid-chain (a blind QA pass from `brand-name-generator`, or
  a user floating one name while thinking about the eventual shortlist) and the chain's finish line
  is more visible than this run's own leg (`shared/velocity.md` §2, goal leakage). `SKILL.md`'s
  ledger line is fixed text for exactly this reason — nothing to compose per-run, nothing to drift.
  If it leaks anyway, check first whether the line was copied verbatim or paraphrased from
  surrounding context before rewording the instruction further.

## Entries

*(none yet — the reflection step appends real, observed entries here after a run.)*
