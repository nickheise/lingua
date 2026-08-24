# Critique output shape

Fill this in. Keep the headings, the order, and the headline form. Worked examples of the finished
article: `docs/reference-critiques/{venture-scout,feature-balance,bad-xzrq}.md`.

---

## The headline — three verdicts, never a composite

```
Ergonomics 89 · Brandability: exceptional world, crowded namespace · Practicality: 2 flags
```

**A number, a clause, a count.** Three different shapes because the three layers have three
different epistemic statuses: a measurement, an argument, and a fact sheet.

**Never average them. Never emit a single overall score, grade, letter, star rating, or
"X/100 overall" anywhere in the critique** — not in the headline, not in a summary line, not in
parentheses at the end. If a reader can extract one number that stands for the name, the critique
has failed at its central job.

**The test case, from PRD §4.1.** Run *Lingua* through this and you get **comfortable,
unoriginal, and it doesn't matter** — three separate verdicts that a composite would have blended
into a meaningless 84. Ergonomically strong; brandability weak (descriptive-suggestive Latin for
"tongue", dense namespace, low generativity); practicality irrelevant because it is a personal
toolkit. Those three findings point in three directions and all three are actionable. The 84 is
not.

| Slot | Form | Source |
|---|---|---|
| Ergonomics | `Ergonomics <n>` — the script's `ergonomics_score`, unmodified | Layer 1 |
| Brandability | a short clause, usually two properties in tension | Layer 2 |
| Practicality | `<n> flags` — the count of **`high`**-severity findings only | Layer 3 |

Good brandability clauses: *exceptional world, crowded namespace* · *no world, exact fit* ·
*no world, no reader* · *strong lore, wrong ending*. Bad ones: *good* · *7/10* · *B+*.

---

## Skeleton

````markdown
# <Name>

**Profile:** <venture / product | feature / UI | internal codename> · **Candidate for:** <one line
on what it would name> · **<Any alternative under consideration>**

**Ergonomics <n> · Brandability: <clause> · Practicality: <n> flags**

<One short paragraph: what the three verdicts say, and where they disagree. The disagreement is
usually the finding. Do not reconcile them into an overall impression.>

---

## Context

<Which profile is running and why. What it weights up, what it weights down, its special rule.
One paragraph. If the profile choice was inferred rather than stated, say so — and say what would
change if it were wrong.>

---

## Layer 1 — Ergonomics (computed)

<!-- PROVISIONAL: reconcile against real phonetics.py output -->
<!-- Delete the line above once the numbers come from an actual run. -->

`python3 ${CLAUDE_SKILL_DIR}/scripts/phonetics.py "<Name>"`

**Pronunciation:** `<ARPABET>` · /<IPA>/ · source `<cmudict|cmudict-compound|g2p>`,
confidence **<high|medium|low>**.

<If confidence is low, a visible caveat block BEFORE the table: the name is not in the dictionary,
the transcription is an estimate, and every score below inherits that uncertainty. Quote the
script's `warnings`. Never present an estimate as a measurement.>

**Structure:** <n> syllables, `<CVC · VCC>`, stress pattern `<10>` — <shape>.
<Include phonotactics and orthography lines only when they carry a finding.>

| Dimension | Score | Evidence |
|---|---:|---|
| Pronounceability | <n> | <verbatim from `dimensions.pronounceability.evidence`> |
| Spellability | <n> | <verbatim> |
| Distinctiveness | <n> | <verbatim> |
| Rhythm & recall | <n> | <verbatim> |
| Verbability | <n> | <verbatim> |
| International robustness | <n> | <verbatim> |

**`ergonomics_score`: <n>** — the equal-weight mean, profile-independent. <Say that re-weighting
is done in prose below and not by recomputing the number.>

**Under the <profile> profile.** <Two or three sentences or bullets. Take the dimensions this
profile weights highest and say what the score costs or buys, concretely. Say explicitly where a
low score does not matter — or is the requirement. Lead with any floor breach (01-ergonomics §3)
regardless of the mean.>

---

## Layer 2 — Brandability (argued)

<One line: position plus strongest counter-argument for each; no scores, because a number here
would be false precision.>

### Generativity — `breadth × fidelity`

**Position: <…>** — `world, not word`.

**`six-siblings test`:**

| Sibling | What it names in the product | Icon already drawn? |
|---|---|---|
| … | … | … |

**Fidelity.** <For each sibling: was the mapping already true, or did it need justifying?>

**Find the breaking point.** <Error state · permissions · empty state · billing. Say which surface
breaks and whether it is a seam (peripheral) or a hole (core).>

**Keep the metaphor off the buttons.** <Which terms are concepts and which would be UI labels.>

**Counter-argument:** <the one you would least like to answer>

### Cultural familiarity

**Position: <cultural commons — weight heavily | owned IP — flag as a risk requiring
justification>.** <…>

**Counter-argument:** <…>

### Lore integrity — `read the ending`

**Position: <…>** <Referent · the full story · how it ends, in one sentence · clean, ironic, or
actively damaging · who would notice. Run it even when the answer is "nothing is down there," and
record that as a clean pass.>

**Severity: <low|medium|high>.**

### Sound-symbolism fit

**Position: <…>** <Phonetic personality vs. positioning personality.>

**Evidence strength: <moderate|weak|none>.** <Mandatory. A tie-breaker and territory hint, never a
scoring rule. If `none` — including when the pronunciation itself is uncertain — say the criterion
cannot be assessed and stop. Do not invent a reading.>

### Ownability — `flag, never block`

**Position: <…>** <Competitors for the term, ordered by collision risk: same category and same
buyer first. Convert to a currency — legal exposure, marketing spend, or nothing. Then state the
profile's weighting in the form: for X this is irrelevant; for Y it is the whole conversation.>

**Counter-argument:** <…>

---

## Layer 3 — Practicality (flags)

Facts with severity. **Heuristic screen only — this never gives clearance.** Real clearance is a
trademark attorney.

| Check | Finding | Severity |
|---|---|---|
| **TM distinctiveness tier** | <tier, against these goods/services; point at `${CLAUDE_PLUGIN_ROOT}/shared/name-types.md`, do not restate the taxonomy> | <…> |
| **Knockout collision** | <known users, ordered by risk; "no conflicts known to me; this is not a search"> | <…> |
| **Domain / handle** | <known vs. must-be-verified; realistic fallbacks> | <…> |
| **SEO collision** | <bare term winnable? the compound brand term that is> | <…> |
| **Cross-cultural screen** | <languages screened; adverse meanings; false friends. Screened against `references/myths-blocklist.md`; no folk naming myth repeated as fact> | <…> |
| <profile-specific row> | <sibling consistency / leak check> | <…> |

**Headline count = flags at severity `high`: <n>.** <Medium, low, clear and n/a are listed but not
counted.>

---

## Recommendation

Not a verdict. An argued recommendation; you decide.

**<The recommendation in one line — and it is allowed to be conditional on something the user
knows and you do not.>**

<Two to four numbered points carrying the reasoning, in the order the layers were run. Where the
layers disagree, say which one should dominate here and why — do not split the difference.>

**What would change this read:** <the specific new facts that would flip it — a clean knockout
search, a different positioning, a change of profile. Be concrete enough to be actionable.>
````

---

## Rules the template enforces

1. **Three verdicts in the headline. No composite anywhere.** No overall score, grade, or rating.
2. **Layer 1 numbers come from the script**, quoted with their evidence strings. Re-weighting is
   prose. Never recompute the score for a profile.
3. **Layer 2 has no numbers.** Every criterion gets a position *and* its strongest
   counter-argument — including the criteria that pass easily.
4. **Layer 3 has no opinions**, carries a severity on every row including `clear` and `n/a`, and
   states that it never gives clearance.
5. **Leading words verbatim**, never paraphrased: `world, not word`, `breadth × fidelity`,
   `six-siblings test`, `rare letters, common sounds`, `read the ending`, `flag, never block`.
6. **Ends in an argued recommendation with a "what would change this read."** Never a verdict.
7. **Length follows the case.** A clean name is short. A name whose layers disagree earns the
   space. Never pad a section to fill the shape — an empty finding is written as one line.
