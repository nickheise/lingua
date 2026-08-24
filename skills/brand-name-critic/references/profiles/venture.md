# Profile: Venture / Product

Loaded alone, as a branch. Do not restate the rubric — dimension definitions and evidence
requirements live in [`../01-ergonomics.md`](../01-ergonomics.md) and
[`../02-brandability.md`](../02-brandability.md). This file only sets the weights and the
special rule for this context.

## 1. When this profile applies

**Trigger test:** the name will sit on a cap table, a domain, a logo, or a homepage — it names
the *thing itself*, not a control inside it.

If the user hasn't said which context they're in, **ask, briefly** — "Is this the product/venture
name, a feature inside an existing product, or an internal codename?" — before picking a profile.
Do not guess silently. Venture is the highest-consequence misapplication of the three (see
[`feature.md`](feature.md) for why applying this profile to a feature name is the Copilot failure
mode in reverse).

## 2. Weights

`ergonomics_score` in the script output is profile-independent — this table is what the skill
does with `dimensions[*].score` before arguing brandability. Multiply, don't re-derive.

| Ergonomics dimension | Weight | Note |
|---|---|---|
| Pronounceability | ×1.0 neutral | Baseline hearability still gates everything |
| Spellability | ×1.0 neutral | Not a venture-specific lever |
| Distinctiveness | **×1.5 up** | Core venture asset — low neighborhood density, search ownability |
| Rhythm & recall | ×1.0 neutral | Always useful, not profile-specific |
| Verbability | **×1.4 up** | "Let's Scout this" is a growth signal a feature name never needs |
| International robustness | ×1.0 neutral | Matters if the market is global; not the defining axis here |

| Brandability criterion | Weight | Note |
|---|---|---|
| Generativity | **×1.5 up** | `world, not word` — this is the single highest-leverage axis for a venture name |
| Cultural familiarity (cultural-commons mode) | **×0.7 down** | This is where "weight down instant descriptiveness" cashes out: pre-loaded meaning is good, but too much of it *is* descriptiveness, which is the opposite of what a venture name wants |
| Cultural familiarity (owned-IP mode) | ×1.0 neutral | Still flag as a risk requiring justification per the base rubric — this profile doesn't change that |
| Lore integrity | ×1.0 neutral | `read the ending` applies at full strength regardless of profile |
| Sound-symbolism fit | ×1.0 neutral | Tie-breaker at any weight |
| Ownability | **×1.6 up** | Highest-weighted axis of the three profiles — see special rule |

**On "weight down instant descriptiveness":** this isn't a rubric dimension to multiply, it's an
instruction that reaches into practicality's trademark-distinctiveness tier
([`../03-practicality.md`](../03-practicality.md)). A venture candidate sitting at "descriptive"
on the generic → descriptive → suggestive → arbitrary → fanciful spectrum should read as a
finding, not a pass, even if every ergonomics dimension scores high. See
[`${CLAUDE_PLUGIN_ROOT}/shared/name-types.md`](${CLAUDE_PLUGIN_ROOT}/shared/name-types.md) for
the full spectrum mapping.

## 3. Special rule: tolerate opacity

A venture name **should** be slightly opaque. Do not penalize a candidate for failing to
describe the product — that's the wrong instinct imported from feature naming
(see [`feature.md`](feature.md), which wants exactly the opposite). Suggestive, arbitrary, and
fanciful names are all acceptable outcomes here; generic and descriptive are the only tiers worth
flagging.

**Ownability matters most here of the three profiles.** Crowded namespaces are, per PRD §3.5,
"the whole conversation" for a venture — trademark collision, domain availability, and SEO
crowding compound directly into cost of acquisition. Report ownability findings with real
severity language (`high` / `medium` / `low`, named collisions, not vague hedging).

But **`flag, never block` still holds, even here.** Ownability has no veto power in this profile
either — a crowded namespace is a cost to plan around (legal budget, a modifier word, a
differentiated domain), never a disqualification the critic imposes unilaterally. The user
decides whether the cost is worth paying.

## 4. What a good verdict / rejection look like here

**Good verdict:** high generativity with a real `six-siblings test` pass, strong verbability,
distinctiveness that at minimum sits above the neighborhood-density median — with ownability
findings reported honestly, severity-labeled, and never treated as disqualifying on their own.

**Rejection looks like:** a name that is high-generic on the TM spectrum (literally names the
category — "the payments app called Payments"), or one with near-zero generativity (`breadth × fidelity`
both fail — no sibling vocabulary and no metaphor to extend), regardless of how clean its
ergonomics score is. A venture name can survive a crowded namespace; it cannot survive having
nothing to say once the first ten sibling names run out.

## 5. Failure mode this profile prevents

Picking a name that is comfortable and instantly understood but has nothing left to give a
product as it grows — a name that describes the category instead of building brand architecture.
Comfortable and unoriginal is a valid verdict; the profile exists so it gets said out loud instead
of hiding behind a high ergonomics score.

## Worked micro-example: Scout

Under this profile, Scout scores strongly: generativity is near-maximal — waypoints, blazes,
cairns, routes, base camp, field notes, all arriving with an icon already implied, a clean
`six-siblings test` pass, `breadth × fidelity` both hold (a waypoint really is a saved position).
Verbability is strong ("scout it out"). Distinctiveness and ownability are where the tension
lives: Scout Motors, Scout24, Scout APM, and the scouting movement all occupy this word, so the
ownability finding is reported at `high` severity — the loudest ownability language of the three
profiles, because this is where it matters most. Per `flag, never block`, that finding does not
sink the recommendation; it becomes a named cost (trademark search, likely need for a modifier or
a differentiated visual mark) the user weighs against the generativity payoff. Net verdict:
recommend, with the ownability risk stated plainly rather than buried.
