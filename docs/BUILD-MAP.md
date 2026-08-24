# Lingua — Build Map

**The plan of record.** Every file this plugin will contain, who builds it, what it must
satisfy, and how we know it is done. Read this before starting work; update it when the
plan changes rather than drifting from it silently.

Source specification: [`docs/PRD.md`](PRD.md). Section references below (§) point into it.
Rationale for anything that deviates from the PRD: [`docs/DECISIONS.md`](DECISIONS.md).

---

## 0. What we are building

A Claude Code **plugin** named `lingua` that ships three Agent Skills for naming work:

| Skill | Invocation | Job | Terminates at |
|---|---|---|---|
| `brand-name-worlds` | User | Brief → 3–5 stress-tested semantic worlds | A chosen world. **No names produced.** |
| `brand-name-generator` | User | Chosen world → clustered shortlist | ~12 candidates with rationale |
| `brand-name-critic` | **Model** | Candidate → three-layer evaluation | An argued recommendation |

The governing rule for invocation (§5.1): **critics are model-invoked, makers are user-invoked.**
Makers carry `disable-model-invocation: true` so they cost zero standing context.

`Lingua` is the **module name, not a skill name** (§7.2). Skill names are boring on purpose
because the model matches on them.

---

## 1. Leading words — the steering vocabulary

These phrases must appear **verbatim and repeatedly** in the skill files, never paraphrased
(§5.4). They are how the agent steers itself. Every builder is accountable for using them.

| Phrase | Where it must appear |
|---|---|
| `world, not word` | worlds SKILL.md, generator SKILL.md, critic brandability ref |
| `breadth × fidelity` | worlds fidelity-test ref, critic brandability ref |
| `six-siblings test` | worlds, generator converge, critic brandability |
| `rare letters, common sounds` | critic ergonomics ref, generator operators ref |
| `read the ending` | critic brandability ref, critic SKILL.md |
| `flag, never block` | critic SKILL.md, practicality ref, all three profiles |
| `diverge → cluster → converge` | generator SKILL.md |

**Verification is a build step, not a preference.** Phase 3 runs a blind trace audit: run each
skill, read the reasoning trace, confirm the phrases are echoed back. If they are not, the
steering failed and the words get stronger or more consistent — the skill is not done.

---

## 2. File inventory

Status legend: `▢` not started · `◐` in progress · `▣` built · `✅` reviewed & accepted

```
lingua/
├── .claude-plugin/
│   ├── plugin.json                        ▢  P0  manifest
│   └── marketplace.json                   ▢  P0  single-plugin marketplace, installable from the repo
├── README.md                              ▢  P0  what it is, install, the three skills, method
├── CHANGELOG.md                           ▢  P0  Keep a Changelog; one entry per phase
├── LICENSE                                ▢  P0  MIT
├── .gitignore                             ▢  P0
│
├── docs/
│   ├── PRD.md                             ▢  P0  source spec, checked in verbatim
│   ├── BUILD-MAP.md                       ▢  P0  this file
│   ├── DECISIONS.md                       ▢  P0  ADR log — every judgment call, with rationale
│   └── reference-critiques/               ▢  P1  hand-written ideal outputs (§8 method note)
│       ├── 00-README.md                   ▢      how these are used as build targets
│       ├── venture-scout.md               ▢      strong venture name
│       ├── feature-balance.md             ▢      feature/UI name
│       └── bad-xzrq.md                    ▢      deliberately bad name
│
├── skills/
│   ├── brand-name-critic/                          ── PHASE 1 ──
│   │   ├── SKILL.md                       ▢  MODEL-INVOKED. 4 steps. ≤500 words.
│   │   ├── references/
│   │   │   ├── 01-ergonomics.md           ▢  interprets script JSON; 6 dimensions
│   │   │   ├── 02-brandability.md         ▢  generativity, familiarity, lore, fit, ownability
│   │   │   ├── 03-practicality.md         ▢  TM tiers, knockout heuristic, domains
│   │   │   ├── myths-blocklist.md         ▢  Chevy Nova et al. — never repeat as fact
│   │   │   ├── troubleshooting.md         ▢  self-improvement log (§5.6), seeded empty
│   │   │   └── profiles/
│   │   │       ├── venture.md             ▢  weights up distinctiveness/generativity/ownability
│   │   │       ├── feature.md             ▢  weights up clarity/spellability/sibling consistency
│   │   │       └── codename.md            ▢  memorability/fun; must never leak into UI
│   │   ├── scripts/
│   │   │   ├── phonetics.py               ▢  the deterministic layer → JSON
│   │   │   ├── build_lexicon.py           ▢  reproducible generator for the vendored lexicon
│   │   │   ├── data/lexicon.txt.gz        ▢  ~112k CMUdict entries ≤10 phonemes, ~700KB
│   │   │   └── README.md                  ▢  usage, JSON contract, g2p error rate
│   │   ├── tests/
│   │   │   ├── test_phonetics.py          ▢  unit + determinism tests
│   │   │   └── benchmark.txt              ▢  the 20-name benchmark set
│   │   └── assets/critique-template.md    ▢  output shape
│   │
│   ├── brand-name-worlds/                          ── PHASE 2 ──
│   │   ├── SKILL.md                       ▢  user-invoked. 4 steps. MUST NOT produce names.
│   │   ├── references/
│   │   │   ├── 01-brief.md                ▢  4-question mini-brief; positioning-canvas mapping
│   │   │   ├── 02-world-sourcing.md       ▢  fixed catalogue + "propose one not on this list"
│   │   │   ├── 03-fidelity-test.md        ▢  5-concept mapping test; breaking-point probes
│   │   │   └── troubleshooting.md         ▢
│   │   └── assets/world-brief-template.md ▢
│   │
│   └── brand-name-generator/                       ── PHASE 2 ──
│       ├── SKILL.md                       ▢  user-invoked. 3 steps. Ends by spawning blind QA.
│       ├── references/
│       │   ├── 01-operators.md            ▢  compound, blend, affix, clip, respell, coinage…
│       │   ├── 02-converge.md             ▢  cluster → shortlist → usage-in-a-sentence
│       │   └── troubleshooting.md         ▢
│       └── assets/shortlist-template.md   ▢
│
└── shared/                                    ── built in Phase 1, used by all three ──
    ├── name-types.md                      ▢  descriptive → suggestive → coined, mapped to TM tiers
    ├── example-bank.md                    ▢  real names by type, industry, era
    └── naming-decisions-log.md            ▢  the taste log (§5.6) — proposed / chosen / rejected
```

Skills reach shared material through `${CLAUDE_PLUGIN_ROOT}/shared/<file>.md`. It sits *outside*
`skills/` deliberately — see DECISIONS.md ADR-003.

**Note on two files both called "decisions".** `docs/DECISIONS.md` is the *engineering* ADR log
for building this plugin. `shared/naming-decisions-log.md` is the *naming* log from §5.6 —
names proposed, chosen, rejected, and why — which accumulates the user's taste over time. They are
different artifacts with different lifecycles. The second one is renamed from the PRD's
`decisions.md` specifically to stop this collision.

---

## 3. The interface contract — `phonetics.py` JSON

**This is the load-bearing coordination decision.** The rubric author (who interprets the numbers)
and the script author (who produces them) are building in parallel against this contract, so
neither waits on the other. Changing it requires updating both sides and this map.

Invocation:

```bash
python3 scripts/phonetics.py "Scout"                    # single name
python3 scripts/phonetics.py "Scout" "Stripe" "Xzrq"    # batch → JSON array
python3 scripts/phonetics.py --file benchmark.txt       # one name per line
```

Output — a single JSON object per name, keys stable, no key ever omitted:

```jsonc
{
  "schema_version": "1.0",
  "input": "Scout",
  "normalized": "scout",
  "pronunciation": {
    "source": "cmudict",            // cmudict | g2p | cmudict-compound
    "confidence": "high",           // high (in dictionary) | medium (compound of known parts) | low (g2p)
    "arpabet": ["S","K","AW1","T"],
    "ipa": "skaʊt"
  },
  "syllables": {
    "count": 1,
    "structures": ["CCVC"],         // per syllable
    "onsets": [["S","K"]],
    "codas": [["T"]]
  },
  "stress": { "pattern": "1", "primary_syllable": 0, "shape": "monosyllable" },
  // A vowel-less name does NOT return syllables.count 0. It returns count 1 with an
  // all-consonant structure and stress.shape "no vowel nucleus", so that
  // count == len(structures) == len(onsets) == len(codas) always holds. Key on
  // stress.shape and on `warnings`, never on a count of 0.
  "phonotactics": {
    // arrays of OBJECTS, not strings. Each carries a ready-made `note` sentence the
    // rubric can quote directly: {cluster, position, syllable, note}
    "illegal_clusters": [],         // clusters not attested in English onset/coda position
    "sonority_violations": [],
    "max_onset_length": 2,
    "max_coda_length": 1
  },
  "orthography": {
    "letters": 5,
    "rare_letters": [],             // z q x j k present in the spelling
    "rare_letter_common_sound": null,  // true = the Barton sweet spot. false = a rare letter that
                                       //   either maps to a rare sound OR maps to common sounds
                                       //   arranged into illegal syllables (see ADR-010). null =
                                       //   no rare letter present.
    "ambiguous_graphemes": [],      // objects: {grapheme, positions, readings, note}
    "homophone_spellings": ["scowt","skout"]  // plausible misspellings from hearing it once
  },
  "neighborhood": {
    "density": 7,                   // count of 1-phoneme-edit real-word neighbours
    "neighbors": ["scoot","stout","shout"],   // capped at 12, sorted
    "percentile": 61,               // vs. the vendored lexicon; higher = denser = less distinctive
    "coverage": "complete"          // complete | truncated (name longer than lexicon cutoff)
  },
  "international": {
    "hard_phonemes": [],            // objects: test with h["phoneme"] == "TH", not `"TH" in list`
    "affected_languages": [],
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
    "pronounceability":          { "score": 96, "evidence": ["1 syllable","legal onset /sk/","no sonority violation"] },
    "spellability":              { "score": 78, "evidence": ["/aʊ/ has two common spellings: ou, ow"] },
    "distinctiveness":           { "score": 62, "evidence": ["neighbourhood density 7 (61st pct)","no rare letters"] },
    "rhythm_recall":             { "score": 90, "evidence": ["monosyllable — maximally reproducible"] },
    "verbability":               { "score": 95, "evidence": ["already a verb","1 syllable"] },
    "international_robustness":  { "score": 88, "evidence": ["no hard phonemes","/aʊ/ near-universal"] }
  },
  "ergonomics_score": 85,           // equal-weight mean of the six; PROFILE-INDEPENDENT
  "warnings": []                    // e.g. "pronunciation inferred by g2p; treat as low confidence"
}
```

Rules the contract enforces:

1. **Deterministic.** Same input → byte-identical output. No randomness, no network, no clock.
2. **Offline.** No pip install, no download at run time. The vendored lexicon is the only data source.
3. **Degrades loudly.** A coined name not in the dictionary still returns every key, with
   `confidence: "low"` and a `warnings` entry. It never guesses silently.
4. **`ergonomics_score` is profile-independent.** The script does not know about venture/feature/
   codename. Re-weighting for a profile is the skill's job, using `dimensions[*].score`.
5. **No composite across layers.** The script never emits a "brandability" or overall number.
   That is the whole point of §4.1 — `ergonomics 85 · brandability: argued · practicality: 2 flags`.

---

## 4. Phases and exit criteria

Each phase ends with a commit, a CHANGELOG entry, and a reviewer pass. The next phase does not
start until the exit criteria are met.

### Phase 0 — Repo foundation `v0.1.0`
Scaffolding, manifest, marketplace entry, README, CHANGELOG, ADR log, this map, PRD checked in.

**Exit:** repo installs as a plugin without error; docs describe the whole plan.

### Phase 1 — `brand-name-critic` `v0.2.0`
Highest confidence, lowest risk, immediately useful, and it forces the rubric to be nailed
down before anything depends on it (§8).

Built by **reverse-engineering**, per the PRD method note: the hand-written ideal critiques in
`docs/reference-critiques/` are written **first**, then the skill is built to produce them, then
a fresh-context subagent runs the skill blind and the outputs are compared.

**Exit criteria:**
- [ ] `phonetics.py` returns stable output for the 20-name benchmark (Scout, Stripe, Notion, Xerox,
      Kodak, Zillow, Flickr, Palantir, Slack, Figma, Lingua + deliberately bad ones)
- [ ] Determinism test passes: two runs byte-identical
- [ ] g2p fallback error rate **measured** against held-out CMUdict and published in `scripts/README.md`
      (this is PRD open question 2 — we answer it with a number, not a shrug)
- [ ] Three context profiles produce visibly different verdicts on the same name
- [ ] Leading words appear in the reasoning trace
- [ ] Blind subagent output resembles the hand-written targets

### Phase 2 — `brand-name-worlds` + `brand-name-generator` `v0.3.0`
Built second because Phase 1 defines what good output looks like, and the generator's
convergence step needs that definition. Built as two skills from the start — the leg-work
split is load-bearing (§5.2).

**Exit criteria:**
- [ ] The world skill terminates **without producing names**. If it leaks names, the split has
      failed and needs stronger steering.
- [ ] Every candidate ships with three sibling names and a usage sentence
- [ ] Subagent QA runs on the shortlist with no generation-session context (§5.5)
- [ ] Running it on three real project ideas produces at least one usable name

### Phase 3 — Factor, audit, prune `v1.0.0`
- [ ] Single source of truth confirmed for every piece of reference material — no duplicated refs
- [ ] Deletion test on every paragraph: would removing this change the output? If no, cut it.
- [ ] Leading-word trace audit across all three skills
- [ ] SKILL.md files all under ~500 words; branch-specific material behind context pointers
- [ ] Troubleshooting and naming-decision logs pruned, with the pruning discipline written down
- [ ] Final reviewer pass against every PRD requirement

---

## 5. Out of scope

Named here so they do not creep in.

- **Not a legal tool.** Trademark risk is flagged heuristically; clearance is an attorney (§2).
- **Not a domain registrar.** No live availability checks in v1 (§2, open question 3).
- **Not a logo/identity tool.** Stops at the name and the vocabulary it implies.
- **Not an oracle.** Argued recommendation, not a verdict.
- **The existing `brand-*` suite retrofit.** PRD §8 Phase 3 calls for extracting the duplicated
  `framework.md` from five existing `brand-*` skills and flipping three of them to
  `disable-model-invocation`. Those skills live in another repo and are not touched here.
  Carried as a follow-up, not a deliverable — see DECISIONS.md ADR-002.
- **`brand-pitch-critic` and `brand-architecture-facilitator`.** Identified as real gaps in §7.1.
  Out of scope for this build; recorded in the README as the natural next modules.

---

## 6. First job for the finished tool

§7.2 leaves two open naming questions, and they are the honest first test of the thing:

1. **The umbrella has no name.** Positioning + naming + content + pitch, collectively — "Lingua"
   is too narrow semantically to cover it.
2. **"Lingua" itself is a weak name** by its own rubric: ergonomically strong, brandability weak
   (descriptive-suggestive Latin for "tongue", dense namespace, low generativity — tongue, Babel,
   Rosetta, grammar, none of which maps onto anything you would build).

So the plugin's first real run is on itself: `/lingua:brand-name-worlds` on the module, then the
generator, then the critic. Whatever replaces it should pass the six-siblings test. The honest
read of "Lingua" from §7.2 is seeded into `shared/naming-decisions-log.md` as entry 001
so that run starts with the prior work already in hand.

Renaming the plugin afterwards is expected. Nothing in the build should make it painful: the
module name appears in `plugin.json`, `marketplace.json`, the README, and the invocation prefix —
and **nowhere in the skill names or the skill bodies**, which is exactly why §7.2 insists Lingua
is the module name and not a skill name.
