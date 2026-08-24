# Changelog

All notable changes to Lingua are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Each minor version
corresponds to a build phase in [`docs/BUILD-MAP.md`](docs/BUILD-MAP.md); every phase has exit
criteria that must be met before the next begins.

## [Unreleased]

### Planned
- **Phase 3 → `1.0.0`** — factor, audit, and prune: single source of truth for every reference,
  the deletion test on every paragraph, and a leading-word trace audit across all three skills.

## [0.3.0] — 2026-08-24

Phase 2. Both maker skills, built as two skills from the start because the leg-work split is
load-bearing and retrofitting it would mean rewriting both.

### Added
- **`brand-name-worlds`** — user-invoked, 471-word SKILL.md, four steps. Turns a brief into 2–3
  stress-tested semantic worlds and **terminates before any names exist.**
  - `references/01-brief.md` — the four-question mini-brief, plus the positioning-canvas mapping.
    Canvas present, use it silently; canvas absent, ask four questions and proceed. Demanding a
    canvas would make the skill useless at idea stage, which is when naming actually happens.
  - `references/02-world-sourcing.md` — answers PRD open question 4 the way the PRD leans: a fixed
    16-domain catalogue plus a mandatory "propose one not on this list" step. Each domain carries
    its vocabulary, what it maps onto, what it is bad at, and whether its imagery is already
    drawn. Gardening is included and flagged as a charm trap, since it is the PRD's own worked
    failure case.
  - `references/03-fidelity-test.md` — `breadth × fidelity`, with the three-of-five shrug
    threshold made mechanical and non-negotiable, and the breaking-point probes separated into
    core versus peripheral failures.
- **`brand-name-generator`** — user-invoked, 483-word SKILL.md, `diverge → cluster → converge`
  plus blind QA.
  - `references/01-operators.md` — nine construction operators worked inside a single cartography
    world so they are comparable, with a quota table that turns "80–100 candidates" into operator
    coverage rather than free-association.
  - `references/02-converge.md` — the three-sibling requirement as a **hard gate**, with weak
    siblings counted as an equal failure to too-few. The `six-siblings test` is only worth running
    if a shrug counts as a miss.
  - Blind subagent QA (§5.5) written as an **allow-list** — exactly two things reach the critic,
    the candidate names alphabetized and the context profile. The world, operator trail, clusters,
    rationales, siblings, and usage sentences are all withheld. An allow-list rather than a list
    of things to omit, because "remember to leave this out" is what a rushed run skips.

### Decided
- Keeping the critic **blind to the world** (PRD open question 5) is deliberate. A critic that
  knew the world could judge fidelity better, but that would destroy the fresh-context property
  the QA step exists to buy.

## [0.2.0] — 2026-08-24

Phase 1. `brand-name-critic`, built by reverse-engineering: the ideal outputs were written by
hand first, then the skill was built to produce them.

### Added
- **`brand-name-critic`** — model-invoked (critique should fire when a name gets floated
  mid-conversation), 402-word SKILL.md with negative triggers so it does not fire on variable or
  branch names. Four steps plus an unnumbered close-out.
- **`scripts/phonetics.py`** — 1,831 lines, standard library only, no network, no clock, no
  randomness. Ships a vendored 112,631-entry lexicon derived from CMUdict (750KB) built by a
  reproducible, byte-stable generator. 80 tests; the 20-name benchmark is byte-identical across
  runs. Handles syllabification by Maximal Onset Principle, sonority sequencing with the licensed
  /s/+stop exception, one-edit phonetic neighbourhood density, and a rule-based g2p fallback.
- **The three layer references** — `01-ergonomics.md` interprets the script's JSON rather than
  re-deriving phonetics; `02-brandability.md` requires a position *and its strongest
  counter-argument* for each of five criteria; `03-practicality.md` routes trademark tiers to
  `shared/name-types.md` and cross-cultural screening to the myths blocklist.
- **Three context profiles** with explicit numeric multipliers across all eleven criteria, each
  reaching a visibly different verdict on the same worked example.
- **`myths-blocklist.md`** — researched rather than recalled. Five stories commonly repeated as
  fact are blocked, seven are verified with caveats, and three are marked unverified rather than
  quietly dropped.
- **`docs/reference-critiques/`** — three hand-written build targets (a strong venture name, a
  feature name, a deliberately bad name), reconciled against real script output.

### Answered
- **PRD open question 2** — the g2p fallback measures **32.8% exact phoneme match / 79.4%
  per-phoneme** on a seeded held-out sample of 2,500 words, rising to 46.9% exact in the
  short-name range where brand names live. The pipeline is deterministic; the transcription of an
  unknown word is an estimate. The JSON distinguishes them via `source`, `confidence`, and
  `warnings`, and the skill must say "estimate" rather than "measurement" when confidence is low.
  Eleven of the twenty benchmark names never touch g2p. See ADR-013.

### Fixed
- `01-ergonomics.md` keyed on a `syllables.count: 0` signal the script never emits. A vowel-less
  name returns count 1 with an all-consonant structure and `stress.shape: "no vowel nucleus"`.
- Reconciling the hand-written targets against real output exposed fabricated evidence in them —
  an invented spelling-ambiguity story for Scout, a wrong cause for Balance's spellability cost,
  and invented `warnings` text for Xzrq. All corrected against what the script actually returns.

### Decided
- **ADR-008** — the script's number is authoritative; the PRD's illustrative `Ergonomics 89` for
  Scout is superseded by the measured 85.
- **ADR-009** — "N flags" in the headline counts high-severity findings only.
- **ADR-010** — `rare letters, common sounds` does not separate Xerox from Xzrq as written, since
  Xzrq's letters also map to common sounds. The principle has a second, implicit half: those
  sounds must assemble into **legal syllables**. Made explicit.
- **ADR-011** — layer 1 measures phonetic neighbourhood density and cannot know a name is already
  taken, so it will disagree with layer 3 about distinctiveness. The critique explains the
  disagreement rather than averaging it.
- **ADR-014** — never lead with `ergonomics_score` on a broken name. Blorbnth averages to 72 while
  being unpronounceable, because it is genuinely easy to spell and genuinely distinctive. That is
  the kill-the-composite argument reappearing one layer down, fixed by presentation rather than by
  re-weighting.

## [0.1.0] — 2026-08-24

Repository foundation. No skills yet; this release is the plan and the scaffolding it will be
built into.

### Added
- `.claude-plugin/plugin.json` — plugin manifest (`lingua`, MIT, semver-pinned).
- `.claude-plugin/marketplace.json` — single-plugin marketplace entry with `source: "./"`, so the
  repo is installable directly via `/plugin marketplace add nickheise/lingua`.
- `README.md` — what the plugin is, the five leading-word principles, the three skills, the
  three-layer evaluation model, the context profiles, install instructions, and the roadmap gaps.
- `docs/PRD.md` — the source specification, checked in verbatim as the build's input.
- `docs/BUILD-MAP.md` — the plan of record: complete file inventory with per-file ownership and
  status, the leading-word steering vocabulary and where each phrase must appear, the phase
  sequence with exit criteria, and an explicit out-of-scope list.
- `docs/DECISIONS.md` — the engineering ADR log.
- `CHANGELOG.md` — this file.
- `LICENSE` — MIT.
- Directory skeleton for all three skills plus `shared/`.

### Decided
- **The `phonetics.py` JSON contract is specified up front**, in the build map, rather than
  emerging from the implementation. It is the interface between the deterministic layer and the
  reasoning layer, so pinning it lets the script and the rubric be built in parallel instead of
  in sequence. See ADR-004.
- **Shared reference material lives in `shared/` at the plugin root, not `skills/_shared/`.**
  Loader behaviour for a `skills/` subdirectory lacking a `SKILL.md` is not documented, and a
  single source of truth is the requirement either way. See ADR-003.
- **The shared reference files are built in Phase 1 rather than extracted in Phase 3.** The PRD's
  warning against factoring early is aimed at retrofitting an existing suite, where the real
  overlap is not yet visible. This is a greenfield build and the overlap is already named in the
  specification. See ADR-005.
- **The PRD's `decisions.md` is renamed `shared/naming-decisions-log.md`** to stop it colliding
  with the engineering ADR log at `docs/DECISIONS.md`. They are different artifacts with
  different lifecycles. See ADR-006.
- **The existing `brand-*` suite retrofit is out of scope.** PRD §8 Phase 3 calls for de-duplicating
  `framework.md` across five existing skills and flipping three of them to
  `disable-model-invocation`. Those skills live in another repository. See ADR-002.

[Unreleased]: https://github.com/nickheise/lingua/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/nickheise/lingua/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/nickheise/lingua/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/nickheise/lingua/releases/tag/v0.1.0
