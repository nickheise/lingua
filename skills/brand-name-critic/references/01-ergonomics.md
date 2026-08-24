# Layer 1 — Ergonomics: reading the script's JSON

**This file does not derive phonetics. The script already did that.** `scripts/phonetics.py` has
looked the name up in a vendored CMUdict-derived lexicon, syllabified it, checked its clusters,
counted its one-edit neighbours and scored six dimensions. Do not re-count syllables by eye, do
not estimate neighbourhood density, do not argue with the transcription. Read the JSON and
interpret it.

Your job in this layer has exactly four parts:

1. Check the confidence before reading any number.
2. Read each of the six dimensions and say what its score *means for this name*.
3. Re-weight for the context profile **in prose**. Never recompute the number.
4. Identify any dimension acting as a **floor** rather than as a term in a sum.

---

## 0. Check confidence first — always, before any number

Read `pronunciation.source`, `pronunciation.confidence` and `warnings` **before** reading
`dimensions`.

| `confidence` | `source` | What it means | What you must write |
|---|---|---|---|
| `high` | `cmudict` | The name is in the dictionary. The transcription is a lookup. | Nothing special. Numbers are measurements. |
| `medium` | `cmudict-compound` | Assembled from known parts (e.g. *Firebase* = *fire* + *base*). Usually right; the join is the risk. | One line: transcription assembled from known parts; the syllable boundary at the join is the least certain part. |
| **`low`** | **`g2p`** | **The transcription is an estimate produced by a grapheme-to-phoneme model.** | **A visible caveat before the table.** See below. |

**When `confidence` is `low`, say so in the critique rather than presenting an estimate as a
measurement.** The required form is a short block before the dimensions table, stating that the
name is not in the dictionary, that the transcription is an estimate, and that every score below
inherits that uncertainty. Then continue — a low-confidence reading is still far better than a
guess, and the script's own `warnings` array tells you which parts are shakiest.

**What survives low confidence and what does not:**

| Robust under g2p | Fragile under g2p |
|---|---|
| Syllable count (usually) | The exact ARPABET string |
| Presence or absence of a vowel nucleus | Fine-grained vowel quality |
| Letter counts, rare letters, `q`-without-`u` | Stress placement |
| Whether an onset cluster is legal English | Neighbourhood density (neighbours of a wrong transcription are the wrong neighbours) |

Rule: build the argument on the robust facts, and hedge anything that rests on the fragile ones.

Also read `neighborhood.coverage`. If it is `truncated`, the name is longer than the lexicon
cutoff and the density figure is a floor, not a count — distinctiveness is *at least* this good.
Say so.

---

## 1. Why six dimensions and not seventeen

Context you need in order to resist the urge to add more.

The source ergonomics document had **seventeen** weighted dimensions. Seventeen fails in a
specific, predictable way: **everything scores 85–95, because no name is bad at all of them, and
the composite becomes noise.** Several were also the same dimension wearing different hats —
phonotactics, syllable simplicity, mouth ergonomics and sonority flow are four views of "is this
easy to say." Neumeier uses seven, Watkins five, Igor four.

Applying the deletion test — *would removing this change the output?* — most were no-ops. The six
that survive:

| # | Dimension | Absorbed | The question it answers |
|---|---|---|---|
| 1 | **Pronounceability** | syllable count, CV structure, sonority sequencing, cluster legality | Can a stranger say it correctly on first sight? |
| 2 | **Spellability** | spelling ambiguity, homophone spellings | Can they spell it correctly having only *heard* it? |
| 3 | **Distinctiveness** | neighbourhood density, `rare letters, common sounds` | Does it stand apart in sound-space and in search? |
| 4 | **Rhythm & recall** | stress pattern, ten-minute reproduction | Will they still have it ten minutes later? |
| 5 | **Verbability** | verb form, clipping, nicknaming | Does it survive being used in a sentence? |
| 6 | **International robustness** | hard phonemes, missing-phoneme screen | Does it survive leaving English? |

### Two dimensions that are deliberately absent

**Typing ergonomics is cut entirely — do not reintroduce it.** It is the one dimension with no
support anywhere in the practitioner literature: Barton, Neumeier, Watkins, Lexicon and Igor all
omit it. Nobody has ever failed because of same-finger repetition or an awkward home-row
transition. Scoring it equal-weight with hearability was the source document's clearest mistake.
If a name is genuinely painful to type, mention it in one clause as a footnote; never as a
dimension.

**Sound symbolism moved out of ergonomics and into brandability.** It is not a property of the
name at all — it is a **fit check** between the name's phonetic personality and the product's
positioning, and it is *unanswerable* without knowing the positioning. An ergonomics layer that
scored it would be scoring half of a comparison. It now lives in
[`02-brandability.md`](02-brandability.md) as a tie-breaker with a required evidence-strength
label. Do not score it here, and do not describe a name as "sounding fast" or "sounding premium"
in Layer 1.

---

## 2. Reading the six dimensions

### The score bands — apply these uniformly

| Band | Reading | How to write it |
|---|---|---|
| 90–100 | Exceptional. An asset worth naming. | State it and move on. |
| 75–89 | Comfortable. Any cost is priced and survivable. | Name the specific cost in one clause. |
| 60–74 | Acceptable **with a named cost**. | You owe the reader the concrete consequence, not a hedge. |
| 40–59 | A real problem on this dimension. | Say what breaks, and check whether the profile weights it up. |
| 0–39 | Structural failure. | Check whether the dimension is a **floor** (§3). If it is, say plainly that no other score compensates. |

Never report a score without a consequence. "Spellability 78" is data. "Spellability 78 — /aʊ/
has two common spellings, so a measurable fraction of people who only hear the name will type
`Skout`, which is a live app" is a finding.

### 1 · Pronounceability

**Reads:** `syllables.count`, `syllables.structures`, `phonotactics.illegal_clusters`,
`phonotactics.sonority_violations`, `phonotactics.max_onset_length`.

**Means:** whether a stranger produces the intended sound on first sight, without hesitation.

| Signal in the JSON | Interpretation |
|---|---|
| `syllables.count` 1–2 | Optimal. 3 is fine. 4+ invites clipping — check `verbability.clippable_to` for what it will be clipped *to*, because that is the real name. |
| `stress.shape: "no vowel nucleus"` | No syllable an English speaker can produce. The script still reports `syllables.count: 1` with an all-consonant structure so the array lengths stay consistent — **key on `stress.shape`, and on the matching entry in `warnings`, never on a count of 0.** Not a low score: the dimension has failed to apply. Fatal. |
| `illegal_clusters` non-empty | Every entry is a place a reader will stumble, insert a vowel, or give up. Quote them. |
| `sonority_violations` non-empty | Sonority must rise to the nucleus and fall after it. Violations produce reliable mispronunciation, not merely difficulty. |
| `max_onset_length` > 3 | English permits three only in the strict /s/ + voiceless stop + liquid/glide template (*spr-*, *str-*, *skw-*). Anything else is illegal regardless of length. |

**Fatal vs cosmetic:** below 40 is **fatal under every profile**, including codename. See §3.
A single legal-but-unusual cluster costing 5–10 points is cosmetic.

### 2 · Spellability

**Reads:** `orthography.ambiguous_graphemes`, `orthography.homophone_spellings`,
`orthography.letters`.

**Means:** hear it once at a conference, type it correctly into a browser that evening.

| Signal | Interpretation |
|---|---|
| `ambiguous_graphemes` non-empty | Each entry is a fork in the road. `ough`, `ea`, `ei`/`ie`, `-ance`/`-ence`, `c` vs `k` vs `ck`, doubled consonants. |
| `homophone_spellings` non-empty | **Check whether any of them is a real, live product.** A misspelling with a destination is worse than a misspelling that 404s. This check is manual and it matters. |
| Deliberate respelling (Flickr, Lyft) | Trades spellability for distinctiveness and domain availability *on purpose*. Report the trade rather than the score alone. |

**Fatal vs cosmetic:** near-fatal under the **feature profile** (in-app search, support
transcripts, documentation) and under any name that will be spoken before it is seen. Merely
expensive under the **venture profile**, where the cost is a domain redirect and some lost
word-of-mouth traffic. Close to irrelevant under **codename**.

### 3 · Distinctiveness

**Reads:** `neighborhood.density`, `neighborhood.neighbors`, `neighborhood.percentile`,
`neighborhood.coverage`, `orthography.rare_letters`, `orthography.rare_letter_common_sound`.

**Means:** two different things that the single score merges, and you must separate them in prose:

- **Phonetic distinctiveness** — `density` and `percentile`. High density means the name sits in a
  busy region of sound-space and will occasionally be misheard. Name the actual confusions from
  `neighbors`; they are the concrete cost.
- **Orthographic distinctiveness** — `rare_letters` and `rare_letter_common_sound`. This is what
  buys search ownability.

> **Critical limitation, state it whenever it bites.** The script measures *phonetic* neighbourhood
> density. It cannot see that a name is a common English word, or that four large companies
> already use it. A plain dictionary word can score a perfectly respectable distinctiveness here
> and still be a namespace disaster. **Semantic and commercial crowding is a Layer 3 finding, not
> a Layer 1 one.** When they disagree, say so explicitly — that disagreement is a finding in
> itself.

#### `rare letters, common sounds`

`orthography.rare_letter_common_sound` is the Barton sweet spot as a boolean:

| Value | Meaning | Reading |
|---|---|---|
| `true` | A rare letter (z q x j k) lands on a common phoneme. | The sweet spot. Orthographic distinctiveness bought without an articulatory cost. |
| `false` | Rare letters present, landing on rare, awkward or impossible sounds. | Distinctiveness bought by making the name harder to say — a bad trade under every profile. |
| `null` | No rare letters in the spelling. | Not a fault. Most good names are here; distinctiveness must then come from density or from Layer 2. |

**The contradiction this resolves, and you should state it when the case calls for it.** Rich
Barton advises using high-point Scrabble letters (Z, Q, X, J, K) *and* advises picking a word a
four-year-old can say — and does not notice that these appear to conflict. His own examples
resolve it:

| Name | Rare letter | Sound it makes | Common sound? |
|---|---|---|---|
| **Xerox** | X | /z/ (and /ks/ at the end) | yes — both ordinary |
| **Kodak** | K | /k/ | yes — one of the most frequent consonants in English |
| **Coke** | K | /k/ | yes |
| **Zillow** | Z | /z/ | yes |

Every one maps a rare **letter** onto a completely common **sound**. **None uses a rare phoneme.**
You get low neighbourhood density and better search ownability without paying an articulatory
cost.

**The rule has a second half that only becomes visible on bad names.** The mapping must be
letter→common-phoneme, *and* those phonemes must be arranged into legal syllables. Xerox and Xzrq
both open with X and both, letter by letter, map onto ordinary sounds — but Xerox is a
pronounceable two-syllable word wearing a rare letter, while Xzrq has no vowel and an illegal
onset. Rare letters buy distinctiveness only when there is a sayable word underneath to attach
them to. When `rare_letter_common_sound` is `false` **or** when it is `true` but
`stress.shape` is `"no vowel nucleus"` or `illegal_clusters` is non-empty, this is the finding
to write.

### When not to lead with `ergonomics_score`

The score is an equal-weight mean of the six dimensions, and on a badly broken name the mean
flatters it. *Blorbnth* scores 72 — higher than its pronounceability (54) and international
robustness (36) would suggest — because it is genuinely unambiguous to spell (92) and genuinely
distinctive (93). Both of those are true. Averaged, they bury the finding.

So: if any of these hold, **lead with the dimension breakdown and report the mean second**,
stating why.

- `stress.shape` is `"no vowel nucleus"`
- `phonotactics.illegal_clusters` is non-empty
- any single dimension scores below 40
- `pronunciation.confidence` is `low`

This is `kill the composite` from §4.1 reappearing one layer down. The mean is a convenience for
comparing *comfortable* names to each other; it is not a summary of a broken one.

**Fatal vs cosmetic:** never fatal on its own; a low score is a *cost*, and how much it costs is
set entirely by the profile. Under **venture** it is a headline concern. Under **feature** a low
score is frequently the requirement — a distinctive feature label is a bug.

### 4 · Rhythm & recall

**Reads:** `stress.pattern`, `stress.shape`, `syllables.count`.

**Means:** reproduction ten minutes later, from memory, correctly stressed.

| Shape | Reading |
|---|---|
| Monosyllable | Maximally reproducible. Ceiling. |
| Trochee (`10`) — *Kodak*, *Notion*, *Balance* | The default strong shape in English. Near-ceiling. |
| Iamb (`01`) — *Adobe*-ish | Fine, slightly less sticky than a trochee. |
| Dactyl (`100`) — *Wikipedia*-ish | Works, but three syllables invites clipping. |
| No dominant stress, or `pattern` empty | The name has no rhythm to remember. Serious. |
| 4+ syllables | Read `verbability.clippable_to`. **Whatever it clips to is the real name** — critique that too. |

**Fatal vs cosmetic:** rarely fatal alone. Under **codename**, where memorability is nearly the
only thing weighted up, a low score here is the closest that profile comes to a disqualification.

### 5 · Verbability

**Reads:** `verbability.verb_form`, `verbability.agentive`, `verbability.clippable_to`,
`verbability.syllable_count`, `verbability.ends_in_vowel`.

**Means:** survival inside ordinary sentences — "just Slack me", "I Googled it", "Scout it first".

> **`verb_form` is always non-null — do not read it as evidence of anything.** The script builds
> it mechanically from the name, so an invented word gets `"to kestrel"` and an agentive of
> `"kestreler"` exactly as readily as *Scout* gets `"to scout"`. The signal that separates them is
> the **evidence string** on `dimensions.verbability`: a name already in the lexicon carries
> `"already an English word — inflects without explanation (+5)"`, and a coined one does not.
> Key on that. Reading a populated `verb_form` as "this is already a verb" produces a confident
> overclaim about usage that does not exist — this happened in a real validation run.

| Signal | Reading |
|---|---|
| evidence includes `already an English word` | Free verb, no education cost. Strong asset under **venture**. |
| evidence lacks it, but 1–2 syllables ending in a consonant | **Verbable in principle, not yet verbed.** It will happen naturally if the product is used enough — a smaller asset than an existing verb, and it must be described as potential rather than fact. |
| 3+ syllables and no clipping | Will not be verbed. Under venture, a real if quiet loss. |
| `clippable_to` non-empty | Users will do this whether you approve or not. Check the clipping is not itself a problem — an unfortunate word, or another product. |

**Fatal vs cosmetic:** never fatal. Weighted **up** under venture, **down** under feature (nobody
verbs a settings screen), **irrelevant** under codename.

### 6 · International robustness

**Reads:** `international.hard_phonemes`, `international.affected_languages`,
`international.risk`.

**Means:** whether the name survives being said by people who do not speak English.

| Signal | Reading |
|---|---|
| `hard_phonemes` includes `TH` | /θ/ and /ð/ are absent from most of the world's major languages. The single most common finding here. |
| Includes an R–L contrast *within the name* | Reliable confusion for Japanese and Korean speakers. An R or an L alone is not the problem; both in one name is. |
| Includes `V`/`W` | Confused across much of South Asia and parts of Central Europe. |
| Unusual vowels (/æ/, /ɜː/) | Usually mapped to the nearest local vowel. Cosmetic — note it, do not weight it heavily. |
| `risk: high` | Treat as a headline finding under **feature** (shipped in every locale) and as a medium finding under **venture**. |

**This dimension does not screen for meaning.** `international.risk` is *phonetic*. Adverse
meanings in other languages are Layer 3, run against
[`myths-blocklist.md`](myths-blocklist.md) — and the blocklist exists because the folk myths in
this area are worse than useless. Never repeat one as fact.

**Fatal vs cosmetic:** weighted heavily **up** under feature. Under venture, a medium concern
unless launch is genuinely global. Under codename, ignore.

---

## 3. Floors, not terms in a sum

`ergonomics_score` is the equal-weight mean of the six. **It is a summary, and sometimes it
lies.** Some dimensions behave as gates: below their floor, no other score compensates, because
everything downstream is conditional on them.

| Dimension | Behaves as a floor? | Floor | Why |
|---|---|---|---|
| Pronounceability | **Yes** | ~40 | Word of mouth, recall, verbability, voice input and saying the name aloud are all gated behind being sayable. |
| Spellability | **Yes, under the feature profile** | ~50 | An unspellable in-app label breaks in-app search, support and docs. |
| Distinctiveness | No | — | A cost, priced by the profile. Can be near-zero and still correct (feature labels). |
| Rhythm & recall | No | — | Degrades memorability; compensable by usage frequency. |
| Verbability | No | — | A missed asset, not a defect. |
| International robustness | No | — | Priced by launch scope. |

**The diagnostic that catches the classic failure:** if `dimensions.distinctiveness.score` is very
high *and* `dimensions.pronounceability.score` is very low, the mean is meaningless and you must
say so. A name can score 99 on distinctiveness precisely *because* nothing in the language sounds
like it — which is the same fact as being unpronounceable, reported with the opposite sign. Write
that sentence explicitly when the pattern appears.

---

## 4. Re-weighting for the profile — in prose, never in arithmetic

**`ergonomics_score` is profile-independent by design** (BUILD-MAP §3, rule 4). The script does
not know which profile is running. Re-weighting is your job, and the correct output of
re-weighting is **an argument about which dimensions matter for this name in this context** — not
a second number.

**Do not compute a weighted score.** A profile-adjusted composite is the same mistake as the
composite the PRD kills, one level down. Report `ergonomics_score` once, unmodified, then argue.

Load the profile file — `references/profiles/{venture,feature,codename}.md` — which owns the
authoritative weighting. The summary below is orientation only:

| Dimension | Venture / product | Feature / UI | Internal codename |
|---|---|---|---|
| Pronounceability | high (floor) | high (floor) | high (floor) |
| Spellability | medium | **very high** | low |
| Distinctiveness | **very high** | **low — often inverted** | medium |
| Rhythm & recall | medium | medium | **very high** |
| Verbability | **high** | low | low |
| International robustness | medium | **high** | ignore |

**The procedure:**

1. Report `ergonomics_score` as computed, and say it is profile-independent.
2. Take the two or three dimensions this profile weights highest and write one sentence each on
   what the name's score there actually costs or buys.
3. Take any dimension the profile weights **down** where the score is low, and say explicitly that
   it does not matter here — and, where it applies, that it is the requirement rather than a
   shortfall.
4. Check §3 for a floor breach. If there is one, it leads the paragraph regardless of the mean.
5. Where Layer 1 and Layer 3 disagree about distinctiveness, flag the disagreement rather than
   averaging it away.

---

## 5. Output shape for this layer

Follow [`../assets/critique-template.md`](../assets/critique-template.md). In brief:

- the invocation line and the transcription, with `source` and `confidence`;
- the low-confidence caveat block, if `confidence` is `low`;
- the six-row table: dimension · score · evidence, taking `evidence` from the JSON verbatim;
- `ergonomics_score`, stated once, described as profile-independent;
- a short prose paragraph headed **"Under the \<profile\> profile"** doing the re-weighting;
- no composite with any other layer, ever.
