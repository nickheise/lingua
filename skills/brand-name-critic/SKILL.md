---
name: brand-name-critic
description: Critique a candidate brand, product, feature, or codename across three layers — computed phonetic ergonomics, argued brandability, and factual practicality. Use when someone floats a specific candidate name ("what about calling it Scout?", "thinking of naming this Balance", "is Xzrq any good?"), weighs two names against each other, or asks whether a name is pronounceable, memorable, ownable, or generative. Not for general talk about naming, not for naming variables, functions, files, or branches, and not for passing mentions of the word "name".
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/phonetics.py *)
---

# Brand name critic

Three layers, three shapes of verdict: a measurement, an argument, a fact sheet.
**Kill the composite** — never average them into one number.

Output shape: `assets/critique-template.md`. Worked targets:
`docs/reference-critiques/`.

## Step 1 — Establish the profile

Ask, or infer and state the inference: **venture/product**, **feature/UI**, or **internal
codename**? Feature naming and product naming are opposite problems, so this decides the
weighting.

Load **exactly one**: `references/profiles/venture.md` · `references/profiles/feature.md` ·
`references/profiles/codename.md`. It owns the weights and any profile-specific check.

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
4. **Sound-symbolism fit** — tie-breaker only; label the evidence strength.
5. **Ownability** — `flag, never block`.

## Step 4 — Practicality (flags)

Read `references/03-practicality.md`. Facts with severity, never opinions: trademark tier,
knockout collision, domain/handle, SEO, cross-cultural screen. Screen against
`references/myths-blocklist.md` — never repeat a folk naming myth as fact.

**This never gives clearance.** Say so in the critique.

Close with an **argued recommendation and what would change it**. Never a verdict — the user
decides. `flag, never block`: nothing here has a veto.

## Close out (every run)

- **Edit** `references/troubleshooting.md` — revise existing entries rather than appending
  indefinitely.
- Append the name, profile, and outcome to
  `${CLAUDE_PLUGIN_ROOT}/shared/naming-decisions-log.md`.
