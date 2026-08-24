# Layer 3 — Practicality: factual flags with severity

**This layer reports facts, never opinions.** Domain taken or not. Collision or not. Tier or no
tier. If a sentence in this layer contains "feels", "reads as", "seems a bit" or "I'd worry that",
it belongs in Layer 2 and must be moved.

## The non-goal, stated here rather than buried in a README

> **This flags trademark risk heuristically and never gives clearance.**
>
> Nothing produced by this layer is a legal opinion, a search report, or permission to use a name.
> A heuristic screen run by a language model against no register at all is a way of finding
> obvious problems early — not a way of establishing that a name is free. **Real clearance is a
> trademark attorney** running full searches in the relevant classes and jurisdictions.
>
> Say this in the critique itself, every time. A skill that lets a reader mistake this layer for
> clearance has done real harm, and the disclaimer costs one line.

`flag, never block`. Every finding here carries a severity and **none of them can sink a
candidate.** The context profile sets the volume; nothing sets a veto. See
[`02-brandability.md`](02-brandability.md) §5 for the argument about what these facts *cost* —
that argument belongs in Layer 2, and this layer supplies the inputs to it.

---

## Severity scale — apply uniformly

| Severity | Meaning | Example |
|---|---|---|
| **high** | A concrete obstacle that will require money, a lawyer, or a change of plan. | Same-class trademark holder with an active mark. |
| **medium** | A real cost, absorbable with a workaround decided in advance. | `.com` unavailable; realistic alternatives exist. |
| **low** | Worth recording; no action required now. | An unusual vowel that a few locales will flatten. |
| **clear** | The check ran and found nothing. | No adverse meanings in the target languages. |
| **n/a** | The check does not apply to this profile. | SEO, for a feature label inside an app. |

**Headline count convention: the number in the headline is the count of `high` findings only.**
`Practicality: 2 flags` means two high-severity findings. Medium, low, clear and n/a all appear in
the table but are not counted, so the headline number stays comparable between critiques. State
the convention in the critique if the table's shape makes it ambiguous.

**`clear` and `n/a` are results.** Report them. A check that ran and found nothing is information;
a check that was silently skipped is a hole, and the reader cannot tell the difference unless the
row is there.

---

## The five checks

Run all five, in this order, every time.

### 1 · Trademark distinctiveness tier

Place the name on the distinctiveness spectrum: **generic → descriptive → suggestive → arbitrary →
fanciful.** Protection strengthens left to right; instant comprehensibility weakens left to right.
That trade is the whole of the analysis.

> **The tier definitions, the boundary cases and the worked examples live in
> [`${CLAUDE_PLUGIN_ROOT}/shared/name-types.md`](../../../shared/name-types.md).** Load it and use
> it. **Do not restate the taxonomy here or in the critique** — it is shared by all three skills
> and there is exactly one copy of it on purpose (DECISIONS ADR-005). A second copy is a second
> thing to keep correct, and the second copy is the one that goes stale.

**What this layer writes:** the tier, in one word, plus the goods/services it is being placed
against — because the tier is *relative to the category*. The same word can be generic in one
class and arbitrary in another; *Apple* is fanciful-by-arbitrariness for computers and generic for
fruit.

| Tier | Typical severity | Reading |
|---|---|---|
| Generic **for this category** | **high** | Not registrable. Correct and intentional for a feature label under a parent mark; fatal for a venture that expects to own a term. |
| Descriptive | **high** unless secondary meaning is realistic | Weak protection. Under the feature profile this is frequently the *target* — say so rather than reporting it as a defect. |
| Suggestive | medium | Protectable. Watch for a suggestive name that fits so well it drifts toward descriptive. |
| Arbitrary | low | A real word applied to an unrelated category. Strong protection plus commons familiarity — usually the best available trade. |
| Fanciful | clear | A coinage. Strongest protection. Note the cost: zero pre-loaded meaning, which is a Layer 2 finding. |

Always pair the tier with its cost, so the reader does not read "fanciful" as "best." Under the
**feature profile**, descriptive is what the profile asked for and a `high` unownability flag is
the correct price of it, not a failure.

### 2 · Knockout collision check — heuristic

> **Live search: no, for every check in this layer — including this one.** The no-live-lookups
> non-goal is usually stated for domains, which leaves the knockout check looking like it might be
> an exception. It is not. Run it from your own knowledge, say plainly that it is from memory and
> not a search, and order the collisions by risk. Never write "no conflicts found" — you did not
> look. If a web search tool happens to be available, using it here would make this table more
> defensible but would also make the critique's cost and latency unpredictable and its output
> non-reproducible, which is why v1 stays offline. Recommending a real search is the correct
> output; performing one is not this layer's job.


A knockout search is the cheap first pass a professional runs before paying for a full search: are
there obvious, identical or near-identical marks in the same or adjacent classes? **Ours is
heuristic and model-based** — no register is being queried — so it finds the obvious and misses
the rest.

**Procedure.**

1. List known users of the exact term, from memory, and say plainly that this is from memory.
2. For each, record: **who**, **what category**, **same buyer or not**, **how loud** (funding,
   advertising, search dominance).
3. Order them by collision risk:
   - **Same category and same buyer** — the dangerous one. `high`.
   - **Different category, very loud** — a marketing and search problem rather than a legal one.
     `medium`.
   - **Generic or historical usage** — background noise. `low`.
4. Check near-misses too: plurals, common misspellings from
   `orthography.homophone_spellings`, and one-letter variants. **A misspelling that lands on a
   real product is worse than one that 404s.**
5. State what a real search would add: full registers, pending applications, common-law use,
   design marks, and the jurisdictions that matter.

**Never write "no conflicts found."** Write **"no conflicts known to me; this is not a search."**
The first is a claim about the world and it is not one this layer can make.

### 3 · Domain and handle reality

No live lookups in v1 — this is a non-goal, and a stale availability claim is worse than none.
**Report what is known and what must be checked**, never a guess dressed as a fact.

| Situation | What to write |
|---|---|
| Common English word or well-known brand | `.com` is taken; treat as certain. Severity `medium`. |
| Distinctive coinage | Plausibly available; **must be verified**. Do not assert it. |
| Any case | Name the realistic fallbacks: a modifier (`get-`, `-app`, `-hq`), an alternative TLD (`.dev`, `.ai`, `.io`), or a respelling — and note that a respelling changes the Layer 1 spellability score, so it is a real trade rather than a free workaround. |
| Handles | Same reasoning. A handle mismatch across platforms is a persistent, low-grade brand cost. |
| Feature profile | Usually `n/a`. A label inside an app needs no domain; a marketing page lives under the parent domain as a path. |

### 4 · SEO and discoverability collision

**A distinct check from trademark, and it is the one people skip.** A name can be legally clean and
commercially invisible.

1. Is the term already dominated by a large incumbent, an institution, or ordinary English usage?
2. Would the product realistically rank for the bare term within eighteen months?
3. If not: what is the **compound brand term** — "name + category" — that it *can* own, and is that
   compound acceptable in ordinary speech?

| Finding | Severity |
|---|---|
| Bare term unwinnable for years against a well-funded incumbent | **high** for venture; `n/a` for feature |
| Bare term contested but reachable | medium |
| Term effectively unused | clear |

Also record the inverse case: a name so distinctive that it is unsearchable *until it exists* is
not an SEO problem, and it should not be reported as one.

**Feature profile:** SEO is generally `n/a`. The relevant surface is **in-app search**, and the
right question is whether the label is the literal word a user would type. That is usually an
argument *for* a plain descriptive name.

### 5 · Cross-cultural screen

**Run it against [`myths-blocklist.md`](myths-blocklist.md) before writing a word of it.**

> **The rule, and it is not negotiable: never repeat a folk naming myth as fact.**
>
> The Chevy Nova "no va" story is false — Snopes-debunked, the car sold fine in Mexico and
> Venezuela, and Pemex sold Nova-branded gasoline at the same time. It appears in nearly every
> naming listicle, and repeating it is the fastest way to tell a knowledgeable reader that nothing
> else in the critique was checked either. **A skill that repeats folk myths as fact loses
> credibility instantly.** The blocklist is the authoritative list; consult it, do not reconstruct
> it from memory, and do not add new folklore to the critique.

**Procedure.**

1. Establish the target languages. If launch scope is unknown, screen the majors — Spanish,
   French, German, Portuguese, Japanese, Mandarin, Hindi, Arabic — and say that is what you did.
2. For each, check: adverse meaning, unfortunate homophone, and whether the string is even legal
   orthography in that script or language.
3. **Check the claim against `myths-blocklist.md`.** If it is on the list, do not use it. If it is
   plausible but unverified, label it as unverified and recommend a native-speaker check.
4. Distinguish the two failure types, because they need different responses:
   - **Offence** — the name means something bad. `high` if real.
   - **Usability** — the name is fine but unsayable or unspellable in that language. Usually
     `medium`, and it is largely a Layer 1 consequence surfacing as an operational fact.
5. Note **false friends**, which are the most common real finding and the least reported: a word
   that exists in the target language with a *different* meaning. These are localisation
   instructions, not naming flags — record them as such.
6. State the limit honestly: this is a model-based screen, not native-speaker review. For a
   funded launch, recommend the real thing.

---

## Profile-specific extra checks

The three profile files own their own additions. Load the one in play and run whatever it adds.

| Profile | Additional practicality check | Owner |
|---|---|---|
| Venture / product | Full weight on all five above. | [`profiles/venture.md`](profiles/venture.md) |
| Feature / UI | **Sibling consistency** — does the name match the register, length and grammatical class of its neighbours in the same surface, and is it already used elsewhere in the product for a *different* concept? | [`profiles/feature.md`](profiles/feature.md) |
| Internal codename | **Leak check** — the name must never reach the UI, docs, URLs, or support macros. State this explicitly in the critique. | [`profiles/codename.md`](profiles/codename.md) |

---

## Writing this layer

- One table. Columns: **Check · Finding · Severity**. Five rows minimum, plus any profile
  additions.
- Facts only. Move every judgement to Layer 2.
- Every row gets a severity, including `clear` and `n/a`.
- The headline count is `high` findings only.
- The clearance disclaimer appears in the critique, not only in this file.
- Cross-cultural screening cites `myths-blocklist.md` and never repeats a folk naming myth as
  fact.
- Trademark tiers point at `${CLAUDE_PLUGIN_ROOT}/shared/name-types.md`; the taxonomy is never
  restated.
- `flag, never block` — this layer informs the recommendation and never makes it.
