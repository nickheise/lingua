# Shortlist — *(fill in)*

Fill this in per run. A field left as *(fill in)* is a visible gap, not a silent omission — the
point of writing placeholders instead of blank cells is that a skipped step is obvious on read.

---

## World

**World:** *(fill in — the chosen world's name, from `brand-name-worlds`)*
**Source brief:** *(one line — what the world skill was run on, and when)*
**Context profile:** *(venture / product | feature / UI | internal codename)*
**Fidelity evidence carried over:** *(fill in — quote the `breadth × fidelity` read from the
worlds output; do not re-derive it here)*

---

## Operator coverage — Step 1 (diverge)

A blank **Generated** cell means that operator was not worked. That is a finding, not a rounding
error — see `references/troubleshooting.md`.

| Operator | Quota | Generated | Notes |
|---|---:|---:|---|
| Compound | 15 | *(fill in)* | |
| Blend (splice search) | 15 | *(fill in)* | |
| Affix | 10 | *(fill in)* | |
| Clip | 8 | *(fill in)* | |
| Respell | 8 | *(fill in)* | |
| Foreign-source | 8 | *(fill in)* | |
| Phoneme coinage | 10 | *(fill in)* | |
| Shortest-synonym (Synomin pattern) | 8 | *(fill in)* | |
| Acronym / initialism | 6 | *(fill in)* | |
| **Total** | **88** | *(sum)* | Target range 80–100 |

---

## Clusters — Step 2

| Cluster | Definition | Candidates sorted here |
|---|---|---|
| Direct | Literal world vocabulary, as-is or barely touched | *(fill in)* |
| Oblique | Peripheral world vocabulary, one inferential step out | *(fill in)* |
| Coined-from-root | Blend / affix / clip / respell on a world root | *(fill in)* |
| Compound | Two whole words concatenated | *(fill in)* |

---

## Shortlist — Step 3 (converge)

One block per surfaced candidate (~12 total, spread across clusters). All five fields are
required. `references/02-converge.md` defines each one; the sibling-name gate is a **hard gate**
— a candidate without three real siblings should not appear here at all (see the discard log
below instead).

### *(Candidate name)*

| Field | Value |
|---|---|
| Cluster | *(fill in)* |
| Type classification | *(fill in — `shared/name-types.md` axis 1)* |
| TM distinctiveness tier | *(fill in — `shared/name-types.md` axis 2; heuristic, not clearance)* |
| Rationale | *(fill in — one line)* |
| Sibling 1 | *(fill in)* |
| Sibling 2 | *(fill in)* |
| Sibling 3 | *(fill in)* |
| Usage sentence | *(fill in — a realistic sentence, not a tagline)* |

**Blind critic read (Step 4):** *(fill in after the subagent returns — leave as "pending" until
then, never fabricated)*

> Ergonomics *(n)* · Brandability: *(clause)* · Practicality: *(n)* flags
>
> *(paste the returned critique's headline, then either the full critique text or a pointer to
> where it's filed)*

<!-- Repeat the "### (Candidate name)" block above for each surfaced candidate. -->

---

## Discarded at the sibling gate

Evidence the gate actually ran, not overhead — every candidate that reached Step 3 and then
failed here, and why.

| Candidate | Cluster | Failure mode | What was tried |
|---|---|---|---|
| *(fill in)* | *(fill in)* | too few / weak siblings | *(fill in — the siblings that didn't hold up)* |

*(Leave this table with a single "— none —" row if nothing was discarded; an empty table with no
row at all reads the same as "not run," which is the ambiguity this section exists to avoid.)*

---

## Blind QA record — Step 4

**Exact prompt sent to the subagent:**

```
(paste verbatim — must contain only the alphabetized candidate names and the context profile)
```

**Context withheld (confirm each, don't skip the confirmation):**

- [ ] World name and rationale
- [ ] Operator that produced each candidate
- [ ] Cluster assignment
- [ ] Generation order / any note of a favorite
- [ ] This skill's own sibling names and usage sentences

**Subagent identity / run reference:** *(fill in, if the harness exposes one, for auditability)*
