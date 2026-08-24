---
name: brand-name-critic
description: Critique a candidate brand, product, feature, or codename across three layers — computed phonetic ergonomics, argued brandability, and factual practicality. Use when someone floats a specific candidate name ("what about calling it Scout?", "thinking of naming this Balance", "is Xzrq any good?"), weighs two names against each other, or asks whether a name is pronounceable, memorable, ownable, or generative. Not for general talk about naming, not for naming variables, functions, files, or branches, and not for passing mentions of the word "name".
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/phonetics.py *)
---

# Brand name critic

Three layers, three shapes of verdict: a measurement, an argument, a fact sheet. **Kill the
composite** — never average into one number. Ends at a verdict (`names or a verdict`;
`${CLAUDE_PLUGIN_ROOT}/shared/velocity.md` is binding).

Output shape: `assets/critique-template.md`; targets: `docs/reference-critiques/`. Open every
response `Step N of M · toward an argued recommendation` — this skill's deliverable.

> **Paths.** If `${CLAUDE_PLUGIN_ROOT}`/`${CLAUDE_SKILL_DIR}` are empty (bare checkout, subagent,
> sandbox), resolve yourself: plugin root holds `skills/`+`shared/`, skill dir is this file's
> folder. Never skip a file over an unexpanded path.

## Step 0 — Mode

Two-plus candidates, or an explicit "which is better" → **comparison mode**: state
`Mode: comparison`, follow `references/04-comparison.md` instead of Steps 2–4. Same rubric,
different shape. One name → continue below.

## Step 1 — Establish profile and positioning

Ask both, one message: **(1) venture/product, feature/UI, or codename** — sets every
weighting below; **(2) one or two adjectives for how this should feel to use** — Layer 2's only
sound-symbolism input; unanswered, it's "not assessable," not a tie-breaker. No answer → infer and
state it. Never stall.

Load **exactly one** profile — `venture.md` · `feature.md` · `codename.md`, under
`references/profiles/` — it owns the weights and profile checks.

## Step 2 — Ergonomics (computed)

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/phonetics.py "<name>"
```

Read `references/01-ergonomics.md` and reason over the JSON. Do not re-derive phonetics — the
script did that. Check `pronunciation.confidence` **before** any score; if it is `low`, say the
transcription is an estimate rather than a measurement.

Report `ergonomics_score` once, unmodified. Re-weight for the profile **in prose, never in
arithmetic**. `rare letters, common sounds` is the distinctiveness rule.

## Step 3 — Brandability (argued)

Read `references/02-brandability.md`. Five criteria, each with a position **and its strongest
counter-argument**. No scores.

1. **Generativity** — `world, not word`; `breadth × fidelity`; run the `six-siblings test`, find
   the breaking point, and keep the metaphor off the buttons.
2. **Cultural familiarity** — commons (weight heavily) vs. owned IP (flag as a risk).
3. **Lore integrity** — `read the ending`. Run the full story, report how it ends.
4. **Sound-symbolism fit** — tie-breaker only, using Step 1's positioning answer; label the
   evidence strength.
5. **Ownability** — `flag, never block`.

## Step 4 — Practicality (flags)

Read `references/03-practicality.md`: trademark tier, knockout collision, domain/handle,
SEO, cross-cultural screen — facts with severity, never opinions. Screen against
`references/myths-blocklist.md`; never repeat a folk naming myth as fact.

**This never gives clearance.** Say so in the critique.

Close with an **argued recommendation and what would change it** — never an absolute
yes/no; the user decides. `flag, never block`: nothing here has a veto.

## Close out

Terminal artifact — say so, and offer one follow-on: `/lingua:brand-name-generator` for
alternatives, if the recommendation was negative.

- **Edit** `references/troubleshooting.md` — revise existing entries rather than appending
  indefinitely.
- Append the name, profile, and outcome to
  `${CLAUDE_PLUGIN_ROOT}/shared/naming-decisions-log.md`.

**Read-only runs** (blind QA from the generator, an eval harness, no write access) skip both
and say `Close-out skipped — read-only run.` — never fail here, never pretend to have logged.
