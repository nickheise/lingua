# Troubleshooting Log

Format and pruning discipline: `${CLAUDE_PLUGIN_ROOT}/shared/troubleshooting-format.md` — read it
before adding an entry.

## Watchlist (anticipated — not yet observed)

- **Diverge stops short of the 80-100 quota and nobody notices.** Watch for Step 1 landing around
  thirty to forty candidates with clustering and convergence proceeding anyway — `01-operators.md`
  is reference material, and reference material is exactly what a run under time pressure treats
  as optional once a handful of operators have already produced names that feel good enough. The
  per-operator quota table and the operator-coverage table in `assets/shortlist-template.md` exist
  to make a partial pass visible (a blank "Generated" cell isn't silently skippable), but that
  hasn't been tested under real pressure yet. If observed, make `SKILL.md` Step 1 state the total
  as an explicit gate before Step 2 begins, not just a target to aim for.

- **The Step 4 subagent prompt picks up generation context by accident.** Watch for the world's
  name, unalphabetized ordering, or a stray rationale line slipping into the blind-QA prompt — the
  shortlist artifact built through Steps 1-3 already holds the world, the clusters, and the
  rationale together, so copying from it directly is the path of least resistance when assembling
  the withheld-down prompt. A leak here is invisible from outside, since the subagent still returns
  a plausible-looking critique either way. `SKILL.md` Step 4 already states an allow-list (names,
  alphabetized; profile) and an explicit withhold list; if a leak is observed anyway, replace both
  with a literal template string to copy rather than compose freely.

- **The step ledger states the chain's goal instead of this skill's.** Watch the opening line for
  naming "names," "a verdict," or another neighboring artifact instead of "a critiqued shortlist of
  ~12 candidates" — this skill sits in the middle of the three-skill chain with a named deliverable
  on both sides, the position most exposed to goal leakage (`shared/velocity.md` §2). The ledger
  line is fixed text for this reason; if it drifts, check it was copied verbatim before rewording
  it.

## Entries

*(none yet — the reflection step appends real, observed entries here after a run.)*
