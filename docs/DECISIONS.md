# Decision Log

Engineering decisions made while building Lingua, in the order they were made. Each entry records
what was decided, what the alternatives were, and why one won — so the progression is legible
later and so a decision can be *revisited* rather than silently re-litigated.

**Scope note.** This is the *engineering* log for building the plugin. The *naming* log from
PRD §5.6 — names proposed, chosen, rejected, and why — is a separate, longer-lived artifact at
[`shared/naming-decisions-log.md`](../shared/naming-decisions-log.md). See ADR-006.

Status values: `accepted` · `superseded by ADR-NNN` · `revisited`

---

## ADR-001 — Ship as a Claude Code plugin, not a bare skills directory

**Date:** 2026-08-24 · **Status:** accepted · **Phase:** 0

**Context.** The PRD (§5.3) draws Lingua as a folder of skill directories. The repository it is
being built into is empty, so the packaging is an open choice: a loose `skills/` tree the user
copies into `~/.claude/skills/`, or a proper plugin.

**Decision.** Ship as a plugin: `.claude-plugin/plugin.json` plus a `.claude-plugin/marketplace.json`
with `source: "./"`, making the repository itself installable with
`/plugin marketplace add nickheise/lingua`.

**Why.**
- Versioning becomes real. The PRD's phase sequence has exit criteria per phase; semver plus a
  changelog makes "which phase is this" answerable from the artifact rather than from memory.
- Namespaced invocation (`/lingua:brand-name-worlds`) matches §7.2's insistence that *Lingua* is
  the module name and the skill names are boring on purpose. The prefix carries the module
  identity so the skill names do not have to.
- Bundled scripts get portable paths via `${CLAUDE_PLUGIN_ROOT}` and `${CLAUDE_SKILL_DIR}`, which
  is what makes `phonetics.py` and its vendored lexicon work from any working directory.
- `claude plugin validate` gives us a schema check we can run in CI.

**Cost.** One more layer of manifest to keep in sync with the version in the changelog.

---

## ADR-002 — The existing `brand-*` suite retrofit is out of scope

**Date:** 2026-08-24 · **Status:** accepted · **Phase:** 0

**Context.** PRD §5.1 and §8 Phase 3 call for auditing five existing `brand-*` skills:
de-duplicating a `references/framework.md` copied across all five, and flipping
`brand-positioning-facilitator`, `brand-pitch-builder`, and `brand-content-writer` to
`disable-model-invocation: true`.

**Decision.** Do not touch them. Record the work as a follow-up in the build map's out-of-scope
section and in the README's roadmap.

**Why.** Those skills are not in this repository, and this session's access is scoped to
`nickheise/lingua`. Speculatively writing files for a suite whose actual contents we cannot read
would produce plausible-looking guesses, which is worse than an honest gap.

**Consequence.** The context-tax arithmetic in §5.1 — five model-invokable descriptions dropping
to three — does not happen as part of this build. Lingua contributes exactly one model-invokable
description (`brand-name-critic`) and two user-invoked skills that cost nothing standing.

---

## ADR-003 — Shared material lives in `shared/`, not `skills/_shared/`

**Date:** 2026-08-24 · **Status:** accepted · **Phase:** 0

**Context.** PRD §5.3 places `_shared/` as a sibling of the skill directories, and PRD open
question 1 asks whether cross-skill references resolve at all or whether a stamping script is
needed. In plugin layout the skills live under `skills/`, so the literal translation would be
`skills/_shared/` — a directory under `skills/` with no `SKILL.md` in it.

**Decision.** Put shared reference files in `shared/` at the **plugin root**, one level up from
`skills/`. Skills reach them by `${CLAUDE_PLUGIN_ROOT}/shared/<file>.md`.

**Why.** Whether the plugin loader silently skips a `skills/` subdirectory lacking a `SKILL.md`,
warns, or errors is not documented, and we would rather not depend on undocumented behaviour for
something this structural. Moving one level up removes the question entirely. It is also closer
to the PRD's own drawing, where `_shared/` sits beside the skills rather than inside a container
with them.

**This answers PRD open question 1: no stamping script is needed.** A plugin is a real directory
on disk and `${CLAUDE_PLUGIN_ROOT}` resolves to its install path, so a single source of truth is
directly referenceable from every skill. The fallback in §5.3 — a generation script that stamps
the shared file into each skill — is not required and should not be built.

---

## ADR-004 — Pin the `phonetics.py` JSON contract before writing either side

**Date:** 2026-08-24 · **Status:** accepted · **Phase:** 0

**Context.** The deterministic layer (§4.2) produces numbers; the ergonomics reference interprets
them. Built in sequence, the rubric author waits on the script author for a full phase.

**Decision.** Specify the complete output schema in the build map first — every key, its type,
and the five rules it enforces — and have both sides build against it in parallel.

**Why.** It is the one genuine interface in the system, and it is small enough to specify fully
in advance. The rules that matter are architectural, not implementation detail:
`ergonomics_score` is profile-independent (re-weighting is the skill's job, not the script's);
the script never emits a cross-layer composite, because killing the composite is the point of
§4.1; and a coined name outside the dictionary still returns every key, with low confidence and a
warning, rather than failing or silently guessing.

**Cost.** If implementation reveals the schema is wrong, both sides change and so does the build
map. Accepted — the schema is small and the parallelism saves more than a revision would cost.

---

## ADR-005 — Build `shared/` in Phase 1 instead of extracting it in Phase 3

**Date:** 2026-08-24 · **Status:** accepted · **Phase:** 0

**Context.** PRD §8 Phase 3 says to extract `name-types.md` and `example-bank.md` only once both
skills exist and their real overlap is visible, because "factoring shared references before that
is guessing."

**Decision.** Create `shared/` in Phase 1, before the skills that consume it.

**Why.** The warning is aimed at a retrofit, where you are inferring overlap from code you did
not plan. Here the overlap is not inferred — the PRD names both files and both consumers
explicitly, and §5.3 states that a single source of truth is the requirement either way. Building
duplicates in order to de-duplicate them two phases later would manufacture the exact sediment
the pruning discipline exists to prevent, and would cost a full rewrite of both copies.

**What we keep from the original intent.** Phase 3 still runs the audit — confirm single source of
truth for every piece of reference material, and check that nothing has quietly re-duplicated.
The check survives; only the deliberate duplication is dropped.

---

## ADR-006 — Rename the PRD's `decisions.md` to `shared/naming-decisions-log.md`

**Date:** 2026-08-24 · **Status:** accepted · **Phase:** 0

**Context.** PRD §5.6 specifies a `decisions.md` that accumulates naming taste — names proposed,
chosen, rejected, and why. This build also needs an engineering decision log, conventionally
`DECISIONS.md`. Two files with the same name and completely different jobs is a trap.

**Decision.** Engineering ADRs live at `docs/DECISIONS.md`. The naming log lives at
`shared/naming-decisions-log.md`.

**Why.** They have different lifecycles. The ADR log is append-only and closes when the build
does. The naming log is pruned deliberately at every phase boundary (§5.6's own mitigation
against sediment) and is the more valuable of the two long-term — it is the one input no amount
of research supplies.

**Also decided:** the naming log ships **seeded, not empty.** §7.2 already contains a full honest
critique of "Lingua" run through the rubric. That becomes entry 001, so the plugin's first real
job — naming itself and its unnamed parent — starts with the prior work in hand instead of from
a blank page.

---

## ADR-007 — Orchestrate with a lead agent plus specialists, not a separate orchestrator agent

**Date:** 2026-08-24 · **Status:** accepted · **Phase:** 0

**Context.** The build is parallelisable: the phonetics engine, the rubric, the profile files, and
the shared references have no read/write overlap. The brief asked for a dedicated orchestrator, a
reviewer, and several builders.

**Decision.** The lead session acts as orchestrator directly. Below it: specialist builders
running in parallel per phase, and one dedicated reviewer that never writes the code it reviews.

**Why.** A spawned orchestrator would start cold and re-derive the PRD, the build map, and the
JSON contract that the lead session already holds — paying full context cost for a layer that
only forwards instructions. The brief also asked to keep cost and tokens reasonable, and those
two asks point in opposite directions here.

**Model assignment, and the reasoning behind it.**

| Role | Model | Why |
|---|---|---|
| Lead / orchestrator | Opus | Holds the PRD, the contract, and the sequencing |
| Phonetics engineer | Opus | Hardest technical piece: phonotactics, syllabification, g2p fallback, measured error rate |
| Rubric author | Opus | The core IP. Argued judgment with counter-arguments is exactly the work that degrades on a smaller model |
| Reviewer | Opus | Adversarial reading against exit criteria; must catch what the builders rationalised |
| Profiles / blocklist / templates | Sonnet | Structured writing against a fully specified brief |
| Shared references | Sonnet | Taxonomy and example bank — recall and organisation, not novel judgment |
| Worlds / generator authors | Sonnet | Procedure writing against a rubric Phase 1 has already pinned down |

**The reviewer never writes.** §5.5 makes this argument for the naming skills — an agent
evaluating work it just produced sees fewer flaws in it, because it holds the reasons it made
each choice. The same applies to building the plugin, so the property is enforced structurally
here too, not just inside the generator.
