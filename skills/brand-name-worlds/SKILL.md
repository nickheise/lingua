---
name: brand-name-worlds
description: Turn a project idea into 2-3 stress-tested semantic worlds a naming system could be built from. Produces no name candidates — it stops at the chosen world. Run this yourself when you're about to name something and want real leg work instead of picking a word on vibes; it will not fire on its own. Not for critiquing a name you've already got (that's brand-name-critic).
disable-model-invocation: true
---

# Brand name worlds

`world, not word`. This skill finds a semantic domain generative enough to supply a whole
vocabulary — and proves it holds up before anyone gets attached to a word. **It terminates at a
chosen world and produces no names.** That boundary is not a formality — see the guard in Step 4.

**`${CLAUDE_PLUGIN_ROOT}/shared/velocity.md` is binding** — `names or a verdict`,
`earn the question`, never stall, the handoff. Read it. Open every substantive response with
`Step N of 4 · toward 2-3 stress-tested worlds`: *this* skill's deliverable, never the chain's,
or the fidelity test gets rushed to reach it.

> **Paths.** If `${CLAUDE_PLUGIN_ROOT}` or `${CLAUDE_SKILL_DIR}` arrives unexpanded — bare
> checkout, subagent, sandbox — resolve it: the plugin root holds `skills/` and `shared/`; the
> skill dir is this file's own folder. Never skip a file because its path did not expand.

## Step 1 — Load the brief

Three paths: a positioning canvas (auto-populate, ask nothing) · a project document — PRD, spec,
README (extract and cite first, ask only about real gaps, harvest Step 3's five concepts from it)
· neither (four questions, one message; one follow-up round only on answers too vague to drive
Step 3). Structure the brief to seed a positioning facilitator later.

→ `references/01-brief.md`

## Step 2 — Propose 5-7 candidate worlds

Semantic domains, not tonal directions. "Trustworthy" is a tone; cartography is a world. Draw
from the fixed catalogue, plus one candidate not on the list.

→ `references/02-world-sourcing.md`

## Step 3 — Stress-test fidelity before naming anything

`breadth × fidelity`. First the `six-siblings test` — six distinct terms from this world without
straining? Then run the brief's five real product concepts through it: what is each called here?
Three shrugs of five and the world is discarded. Every Step 2 survivor gets this, the favorite
included.

→ `references/03-fidelity-test.md`

## Step 4 — Converge to 2-3 surviving worlds. Stop.

Write the survivors, with the fidelity evidence for each, into
`assets/world-brief-template.md`. Present it. Then stop.

**Read this before writing anything else.** You have just done the hard part, and the next thing
that will occur to you is a candidate name — one of the survivors is going to suggest a word, and
it will feel helpful to say it out loud. Don't. Producing a name here is not a bonus, it's a
failure: this is a separate skill from the generator precisely because naming-in-the-moment is the
failure mode being designed around. If a name surfaces in your own reasoning, note that a world
produced one (that's a good sign for Step 3) without writing the word itself into the output. The
deliverable is the world.

**Then hand off** — the deliverable is complete; this is the next leg, not the names. Close with:

```
Next: /lingua:brand-name-generator
Produces ~12 candidates inside your chosen world, each with three sibling names and a usage
sentence, independently critiqued.
Needs: the chosen world from the brief above.
```

## Close out (every run)

Edit `references/troubleshooting.md` — revise existing entries rather than appending
indefinitely. **On a read-only run, skip it and say `Close-out skipped — read-only run.`**
