# Profile: Internal Codename

Loaded alone, as a branch. Do not restate the rubric — dimension definitions and evidence
requirements live in [`../01-ergonomics.md`](../01-ergonomics.md) and
[`../02-brandability.md`](../02-brandability.md). This file only sets the weights and the special
rule for this context.

## 1. When this profile applies

**Trigger test:** the name is for internal use only — a project, repo, branch, or ticket
identifier — and is not intended to appear on any customer-facing surface.

If the user hasn't said which context they're in, **ask, briefly** — and specifically ask
*"will this ever ship, or could it?"* This is not a rhetorical question: "internal for now" is
not the same claim as "will never leak," and the answer changes whether this profile is even the
right one to load. If there is real uncertainty about whether it ships, treat it as
[`venture.md`](venture.md) or [`feature.md`](feature.md) instead — this profile assumes disposal
by design.

## 2. Weights

`ergonomics_score` in the script output is profile-independent — this table is what the skill
does with `dimensions[*].score` before arguing brandability. Multiply, don't re-derive.

| Ergonomics dimension | Weight | Note |
|---|---|---|
| Pronounceability | ×0.8 down | Still needs to be sayable out loud in standups — not zero |
| Spellability | ×0.6 down | Typed in Slack and commit messages more than search boxes |
| Distinctiveness | ×0.5 down | No commercial namespace to defend |
| Rhythm & recall | **×1.6 up** | Memorability is the whole job — a codename people forget isn't doing its job |
| Verbability | ×0.7 down | A nice bonus for team lingo, not a requirement |
| International robustness | ×0.2 down (near-irrelevant) | A disposable internal name has no obligation to travel |

| Brandability criterion | Weight | Note |
|---|---|---|
| Generativity | ×0.5 down | Doesn't need to generate a product vocabulary — it isn't going to have siblings shipped under it |
| Cultural familiarity | ×0.5 down | Not optimizing for zero-education-cost meaning |
| Lore integrity | ×0.8 down, but not skipped | `read the ending` still applies — see special rule for why |
| Sound-symbolism fit | **×1.4 up** | Reframed as "fun" — does the name have personality the team enjoys saying |
| Ownability | ×0.1 down (near-irrelevant) | A codename is disposable by design; trademark and domain concerns don't attach to it |

**`Flag, never block` still holds even at these low weights.** A weight of ×0.1 on ownability
means the finding gets almost no volume in the final verdict, not that it gets silently dropped —
if a codename happens to collide with something legally live, that still gets one line of flag
text. Low weight is not the same operation as no report.

## 3. Special rule: must never leak into UI — state this explicitly, every time

This is the one non-negotiable output requirement in this profile. **Every codename critique
must include an explicit leak-risk line in the verdict**, regardless of how good or bad the name
scored otherwise — something in the shape of:

> Leak risk: [low / medium / high] — this name must not appear in UI, docs, marketing, or
> support text without a deliberate rename decision.

Do not omit this line because the name seems obviously internal-only. That belief is exactly how
codenames leak.

**Read the lore anyway.** Even a name that will never ship deserves the `read the ending` check —
naming an internal effort after something whose story ends badly is bad for morale even if no
customer ever sees it, and a name good enough to leak (see the failure mode below) inherits its
lore on the way out.

**Exit plan — ask this before closing out the critique:**

1. What event triggers a rename decision — public launch, first customer-facing doc, repo going
   public, first support ticket referencing it?
2. Who owns that decision?
3. Where is the leak risk actually concentrated — repo name in URLs, error messages, Slack
   channel names that customers get added to, support macros copy-pasted verbatim?

A codename critique without an answer to these three is incomplete, independent of how the name
scored.

## 4. What a good verdict / rejection look like here

**Good verdict:** fun, sticky, the team enjoys saying it, and it ships with an explicit exit plan
already on record — not just a high fun score. Ownability and international robustness findings,
if any, still get one line per `flag, never block` — they just don't move the verdict.

**Rejection looks like:** two different shapes, and both are real here.
- Boring or forgettable — under this profile, that is an actual defect, not a neutral trait, since
  memorability and fun are the up-weighted axes this name has to earn its keep on.
- **Too good.** A name that is distinctive, generative, and brandable enough to pass `venture.md`
  is a rejection-flag *under this profile specifically*, because scoring well on those axes is
  exactly what makes a codename attractive enough to leak. Flag it, don't just admire it.

## 5. Failure mode this profile prevents

A codename that is too good, gets attached to, and ships — the name nobody officially chose
becomes the product name because everyone already loved saying it and no deliberate
venture/practicality pass ever happened before it reached a changelog or a support macro.

## Worked micro-example: Scout

As an internal codename, Scout is close to ideal on this profile's own terms: one syllable, fun
team lingo ("the Scout branch," "ship it behind the Scout flag"), and nobody has to care that
Scout Motors exists because ownability is weighted at ×0.1 here. But that strength is exactly the
danger this profile watches for — Scout is good enough to leak. The critique must flag leak risk
at `medium-high` precisely *because* it scores so well on the up-weighted axes, not despite it,
and must return with the exit-plan questions answered before this reaches a public repo name, a
changelog, or a support macro.
