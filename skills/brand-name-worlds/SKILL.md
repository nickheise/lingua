---
name: brand-name-worlds
description: Turn a project idea into 2-3 stress-tested semantic worlds a naming system could be built from. Produces no name candidates — it stops at the chosen world. Run this yourself when you're about to name something and want real leg work instead of picking a word on vibes; it will not fire on its own. Not for critiquing a name you've already got (that's brand-name-critic).
disable-model-invocation: true
---

# Brand name worlds

`world, not word`. Finds a semantic domain generative enough to supply a whole vocabulary, and
proves it holds up before anyone gets attached to a word. **Terminates at a chosen world, no
names** — see the guard in Step 4.

**`${CLAUDE_PLUGIN_ROOT}/shared/velocity.md` is binding** — `names or a verdict`,
`earn the question`, never stall, the handoff. Open every response with
`Step N of 4 · toward 2-3 stress-tested worlds`, this skill's deliverable, never the chain's, or
the fidelity test gets rushed to reach it.

> **Paths.** If `${CLAUDE_PLUGIN_ROOT}` or `${CLAUDE_SKILL_DIR}` arrives unexpanded, resolve it
> yourself: plugin root holds `skills/`+`shared/`, skill dir is this file's folder. Never skip a
> file because its path didn't expand.

## Step 1 — Load the brief

Three paths: a positioning canvas (auto-populate, ask nothing) · a project document (extract and
cite first, ask only real gaps, harvest Step 3's five concepts from it) · neither (four
questions, one message; one follow-up round only on answers too vague for Step 3). Structure the
brief to seed a positioning facilitator later. → `references/01-brief.md`

## Step 2 — Propose 5-7 candidate worlds

Semantic domains, not tonal directions — "trustworthy" is a tone, cartography is a world. Draw
from the fixed catalogue, plus one candidate not on the list. → `references/02-world-sourcing.md`

## Step 3 — Stress-test fidelity before naming anything

`breadth × fidelity`. First the `six-siblings test` — six distinct terms without straining? Then
run the brief's five real concepts through it: what is each called here? Three shrugs of five and
the world is discarded. Every survivor gets this, favorite included. → `references/03-fidelity-test.md`

## Step 4 — Converge to 2-3 surviving worlds. Ask which one. Stop.

Write the survivors, with the fidelity evidence for each, into
`assets/world-brief-template.md`. Present it.

**Read this before writing anything else.** One survivor is about to suggest a word it will feel
helpful to say out loud. Don't. Naming here is a failure, not a bonus — this is a separate skill
from the generator precisely because naming-in-the-moment is the failure mode being designed
around. If a name surfaces in your own reasoning, note that a world produced one (good sign for
Step 3) without writing the word itself.

**Then ask which world to build in — directly, and wait.** A world is a domain, not a candidate;
choosing "cartography" names nothing. This is the one exception to `velocity.md`'s "never stall":
the generator cannot run without one chosen world. Record it in the template's **Chosen world**
field; runners-up stay in as discarded-but-recorded (template rule 2).

**Then hand off** — the deliverable is complete; this is the next leg, not the names. Close with:

```
Next: /lingo:brand-name-generator
Produces ~12 candidates inside <chosen world>, each with three sibling names and a usage
sentence, independently critiqued.
Needs: nothing further — the chosen world is recorded above.
```

## Close out (every run)

Edit `references/troubleshooting.md` — revise, don't append. **Attempt the write; if it
fails, say `Close-out skipped — read-only run (write unavailable: <reason>).`** Don't assert
read-only without trying.
