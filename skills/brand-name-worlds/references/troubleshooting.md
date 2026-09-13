# Troubleshooting Log

Format and pruning discipline: `${CLAUDE_PLUGIN_ROOT}/shared/troubleshooting-format.md` — read it
before adding an entry.

## Watchlist (anticipated — not yet observed)

- **A chosen world's word leaks into the output — including through the handoff block.** Watch for
  a candidate word for the product surfacing anywhere in Step 4's output: the survivors' argument,
  a parenthetical, the closing summary, or — the newer risk — the handoff block that now names
  `/lingo:brand-name-generator`. Naming the next *command* is not naming the product, but it puts
  the word "generator" in the agent's mouth right as the guard is holding back a candidate; the
  likely slip is a bridging sentence or a `Needs:` line that pairs a survivor with a word it
  suggests. This is the exact failure the skill was split out of a combined worlds-and-names skill
  to prevent (PRD §5.2, BUILD-MAP §4 exit criterion). If observed, log the precise leak location
  (between the guard and the handoff block, inside the `Needs:` line, or elsewhere) before editing
  — the handoff block is copied verbatim with no free-text slot (template rule 6), so the fix is
  removing stray free text around it, not removing the handoff.

- **The one-follow-up-round rule gets quietly exceeded.** Watch for a second follow-up round firing
  on a follow-up's own answer, or Path C's gap questions splitting across multiple messages — each
  additional question feels individually justified in the moment, so a written stopping rule
  doesn't automatically self-enforce. If observed, the fix is a visible counter rather than a
  firmer instruction: state the round number in the message itself ("one follow-up round, then I
  proceed on assumptions"). Do not fix this by reinstating the old four-questions-only ceiling —
  that produced the thin briefs this path change exists to end.

- **The step ledger leaks the chain's goal.** Watch the opening line for naming "a shortlist of
  names" or "naming the product" instead of "2-3 stress-tested worlds" — the same goal-leakage
  pressure as above, one step earlier (`shared/velocity.md` §2). If observed, check whether it
  correlates with a thinner fidelity test in the same run — that correlation is the useful signal,
  and would justify treating the ledger string as copy-verbatim rather than composed.

## Entries

### 2026-09-13 — the handoff named a "chosen world" that never got chosen
**Symptom:** an adversarial review found that Step 4 converges to 2-3 survivors and stops, then
the handoff's `Needs:` line read "the chosen world from the brief above" — but nothing in the
skill ever asked the user to pick one. `brand-name-generator` correctly refuses to proceed
without a single world, so a user following worlds straight into the generator was bounced back
to the skill they had just finished.
**Cause:** the handoff was added in the velocity retrofit without rereading whether its
precondition — a singular chosen world — actually existed anywhere upstream. It didn't; the skill
only ever produced a plural shortlist of survivors.
**Fix:** `resolved-into-docs`. Step 4 now has an explicit selection sub-step between presenting
survivors and handing off: ask which world to build in, directly, and wait — stated as the one
deliberate exception to `velocity.md`'s "never stall," since the generator genuinely cannot run
without an answer. The template gained a **Chosen world** section (with a **Runners-up** field
distinct from **Discarded worlds** — one reached the choice and lost, the other never reached it)
and the `Needs:` line now reads "nothing further — the chosen world is recorded above" instead of
pointing at something that may not exist.
**Status:** resolved-into-docs.
