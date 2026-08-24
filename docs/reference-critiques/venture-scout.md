# Scout

**Profile:** venture / product · **Candidate for:** a research-and-note-taking tool for people
working through large bodies of material · **Run:** hand-written target, Phase 1

**Ergonomics 85 · Brandability: exceptional world, crowded namespace · Practicality: 2 flags**

Three verdicts, deliberately not averaged. The ergonomics number is a measurement, the
brandability line is an argument, and the flag count is a fact. Averaging them would produce a
single number that is true of none of them. Read all three; they disagree, and the disagreement
*is* the finding.

---

## Context

Venture profile, which weights **up** distinctiveness, generativity, verbability and ownability,
and weights **down** instant descriptiveness. Opacity is tolerated: a venture name is allowed to
need a sentence of explanation, because it will get one, several million times, in launch copy.

That weighting is what makes this a hard case rather than an easy one. Scout scores at opposite
ends of two dimensions the venture profile cares about most.

---

## Layer 1 — Ergonomics (computed)

`python3 scripts/phonetics.py "Scout"`

**Pronunciation:** `S K AW1 T` · /skaʊt/ · source `cmudict`, confidence **high**.
The name is in the dictionary, so nothing below is inferred. Everything in this block is a
lookup, not an estimate.

| Dimension | Score | Evidence |
|---|---:|---|
| Pronounceability | 96 | 1 syllable; all clusters attested in English; no sonority violation; 1 consonant cluster (-4) |
| Spellability | 84 | 1 ambiguous grapheme: `ou` (-10); 1 plausible misspelling from hearing it once: scowt (-6) |
| Distinctiveness | 50 | neighbourhood density 26 (84th percentile of the lexicon); no rare letters (z q x j k) |
| Rhythm & recall | 90 | monosyllable — maximally reproducible (base 90); stress 1: monosyllable |
| Verbability | 95 | 1 syllable (base 90); already an English word — inflects without explanation (+5) |
| International robustness | 96 | no phonemes outside the cross-linguistically common core; 1 consonant cluster — costly for CV-syllable languages (-4) |

**`ergonomics_score`: 85** — the equal-weight mean, profile-independent. The script does not know
which profile is running. Re-weighting is this critique's job, and it is done in prose below, not
by recomputing the number.

**Under the venture profile.** Verbability 95 and pronounceability 96 are both dimensions this
profile weights up, and both are near-ceiling. "Scout it" and "I scouted that paper" are already
grammatical English; you get the verb for free rather than manufacturing one.

Distinctiveness 50 is the soft spot, and this profile weights distinctiveness **very high**, so it
does not get a footnote. Neighbourhood density 26 puts Scout at the 84th percentile of the
lexicon — a genuinely busy stretch of English sound-space, with `scoot`, `scot`, `scour` and `scow`
sitting one phoneme away. Concretely: Scout will occasionally be misheard as one of those in noisy
audio, and any feature built on hearing the name — a voice assistant, a phone-support agent typing
what they heard — needs to disambiguate.

It is worth being precise about which crowding this is, because there are two and they are not the
same finding. This one is *phonetic*: Layer 1, density in sound-space, computed straight from the
lexicon. The other, larger crowding problem for this name — Scout APM, Scout Motors, Scout24, the
Scouting movement — is *semantic and commercial*, and the script has no way to see it; it shows up
only in Layer 3 below. Per ADR-011, the two readings are reported separately rather than averaged
into one number. They agree on the direction — Scout is a crowded name — and disagree on the
mechanism: a busy corner of English phonology versus four organisations already trading on the
word. Both are real, independently, at the same time, and the Layer 3 crowding is the one that
actually costs money.

Spellability 84 is comfortable, and lower than it looks on first read. The script finds one
ambiguous grapheme — `ou`, which carries four common readings (*out*, *soup*, *tough*, *four*) —
and one plausible one-hearing misspelling, `scowt`. That is a narrower problem than a general
ambiguity finding: *scout* is familiar enough as a whole word that most people spell it from
recognition rather than by sounding out the grapheme, so the risk concentrates in the population
that hears the name with no prior exposure to it. Under the feature profile this score would clear
that profile's spellability floor (~50, see `01-ergonomics.md` §3) comfortably rather than skating
close to it. Under the venture profile the cost is smaller still: a domain redirect and a handful
of misdirected first-time visitors. (The more intuitive misspelling, `Skout`, is not what the
script flags here — it belongs to Layer 3 below, where it turns out to be a real, separate app.)

---

## Layer 2 — Brandability (argued)

Each criterion gives a position and the strongest argument against it. No scores — a number here
would be false precision dressed up as rigour.

### Generativity — `breadth × fidelity`

**Position: exceptional, and this is the reason to choose the name.** `world, not word` — the
question is not whether *Scout* is a good word but whether it hands over a working vocabulary,
and it hands over an unusually complete one.

**`six-siblings test`** (can you name six siblings without straining?):

| Sibling | What it names in the product | Icon already drawn? |
|---|---|---|
| **Waypoint** | a saved position in a document you will return to | yes — pin/flag |
| **Blaze** | a mark left in shared material for whoever comes next | yes — axe-mark on bark |
| **Cairn** | a stack of related findings marking a conclusion | yes — stacked stones |
| **Route** | an ordered path through a body of material | yes — dotted line |
| **Contour lines** | density/difficulty view over a corpus | yes — topographic rings |
| **Base camp** | the workspace you return to between excursions | yes — tent |
| **Field notes** | raw capture, unedited, timestamped | yes — notebook |

Seven, comfortably, and each arrives with an icon already drawn. That is not a name, it is a
nomenclature system acquired for the price of one word.

**Fidelity — the half that usually fails, and does not here.** Breadth without fidelity is the
dangerous failure *because it feels productive*: "Garden" for a database tool gives you seeds,
soil, pruning, harvest, compost in ten seconds, and then you ask what "pruning" is, and the
answer is "uh, deleting rows I guess," and you have built a decoder ring users must memorise.
Arbitrary mapping is worse than a plain name, because plain names do not ask anyone to learn
anything.

Scout passes fidelity on every term above. A waypoint genuinely *is* a saved position you will
return to. A route genuinely *is* a path through material. A blaze genuinely *is* a mark left for
whoever comes next. Nothing is being translated — the metaphor and the product have the same
shape. The test is not "can I justify this mapping"; it is "did I have to."

**Find the breaking point.** Every metaphor fails somewhere and you want to know where before you
commit. Probe the unglamorous surfaces:

- *Error state* — "off the trail", "you have lost the blaze". **Holds, elegantly.**
- *Permissions* — "who is on this expedition", "party", "guide vs. member". **Holds.**
- *Empty state* — "no waypoints yet — start walking". **Holds.**
- *Billing / invoicing* — outfitting? provisions? **Breaks.** There is no natural scouting word
  for an invoice, and reaching for one produces exactly the decoder-ring failure above.

Billing is a peripheral surface. Cartography handles "you're lost" beautifully and has nothing to
say about invoicing either, and that is survivable in a way that breaking on the *core* object
would not be. The rule: a metaphor that breaks on the billing page has a seam; a metaphor that
breaks on the primary noun has a hole. Scout has a seam. Call the billing screen "Billing."

**Keep the metaphor off the buttons.** The metaphor names concepts, not UI actions. *Waypoint*
should be a first-class noun in the product — in docs, in the data model, in the sidebar heading
— while the button that creates one still says **Save**. Metaphor-as-vocabulary aids memory;
metaphor-as-UI-label costs discoverability. "Blaze this passage" as a button is a puzzle; "Share
a mark on this passage" with the marks *called* blazes is a vocabulary.

**Counter-argument (the strongest one against):** the world is doing work the product may not
earn. An outdoor-navigation vocabulary sets an expectation of exploration, wandering, and
discovery. If the actual product is closer to disciplined retrieval — you know what you are
looking for and you want it fast — then every waypoint and cairn is a small mismatch, and users
will feel the whimsy as friction rather than as help. Generativity is only an asset if the world
you acquired is the world you wanted. That is a positioning question, not a naming one, and it
should be settled before the name is.

### Cultural familiarity — commons, not owned IP

**Position: cultural commons, weight heavily.** *Scout* belongs to the same set as Beacon, Anchor,
Nomad, Forge and Atlas: pre-loaded meaning, zero education cost, trivially spellable once seen,
and instantly parseable in the first second of a pitch. Nobody needs to be told what a scout does.
This is fluency at the semantic level — the name arrives already understood, which is a real and
underrated asset and the single largest reason to prefer it over a coinage.

It is emphatically **not** owned IP. No rights-holder controls "scout" as a concept; there is no
Watkins "Copycat" problem and no borrowed equity to have withdrawn. Contrast Palantir or TARDIS,
where you inherit somebody else's plot along with their goodwill.

**Counter-argument:** commons cuts both ways, and its cost is exactly the Layer 3 finding.
Pre-loaded meaning is available to everyone, which is why four large organisations already took
it. Familiarity and distinctiveness are in direct tension, and this name buys the first by
spending the second.

### Lore integrity — `read the ending`

**Position: no mythological plot, but a live institutional one.**

`read the ending` is normally a check on mythological or literary names — the Palantír problem,
where a seeing-stone that shows true visions selectively arranged to deceive, and corrupts
whoever uses it, has been handed to critics as ammunition for a decade. Icarus is the compact
version: gorgeous name, means *flew too close to the sun and drowned*.

Run the procedure anyway. Scout has no myth to read to the end. Its literary reference — Scout
Finch in *To Kill a Mockingbird* — ends well and is a mild positive. But the procedure surfaces
something the mythological framing would have missed: the dominant institutional referent, the
Scouting movement, carries a live and heavily reported association with the Boy Scouts of
America's abuse-claims bankruptcy and subsequent rename to Scouting America. That is a plot, it
is recent, and it is the first search result an unfriendly journalist would reach for.

**Severity: low.** The word predates and outlives the institution, the association attaches to
the organisation rather than the noun, and no reasonable reader connects a research tool to it.
But `read the ending` means reporting what is down there, not only what is convenient, and this
belongs in the record rather than in a surprise later.

### Sound-symbolism fit

**Position: good fit, weak evidence.** /sk/ is a crisp, fast-onset cluster; /aʊ/ opens outward;
the /t/ coda closes decisively. The phonetic personality reads brisk, capable, outward-moving,
which matches a positioning of *fast, competent exploration* and would clash with a positioning
of *calm, patient, archival depth*.

**Evidence strength: weak-to-moderate, and labelled as such.** The experimental literature
supports size and shape symbolism (the bouba/kiki effect) reasonably well. It supports "onset
cluster → brand personality" much less well. This is a **tie-breaker and a territory hint, never
a scoring rule.** If it were the deciding argument, the argument is too thin.

### Ownability — `flag, never block`

**Position: the namespace is badly crowded, and under this profile that is the whole
conversation.**

Established users of the name, in rough order of collision risk:

- **Scout APM** — application performance monitoring. Adjacent category, developer audience,
  direct search collision. This is the dangerous one.
- **Scout Motors** — Volkswagen Group's revived American vehicle brand, extremely well funded and
  currently spending heavily on exactly the kind of advertising that owns a word.
- **Scout24** — a large listed European digital-marketplace group (AutoScout24, ImmoScout24).
- **Scouting America** (formerly the Boy Scouts of America) and the global Scouting movement — the
  default meaning of the word for most of the population.

`flag, never block`. This does not sink the candidate; it prices it. The context profile sets the
volume: **for a personal tool this is irrelevant** — nobody is competing for your attention inside
your own toolbox and the crowding costs you literally nothing. **For a venture it is the entire
discussion**, because you will be buying search terms against Volkswagen's budget and explaining
in every second sentence which Scout you are.

**Counter-argument (and it is not weak):** crowded namespaces are survivable and are survived
constantly. *Slack* competed with a common English word plus a defunct chat protocol. *Notion*,
*Stripe*, *Arc*, *Linear* and *Cursor* are all dictionary words in busy namespaces, and all won
their term through category dominance rather than through prior ownership. Search ownership is
downstream of category ownership more often than the reverse. The honest statement of the risk is
therefore not "you cannot own this" but "you will pay to own this, and the bill arrives in
marketing spend rather than in legal fees."

---

## Layer 3 — Practicality (flags)

Facts with severity, not opinions. **Heuristic screen only — this never gives clearance.** Real
clearance is a trademark attorney with access to full registers, and nothing below substitutes
for one.

| Check | Finding | Severity |
|---|---|---|
| **TM distinctiveness tier** | *Suggestive* for research software — evokes exploration without describing the product. A protectable tier, but weakened to near-*descriptive* by how well the metaphor fits, and by heavy prior use. See `${CLAUDE_PLUGIN_ROOT}/shared/name-types.md` for the tier definitions. | **high** |
| **Knockout collision** | Scout APM occupies the same class of goods (software/SaaS) with the same buyer. Scout Motors and Scout24 are different classes but very loud. A knockout search would not come back clean. | **high** |
| **Domain / handle** | `scout.com` long taken. Realistic outcomes are a modifier (`getscout`, `scout.dev`, `scoutapp`) or a coined respelling. `@scout` handles gone on every major platform. | medium |
| **SEO collision** | Unwinnable on the bare term for years. Plan for a compound brand term from day one and measure on that instead. | medium |
| **Cross-cultural screen** | No adverse meanings found in the major target languages; the word is a loan into several. Screened against `references/myths-blocklist.md` — no folk myth is being repeated here as fact. | low / clear |
| **Spelling-in-the-wild** | `Skout` is a real and separate app; the misspelling has a destination. | low |

**Headline count = flags at severity `high`: 2.** Medium and low findings are listed but not
counted, so the headline number stays comparable between critiques.

---

## Recommendation

Not a verdict. An argued recommendation, and the decision is yours.

**If this is a personal tool or an internal project:** take it. The world is exceptional, the
ergonomics are strong, and every flag in Layer 3 is priced in a currency you are not spending.
This is the case where `flag, never block` matters most — a rubric that let ownability veto would
have thrown away the best available name for a risk that does not exist at this scale.

**If this is a funded venture:** the honest position is *strong name, expensive name*. Layer 2 is
close to the best outcome this rubric can report, and Layer 3 is close to the worst. Those do not
cancel. What tips it:

1. **Settle the positioning question first.** If the product is disciplined retrieval rather than
   exploration, the world is wrong and the crowding argument never has to be had.
2. **Cost the search problem explicitly.** Get an actual number for what owning "scout + category"
   costs for eighteen months. If that number is affordable, the crowding is a line item. If it is
   not, it is a veto you imposed for yourself — which is different from one the rubric imposed.
3. **Consider keeping the world and moving the word.** The vocabulary is the asset, and it does
   not require this particular name to hold the door. A less crowded name inside the same
   semantic world — one that still yields waypoints, blazes and cairns — retains most of the
   Layer 2 value and drops both `high` flags. That is the option most naming processes never
   surface, because they evaluate words instead of worlds.

**What would change this read:** a clean knockout search in the relevant class; evidence that
Scout APM is winding down; or a positioning that leans hard enough into exploration that the
world becomes load-bearing rather than decorative.
