# `phonetics.py` — the deterministic measurement layer

This directory is Layer 1 of `brand-name-critic`: the part of the rubric that is
**computed, not vibed** (PRD §4.2). It takes a candidate name and returns a stable
JSON object describing what is measurably true about how the name sounds, how it
is spelled, and how crowded its phonetic neighbourhood is.

It has opinions about none of it. See [What this does not do](#what-this-does-not-do).

---

## Files

| File | What it is |
|---|---|
| `phonetics.py` | The measurement script. Python 3.8+ standard library only. |
| `build_lexicon.py` | Build-time generator for the vendored lexicon. The only place `cmudict` is imported. |
| `data/lexicon.txt.gz` | 112,631 CMUdict entries of ≤10 phonemes, sorted, gzipped, ~750 KB. Byte-stable. |
| `../tests/test_phonetics.py` | 80 tests. `python3 -m unittest discover -s tests` |
| `../tests/benchmark.txt` | The 20-name benchmark from PRD §8, annotated with what each name probes. |

---

## Usage

```bash
python3 phonetics.py "Scout"                     # one name  -> a JSON object
python3 phonetics.py "Scout" "Stripe" "Xzrq"     # several   -> a JSON array
python3 phonetics.py --file ../tests/benchmark.txt   # one name per line, '#' comments
python3 phonetics.py "Base Camp" --pretty        # multi-word input works
python3 phonetics.py --version
```

From inside a skill, the portable path is
`${CLAUDE_PLUGIN_ROOT}/skills/brand-name-critic/scripts/phonetics.py`. The lexicon is
resolved relative to `__file__`, so the working directory is irrelevant.

The five rules the contract enforces (BUILD-MAP §3, ADR-004) are all honoured:

1. **Deterministic.** Same input → byte-identical output. No randomness, no network,
   no clock. Verified by `TestDeterminism`.
2. **Offline.** No pip install and no download at run time. `data/lexicon.txt.gz` is
   the only data source. Verified by `TestOfflineAndPure`.
3. **Degrades loudly.** A coined name still returns every key, with `confidence: "low"`
   and a `warnings` entry. It never guesses silently.
4. **`ergonomics_score` is profile-independent.** This script has never heard of
   venture / feature / codename. Re-weighting is the skill's job, from `dimensions[*].score`.
5. **No cross-layer composite.** No "brandability" number, no overall verdict.

Cost: about 0.6 s to load the lexicon, then ~10 ms per name. The whole 20-name
benchmark runs in well under a second.

---

## The JSON contract

```jsonc
{
  "schema_version": "1.0",
  "input": "Scout",                 // exactly as given
  "normalized": "scout",            // lowercased, a-z and single spaces only

  "pronunciation": {
    "source": "cmudict",            // cmudict | cmudict-compound | g2p
    "confidence": "high",           // high | medium | low
    "arpabet": ["S","K","AW1","T"], // stress digits kept
    "ipa": "skaʊt"                  // no stress marks; tokens space-separated
  },

  "syllables": {
    "count": 1,
    "structures": ["CCVC"],         // one per syllable
    "onsets": [["S","K"]],          // one per syllable, stress digits stripped
    "codas": [["T"]]
  },
  // invariant: len(structures) == len(onsets) == len(codas) == count

  "stress": {
    "pattern": "1",                 // one digit per syllable
    "primary_syllable": 0,          // index of the '1' (or the '2', or 0)
    "shape": "monosyllable"         // monosyllable | trochee (DA-da) | iamb (da-DA)
                                    // | dactyl | amphibrach | anapest
                                    // | initial-/medial-/final-stress
                                    // | no vowel nucleus | no syllables
  },

  "phonotactics": {
    "illegal_clusters": [           // objects, not bare strings
      { "cluster": ["Z","Z","R","K"], "position": "onset", "syllable": 0,
        "note": "onset /zzrk/ is not an attested English onset" }
    ],
    "sonority_violations": [        // same shape
      { "cluster": ["R","K"], "position": "onset", "syllable": 0,
        "note": "onset /rk/ does not rise in sonority (liquid then stop)" }
    ],
    "max_onset_length": 2,
    "max_coda_length": 1
  },

  "orthography": {
    "letters": 5,
    "rare_letters": ["x"],              // j k q x z present in the spelling, sorted
    "rare_letter_common_sound": null,   // true | false | null — see below
    "ambiguous_graphemes": [
      { "grapheme": "ou", "positions": [2],
        "readings": ["/aʊ/ out","/uː/ soup","/ʌ/ tough","/ɔː/ four"],
        "note": "four common readings" }
    ],
    "homophone_spellings": ["scowt"]    // sorted, max 8, never the correct spelling
  },

  "neighborhood": {
    "density": 26,                  // real words one phoneme edit away
    "neighbors": ["scat","scoot"],  // sorted, capped at 12
    "percentile": 84,               // higher = denser = less distinctive
    "coverage": "complete"          // complete | truncated
  },

  "international": {
    "hard_phonemes": [ { "phoneme": "TH", "ipa": "/θ/", "note": "..." } ],
    "affected_languages": ["French","Japanese"],   // sorted
    "risk": "low"                   // low | medium | high
  },

  "verbability": {
    "syllable_count": 1,
    "ends_in_vowel": false,
    "clippable_to": [],             // shorter forms that stay pronounceable
    "verb_form": "to scout",
    "agentive": "scouter"
  },

  "dimensions": {
    "pronounceability":         { "score": 96, "evidence": ["1 syllable", "..."] },
    "spellability":             { "score": 84, "evidence": [...] },
    "distinctiveness":          { "score": 50, "evidence": [...] },
    "rhythm_recall":            { "score": 90, "evidence": [...] },
    "verbability":              { "score": 95, "evidence": [...] },
    "international_robustness": { "score": 96, "evidence": [...] }
  },

  "ergonomics_score": 85,           // equal-weight mean of the six, rounded
  "warnings": []
}
```

`evidence` strings carry their own arithmetic (`"1 ambiguous grapheme: <ou> (-10)"`),
so a critique can quote the reason rather than restating the number.

---

## How each layer is measured

### Syllabification — Maximal Onset Principle, over an explicit onset inventory

Consonants between two nuclei go to the following onset, taking the **longest suffix
of the run that is an attested English onset**; the rest closes the preceding
syllable. The inventory is shipped as a literal set in `LEGAL_ONSETS`, never inferred:

* three-consonant: /str/ /spl/ /skr/ /spr/ /skw/
* /s/ + stop or sonorant: /sk/ /st/ /sp/ /sl/ /sm/ /sn/ /sw/
* obstruent + liquid: /pl/ /pr/ /bl/ /br/ /tr/ /dr/ /kl/ /kr/ /gl/ /gr/ /fl/ /fr/ /θr/ /ʃr/
* consonant + glide: /tw/ /kw/ /dw/ /hw/ /gw/ /θw/, and C+/j/ (cute, few, music)
* every singleton consonant except /ŋ/, which cannot begin an English word

A string with no vowel at all (Xzrq → `Z Z R K`) is returned as one *defective*
syllable with an empty nucleus, so the `count == len(structures)` invariant holds and
the caller still gets a CV structure to look at.

### Sonority sequencing

Every phoneme has a rank: stops 1 < affricates 2 < fricatives 3 < nasals 4 <
liquids 5 < glides 6 < vowels 7. **Onsets must rise** toward the nucleus, **codas must
fall** away from it. Two licensed exceptions:

* **/s/ + voiceless stop.** The /s/ is an extrasyllabic appendix, not part of the
  sonority slope, so /sp/ /st/ /sk/ and their /spl/ /str/ /skr/ /spr/ /skw/ extensions
  are checked from the stop onward. Without this, **Scout** and **Stripe** — two of the
  benchmark's best names — would both be flagged. That would be a false positive, not a
  finding.
* **Word-final coronal obstruents** /t d s z θ/ in a coda (cats, lapsed, sixths) attach
  outside the coda proper and are stripped before the falling check.

A coda is reported as *illegal* (rather than merely violating sonority) when it
contains /h/, /w/ or /j/, or when its core after appendix-stripping is three or more
consonants that do not fall — e.g. Blorbnth's /rbnθ/.

### Neighbourhood density

Count of real words one phoneme edit away — substitution, insertion, or deletion —
with stress digits ignored when comparing, because "récord" and "recórd" are the same
phonetic neighbour.

The lexicon is bucketed by phoneme length, so a query of length *N* only ever touches
buckets *N−1*, *N* and *N+1*, and every test is an **O(1) set membership** rather than
a pairwise edit distance against 112k entries. Cost is ~80·*N* set lookups per name:
about 10 ms, not seconds.

`percentile` is the **mid-rank percentile** against a build-time sample of 8,046 words
(every 14th entry of the sorted lexicon — a stride, so no seed is involved). The
sample's density histogram is generated by `build_lexicon.py` and stored in the
lexicon file's own header, so it is regenerable rather than a magic constant baked
into the script.

`coverage` is `"truncated"` when the name has 10 or more phonemes, because the
lexicon's ≤10-phoneme cutoff means its *N+1* bucket is not fully represented and the
density is then a lower bound. A warning says so.

**Note on what counts as a neighbour:** every CMUdict entry does, including inflected
forms and surnames. Scout's neighbours therefore include *scouts*, *scouter* and
*Schuette*. This is the standard psycholinguistic definition and it is why Scout's
density (26, 84th percentile) is higher than a hand-count of dictionary headwords
would suggest — Scout really does live in a crowded phonetic street.

### `rare_letter_common_sound` — the Barton test (PRD §3.3)

| Value | Meaning |
|---|---|
| `null` | No rare letter (j k q x z) in the spelling. The test does not apply. |
| `true` | A rare letter sits on top of sounds that are all common in English, in a phonotactically legal word. **Xerox, Zillow, Kodak, Slack, Flickr.** |
| `false` | The rare letter buys distinctiveness by spending articulation: a phoneme outside the common English set, or a cluster English does not license, or no vowel at all. **Xzrq, Sqwrlyx, Vzzt.** |

"Common English phonemes" excludes /ʒ/, /ɔɪ/, /ʊ/, /θ/ and /ð/ — the five that are
genuinely low-frequency or marginal in English. The bar is *English* frequency, not
cross-linguistic frequency: /ɜr/ is hard for a Spanish speaker but trivially common in
English, so Flickr is not penalised for it here. Cross-linguistic difficulty is the
`international` block's job, and it is reported separately on purpose.

The legality clause is what separates Xerox from Xzrq, which is the exact distinction
PRD §3.3 says the source ergonomics document could not articulate.

### `ambiguous_graphemes`

Driven by `AMBIGUOUS_TABLE`, an explicit inventory of spellings with more than one
common English reading, each entry carrying the readings it is claiming:
`ough` `augh` `eigh` `ea` `ie` `ei` `oo` `ou` `ow` `ai` `ay` `au` `ch` `gh` `ph`,
`ti`/`ci`/`si` before a vowel, the silent-letter onsets `kn` `gn` `wr` `ps`, final `mb`
`mn`, soft/hard `c` and `g` before e/i/y, `x`, `q` without `u`, and non-initial `y`.

Repeated occurrences of the same grapheme collapse into one entry with a list of
positions, so a name is not penalised twice for the same problem.

### `homophone_spellings`

Plausible misspellings someone would produce hearing the name once. Generated, not
guessed:

1. Segment the spelling into graphemes with the g2p aligner.
2. For each segment, substitute the alternate spellings `SPELLINGS` lists for that
   segment's phonemes (one substitution at a time — deterministic and small).
3. Reject anything orthographically impossible: word-initial geminates or `ck`,
   geminates not preceded by a vowel, `q` without `u`, three identical letters running.
4. **Keep only candidates the g2p engine reads back as the same phoneme string as the
   name itself.** This is the step that stops the list filling with letter salad:
   *Linguo* is rejected (it reads /lɪŋɡwoʊ/), *Lyngua* is kept.

Sorted, capped at 8, never includes the correct spelling. The accuracy of step 4 is
bounded by the g2p engine's, measured below.

### `international.hard_phonemes`

| Item | Weight | Affected |
|---|---|---|
| /θ/ | 2 | French, German, Spanish, Italian, Portuguese, Russian, Mandarin, Japanese, Korean, Hindi |
| /ð/ | 2 | as above, minus Spanish |
| /ʒ/ | 2 | Spanish, German, Mandarin, Japanese, Korean, Hindi |
| /ŋ/ word-initially | 2 | English and most European languages disallow it entirely |
| /æ/ | 1 | Spanish, Italian, Portuguese, Russian, Mandarin, Japanese |
| /ɜr/ | 1 | French, German, Spanish, Italian, Japanese, Korean |
| /ɔɪ/ | 1 | Mandarin, Japanese, Korean |
| /r/–/l/ **contrast** (both present in one name) | 1 | Japanese, Korean |
| /v/–/w/ **contrast** (both present in one name) | 1 | Hindi, German, Japanese, Korean |

The two contrasts only fire when both members appear in the same name — a name with
/r/ and no /l/ poses no contrast problem. /ɜr/ counts as a rhotic for that test.

`risk` bands on the weight total **plus structural difficulty**: +1 for any consonant
cluster of three or more, +2 for no vowel nucleus (both punishing in CV-syllable
languages). 0 → `low`, 1–2 → `medium`, 3+ → `high`.

### `verbability`

`clippable_to` cuts at the first syllable boundary and offers both the maximal-onset
cut and the "closed" variant that pulls the next consonant back into the coda —
Lingua → *ling*, Figma → *fig*, Palantir → *pal*. A candidate is kept only if it is
three letters or more and its own phonotactics are clean.

`agentive` uses regular English derivation, spelled out so it is auditable:
`-e` → +r (Stripe → striper) · `-y` → −y +ier · monosyllabic CVC → double the final
consonant (Scan → scanner) · otherwise +er (Scout → scouter).

---

## The six dimension formulas

Every score is `clamp(0, 100, ...)`. **There are no free parameters that are not
written down here.** All penalties are stated in the `evidence` strings too, so the
arithmetic is visible in the output itself.

### 1. Pronounceability — "can a four-year-old say it"

```
100
  − syllable count penalty      {0,1,2: 0}  {3: 6}  {4: 14}  {5+: 22}
  − 40  if there is no vowel nucleus
  − min(45, 18 × illegal clusters)
  − min(30, 12 × sonority violations)
  −  4 × (syllables with a 2+ onset  +  syllables with a 2+ coda)
  −  8 × max(0, longest cluster − 3)
```
One and two syllables are equally easy; the cliff starts at three. Each consonant
cluster adds articulatory load, and clusters past three consonants add it steeply.
A string with no vowel cannot be produced as a syllable at all, which is why the
no-nucleus penalty is the largest single term in the whole rubric.

### 2. Spellability — "hear it once, spell it right"

```
100
  − 10 × min(distinct ambiguous graphemes, 4)
  −  6 × min(homophone spellings, 5)
  − 10  if rare_letter_common_sound is false
  − min(16, 8 × consonant-letter runs of length 4+)
  − 25  if the spelling contains no vowel letter
```
The two orthographic measures pull in opposite directions and both belong here:
ambiguous graphemes are *spelling → sound* uncertainty, homophone spellings are
*sound → spelling* uncertainty. A name with neither is a name you can dictate.

### 3. Distinctiveness — "is the phonetic street crowded"

```
100 − 0.6 × neighbourhood percentile
    + 12  if rare_letter_common_sound is true
```
The percentile already encodes the whole density distribution, so it is the only
density term. The bonus rewards the Barton sweet spot only: rare letters on *rare*
sounds get nothing here, because the distinctiveness they buy is already priced into
the percentile and the cost is charged on pronounceability and spellability.

Note that a broken name can legitimately score high here. **Xzrq scores 81 on
distinctiveness and that is correct** — it *is* distinctive. It is bad for other
reasons, and the six dimensions are reported separately so you can see which.

### 4. Rhythm & recall — "can you reproduce it ten minutes later"

```
base    20  if there is no vowel nucleus
        else  {1: 90}  {2: 100}  {3: 88}  {4: 74}  {5+: 60}
  − 10  if no primary stress could be located
  +  4  if three syllables in a dactyl (DA-da-da)
  − min(15, 5 × (illegal clusters + sonority violations))
  −  6  if more than 10 letters
```
Two syllables score above one: the trochee is the most reproducible shape in English,
and a monosyllable gives a listener less to hold onto. Clusters English does not
license are hard to repeat back even when you can say them once.

### 5. Verbability — "can it be verbed, clipped, nicknamed"

```
base  {1: 90}  {2: 75}  {3: 55}  {4+: 35}
  − 50  if there is no vowel nucleus
  +  5  if every token is already an English word
  +  5  if it clips to something pronounceable
  −  5  if it ends in a vowel sound
  − 10  if there are illegal clusters   (else − 6 if sonority violations)
```
Short verbs better; existing words inflect without explanation ("to scout" needs no
introduction); vowel-final names inflect awkwardly. **Caveat:** the "+5 already an
English word" term is a proxy — the lexicon has no part-of-speech data, so the script
cannot tell a verb from a noun. The evidence string says "already an English word", not
"already a verb", to avoid claiming more than it measured.

### 6. International robustness

```
100
  − 12 × hard-phoneme weight (the table above; contrasts and initial /ŋ/ included)
  −  4 × (syllables with a 2+ onset  +  syllables with a 2+ coda)
  −  8 × (syllables with a 3+ onset  +  syllables with a 3+ coda)
  −  6 × max(0, longest cluster − 2)
  − 20  if there is no vowel nucleus
  −  6  if more than 10 letters
```
Consonant clusters are charged twice as heavily here as on pronounceability, because
a CV-syllable language does not simplify them — it inserts vowels, and /str/ becomes
three syllables.

### `ergonomics_score`

The equal-weight mean of the six, rounded to an integer. **Profile-independent by
design** (BUILD-MAP §3 rule 4): the script does not know whether this is a venture
name, a feature name, or a codename. Re-weighting for a profile is the skill's job,
using `dimensions[*].score`.

---

## Regenerating the lexicon

```bash
pip install cmudict          # BUILD-time dependency only; phonetics.py never imports it
python3 build_lexicon.py     # rebuilds data/lexicon.txt.gz and prints the g2p measurement
python3 build_lexicon.py --skip-measure    # rebuild only
python3 build_lexicon.py --measure-g2p     # measure only, no rebuild
```

Filtering: lowercase a–z keys only (drops apostrophes, hyphens, periods, digits);
CMUdict's `(2)`/`(3)` alternate-pronunciation duplicates dropped, first pronunciation
kept; entries of more than 10 phonemes dropped.

```
cmudict entries (alternates already grouped): 126052
  dropped, not lowercase a-z only:            8559
  dropped, more than 10 phonemes:             4862
  kept:                                       112631      (750.2 KB gzipped)
```

**Why ≤10 phonemes.** A one-phoneme-edit neighbour of an *N*-phoneme name has *N−1*,
*N* or *N+1* phonemes and nothing else. With a cutoff of 10, every name up to **9
phonemes** has complete neighbourhood coverage. Longer names report
`"coverage": "truncated"` and a warning rather than quietly under-counting. The tail
past 10 phonemes is almost entirely long inflected forms and technical vocabulary that
no brand name is a neighbour of, and dropping it takes the file from ~1 MB to ~750 KB.

Output is sorted and written with `mtime=0` in the gzip header, so two rebuilds from
the same CMUdict release are **byte-identical** — verified by rebuilding twice and
comparing checksums.

---

## PRD open question 2 — how much does g2p undermine the "deterministic" claim?

> *"CMUdict coverage for invented names — coined names aren't in the dictionary. Need
> a grapheme-to-phoneme fallback, which introduces its own error rate. How much does
> that undermine the 'deterministic' claim for Layer 1?"* — PRD §9.2

### The answer, in one paragraph

**The pipeline is deterministic. The transcription of an unknown word is an estimate.**
Those are different claims and the output distinguishes them: a name resolved from
CMUdict carries `source: "cmudict"` and `confidence: "high"`; a name assembled from two
dictionary words carries `"cmudict-compound"` / `"medium"`; a name transcribed by rule
carries `"g2p"` / `"low"` **and a warning saying so in words**. Every downstream number
for a g2p name inherits that confidence. What determinism buys is that the same name
always produces the same answer and the same evidence — you can diff two runs, you can
regression-test the rubric, and you can argue with a specific number. What it does not
buy is that the phoneme string for a coined name is *right*. Below is how often it is.

### Measured, not asserted

Held-out sample: **2,500 words** drawn from the 112,631-entry lexicon with
`random.Random(20260824)` — seeded, so the number is reproducible by anyone running
`python3 build_lexicon.py --measure-g2p`. The g2p engine has no access to the
dictionary, so these are genuinely unseen words.

| Metric | Result |
|---|---|
| Exact phoneme-string match, stress ignored | **32.8 %** |
| Exact phoneme-string match, stress included | 24.2 % |
| Per-phoneme accuracy (1 − phoneme error rate) | **79.4 %** |
| Phoneme error rate (Levenshtein edits / reference phonemes) | 20.6 % |
| Correct phoneme *count* | 79.2 % |

Broken out by word length, because **brand names live in the first row**:

| Word length | n | Exact match | Per-phoneme |
|---|---|---|---|
| ≤ 6 letters | 983 | **46.9 %** | **82.0 %** |
| 7–9 letters | 1,173 | 25.9 % | 78.8 % |
| 10+ letters | 344 | 16.0 % | 77.1 % |

### What the errors actually are

The dominant error family is **vowel quality in unstressed syllables**. CMUdict reduces
most unstressed vowels to /ə/ or /ɪ/; predicting that requires predicting stress, and
predicting English stress from spelling is the hard problem this engine does not
solve — it puts primary stress on the first syllable unless the word starts with a
common unstressed prefix. That single heuristic accounts for most of the gap between
79 % per-phoneme accuracy and 33 % exact match: the consonant skeleton is usually right
and one vowel in the middle is wrong.

**A measured negative result, recorded so nobody re-tries it:** an unstressed-vowel
reduction pass (single-letter vowels outside the primary-stress syllable → /ə/) was
implemented and measured. It *lowered* exact match from 29.1 % to 27.3 % and degraded
Kodak and Xerox specifically, because reduction driven by a wrong stress guess is worse
than no reduction. It was removed. Fixing this properly means a real stress predictor,
not another rule.

Improvements that were measured and kept, from a 25.7 % / 75.8 % baseline:
inflectional endings `-ed` `-es` `-s` (+3.4 pts), an unstressed-suffix table (+2.5),
hard `g` before `i` (+0.8), long `e` only under magic-e (+0.4), intervocalic `s` → /z/.

### Why this is the honest position rather than a cop-out

Three things blunt the error rate before it reaches a critique:

1. **Most real candidates never touch g2p.** Of the 20-name benchmark, 11 resolve from
   CMUdict directly. CMUdict includes a very large proper-noun inventory, so many
   "coined-sounding" names are in it (Xerox, Kodak, Flickr, Firefox all are).
2. **Compound decomposition catches another slice** at `medium` confidence: a name that
   splits into two dictionary words (Firefox → fire + fox, Wavebreak → wave + break)
   is assembled from two known-good transcriptions, not guessed. Both parts must be at
   least three letters *and* three phonemes, so CMUdict's surname inventory cannot read
   "Zillow" as "zill" + "low".
3. **The measurements that matter most degrade gracefully.** Syllable count, stress
   shape and consonant-cluster structure survive a wrong vowel; they depend on the
   *skeleton*, which the 79 % per-phoneme figure mostly describes. Neighbourhood density
   is the measurement most exposed to a transcription error, and it is also the one
   whose dimension (distinctiveness) the PRD already says to treat as
   `flag, never block`.

So: **the score for a `confidence: "low"` name is an estimate with a stated error bar,
and the JSON says so on the tin.** A critique that quotes a g2p name's numbers without
quoting the warning is misreading its own input.

---

## Judgment calls a reviewer should know about

1. **The legal-onset set is larger than the brief's list.** Added, each attested and
   each load-bearing: /spr/ /skw/ (siblings of the /spl/ /skr/ /str/ the brief lists —
   without them "Sprig" is a false positive), **/gw/** (CMUdict gives *lingua* as
   `L IH1 NG G W AH0`; without /gw/ the module's own namesake syllabifies wrong),
   **/θw/** (needed for the benchmark's *Thrixthwaite*), and C+/j/ (*cute* is
   `K Y UW1 T` in CMUdict, so without this family every `-ute`/`-ew` name reports a
   false illegal cluster).
2. **Coda legality is deliberately thin.** There is no exhaustive legal-coda inventory —
   only /h/ /w/ /j/ as impossible codas, plus "three or more consonants that do not
   fall in sonority". Everything else surfaces as a sonority violation instead. A full
   coda inventory would be a much larger, more arguable table for less return.
3. **`illegal_clusters`, `sonority_violations` and `ambiguous_graphemes` are arrays of
   objects, not of bare strings.** The contract in BUILD-MAP §3 shows them empty and
   does not pin the element type. Each object carries a `note` field with a ready-made
   human-readable sentence, so a rubric can quote it directly without needing the
   structure.
4. **`rare_letter_common_sound` also requires phonotactic legality**, not just common
   phonemes. This is what makes Xzrq `false` — its phonemes /z z r k/ are individually
   ordinary; it is the cluster and the missing vowel that break it.
5. **`verb_form` is always emitted** as `"to <name>"`. Whether that reads naturally is a
   judgment, and judgments are not this script's job.
6. **`Blorbnth` scores 72** — higher than its pronounceability (54) and international
   robustness (36) suggest, because it is genuinely unambiguous to spell (92) and
   genuinely distinctive (93). The equal-weight mean is mandated by the contract; the
   dimension breakdown is where the story is. This is exactly the argument PRD §4.1
   makes for killing the composite, reappearing one level down.
7. **`stress.shape` for a name with no vowel is `"no vowel nucleus"`**, and the
   syllable count is 1 rather than 0, so the
   `count == len(structures) == len(onsets) == len(codas)` invariant never breaks.

---

## What this does not do

Stated explicitly, because the temptation to add them will recur:

* **No cross-layer composite.** No "brandability" score, no "practicality" score, no
  overall verdict. Killing the composite is the entire point of PRD §4.1.
* **No profile weighting.** The script has never heard of venture / feature / codename.
  `ergonomics_score` is a flat mean; re-weighting is the skill's job.
* **No opinions.** It does not say whether a name is good. It reports that *Scout* has a
  neighbourhood density of 26 at the 84th percentile; whether a crowded namespace
  matters is a `flag, never block` conversation the profile has, not a number.
* **No semantics.** No meaning, no connotation, no `world, not word`, no
  `breadth × fidelity`, no lore. Those are Layer 2 and they are argued, not scored.
* **No trademark, domain, or availability anything.** Layer 3, and out of scope for v1.
* **No network, no clock, no randomness, no pip.** By construction, and tested.
