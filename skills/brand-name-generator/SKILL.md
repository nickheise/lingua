---
name: brand-name-generator
description: Turn a chosen semantic world into a clustered shortlist of ~12 name candidates, each with type, trademark tier, rationale, three sibling names, and a usage sentence — then hand the shortlist to a blind subagent for independent critique. Run this yourself once brand-name-worlds has produced a world to build from; it will not fire on its own. Requires a chosen world — arrive without one and this points you to /lingua:brand-name-worlds instead of improvising one. Not for critiquing a name you already have (that's brand-name-critic) and not for building the semantic world itself (that's brand-name-worlds).
disable-model-invocation: true
---

# Brand name generator

`diverge → cluster → converge`. `world, not word`. This skill turns one already-chosen semantic
world into a clustered shortlist ready for critique. It does not build worlds.

**Requires a chosen world.** If `/lingua:brand-name-worlds` hasn't been run yet, say so and stop
— don't improvise a world here. Take the world's name, its vocabulary, and its
`breadth × fidelity` evidence as given input.

> **Paths.** `${CLAUDE_PLUGIN_ROOT}` and `${CLAUDE_SKILL_DIR}` are substituted only when the plugin
> is installed. If either comes back empty — a bare checkout, a subagent, a sandbox — resolve it
> yourself: the plugin root holds `skills/` and `shared/`; the skill dir is this file's own folder.
> Never skip a file, or a script, because its path did not expand.

## Step 1 — Diverge

~80–100 candidates inside the chosen world, worked through the construction operators — **not a
freeform brainstorm.** The operator list is reference material to actually work through; quota by
operator, not free-association until tired.

→ `references/01-operators.md`

## Step 2 — Cluster

Group the divergent list into 3–4 approaches *within* the world: direct, oblique,
coined-from-root, compound. A cluster with zero or one entry means Step 1 under-covered that
approach — go back rather than force a candidate into it.

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
fewer flaws in it, because it still holds the reasons for each choice. So before the shortlist is
presented, it gets an independent read.

Spawn a **fresh-context subagent** (the Agent/Task tool, `general-purpose` type) whose entire prompt is:

- the surfaced candidate names, **alphabetized** — never in generation order, never annotated
  with a favorite
- the context profile (venture / feature / codename)
- an instruction to run the `brand-name-critic` skill independently on each name and return its
  full critique

**Withhold everything else** — the world, the operator, the cluster, the rationale, the siblings,
the usage sentence. The subagent derives all of it. Withholding is the point: a critic that knew
the world would judge fidelity better and destroy the fresh-context property this step exists to
buy. See [`references/02-converge.md`](references/02-converge.md) for the full argument.

Attach each critique under its candidate's block. The cross-candidate call is the user's.

## Close out

Edit `references/troubleshooting.md` — revise entries, do not append indefinitely. Append the
world, the candidates, and the outcome to `${CLAUDE_PLUGIN_ROOT}/shared/naming-decisions-log.md`.
**On a read-only run, skip both and say `Close-out skipped — read-only run.`**
