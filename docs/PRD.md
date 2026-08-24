# Lingua — Product Requirements Document

**A naming module for the brand skills suite.**
Status: Planning · Not yet built

---

## 1. Problem

I generate project, product, and feature ideas frequently, and naming is the bottleneck that gates everything downstream — the repo name, the domain, the icon set, the feature vocabulary. Today naming happens ad hoc: a name gets picked in thirty seconds based on vibes, and either it quietly constrains the project for years or it gets changed late and expensively.

Existing naming tools don't solve this. Generators (Namelix, Wordoid, Naminum) emit flat lists of brandable-sounding strings with no reasoning, no positioning input, and no notion of whether the name can support a system of sibling names. Naming guides cover trademark and memorability but skip *speakability* almost entirely, and skip *generativity* completely.

**What's needed:** a repeatable process that can either critique a name I've already fallen for, or generate candidates from a description — grounded in linguistics and practitioner method rather than taste, and integrated with the positioning work I've already built.

---

## 2. Goals & non-goals

### Goals
- Evaluate a candidate name across measurable ergonomics, argued brandability, and factual practicality.
- Generate name candidates from a product description, organized into semantic worlds rather than flat lists.
- Weight criteria differently for venture names, feature names, and internal codenames.
- Read from the existing positioning canvas when one exists; work without one when it doesn't.
- Fit the existing `brand-*` suite's conventions so the whole thing scales past four skills.

### Non-goals
- **Not a legal tool.** Flags trademark risk heuristically; never gives clearance. Real clearance is an attorney.
- **Not a domain registrar.** Doesn't perform live availability checks in v1.
- **Not a logo/identity tool.** Stops at the name and the vocabulary it implies.
- **Not an oracle.** Outputs an argued recommendation, not a verdict. I decide.

---

## 3. Design principles

Five ideas do most of the work. They're written as **leading words** — short, high-density phrases repeated verbatim throughout the skill files, because agents echo them back in reasoning traces and steer themselves with them. If these phrases don't appear in the traces, the steering has failed and the skill needs revision.

### 3.1 "World, not word"
The most valuable property of a name is **generativity**: does it come with a vocabulary and an iconography attached? *Scout* gives you waypoints, blazes, cairns, routes, contour lines, base camp, field notes — and each arrives with an icon already drawn. That isn't a name, it's a nomenclature system acquired for the price of one word. *Lingua* gives you tongue, Babel, Rosetta, grammar: thin, academic, and unmappable onto anything you'd build.

A generative name **is** brand architecture. Feature naming stops being a blank page and becomes "which bucket does this live in."

### 3.2 "Breadth × fidelity"
A world can supply plenty of vocabulary and still be the wrong world. Generativity has two halves:

- **Breadth** — does it supply sibling vocabulary? (The six-siblings test.)
- **Fidelity** — does the vocabulary *mean the right things*? Does the metaphor's internal structure map onto the product's actual structure?

Breadth without fidelity is the dangerous failure because it *feels* productive. Call a database tool "Garden" and you get seeds, soil, pruning, harvest, compost in ten seconds. Now ask what "pruning" is. If the answer is "uh, deleting rows I guess," you haven't built a naming system — you've built a decoder ring users must memorize. Arbitrary mapping is worse than a plain name, because plain names don't ask anyone to learn anything.

Scout passes both. A waypoint genuinely *is* a saved position you'll return to. A route genuinely *is* a path through material. A blaze genuinely *is* a mark left for whoever comes next. Nothing is being translated — the metaphor and the product have the same shape.

### 3.3 "Rare letters, common sounds"
Rich Barton's advice to use high-point Scrabble letters (Z, Q, X, J, K) contradicts his own advice to pick a word a four-year-old can say — and he doesn't notice. His examples resolve it: Xerox, Kodak, Coke, Zillow. Every one maps a rare *letter* onto a completely common *sound* — X→/z/, K→/k/, Z→/z/. None uses a rare phoneme.

You get orthographic distinctiveness (low neighborhood density, better search ownability) without paying an articulatory cost. This is also what separates "Xerox" from "Xzrq" — a distinction the source ergonomics document couldn't articulate.

### 3.4 "Read the ending"
Names with lore have a *plot*, and the plot comes attached whether you want it or not. Palantír: a seeing-stone that shows true visions selectively arranged to deceive, and corrupts whoever uses it. Critics have used that against the company for a decade. Icarus is the compact version — gorgeous name, means *flew too close to the sun and drowned*.

If a name has depth, something is down there. Read to the end before committing.

### 3.5 "Flag, never block"
Ownability (trademark, domain, SEO, neighborhood density) is **reported with a severity note and has no power to sink a candidate.** Generativity and familiarity both push *against* distinctiveness — Scout is a perfect world *and* a crowded namespace (Scout Motors, Scout24, Scout APM, the scouting movement). For a personal tool that's irrelevant. For a venture it's the whole conversation. The context profile sets the volume; nothing sets a veto.

---

## 4. The evaluation model

### 4.1 Three layers, three different kinds of verdict

The source `name-ergonomics.md` proposed Ergonomics / Brandability / Practicality. That split was right. The upgrade: **each layer outputs a different shape, because each has different epistemic status.**

| Layer | Output | Computed by | Why |
|---|---|---|---|
| **Ergonomics** | Numeric score, 6 dimensions | `scripts/` (deterministic) | Syllable count, phonotactic legality, spelling ambiguity are near-objective. A score is defensible. |
| **Brandability** | Argued judgment + counter-argument | LLM reasoning | Generativity, resonance, distinctiveness are contested among professionals. A number here is false precision. |
| **Practicality** | Pass/fail flags with severity | Checks + lookups | Domain taken or not. Collision or not. Facts, not opinions. |

**Kill the composite score.** `Ergonomics 89 · Brandability: exceptional world, crowded namespace · Practicality: 2 flags` is more honest and more actionable than a single number averaging a fact with an opinion. The demo case: running "Lingua" through this yields *comfortable, unoriginal, and it doesn't matter* — three separate verdicts a composite would have blended into a meaningless 84.

### 4.2 Ergonomics — six dimensions, computed not vibed

The source document had seventeen dimensions. That's too many. Neumeier uses seven, Watkins five, Igor four. Seventeen weighted dimensions fail predictably: everything scores 85–95 because no name is bad at *all* of them, and the composite becomes noise. Several were also the same dimension wearing different hats — phonotactics, syllable simplicity, mouth ergonomics, and sonority flow are four views of "is this easy to say."

Applying the deletion test — would removing this change the output? — most of them are no-ops. Collapsed to six:

1. **Pronounceability** — syllable count, CV structure, sonority sequencing, cluster legality *(was 1, 2, 3, 4)*
2. **Spellability** — hear it once, spell it right *(was 9, 10)*
3. **Distinctiveness** — phonetic neighborhood density, rare-letters/common-sounds *(was 8, + Barton)*
4. **Rhythm & recall** — stress pattern, ten-minute reproduction *(was 5, 17)*
5. **Verbability** — can it be verbed, clipped, nicknamed *(was 16, + Barton)*
6. **International robustness** — no "th", no missing phonemes, screened for meaning *(was 15)*

**Cut entirely: typing ergonomics.** It's the one dimension with no support anywhere in the practitioner literature — Barton, Neumeier, Watkins, Lexicon, Igor, none mention it. Nobody has ever failed because of same-finger repetition. Keep as a footnote if desired; scoring it equal-weight to hearability was a mistake.

**Moved to Brandability: sound symbolism.** It isn't an ergonomics dimension, it's a *fit* check — "does this name's phonetic personality match the positioning?" — and it's unanswerable without knowing the positioning. This is the first real integration point with the positioning suite.

**These six should be computed in `scripts/`, not reasoned about.** Syllable count, phoneme sequence, neighborhood density, and stress pattern are exactly the kind of thing an LLM estimates inconsistently and a script gets right every time. CMUdict gives the phoneme inventory; neighborhood density is a one-edit-distance count over the dictionary. A Python script returns a stable JSON blob, the skill reasons over the blob. This is what makes the numeric layer trustworthy — and it's why "is this defensible as a score" gets a yes for this layer and a no for the others.

### 4.3 Brandability — argued, not scored

Five criteria, each producing a position plus the strongest counter-argument:

- **Generativity** — breadth × fidelity. The six-siblings test. Plus two probes:
  - *Find the breaking point.* Every metaphor fails somewhere; you want to know where in advance. The reliable probes are the unglamorous surfaces — what's an error state in this world? A permissions setting? The billing page? Cartography handles "you're lost" beautifully and has nothing to say about invoicing. Not disqualifying — but a metaphor that breaks on a *core* surface rather than a peripheral one is a real problem.
  - *Keep the metaphor off the buttons.* The metaphor names concepts, not necessarily UI actions. Scout can have waypoints as a first-class concept while the button still says "Save." Metaphor-as-vocabulary aids memory; metaphor-as-UI-label costs discoverability.
- **Cultural familiarity** — split into two, because they behave oppositely:
  - *Cultural commons* (Scout, Beacon, Anchor, Nomad, Forge, Atlas) — pre-loaded meaning, zero education cost, trivially spellable. **Weight heavily.** This is fluency at the semantic level: the name arrives already understood.
  - *Owned IP* (Palantir, TARDIS, Skynet, franchise references) — borrowing equity you don't control, walking into Watkins' "Copycat" deal-breaker, inheriting the whole plot. **Flag as a risk requiring justification.**
- **Lore integrity** — read the ending. For any name with mythological or literary weight, run the full story and report how it ends.
- **Sound-symbolism fit** — phonetic personality vs. positioning personality. A tie-breaker and territory hint, never a scoring rule; label evidence strength.
- **Ownability** — the counterweight. Flag, never block.

### 4.4 Practicality — factual flags

Trademark distinctiveness tier (generic → descriptive → suggestive → arbitrary → fanciful), heuristic knockout collision check, domain/handle reality, SEO collision, cross-cultural screening.

**Hard requirement: a debunked-myths blocklist.** The Chevy Nova "no va" story is false — Snopes-debunked, the car sold fine in Mexico and Venezuela, and Pemex sold Nova-branded gasoline — and it appears in nearly every naming listicle. A skill that repeats folk myths as fact loses credibility instantly. Ship the blocklist as reference material.

### 4.5 Context profiles

Feature naming and product naming are opposite problems. Apple's own guidance rejected "Spending Power" for the plain word "Balance" because clarity and trust beat brand expression inside an app; NN/G is emphatic that command text should be descriptive rather than branded. Meanwhile a venture name wants distinctiveness and ownability and *should* be slightly opaque.

Same rubric, three weighting profiles, selected at invocation:

| Profile | Weights up | Weights down | Special rule |
|---|---|---|---|
| **Venture / product** | Distinctiveness, generativity, verbability, ownability | Instant descriptiveness | Tolerate opacity |
| **Feature / UI** | Spellability, clarity, sibling consistency, international | Distinctiveness, cleverness | Penalize coined names hard; check fit with existing system |
| **Internal codename** | Memorability, fun | Nearly everything else | Must never leak into UI — state explicitly |

Microsoft Copilot is the cautionary tale: the name got attached to ~80 different things until the NAD found customers couldn't distinguish the products. A feature-naming skill without a sibling-consistency check will happily help you build that.

---

## 5. Skill architecture

### 5.1 Trigger design — the invocation split

Model-invoked skills cost **context load**: every description sits in context on every request, and the model may decline to follow the pointer anyway. User-invoked skills cost **cognitive load**: I have to remember they exist. Neither is free.

The resolution maps cleanly onto the suite's existing maker/critic pattern:

> **Critics are model-invoked. Makers are user-invoked.**

Critique is cheap, fast, and welcome — it should fire when I float a name mid-conversation. A false positive costs three seconds of scrolling. Generation is a heavyweight interactive process that takes over the conversation; if it fires every time I describe a project idea, I'll hate it within a week. Makers get `disable-model-invocation: true`.

**Audit action for the existing suite:** five `brand-*` skills currently carry model-invokable descriptions, which is five descriptions of context tax on every request. Under this rule, `brand-positioning-facilitator`, `brand-pitch-builder`, and `brand-content-writer` should become user-invoked — they're deliberate acts, never ambient ones. That drops the standing context load from five descriptions to two (critics), then to three once `brand-name-critic` lands.

### 5.2 The leg-work split — three skills, not two

This is a correction to an earlier plan. "Generate worlds first, names second" is the right method, but as a single skill it will fail in a specific, predictable way: the agent sees "produce names" as the terminal goal, does thirty seconds of world-building, and rushes to the list. This is exactly the plan-mode failure where "ask clarifying questions" is always shortchanged because the model can see that the real goal is the plan.

The fix is to **hide the future step** by splitting the phase into its own skill. So:

| Skill | Invocation | Job | Terminates at |
|---|---|---|---|
| `brand-name-worlds` | User | Brief → 3–5 stress-tested semantic worlds | A chosen world. **No names produced.** |
| `brand-name-generator` | User | Chosen world → clustered shortlist | ~12 candidates with rationale |
| `brand-name-critic` | **Model** | Candidate → three-layer evaluation | An argued recommendation |

The world skill terminating *before* any names exist is the whole point. It forces real leg work on the mapping stress-test, which is where the value is.

### 5.3 Structure — steps and reference, branches behind pointers

Every skill is **steps** (the procedure) plus **reference** (supporting material). SKILL.md stays under ~500 words and holds workflow only; anything used by only one branch moves behind a context pointer. The existing suite already gets this right — don't let ergonomics tables leak into SKILL.md.

The context profiles are the branches. Profile-specific material lives in separate files loaded on demand.

```
lingua/
├── brand-name-worlds/
│   ├── SKILL.md                     # user-invoked; 4 steps
│   ├── references/
│   │   ├── 01-brief.md              # 4-question mini-brief; canvas mapping
│   │   ├── 02-world-sourcing.md     # cartography, seafaring, masonry, printing,
│   │   │                            #   birding, geology, husbandry, archery…
│   │   └── 03-fidelity-test.md      # 5-concept mapping test; breaking-point probes
│   └── assets/
│       └── world-brief-template.md
│
├── brand-name-generator/
│   ├── SKILL.md                     # user-invoked; 3 steps
│   ├── references/
│   │   ├── 01-operators.md          # compound, blend w/ splice search, affix, clip,
│   │   │                            #   respell, foreign-source, phoneme coinage,
│   │   │                            #   shortest-synonym (Synomin pattern)
│   │   └── 02-converge.md           # cluster → shortlist → usage-in-a-sentence
│   └── assets/
│       └── shortlist-template.md
│
├── brand-name-critic/
│   ├── SKILL.md                     # MODEL-INVOKED; 4 steps
│   ├── references/
│   │   ├── 01-ergonomics.md         # interprets script output; 6 dimensions
│   │   ├── 02-brandability.md       # generativity, familiarity, lore, fit, ownability
│   │   ├── 03-practicality.md       # TM tiers, knockout heuristic, domains
│   │   ├── myths-blocklist.md       # Chevy Nova et al. — never repeat as fact
│   │   └── profiles/
│   │       ├── venture.md
│   │       ├── feature.md
│   │       └── codename.md
│   ├── scripts/
│   │   └── phonetics.py             # CMUdict; syllables, stress, clusters,
│   │                                #   neighborhood density → JSON
│   └── assets/
│       └── critique-template.md
│
└── _shared/
    ├── name-types.md                # descriptive → suggestive → coined taxonomy,
    │                                #   mapped to TM distinctiveness spectrum
    └── example-bank.md              # real names by type, industry, era
```

**`_shared/` exists because of a DRY problem the current suite already has.** `references/framework.md` is duplicated across all five `brand-*` skills. When Dunford's framework needs an edit, it gets edited five times and one gets missed. Both naming skills need the name-type taxonomy and the example bank; neither should own a copy. If the runtime can't resolve cross-skill references cleanly, the fallback is a single generation script that stamps the shared file into each skill — but a single source of truth is the requirement either way.

### 5.4 Steering — leading words

The five principles in §3 are the steering vocabulary and must appear **verbatim and repeatedly** in the skill files, not paraphrased:

`world, not word` · `breadth × fidelity` · `rare letters, common sounds` · `read the ending` · `flag, never block` · `six-siblings test` · `diverge → cluster → converge`

**Verification method:** run the skill and read the reasoning trace. If the agent isn't echoing these phrases back, the steering has failed and the words need to be more consistent or more powerful. This is a testable property, not a stylistic preference.

### 5.5 Subagent QA

The generator should not grade its own output. An agent evaluating work it just produced sees fewer flaws in it, because it holds the reasons it made each choice.

`brand-name-generator` ends by spawning a **fresh-context subagent** running `brand-name-critic` over the shortlist, with no visibility into the generation session. The critic's independent read gets attached to the shortlist. This is the maker/critic split enforced structurally rather than merely conceptually, and it's a strong argument for keeping them as separate skills.

### 5.6 Self-improvement loop

Each skill ends with a reflection step: examine friction encountered during the run, and append to `references/troubleshooting.md`.

For Lingua specifically there's a second, more valuable log: **`decisions.md`** — names proposed, names chosen, names rejected, and why. Over time this accumulates my actual taste, which is the one input no amount of research supplies. A naming skill that has seen fifty of my decisions is worth considerably more than one that hasn't.

This is in mild tension with the pruning discipline — logs are exactly how skills accumulate sediment. Mitigation: the reflection step must *edit* the log rather than append indefinitely, and the log gets a pruning pass at each phase boundary.

---

## 6. Generation method

### 6.1 The world skill
1. **Load the brief.** If a positioning canvas exists, auto-populate and ask nothing. If not, a compressed four-question mini-brief: what it does / who for / what it's replacing / one-word personality. Structure the output so it can seed the facilitator later — naming work shouldn't be thrown away.
2. **Propose 5–7 candidate worlds.** Semantic domains, not tonal directions. Cartography, seafaring, masonry, printing, birding, geology, archery, husbandry, weather, textiles.
3. **Stress-test fidelity before naming anything.** Take five real product concepts and ask what each is called in this world. If three of five require a shrug, discard the world. Then run the breaking-point probes (error state, permissions, billing).
4. **Converge to 2–3 surviving worlds.** Stop. Do not produce names.

Cheap to test, and it kills bad metaphors before I've fallen in love with a word.

### 6.2 The generator skill
1. **Diverge** — ~80–100 candidates inside the chosen world using explicit operators. Not a freeform brainstorm; the operator list is reference material.
2. **Cluster** — group into 3–4 approaches *within* the world (direct / oblique / coined-from-root / compound).
3. **Converge** — ~12 surfaced, each with: type classification, TM distinctiveness tier, one-line rationale, **three sibling names it would produce**, and **used in a sentence**.

Two of those deliverables matter more than the name itself. The sibling names are the six-siblings test applied per candidate: if you can't generate three, it's a dead end, and you learn that in five seconds instead of eighteen months. The usage sentence exists because names fail in usage, not in lists — "Open it in Fable" reads differently than "Fable" on a slide.

### 6.3 Integration with positioning

The naming brief is a **subset of the positioning canvas**. That's the whole integration:

```
brand-positioning-facilitator ──→ canvas ──┬─→ brand-name-worlds ─→ generator ─→ shortlist
                                            └─→ brand-name-critic ←── candidate
```

Best-fit customer, market category, competitive alternatives, and differentiated value are exactly what a naming brief needs. Competitive alternatives are especially valuable — they define the phonetic and semantic white space to *avoid*.

The friction to design around: **I name things at idea stage, before positioning exists.** Demanding a canvas would make the skill useless for my actual workflow. So — canvas present, use it silently; canvas absent, four-question mini-brief and proceed; either way, note that a name chosen pre-positioning should be re-validated after. Names are cheap to change at idea stage and expensive later.

---

## 7. Suite architecture

### 7.1 The naming schema

`brand-{object}-{mode}` — already implicit in the existing suite. Make it explicit:

| | Make (user-invoked) | Evaluate (model-invoked) | Produce (user-invoked) |
|---|---|---|---|
| **positioning** | facilitator ✅ | critic ✅ | — |
| **name** | worlds 🆕 · generator 🆕 | critic 🆕 | — |
| **content** | — | critic ✅ | writer ✅ |
| **pitch** | — | *gap* | builder ✅ |

Two gaps this exposes. `brand-pitch-critic` is a missing cell worth filling eventually. More importantly for me: **there is no brand-architecture skill**, and that's the one governing whether a portfolio of many projects hangs together. The portfolio question — *do these share a naming system, or is each standalone?* — is brand architecture, and it's the input that makes feature naming decidable. A future `brand-architecture-facilitator` is the natural next module.

### 7.2 On the word "Lingua"

Make it the **module name, not a skill name.** Skill names are feature names — the model matches on them, so they should be boring on purpose. `brand-name-critic` is what the model needs to see; *Lingua* is what I call the folder.

Honest read, run through the rubric: ergonomically strong (two syllables, DA-da, clean CVC-CV, unambiguous spelling). Brandability weak — it's descriptive-suggestive Latin for "tongue," the first word anyone reaches for in this space, sitting in a dense namespace with Linguee, Lingua Franca, Lingua.ly. Low generativity: tongue, Babel, Rosetta, grammar, and none of it maps onto anything. It tells you the domain but nothing about the point of view, and the point of view here is interesting — this isn't "language," it's *ergonomics applied to language*.

Practicality: irrelevant. Personal toolkit, no TM, no domain, no SEO. Which is exactly why I wouldn't spend more than five minutes on it.

**Open item:** the umbrella covering positioning + naming + content + pitch still has no name, and "Lingua" is too narrow semantically to be it. Fitting first job for the finished skill: name its own parent. Whatever it is should pass the six-siblings test.

---

## 8. Sequencing

Three phases. Each has an exit criterion that must be met before the next begins.

### Phase 1 — `brand-name-critic`
Highest confidence, lowest risk, immediately useful, and it forces the rubric to be nailed down before anything depends on it.

Build: SKILL.md, the three layer references, `scripts/phonetics.py`, the three profile files, the myths blocklist, the critique template.

**Method note:** build this one by reverse-engineering. Write three or four ideal critique outputs by hand first (one venture name, one feature name, one deliberately bad name), then build the skill that produces them, then have a fresh-context subagent run the skill blind and compare. Iterate until the blind output resembles the target. Naming critique is subjective enough that specifying the output first is the only reliable way to know the skill works.

**Exit criteria:**
- `phonetics.py` returns stable output for a 20-name benchmark set (Scout, Stripe, Notion, Xerox, Kodak, Zillow, Flickr, Palantir, Slack, Figma, Lingua, plus deliberately bad ones).
- Three context profiles produce visibly different verdicts on the same name.
- Leading words appear in the reasoning trace.
- Blind subagent output resembles the hand-written targets.

### Phase 2 — `brand-name-worlds` + `brand-name-generator`
Built second because Phase 1 defines what good output looks like, and the generator's convergence step needs that definition.

Built as two skills from the start, not one — the leg-work split is load-bearing, and retrofitting it means rewriting both.

**Exit criteria:**
- The world skill terminates without producing names. If it leaks names, the split has failed and needs stronger steering.
- Every candidate ships with three sibling names and a usage sentence.
- Subagent QA runs on the shortlist with no generation-session context.
- Running it on three real project ideas produces at least one name I'd actually use.

### Phase 3 — factor and prune
Only once both skills exist and their real overlap is visible. Factoring shared references before that is guessing.

- Extract `_shared/name-types.md` and `_shared/example-bank.md`; remove the duplicated copies.
- Retrofit the same treatment on the existing suite's five duplicated `framework.md` files.
- Flip `brand-positioning-facilitator`, `brand-pitch-builder`, and `brand-content-writer` to `disable-model-invocation: true`.
- Full pruning pass on all skills: deletion test on every paragraph, hunt for no-ops and sediment, confirm single source of truth for every piece of reference material.
- Prune the accumulated `troubleshooting.md` and `decisions.md` logs.

---

## 9. Open questions

1. **Cross-skill reference resolution** — can `_shared/` be referenced from sibling skills, or is a stamping script needed? Determines whether §5.3 works as drawn.
2. **CMUdict coverage for invented names** — coined names aren't in the dictionary. Need a grapheme-to-phoneme fallback (g2p-en or similar), which introduces its own error rate. How much does that undermine the "deterministic" claim for Layer 1?
3. **Live availability checks** — out of scope for v1, but domain/handle status is genuinely useful. Worth a v2 script, or does it rot too fast?
4. **World-sourcing breadth** — should `02-world-sourcing.md` ship a fixed catalogue of semantic domains, or should the agent generate them freely each run? Fixed is more consistent and more prunable; free is more surprising. Probably fixed catalogue plus an explicit "propose one not on this list" step.
5. **Does the critic need the generator's context?** Currently no, deliberately. But a critic that knows which world a name came from could evaluate fidelity better. That would compromise the fresh-context QA property. Leaning toward keeping them blind.

---

## 10. Note on tooling

Skipped `skill-creator` for this document — it scaffolds skills, and this phase is specification rather than construction. It should be used at the start of Phase 1 to generate the file structure, at which point this PRD becomes the input. Matt Pocock's "writing great skills" skill is worth running over the result as an audit pass before Phase 3's pruning.
