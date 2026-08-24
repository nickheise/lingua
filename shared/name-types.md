# Name types × trademark distinctiveness

Two axes. They correlate but are **not the same axis**, and the gap between them is where the
useful judgment lives. Confusing them is the single most common naming-critique error: treating
"clever" as "protectable," or "plain" as "weak."

- **Name type** — a *linguistic/construction* classification. How the name was built.
- **Trademark distinctiveness tier** — a *legal* classification. How hard it is to own.

This file is taxonomy and examples only. The rubric that weighs these against context profiles
lives in the skills, not here.

---

## Axis 1 — Name type (construction)

Ordered by how far the name sits from the plain descriptive term for the thing.

| Type | Definition | Construction operators that produce it |
|---|---|---|
| **Descriptive** | States what the thing is or does, directly | Plain compound of category terms; literal noun phrase |
| **Suggestive** | Hints at a benefit or quality; requires a small inferential step | Metaphor-lite compounding; affix on a benefit word; partial abstraction |
| **Associative / metaphoric** | Imports a whole external domain (cartography, seafaring, mythology) as vocabulary | Domain transplant; extended metaphor; borrowed lexicon from an unrelated field |
| **Coined-from-root** | Built from real morphemes (Latin/Greek roots, real affixes) but not a dictionary word | Root + affix; blend of two real words (portmanteau); clipping + suffix |
| **Arbitrary** | A real, common word with no semantic connection to the product category | Real word transplanted from an unrelated category |
| **Fanciful / invented** | No prior meaning in any language; a pure string | Phoneme coinage; respelling of a common word past recognition; algorithmic generation |

**Notes on construction operators** (cross-reference: these are the same operators
`brand-name-generator`'s `01-operators.md` uses to *produce* candidates — this file classifies
the output, that one drives the process):

- *Compound* → usually descriptive or suggestive (PowerPoint, Photoshop).
- *Affix* (re-, -ify, -io, -ly) on a real root → suggestive or coined-from-root depending on how
  recognizable the root stays (Shopify = suggestive; Spotify = coined-from-root, "spot" + "-ify"
  drifted from literal).
- *Blend / splice* (portmanteau) → coined-from-root (Pinterest = pin + interest).
- *Clip* (truncation of a longer word) → ranges descriptive → arbitrary depending on what's left
  recognizable (Google clipped/misspelled from "googol" is coined-from-root; "Coke" clipped from
  "Coca-Cola" is arbitrary once detached from the plant).
- *Respell* → fanciful if it breaks recognizability (Flickr, Lyft), coined-from-root if the root
  stays legible (Krispy).
- *Foreign-source transplant* → arbitrary in the target market if the word is common in its source
  language but meaningless to the target audience (Volvo = Latin "I roll," arbitrary in English-
  speaking markets).
- *Phoneme coinage* (no real morphemes at all) → fanciful (Kodak, Xerox, Häagen-Dazs — invented
  syllables with no root).
- *Domain transplant* (metaphor system, not a single word) → associative/metaphoric (Scout,
  Palantir, Slack-as-in-cut-them-some-slack is closer to arbitrary; Scout-as-scouting is
  associative).

---

## Axis 2 — Trademark distinctiveness tier (legal)

Ascending order of protectability. This is the Abercrombie spectrum, the standard US framework.

| Tier | Definition | Protectability |
|---|---|---|
| **Generic** | The common name for the category itself | **Never protectable.** No amount of use or marketing earns rights. "Computer" for computers. |
| **Descriptive** | Directly describes a quality, function, or characteristic of the product | Protectable **only** with proven acquired distinctiveness ("secondary meaning") — the market has to learn to associate the word with one source. Weak until it does. |
| **Suggestive** | Requires imagination or inference to connect the name to the product | **Inherently distinctive.** Protectable immediately, no secondary meaning required. |
| **Arbitrary** | A real, common word with no logical connection to the product category | **Inherently distinctive.** Strong protection — the word already exists but never meant this. |
| **Fanciful** | Invented, no prior meaning anywhere | **Inherently distinctive.** The strongest tier — nothing to dilute, nothing to confuse with prior use. |

---

## The mapping — where the axes align

| Name type (linguistic) | Usual TM tier (legal) | Worked example |
|---|---|---|
| Descriptive | Generic → Descriptive | "The Vitamin Shoppe" (descriptive), "Snowboard" (generic for the category) |
| Suggestive | Suggestive | Netflix (suggests films delivered over the net), Duracell (suggests durable battery cell) |
| Associative / metaphoric | Suggestive → Arbitrary, depending on how far the metaphor's domain sits from the product category | Amazon (river → bookstore is arbitrary-leaning; the association isn't a functional hint), Scout (scouting → navigation app is suggestive-leaning; the metaphor hints at the function) |
| Coined-from-root | Suggestive → Arbitrary | Spotify (suggestive: "spot" hints at discovery), Verizon (veritas + horizon, reads as arbitrary once fused — the roots are legible only on inspection) |
| Arbitrary | Arbitrary | Apple (computers), Shell (petroleum), Camel (cigarettes) |
| Fanciful / invented | Fanciful | Kodak, Xerox, Exxon, Häagen-Dazs |

## Where the axes come apart — this is the part worth reading

The two axes are correlated (fanciful and arbitrary constructions tend to land in the strong legal
tiers; descriptive constructions tend to land in the weak legal tiers) but they are answering
different questions — "how was this built" vs. "how hard is this to own" — and a name can score
high on one and low on the other.

| Case | Name type read | TM tier read | Why they diverge |
|---|---|---|---|
| **Apple** (computers) | Linguistically **obvious** — a common fruit word, zero cleverness in construction | **Arbitrary**, one of the strongest tiers | The construction is trivial (it's just "apple"); the legal strength comes entirely from *category mismatch* — nothing about fruit relates to computers. Simple to build, hard to challenge. |
| **Garden** (hypothetical database tool, PRD's own worked failure) | Linguistically **rich** — a whole associative metaphor arrives instantly (seeds, soil, pruning, harvest, compost) | **Suggestive-to-descriptive**, and legally unremarkable | Breadth of vocabulary is not the same axis as legal strength *or* as fidelity. A metaphor can feel clever and generative while sitting in an ordinary legal tier and — the sharper failure — while mapping onto nothing real in the product. See `breadth × fidelity` in the example bank. |
| **Braun-style descriptive names inside a UI** ("Balance" for a spending-limit feature) | Linguistically plain, almost boring | **Descriptive**, weak — nobody could stop a competitor from calling their feature "Balance" | Legally weak by design, and *correct* — a feature name isn't trying to be ownable, it's trying to be instantly clear. Legal weakness here is not a defect. |
| **Xerox** | Linguistically **invented** — pure phoneme coinage, no root | **Fanciful**, the strongest tier | Here the axes align — but Xerox is also the case that shows fanciful strength has a *cost*: the company spent decades fighting to keep "xerox" from becoming the generic verb for photocopying (genericide risk lives at the top of the tier scale too, just via a different mechanism). |
| **Scout** | Linguistically generative — associative/metaphoric, passes `breadth × fidelity` cleanly | **Suggestive**, moderate — and crowded (Scout Motors, Scout24, Scout APM, the scouting movement itself) | High generativity does not buy legal cleanliness. A name can be an excellent `world, not word` and a mediocre trademark simultaneously — this is exactly the case §3.5 of the PRD calls out: ownability is `flag, never block`, because the two axes are independent inputs to different decisions. |

**The general rule:** name type predicts *how the name was made and what it can generate*.
TM tier predicts *how hard it is to defend*. A context profile should ask both questions
separately, never conflate them into one score.

---

## Trade-offs by name type — decision table

| Name type | Education cost | Protectability (typical) | Memorability | Generativity potential | Domain/namespace difficulty |
|---|---|---|---|---|---|
| Descriptive | None — self-explanatory | Weak (generic→descriptive) | Low — forgettable, interchangeable with competitors' equally-plain names | Low — nowhere to grow a vocabulary from | Very hard — the exact-match domain is almost always taken |
| Suggestive | Low — one inferential step | Good — inherently distinctive | Medium-high | Medium — hints at one benefit, doesn't usually supply a system | Hard — still a real word or near-word |
| Associative / metaphoric | Medium — must learn the mapping | Suggestive-to-arbitrary, variable | High if fidelity holds | **High** — this is the type that can pass `world, not word` | Medium — often a common word from an unrelated field, still contested |
| Coined-from-root | Medium — roots give a foothold but aren't obvious | Suggestive-to-arbitrary | Medium-high | Medium — some internal logic to extend, less than a full metaphor system | Easier — novel string |
| Arbitrary | Low-medium — the word is familiar, the *use* isn't | Strong | High once established, but slow to start (no hook at day one) | Low-medium — no built-in vocabulary, has to be built from nothing | Medium — common word, but wrong category, so more often available |
| Fanciful / invented | **High** — nothing to hook onto, pure memorization | Strongest | High once learned, but expensive to teach | Low, unless deliberately engineered (Kodak did not supply a vocabulary) | Easiest — novel string, usually clears |

## Connection to context profiles

This table is *why* the three profiles weight oppositely — the connection, not a restatement of
the rubric itself:

- **Venture profile** tolerates the high education cost and wants the top tiers (arbitrary,
  fanciful, or a well-fidelity associative/metaphoric name) because a venture has years and a
  marketing budget to pay down that education cost, and wants the strongest legal tier it can get.
  Opacity at launch is an acceptable, even desirable, trade.
- **Feature profile** cannot afford *any* education cost — a button label doesn't get a marketing
  budget, it gets one glance. It correctly wants descriptive or mildly suggestive names and
  correctly does not care that the TM tier is weak, because **nobody is trademarking a button
  label.** Inside an app, clarity beats protectability, full stop.
- **Codename profile** is orthogonal to both tables — it optimizes memorability and fun for an
  audience of the team, not the market, and must never leak into UI, so neither education cost nor
  TM tier matters at all.

---

## Standing caveat

**This is a heuristic tier assignment, not clearance.** Lingua flags trademark risk — construction
type and rough distinctiveness tier — as a starting orientation. It never clears a name. It does
not search live trademark registers, does not check use-in-commerce, does not evaluate a specific
class of goods, and cannot see confusingly-similar marks outside its own reference material. Real
clearance is an attorney.
