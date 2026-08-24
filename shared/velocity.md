# The velocity contract

**Every skill in this suite is a means. The run is over when there are names, or a verdict.**

> **One word, two senses — worth separating once, here.** "A verdict" in this file means the
> *completed three-layer readout*: ergonomics, brandability, practicality, and an argued
> recommendation. It is never "the verdict" in the sense the critic itself explicitly refuses to
> give — a final, unappealable yes/no. Reaching a verdict-artifact and delivering an absolute
> verdict-judgment are different things; this suite always does the first and never the second.
> `flag, never block` is what keeps them separate in practice.

World-building, briefs, operator sweeps, and rubric layers are all necessary work — and none of
them is a destination. A run that ends with a thoughtful document and no next move has failed,
however good the document is. This file is the contract every skill honours so that does not
happen. It is referenced, never copied.

---

## 1 · The outcome invariant — `names or a verdict`

Every chain through this suite terminates at exactly one of two artifacts:

| Terminal artifact | Reached by | Looks like |
|---|---|---|
| **A set of names** | worlds → generator | ~12 candidates, each with three sibling names and a usage sentence, plus an independent blind critique |
| **A verdict on a name** | critic | `Ergonomics N · Brandability: <clause> · Practicality: N flags`, an argued recommendation, and what would change it |

There is no third ending. If a run is drifting toward "here is some interesting thinking about
naming," it has lost the thread — return to whichever of the two outcomes the user came for and
name the remaining distance to it.

**Which one the user came for is decidable in one question, and usually in zero.** They arrived
with a name → verdict. They arrived with a concept, a description, or a document → names. If it is
genuinely ambiguous, ask once, in one line, and do not proceed on a guess.

## 2 · The step ledger

Open every substantive response with one line:

```
Step 2 of 4 · toward <this skill's terminal deliverable>
```

**State this skill's own deliverable, not the chain's.** `brand-name-worlds` is working toward
*2–3 stress-tested worlds*, not toward a shortlist of names. This is not bookkeeping pedantry —
an agent that can see "names" as the goal while doing the fidelity test will rush the fidelity
test to get there, which is the exact failure the maker split exists to prevent. The user gets
the whole roadmap from the README and from the handoff at the end. The agent gets the current
leg.

The ledger costs one line and it is what makes a multi-step process feel like progress rather
than like an interview with no visible end.

## 3 · `earn the question`

**Ask as many questions as the work genuinely needs. Ask no question that does not change the
output.**

The user has explicitly said they would rather be grilled than hand-held, and that they expect to
share the workload — quality has a cost and they are willing to pay it. So a thin brief is not
politeness, it is a worse deliverable. But an unbounded discovery interview is the opposite
failure, and the deletion test applies to questions exactly as it applies to prose: *would the
answer change what I produce?* If no, cut it.

Three rules make this concrete:

1. **Every question names what it unblocks.** Not "what's the personality?" but "what should this
   feel like to use — that decides which worlds are even eligible in Step 2." A question whose
   purpose you cannot state in a clause is a question you have not earned.
2. **Batch, don't drip.** One message with four questions beats four messages with one. Follow-up
   rounds are fine; ping-pong is not.
3. **Follow up only on an answer too vague to run the next step on.** "It's for developers" cannot
   drive a fidelity test; "staff engineers debugging someone else's service at 2am" can. Name the
   vagueness and ask again — once. Then proceed on what you have and say what you assumed.

**Never stall for an answer you can proceed without.** Missing input is a stated assumption, not
a blocker. Say what you assumed, mark it as an assumption, and keep moving toward the outcome.

## 4 · The handoff

A skill that stops without telling the user what comes next has stranded them. Every terminating
step ends with:

- **the exact command** to run next, copy-pasteable
- **what it will produce** in one clause
- **what it needs** from what was just produced

```
Next: /brand:name-generator
Produces ~12 candidates inside your chosen world, each with three sibling names and a usage
sentence, independently critiqued.
Needs: the chosen world from the brief above.
```

If the run has reached a terminal artifact — names or a verdict — say so plainly and offer the
one obvious follow-on rather than inventing more process.

## 5 · The anti-patterns

Name these when you catch yourself in one.

| Anti-pattern | What it looks like | The fix |
|---|---|---|
| **Process for its own sake** | A beautiful world brief with no route onward | The handoff in §4 |
| **The interview that never converges** | Round five of clarifying questions | `earn the question`; batch; proceed on assumptions |
| **The polite thin brief** | Four vague answers accepted without challenge, producing mush downstream | One targeted follow-up round on the vague ones |
| **Silent stalling** | Waiting on an answer that would not change the output | Assume, state the assumption, continue |
| **Goal leakage** | Naming the chain's outcome while mid-way through a leg | Ledger states *this skill's* deliverable only |
| **The unearned stop** | Ending mid-chain because the current artifact looks finished | `names or a verdict` — neither is a document about naming |
