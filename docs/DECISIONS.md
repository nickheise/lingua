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

---

## ADR-008 — The script's number for Scout is authoritative; the PRD's `89` is an illustration

**Date:** 2026-08-24 · **Status:** accepted · **Phase:** 1

**Context.** PRD §4.1 shows `Ergonomics 89` for Scout. The pinned contract in BUILD-MAP §3 carries
a worked Scout example whose six dimension scores average to 85. The rubric author noticed the
discrepancy while writing the target critique and, correctly, did not quietly pick one.

**Decision.** Neither hand-written number is authoritative. `phonetics.py` is. Once the script
lands, its actual output for Scout is patched into `docs/reference-critiques/venture-scout.md`,
into the contract example, and into `assets/critique-template.md`.

**Why.** The entire argument for scoring Layer 1 at all (§4.2) is that syllable count, cluster
legality, stress, and neighbourhood density are things a script gets right every time and a
model estimates inconsistently. A hand-written ergonomics score is precisely the inconsistent
estimate that design exists to eliminate. Treating the PRD's `89` as a target to hit would invert
the point.

**Consequence.** The PRD's `89` stays in `docs/PRD.md` — it is checked in verbatim as the input
to this build and is not edited after the fact. This ADR is the record that it was an
illustration, not a specification.

---

## ADR-009 — "N flags" in the headline counts high-severity findings only

**Date:** 2026-08-24 · **Status:** accepted · **Phase:** 1

**Context.** The PRD's headline format is `Ergonomics 89 · Brandability: … · Practicality: 2
flags`, but nothing in it defines what counts as a flag. Practicality covers trademark tier,
knockout collisions, domain and handle reality, SEO collision, and cross-cultural screening — so
the same critique could honestly report 2 or 6 depending on whether medium and low findings and
clean checks are counted.

**Decision.** The headline count is **high-severity findings only**. Medium, low, clear, and
not-applicable results all appear in the practicality table but are not counted in the headline.

**Why.** An uncounted convention is a number that drifts, and a drifting number in the headline
undermines the one layer that is supposed to be factual. Counting only high severity also keeps
the headline honest under `flag, never block` — the count communicates "how much should worry
you," not "how many boxes were ticked."

**Provenance.** This rule is not in the PRD. It was invented during the build to close a real
gap, and it is recorded here rather than buried in a reference file so it can be revisited.

---

## ADR-010 — `rare letters, common sounds` has a second, implicit half: legal arrangement

**Date:** 2026-08-24 · **Status:** accepted · **Phase:** 1

**Context.** PRD §3.3 argues that Xerox works and Xzrq does not, because the first maps a rare
*letter* onto a common *sound*. Taken literally, the rule does not actually separate them: Xzrq's
letters also map to common sounds — x→/z/, z→/z/, q→/k/ are all ordinary English phonemes. The
principle as written cannot express what is wrong with Xzrq, and the contract's single nullable
boolean inherits that gap.

**Decision.** The principle has a second half that §3.3 leaves implicit and the plugin makes
explicit: the common sounds must also be **assembled into legal syllables.** Xzrq fails on
arrangement, not on mapping — no vowel, an onset English does not license. `rare_letter_common_sound`
returns `false` for a name that fails either half, and `01-ergonomics.md` states both halves.

**Why.** This strengthens the principle rather than patching around it. It is also what makes the
rule do real work: without the second half, "rare letters, common sounds" would endorse any
unpronounceable consonant pile built from ordinary phonemes, which is the exact failure the
principle was introduced to explain.

**Consequence.** The contract comment in BUILD-MAP §3 is updated so the script author and the
rubric author read the boolean the same way.

---

## ADR-011 — Layer 1 and Layer 3 may disagree about distinctiveness, and the critique explains the disagreement rather than averaging it

**Date:** 2026-08-24 · **Status:** accepted · **Phase:** 1

**Context.** PRD §4.2 lists distinctiveness as a computed ergonomics dimension. But the script can
only measure *phonetic neighbourhood density* — how many real words sit one phoneme away. It
cannot know that "Scout" is a common English word already used by Scout Motors, Scout24, Scout
APM, and the scouting movement. So Layer 1 and Layer 3 will routinely return different readings
of how distinctive the same name is.

**Decision.** Do not reconcile them numerically. `01-ergonomics.md` states the limitation at the
point of use; `02-brandability.md` adjudicates the tension by explaining it. The critique reports
both readings and says why they differ.

**Why.** The disagreement is information, not noise — it is the difference between "this name is
easy to tell apart when spoken" and "this name is already taken." Averaging them would produce a
number that answers neither question, which is the composite-score failure of §4.1 reappearing
one layer down.

---

## ADR-012 — Report the PRD's citations as the PRD reports them; never invent a source

**Date:** 2026-08-24 · **Status:** accepted · **Phase:** 1

**Context.** PRD §4.5 attributes the choice of "Balance" over "Spending Power" to "Apple's own
guidance." The primary source could not be verified during the build.

**Decision.** Report it exactly as the PRD reports it. Do not invent a document title, a URL, or a
date to make the citation look solid.

**Why.** This is the same standard the myths blocklist imposes on the plugin's own output: never
present an unverified claim as established fact, and prefer saying "uncertain" to manufacturing
confidence. A build that violated that rule while shipping a reference file about it would be
incoherent. The blocklist's three-way split — debunked, verified, unverified — exists precisely
so an unconfirmed claim has an honest place to live.
