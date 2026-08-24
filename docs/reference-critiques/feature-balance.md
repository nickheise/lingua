# Balance

**Profile:** feature / UI · **Candidate for:** the screen in a consumer payments app showing how
much money is available · **Alternative under consideration:** *Spending Power* · **Run:**
hand-written target, Phase 1

**Ergonomics 82 · Brandability: no world, exact fit · Practicality: 1 flag**

Three verdicts. The interesting one is the middle: "no world" is a **failure** under the venture
profile and a **non-issue** under this one. Same rubric, inverted weighting, opposite conclusion.
That inversion is the point of running a profile at all.

---

## Context

Feature profile, which weights **up** spellability, clarity, sibling consistency and international
robustness, and weights **down** distinctiveness and cleverness. Coined names are penalised hard.
Fit with the existing system is a first-class check rather than an afterthought.

The reason for the inversion: **feature naming and product naming are opposite problems.** A
venture name is competing for attention in a market and is allowed to be slightly opaque. A
feature name is competing with *nothing* — the user is already inside the app, already committed,
and every unit of cleverness they have to decode is a unit of trust spent. Apple's own guidance
rejected "Spending Power" in favour of the plain word "Balance" for exactly this reason: inside an
app, clarity and trust beat brand expression. NN/G is emphatic on the same point — command text
should be descriptive, not branded.

**So this critique is going to approve a boring name, and the boringness is the argument, not a
concession.**

---

## Layer 1 — Ergonomics (computed)

<!-- PROVISIONAL: reconcile against real phonetics.py output -->

`python3 scripts/phonetics.py "Balance"`

**Pronunciation:** `B AE1 L AH0 N S` · /ˈbæləns/ · source `cmudict`, confidence **high**.
Dictionary word; nothing here is inferred.

**Structure:** 2 syllables, `CVC · VCC`, stress pattern `10` — trochee, the default strong shape
in English.

| Dimension | Score | Evidence |
|---|---:|---|
| Pronounceability | 94 | 2 syllables; no clusters in onset; no sonority violation; /ns/ a common coda |
| Spellability | 89 | one real trap: the `-ance`/`-ence` alternation; plausible misspellings `balence`, `ballance` |
| Distinctiveness | 52 | neighbourhood density 4 (55th pct: `valance`, `ballads`…); no rare letters |
| Rhythm & recall | 88 | trochaic disyllable — the most reproducible two-syllable shape in English |
| Verbability | 88 | already a verb ("to balance"); agentive "balancer"; 2 syllables |
| International robustness | 82 | /æ/ absent from Spanish, Italian, Japanese (maps to /a/); no `th`, no R–L contrast in-word |

**`ergonomics_score`: 82** — equal-weight mean, profile-independent. The re-weighting below is
prose, not a recomputed number.

**Under the feature profile.**

- **Spellability 89 is the dimension that matters most here, and it is the only one carrying a
  real ding.** `-ance`/`-ence` is among the most-missed spelling patterns in English. In practice
  this costs almost nothing, because a feature label is *read*, not transcribed from hearing —
  the user sees the word before they ever type it, and they rarely type it at all. Note the
  asymmetry: under the venture profile, spellability failures cost you domain typos and word of
  mouth. Under the feature profile they cost you in-app search. In-app search is a smaller
  surface, so an 89 here is comfortable.
- **Distinctiveness 52 is not a weakness under this profile. It is the requirement.** A feature
  name that scored 95 on distinctiveness would be a coined word on a screen where the user needs
  to understand, not to remember. This is the single clearest illustration of why a
  profile-independent composite would be worse than useless: 52 is bad news for a venture and
  good news here, and one number cannot say both.
- **Verbability 88 is largely irrelevant.** Nobody says "let me balance that" about checking an
  account. The profile weights this down and the score can be ignored rather than celebrated.
- **International robustness 82** is the second-most-relevant dimension for a shipped feature,
  and it is fine. See the localisation note in Layer 3 — the risk is not phonetic.

**Compare `Spending Power` on the same measures:** 4 syllables across 2 words, stress `10 · 10`,
and — decisively — it is a *phrase*, not a name. Phrases do not fit in a tab bar, do not survive
localisation at the same length, and cannot be searched for by a user who half-remembers them.
Its distinctiveness would score higher. Under this profile that is a mark against it.

---

## Layer 2 — Brandability (argued)

### Generativity — `breadth × fidelity`

**Position: breadth ≈ 0, fidelity = perfect, and under this profile that product is exactly
right.**

`world, not word` is the governing question for a venture name and a near-irrelevance for a
feature name, because **the feature does not need to generate a world — the parent brand already
did.** A feature name that arrives with its own vocabulary is a feature name competing with its
own product for the user's attention.

Run `six-siblings test` honestly and it fails: balance sheet, equilibrium, scales, counterweight,
offset, ballast. Six words, and not one of them names anything you would build in a payments app.
There is no world here.

Now run **fidelity**, which is the half that decides it: a balance genuinely *is* the amount
remaining after credits and debits. That is the literal, primary, dictionary sense of the word,
in continuous financial use for six centuries. Nothing is being translated. `breadth × fidelity`
with breadth near zero gives a low product — and a low product is the correct answer for a
feature, where the value being sought is not a nomenclature system but a word the user does not
have to think about.

**Contrast with the failure mode.** *Spending Power* has more breadth (it implies a world of
power, capacity, headroom, limits) and worse fidelity, because "spending power" is not a synonym
for "balance" — it is a distinct financial concept involving credit limits, pending
authorisations and purchasing capacity. A user seeing it must decide whether it is the same
number as their balance. That decision is the cost. Breadth without fidelity is the dangerous
failure *because it feels productive*, and it feels productive here too: "Spending Power" sounds
like a naming *win* in a review meeting, right up until someone asks whether it includes pending
transactions.

**Counter-argument:** a plain word forfeits brand expression at a moment of high engagement. The
balance screen is the most-visited surface in a banking app; a distinctive name there would be
seen more often than any advertisement the company will ever buy. That argument is real, and it
is the one Apple's guidance decides against — on the grounds that a financial surface trades in
trust, and trust is built by being unambiguous rather than by being memorable. Accept that
trade-off deliberately, not by default.

### Sibling consistency — the feature-profile-specific check

This check does not exist under the venture profile. Under this one it is close to decisive.

**Existing siblings in the surface:**

| Sibling | Form | Register |
|---|---|---|
| Activity | one word, plain noun | descriptive |
| Payments | one word, plain noun | descriptive |
| Statements | one word, plain noun | descriptive |
| Transfers | one word, plain noun | descriptive |
| Card | one word, plain noun | descriptive |
| **Balance** | one word, plain noun | descriptive |

Balance is indistinguishable from its siblings in form, length, register and grammatical class.
That is a **pass**, and it is the strongest single argument in the critique. *Spending Power*
fails the same check on every column: two words where the others use one, a modifier-plus-noun
compound where the others use a bare noun, and an evaluative register where the others are
neutral. It would be the one label in the set that announces itself.

**The Microsoft Copilot cautionary tale.** Copilot is the compact demonstration of what sibling
consistency is actually protecting. It is a genuinely good name that got attached to roughly
eighty different products, until the National Advertising Division found that customers could not
distinguish the products from one another. The failure was not the name. It was applying one name
across a set of things that were not siblings.

**The check that follows from it, and it runs in both directions:**

1. **Does this name already exist elsewhere in the product?** If yes, does it name the *same
   concept*? Same concept → reuse is consistency and is good. Different concept → this is the
   Copilot failure in miniature and the name must change. *Balance* must mean the same number on
   the account screen, in the widget, and in the notification, or it should not be called Balance
   in all three.
2. **Would this name be reachable for the next four features?** A name that generalises too well
   invites reuse, and reuse without discipline is how eighty Copilots happen. *Balance* is
   pleasantly un-reusable: it names one number and cannot be stretched over a second concept
   without obvious wrongness. That is a virtue here.

A feature-naming process without this check will happily help you build the eighty-Copilot
problem, one locally reasonable decision at a time.

### Cultural familiarity

**Position: cultural commons at maximum strength — weight heavily.** *Balance* is not merely
familiar, it is the term of art the user already holds. Education cost is not low, it is zero, and
below zero relative to any alternative: the user arrives knowing the word *and* knowing what
number it refers to. This is fluency at the semantic level in its purest available form.

No owned-IP exposure. Nobody's franchise, nobody's equity to borrow, no Watkins "Copycat"
deal-breaker in reach.

### Lore integrity — `read the ending`

**Position: clean — and the procedure still runs.**

`read the ending` is a check on names with mythological or literary weight, and it must be run
even when the expected answer is "nothing is down there," because the cost of skipping it is
Palantír. Here the trace goes: Latin *bilanx*, "two-panned"; the scales as an instrument; the
scales of justice; Libra; the weighing of the heart against the feather of Ma'at.

Read those to the end and they end well — or at worst neutrally. Justice, judgement, fair measure.
Nothing lurks. There is no Icarus in this word: no gorgeous surface concealing *flew too close to
the sun and drowned*.

One line of nuance worth recording: the weighing-of-the-heart imagery is *judgement*, and a
payments app is a surface where users already feel judged about their spending. That is an
argument about tone rather than about the name, it is faint, and it does not change the
recommendation. It is here because `read the ending` means reporting what the reading turned up.

### Sound-symbolism fit

**Position: neutral, and neutral is correct.** A trochee with a soft /b/ onset, a lateral, and a
sibilant close reads as settled and unremarkable — no urgency, no aggression, no whimsy. It does
not pull the surface anywhere.

**Evidence strength: weak, and it barely matters.** A tie-breaker and a territory hint, never a
scoring rule. On a feature label the desired phonetic personality is *no personality*, and this
delivers it. Note only that if the app's positioning were built on energy or ambition, "Balance"
would read as slightly sedate — a mismatch worth a sentence in a positioning review, not a naming
objection.

### Ownability — `flag, never block`

**Position: unownable, and that is fine here.**

*Balance* is generic-to-descriptive for a financial feature and cannot be owned as a mark in this
context. Under the venture profile this would be the largest finding in the critique. Under the
feature profile it is close to a non-event: feature labels inside an app are generally not
independently registered, they live under the parent mark, and descriptiveness — the very thing
that destroys ownability — is the property the profile is asking for.

`flag, never block`, in the direction people forget: ownability has no veto, so a zero here cannot
sink a name that the profile says is right. The flag is recorded in Layer 3 and priced at what it
is worth on this surface, which is almost nothing.

**Counter-argument:** if the feature is ever spun out, marketed independently, or made the hook of
a campaign, the name has no protection and no distinctiveness to build on. That is a real
scenario and it is how feature names become product names by accident. Mitigation is structural
rather than linguistic: if that day comes, the *product* gets a name and *Balance* stays as the
label on the screen.

---

## Layer 3 — Practicality (flags)

Facts with severity. **Heuristic screen only — this never gives clearance.** Real clearance is a
trademark attorney.

| Check | Finding | Severity |
|---|---|---|
| **TM distinctiveness tier** | *Generic-to-descriptive* for a financial feature; not registrable as a standalone mark in this class. Correct and intended for a feature label under a parent brand. Tier definitions and worked examples: `${CLAUDE_PLUGIN_ROOT}/shared/name-types.md`. | **high** |
| **Knockout collision** | Not applicable in the usual sense — the word is in ubiquitous use across the entire financial category, which is precisely why nobody can assert it against you either. | low / clear |
| **Domain / handle** | Not applicable. A feature label does not need a domain. If a marketing page is wanted, it lives under the parent domain as a path. | n/a |
| **SEO collision** | Not applicable. Feature labels are found in the app, not in search. In-app search is the relevant surface and the label is the literal query users will type. | n/a |
| **Cross-cultural screen** | No adverse meanings. One **localisation** note, not a naming flag: Spanish uses *saldo* for an account balance, while *balance* in Spanish means a balance sheet or an appraisal. The cognate is a false friend and the localised string must be *saldo*, not a passthrough. Screened against `references/myths-blocklist.md`; no folk naming myth is repeated here as fact. | low |
| **Sibling consistency** | Pass — see Layer 2. Matches Activity / Payments / Statements / Transfers / Card in form, length and register. | clear |

**Headline count = flags at severity `high`: 1.** The single high flag is unownability, and this
profile has already argued that it is the price of the property it wanted.

---

## Recommendation

Not a verdict. An argued recommendation; you decide.

**Ship "Balance." Reject "Spending Power."**

The reasoning, in the order the layers were run:

1. **Ergonomics 82** is comfortable, and the one soft spot — `-ance`/`-ence` spellability — sits
   on a surface where labels are read rather than typed.
2. **Brandability says "no world, exact fit,"** and under this profile that is the target
   outcome, not a shortfall. Perfect fidelity with near-zero breadth is what a feature label
   should look like. *Spending Power* has more breadth, worse fidelity, and introduces a question
   ("is that my balance?") on a screen whose entire job is to answer a question.
3. **Sibling consistency is the decisive check** and *Balance* passes it on every column while
   *Spending Power* fails it on every column. The Copilot precedent says this is the failure mode
   that compounds.
4. **The one high flag — unownability — is the correct price** for a descriptive label under a
   parent mark.

**What is actually being traded away, stated plainly:** brand expression on the app's
highest-traffic surface. That is a genuine loss and it should be an explicit decision rather than
a default. The counterweight is that a financial surface trades in trust before anything else, and
the clearest word is the most trustworthy word.

**What would change this read:**

- If the feature genuinely shows *spending power* — available credit including limits and pending
  authorisations — rather than an account balance, then "Balance" is factually wrong and fidelity
  fails. Fix the name to match the number, or fix the number to match the name. Do not ship the
  ambiguity.
- If the siblings change register — if the surrounding tabs become expressive — then consistency
  argues the other way, and *Balance* becomes the odd one out. Consistency is a check against the
  actual system, not against a preference for plain words.
- If this stops being a feature and becomes a product, re-run under the venture profile. The
  answer will be different, and it should be.
