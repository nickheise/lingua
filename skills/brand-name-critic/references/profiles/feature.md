# Profile: Feature / UI

Loaded alone, as a branch. Do not restate the rubric — dimension definitions and evidence
requirements live in [`../01-ergonomics.md`](../01-ergonomics.md) and
[`../02-brandability.md`](../02-brandability.md). This file only sets the weights and the special
rule for this context.

## 1. When this profile applies

**Trigger test:** the name will appear as UI text inside an existing, already-named product — a
menu item, a settings label, a command, a button, a feature the user encounters *after* they
already opened the app.

If the user hasn't said which context they're in, **ask, briefly** — and specifically ask for
the names of the sibling features it will sit next to. This profile cannot be applied correctly
without that list; do not guess it, and do not proceed on assumed siblings.

**Feature naming and product naming are opposite problems.** A candidate that scores well under
[`venture.md`](venture.md) may correctly fail here — that is not a contradiction, it is the point
of having separate profiles.

## 2. Weights

`ergonomics_score` in the script output is profile-independent — this table is what the skill
does with `dimensions[*].score` before arguing brandability. Multiply, don't re-derive.

| Ergonomics dimension | Weight | Note |
|---|---|---|
| Pronounceability | ×1.0 neutral | Still gates everything; not a special lever here |
| Spellability | **×1.5 up** | It will appear in search boxes, support macros, and typed commands |
| Distinctiveness | **×0.5 down** | The opposite instinct from venture — blending into the existing UI vocabulary is correct |
| Rhythm & recall | ×1.0 neutral | Not a special lever |
| Verbability | ×1.0 neutral | A feature name earning a verb is a nice accident, not a goal |
| International robustness | **×1.4 up** | Support text, localization, and screen-reader use raise the cost of a hard phoneme far above venture-naming stakes |

| Brandability criterion | Weight | Note |
|---|---|---|
| Generativity | **×0.6 down** | Re-scope, don't discard: score it as *fit into the existing system*, not new-world creation — see special rule |
| Cultural familiarity (cultural-commons mode) | **×1.5 up** | This is where "weight up clarity" cashes out: pre-loaded, zero-education meaning is exactly what UI text needs |
| Cultural familiarity (owned-IP mode) | ×1.0 neutral | Still flag as a risk requiring justification per the base rubric |
| Lore integrity | ×1.0 neutral | `read the ending` applies at full strength regardless of profile |
| Sound-symbolism fit | **×0.6 down** | Where "weight down cleverness" cashes out — a clever phonetic personality is not what a command label needs |
| Ownability | **×0.5 down** | Near-irrelevant inside an existing product's UI; the parent product carries the trademark load |

`Flag, never block` still holds at this weight — a down-weighted ownability finding still gets
reported if something is genuinely collision-prone, it just carries less volume in the verdict
than it would under [`venture.md`](venture.md). Down-weighting is not the same operation as
skipping the check.

## 3. Special rule: penalize coined names hard, check fit with the existing system

**Coined-name penalty.** If the candidate's TM-distinctiveness tier (see
[`${CLAUDE_PLUGIN_ROOT}/shared/name-types.md`](${CLAUDE_PLUGIN_ROOT}/shared/name-types.md)) is
coined or fanciful, apply an *additional* ×0.5 on top of the distinctiveness down-weight above.
Ground this in the real case: Apple's own guidance rejected "Spending Power" for the plain word
"Balance" — clarity and trust beat brand expression inside an app. NN/G is emphatic that command
text should be descriptive, not branded. A feature name earning a high score by being clever is
scoring on the wrong axis entirely.

**Sibling-consistency check — run this explicitly, every time:**

1. List the actual names of the sibling features the candidate will sit beside.
2. Extract their pattern: part of speech (noun vs. verb-phrase), register (plain vs. branded),
   metaphor-or-plain (do the neighbors carry a world, or are they literal?), capitalization,
   typical length.
3. Score the candidate against that pattern as **pass / fail**, not a weighted number. This is a
   `six-siblings test` run in the opposite direction — instead of asking "can this name produce
   three siblings," ask "does this name belong among the three-plus siblings that already exist."
4. A fail here is a rejection-level finding regardless of how well the candidate scores on every
   other axis in this table.

**The cautionary tale is Microsoft Copilot:** the name got attached to roughly 80 different
things until the NAD found customers could not distinguish the products. A feature-naming skill
without a sibling-consistency check will happily help build that. Running step 1–4 above is what
prevents it.

## 4. What a good verdict / rejection look like here

**Good verdict:** plain, spellable, passes the sibling-consistency check without qualification —
"Balance" beside "Overview," "Activity," "Settings," not "Spending Power" beside them.

**Rejection looks like:** a coined or branded name for a command or label — something that would
need onboarding copy to explain what it does, or a name that would become one more Copilot
attached to an unrelated surface. High ergonomics or brandability scores do not rescue a
sibling-consistency fail.

## 5. Failure mode this profile prevents

Importing venture-naming instincts into UI text — reaching for distinctiveness and cleverness
where clarity and trust were needed — and, at the system level, the Microsoft Copilot collapse:
one brandable name stretched across enough unrelated features that customers stop being able to
tell the products apart.

## Worked micro-example: Scout

Proposed as a feature name inside a product whose sibling features are plainly named — "Search,"
"Filters," "History" — Scout fails the sibling-consistency check outright, even though it scored
well under `venture.md`. It's a branded, metaphor-bearing name dropped into a plain-language
system: exactly the opposite-problem case this profile exists to catch. Verdict: reject as
proposed. The only path to a pass is if the *whole* sibling set is being deliberately renamed
together into Scout's cartography vocabulary (waypoints, routes, base camp as first-class UI
concepts) — at which point this stops being a single feature-naming decision and becomes a
system redesign, which is out of scope for this profile alone.
