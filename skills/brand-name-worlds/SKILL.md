---
name: brand-name-worlds
description: Turn a project idea into 2-3 stress-tested semantic worlds a naming system could be built from. Produces no name candidates — it stops at the chosen world. Run this yourself when you're about to name something and want real leg work instead of picking a word on vibes; it will not fire on its own. Not for critiquing a name you've already got (that's brand-name-critic).
disable-model-invocation: true
---

# Brand name worlds

`world, not word`. The most valuable property of a name is generativity — a vocabulary and an
iconography attached for free. This skill's whole job is finding a semantic domain worth building
that vocabulary from, and proving it holds up before anyone gets attached to a word.

**This skill terminates at a chosen world. It does not produce names.** That boundary is not a
formality — see the guard in Step 4.

> **Paths.** `${CLAUDE_PLUGIN_ROOT}` and `${CLAUDE_SKILL_DIR}` are substituted only when the plugin
> is installed. If either comes back empty — a bare checkout, a subagent, a sandbox — resolve it
> yourself: the plugin root holds `skills/` and `shared/`; the skill dir is this file's own folder.
> Never skip a file, or a script, because its path did not expand.

## Step 1 — Load the brief

Check for an existing positioning canvas. If one exists, auto-populate from it and ask nothing.
If not, run the compressed four-question mini-brief. Either way, structure the output so it can
seed a positioning facilitator later — this leg work should not be thrown away.

→ `references/01-brief.md`

## Step 2 — Propose 5-7 candidate worlds

Semantic domains, not tonal directions. "Trustworthy" is a tone; cartography is a world. Draw
from the fixed catalogue, plus one candidate not on the list.

→ `references/02-world-sourcing.md`

## Step 3 — Stress-test fidelity before naming anything

`breadth × fidelity`. First the `six-siblings test` — can you name six distinct terms from this
world without straining? Then take five real product concepts from the brief and ask what each is
called in this world. If three of five require a shrug, discard the world. Run this on every
surviving candidate from Step 2 — this is the step most likely to get rushed, and it's where the
value is.

→ `references/03-fidelity-test.md`

## Step 4 — Converge to 2-3 surviving worlds. Stop.

Write the survivors, with the fidelity evidence for each, into
`assets/world-brief-template.md`. Present it. Then stop.

**Read this before writing anything else.** You have just done the hard part, and the next thing
that will occur to you is a candidate name — one of the survivors is going to suggest a word, and
it will feel helpful to say it out loud. Don't. Producing a name at this point is not a bonus,
it's a failure of this skill: the entire reason this is a separate skill from the generator is
that naming-in-the-moment is exactly the failure mode being designed around. If a name surfaces in
your own reasoning, note that a world produced one (that's a good sign for Step 3) without writing
the word itself into the output. The deliverable is the world. Naming happens in a different skill,
later, deliberately.

## Close out (every run)

Edit `references/troubleshooting.md` — revise existing entries rather than appending
indefinitely.

**On a read-only run, skip the close-out and say `Close-out skipped — read-only run.`**
