# The brief

Two paths in. Take whichever applies — never ask for both.

## Path A — a positioning canvas exists

Auto-populate from it. Ask nothing. Map these canvas fields directly into the brief fields below:

These are the **actual section headings** of the positioning canvas, not paraphrases. Match on
them literally; if a heading is missing, treat that field as absent rather than guessing which
nearby section meant it.

| Canvas section | Brief field | Why it matters here |
|---|---|---|
| **Best-fit customers** | Who for | Sets the register a world's vocabulary needs to land with |
| **Market category** | What it does | The functional shape the metaphor has to map onto |
| **Unique capabilities** | What it does (specifics) | The concrete things the metaphor must be able to name. Feed these straight into the five-concept fidelity test in Step 3 — they are the real product concepts, so they beat any you would invent. |
| **Value themes** | One-word personality (inferred) | The angle a world should sharpen, not flatten. Dunford's chain runs capabilities → value themes, so infer personality from the themes, not from the capability list. |
| **Competitive alternatives** | What it's replacing | **Especially valuable** — see below |
| **Relevant trends** (optional) | Era check | If present, use it against the eras section of `${CLAUDE_PLUGIN_ROOT}/shared/example-bank.md` — a world that sounds like 2011 dates the product before it ships. |

**Competitive alternatives are worth more than the other fields combined for this
purpose.** They define the phonetic and semantic white space to avoid — if three competitors
already lean nautical, a fourth nautical world isn't distinctive, it's confirmation. Read the
alternatives list before proposing worlds in Step 2, not after.

State plainly that the canvas was found and used, and name the file or source. Do not re-ask
anything the canvas already answers.

## Path B — no canvas exists

Ask the compressed four-question mini-brief, in this order, as one message:

1. **What does it do?** One or two sentences, functional, not aspirational.
2. **Who is it for?** A person or role, not a market segment abstraction.
3. **What is it replacing?** An existing tool, habit, or workaround — this doubles as the
   competitive-alternatives field a canvas would have supplied, so press for a real answer here
   rather than "nothing, it's new."
4. **One-word personality.** A single adjective. Resist a sentence — the compression is the
   point; a world-sourcing pass on a paragraph produces mush.

Do not expand this into a longer discovery interview. Four questions, one message, proceed on
the answers given.

## Either way — this brief is provisional

State this explicitly in the output, once, and move on:

> A name chosen at idea stage is cheap to change. A name chosen after positioning exists is
> expensive to change. This brief was built [from an existing canvas | without one]; if it was
> built without one, re-validate the chosen world against a real positioning canvas once one
> exists — the world that fit a four-question guess may not survive contact with the actual
> best-fit customer and competitive set.

Structure the brief's own output (what it does / who for / what it's replacing / personality,
plus competitive alternatives if known) as a small standalone block at the top of the eventual
`world-brief-template.md`. It should be legible on its own to a future positioning facilitator
run — this leg work seeds that step, it isn't thrown away once naming is done.
