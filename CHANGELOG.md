# Changelog

All notable changes to Lingua are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Each minor version
corresponds to a build phase in [`docs/BUILD-MAP.md`](docs/BUILD-MAP.md); every phase has exit
criteria that must be met before the next begins.

## [Unreleased]

### Planned
- **Phase 1 → `0.2.0`** — `brand-name-critic`: the three-layer rubric, `phonetics.py`, the three
  context profiles, the debunked-myths blocklist, the critique template.
- **Phase 2 → `0.3.0`** — `brand-name-worlds` and `brand-name-generator`, built as two skills from
  the start because the leg-work split is load-bearing.
- **Phase 3 → `1.0.0`** — factor, audit, and prune: single source of truth for every reference,
  the deletion test on every paragraph, and a leading-word trace audit across all three skills.

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

[Unreleased]: https://github.com/nickheise/lingua/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/nickheise/lingua/releases/tag/v0.1.0
