---
name: brand-name-generator
description: Turn a chosen semantic world into a clustered shortlist of ~12 name candidates, each with type, trademark tier, rationale, three sibling names, and a usage sentence — then hand the shortlist to a blind subagent for independent critique. Run this yourself once brand-name-worlds has produced a world to build from; it will not fire on its own. Requires a chosen world — arrive without one and this points you to /lingua:brand-name-worlds instead of improvising one. Not for critiquing a name you already have (that's brand-name-critic) and not for building the semantic world itself (that's brand-name-worlds).
disable-model-invocation: true
---

# Brand name generator

`diverge → cluster → converge`. `world, not word`. Turns one chosen semantic world into a
clustered shortlist ready for critique; it does not build worlds. Terminates at **names**
(`names or a verdict`; `${CLAUDE_PLUGIN_ROOT}/shared/velocity.md` is binding).

Open every response `Step N of M · toward a critiqued shortlist of ~12 candidates` — this skill's
deliverable, not the chain's.

**Requires a chosen world.** Arrive without one → say this and stop, don't improvise one:
`Next: /lingua:brand-name-worlds` — produces 2–3 stress-tested worlds; needs your brief or
concept.

> **Paths.** If `${CLAUDE_PLUGIN_ROOT}`/`${CLAUDE_SKILL_DIR}` are empty (bare checkout, subagent,
> sandbox), resolve yourself: plugin root holds `skills/`+`shared/`, skill dir is this file's
> folder. Never skip a file over an unexpanded path.

## Step 1 — Diverge

~80–100 candidates inside the chosen world, worked through the construction operators — **not a
freeform brainstorm.** The operator list is reference material to actually work through; quota by
operator, not free-association until tired.

→ `references/01-operators.md`

## Step 2 — Cluster

Group the divergent list into 3–4 approaches *within* the world: direct, oblique,
coined-from-root, compound. An empty or single-entry cluster means Step 1 under-covered that
approach — go back rather than force a fit.

## Step 3 — Converge

Surface ~12 candidates, spread across the clusters. Each ships with all five: type
classification, TM distinctiveness tier, one-line rationale, three sibling names, a usage
sentence.

**The sibling names are the `six-siblings test` applied per candidate, and they are a hard gate:
a candidate that cannot produce three siblings does not make the shortlist.** Learn the dead end
in five seconds here, not eighteen months from now. The usage sentence exists for the same
reason names fail in usage, not in lists — write a realistic sentence, not a tagline.

→ `references/02-converge.md`. Fill `assets/shortlist-template.md`.

## Step 4 — Blind subagent QA (mandatory, every run)

The generator does not grade its own output — an agent evaluating work it just produced sees
fewer flaws in it, because it still holds the reasons for each choice.

Spawn a **fresh-context subagent** (Agent/Task tool, `general-purpose` type). Prompt: the
candidate names **alphabetized** — never generation order, never a favorite flagged — the context
profile, and an instruction to run `brand-name-critic` on each and return its critique.

**Withhold everything else** — world, operator, cluster, rationale, siblings, usage sentence. A
critic that knew the world would judge fidelity better and destroy the fresh-context property this
step buys. Full argument: [`references/02-converge.md`](references/02-converge.md).

Attach each critique under its candidate's block.

## Close out

Terminal artifact — names, each already critiqued. Say so; the cross-candidate call is the
user's. A candidate reading weak against its critique gets another generator pass, not a manual
patch here.

Edit `references/troubleshooting.md` — revise entries, don't append indefinitely. Append the
world, the candidates, and the outcome to `${CLAUDE_PLUGIN_ROOT}/shared/naming-decisions-log.md`.
**On a read-only run, skip both and say `Close-out skipped — read-only run.`**
