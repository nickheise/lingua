# Profile: Feature / UI

Loaded alone, as a branch. Do not restate the rubric — dimension definitions and evidence
requirements live in [`../01-ergonomics.md`](../01-ergonomics.md) and
[`../02-brandability.md`](../02-brandability.md). This file only sets the weights and the special
rule for this context.

## 1. When this profile applies

**Trigger test:** the name will appear as UI text inside an existing, already-named product — a
menu item, a settings label, a command, a button, a feature the user encounters *after* they
already opened the app.

This profile has one more question `SKILL.md` Step 1 doesn't already ask: **name the sibling
features it will sit next to.** Ask directly, not apologetically — this profile cannot be applied
correctly without that list, so it isn't optional politeness, it's the input the sibling-
consistency check runs on. Do not guess it, and do not proceed on assumed siblings.

**Feature naming and product naming are opposite problems.** A candidate that scores well under
[`venture.md`](venture.md) may correctly fail here — that is not a contradiction, it is the point
of having separate profiles.

## 2. Emphasis

`ergonomics_score` in the script output is profile-independent, and there is no weighted
recomputation anywhere in this skill — see `SKILL.md` ("re-weight in prose, never in arithmetic")
and [`../01-ergonomics.md`](../01-ergonomics.md) §4 ("do not compute a weighted score"). What this
table sets is **how much space each dimension gets in the argument.**

| Ergonomics dimension | Emphasis | Note |
|---|---|---|
| Pronounceability | medium | Still gates everything; not a special lever here |
| Spellability | **very high** | It will appear in search boxes, support macros, and typed commands |
| Distinctiveness | **low — often inverted** | The opposite instinct from venture — blending into the existing UI vocabulary is correct |
| Rhythm & recall | medium | Not a special lever |
| Verbability | medium | A feature name earning a verb is a nice accident, not a goal |
| International robustness | **high** | Support text, localization, and screen-reader use raise the cost of a hard phoneme far above venture-naming stakes |

Brandability has no scores to set emphasis on — [`../02-brandability.md`](../02-brandability.md)
is explicit that a number here would be false precision. What this table sets instead is **how
much scrutiny each criterion gets**, which argument leads, and which counter-argument matters most:

| Brandability criterion | Scrutiny here | Note |
|---|---|---|
| Generativity | **re-scoped, not discarded** | Score it as *fit into the existing system*, not new-world creation — see special rule |
| Cultural familiarity (cultural-commons mode) | **the lead argument** | This is where "weight up clarity" cashes out: pre-loaded, zero-education meaning is exactly what UI text needs |
| Cultural familiarity (owned-IP mode) | full strength | Still flag as a risk requiring justification per the base rubric |
| Lore integrity | full strength | `read the ending` applies at full strength regardless of profile |
| Sound-symbolism fit | **discount it** | Where "weight down cleverness" cashes out — a clever phonetic personality is not what a command label needs |
| Ownability | **near-irrelevant** | The parent product carries the trademark load |

`Flag, never block` still holds even at low emphasis — a de-emphasized ownability finding still
gets reported if something is genuinely collision-prone, it just carries less airtime in the
recommendation than it would under [`venture.md`](venture.md). De-emphasizing is not the same
operation as skipping the check.

## 3. Special rule: penalize coined names hard, check fit with the existing system

**Coined-name penalty.** If the candidate's TM-distinctiveness tier (see
[`${CLAUDE_PLUGIN_ROOT}/shared/name-types.md`](${CLAUDE_PLUGIN_ROOT}/shared/name-types.md)) is
coined or fanciful, that is a **rejection-level finding under this profile**, on top of — not
instead of — the low emphasis on distinctiveness above. Ground this in the real case: Apple's own
guidance rejected "Spending Power" for the plain word "Balance" — clarity and trust beat brand
expression inside an app. NN/G is emphatic that command text should be descriptive, not branded.
A feature name earning a high score by being clever is scoring on the wrong axis entirely.

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

## 4. What a good outcome / rejection look like here

**Good outcome:** plain, spellable, passes the sibling-consistency check without qualification —
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
system: exactly the opposite-problem case this profile exists to catch. Reject as proposed. The
only path to a pass is if the *whole* sibling set is being deliberately renamed
together into Scout's cartography vocabulary (waypoints, routes, base camp as first-class UI
concepts) — at which point this stops being a single feature-naming decision and becomes a
system redesign, which is out of scope for this profile alone.
