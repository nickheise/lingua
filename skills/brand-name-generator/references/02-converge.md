# Cluster → converge

From ~80–100 diverged candidates to ~12 surfaced, in two moves.

---

## Cluster (Step 2)

Sort every surviving candidate into exactly one of 3–4 approaches, all *within* the chosen world
— this is not the operator taxonomy from `01-operators.md` again, it's a coarser grouping by how
far each candidate sits from the world's literal vocabulary:

| Cluster | What lands here |
|---|---|
| **Direct** | A real term straight from the world's vocabulary, used as-is or barely touched. Highest fidelity by construction; the risk is namespace crowding — the world's most obvious terms get reused across every product built from that world. |
| **Oblique** | A real term from the world, but a peripheral one — one inferential step from the core metaphor, not the first word anyone reaches for. Trades a little fidelity for real distinctiveness. |
| **Coined-from-root** | Built on a world root via blend, affix, clip, or respell — a new string, but the root is still legible. |
| **Compound** | Two whole words concatenated — a world term plus a plain word, or two world terms. |

Use 3 clusters if the world doesn't naturally support a fourth; don't force a category empty.
**A cluster with zero or one entry is a signal Step 1 under-covered that approach** — go back to
`01-operators.md` and work the operator most likely to fill it (usually compound or blend for
"direct" gaps, affix or respell for "coined-from-root" gaps), rather than padding the shortlist
with a weak fit.

---

## Surface ~12 (Step 3)

Pull 3–4 per cluster, spread rather than concentrated. Prefer candidates that already look clean
on their operator's typical cost from `01-operators.md` — a phoneme coinage that already reads as
an illegal consonant pile, or a respell nobody would spell correctly from hearing it once, is a
weak pull even before the gate below.

### The five required deliverables

Every surfaced candidate ships with all five. No exceptions, no "TBD" — an incomplete deliverable
means the candidate isn't done, not that the field gets skipped.

1. **Type classification** — `${CLAUDE_PLUGIN_ROOT}/shared/name-types.md`, axis 1.
2. **TM distinctiveness tier** — same file, axis 2. Heuristic, not clearance; say so if genuinely
   unsure rather than guessing a tier.
3. **One-line rationale** — why this candidate, in one line, not a paragraph.
4. **Three sibling names** — see the gate immediately below. Two of the five deliverables matter
   more than the name itself, and this is one of them.
5. **Usage sentence** — see the requirement immediately below. This is the other one.

### The sibling-name gate — hard gate, no exceptions

This is the `six-siblings test` applied to one candidate instead of one world. If the world
genuinely fits, three more names should fall out of it in seconds, because the vocabulary is
already sitting there. **A candidate that cannot produce three siblings does not make the
shortlist.** Pull the next candidate from that cluster instead. This is `breadth × fidelity` and
`world, not word` doing real work at the level of a single name: failing here costs five seconds;
failing to notice and shipping the name anyway costs eighteen months.

Two failure modes, both fail the gate the same way:
- **Too few.** You can produce one or two siblings and then it dries up.
- **Weak siblings.** You can produce three, but each one needs a shrug and a justification before
  it reads as belonging to the same system. A sibling that requires explaining is not a sibling
  that passed — don't pad the count with three near-misses and call the gate satisfied.

### The usage-sentence requirement

Names fail in usage, not in lists. Write one realistic sentence that puts the candidate where it
will actually get said or read — someone saying it out loud, a doc heading, a CLI invocation, an
error message, a Slack message asking someone to check it out. Not a tagline, not "X is the
future of Y." "Open it in Fable" surfaces things "Fable" alone on a slide never will — try the
name plural, possessive, and said quickly before accepting the sentence as evidence.

---

## Fill the artifact

Write the clusters and the surfaced candidates into `assets/shortlist-template.md`, including any
candidates discarded at the sibling gate (the template has a slot for this — it's evidence the
gate actually ran, not overhead). Leave every blind-critique slot empty; SKILL.md Step 4 fills
those after the subagent returns.
