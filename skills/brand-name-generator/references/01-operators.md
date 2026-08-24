# Construction operators

The mechanism for Step 1. **80–100 candidates means working this list to quota, not
free-associating until tired.** Nine operators, worked below inside one consistent world
(cartography) so they're comparable. Swap in the chosen world's own vocabulary when actually
running the step — these examples are the pattern, not the output.

Each operator's *output type* is classified by `${CLAUDE_PLUGIN_ROOT}/shared/name-types.md` —
that file owns the construction→type mapping and is not restated here. This file drives
production; that one classifies what came out.

---

## The quota (Pass 1)

Generate to the number per operator before judging anything. Don't self-censor for quality here
— that's Step 2 and Step 3's job.

| Operator | Quota |
|---|---:|
| Compound | 15 |
| Blend (splice search) | 15 |
| Affix | 10 |
| Clip | 8 |
| Respell | 8 |
| Foreign-source | 8 |
| Phoneme coinage | 10 |
| Shortest-synonym (Synomin pattern) | 8 |
| Acronym / initialism | 6 |
| **Total** | **88** |

**Pass 2 — one quick prune, nothing more.** Drop anything phonotactically illegal (no legal
vowel nucleus, an onset English doesn't license) or an exact collision with a famous name in an
adjacent category. That is the entire Pass 2. Do not cluster, rank, or apply the sibling test
here — that's Step 2 and Step 3. Trademark and domain screening is the critic's job in Step 4, not
this skill's.

---

## The operators

### Compound
**Definition.** Two whole words concatenated — a world term plus a plain word, or two world
terms.
**Worked example.** "way" + "mark" → **Waymark**.
**Produces.** Descriptive-to-suggestive, per `shared/name-types.md`'s compound row.

### Blend, with splice search
**Definition.** A portmanteau of two words — but the splice point is **searched systematically**,
not guessed once. Enumerate every plausible split of each word, cross them, and evaluate the
results against phonotactic legality before picking a winner.
**Worked example.** "chart" × "orient" — splice candidates: `ch-orient`, `char-orient`,
`chart-orient`, `cha-rient`. The last resolves to a legal CV-heavy string a four-year-old could
say: **Charient**. The others are unpronounceable or just look like the two source words taped
together. The method is the deliverable here, not the specific winner — run the same grid on the
world's own vocabulary.
**Produces.** Coined-from-root, usually suggestive-to-arbitrary depending how legible the roots
stay.

### Affix
**Definition.** A real prefix or suffix on a world root.
**Worked example.** "chart" + "-ify" → **Chartify**. Same pattern as Shopify (shop + -ify) in
`shared/example-bank.md` — the root stays fully legible, so this lands suggestive rather than
drifting to coined-from-root the way Spotify's "spot" partially does.
**Produces.** Suggestive-to-coined-from-root depending on root legibility (see
`shared/name-types.md`'s affix row for the split).

### Clip
**Definition.** Truncate a longer world term.
**Worked example.** "cartography" clipped → **Carto**.
**Produces.** Ranges descriptive → arbitrary depending on what stays recognizable; "Carto" reads
suggestive because the root is still obvious.

### Respell
**Definition.** Deviate from the correct spelling of a real world-vocabulary word past
straightforward correction.
**Worked example.** "compass" → **Kompaz** — C→K and S→Z both swap an ordinary letter for a rare
one on the *same* common sound (/k/, /z/), the exact `rare letters, common sounds` move.
**Cost.** Buys distinctiveness, costs spellability — a reader who's only heard it said now has to
guess between the real spelling and this one.
**Produces.** Fanciful if the respell breaks recognizability, coined-from-root if the root stays
legible.

### Foreign-source
**Definition.** A real word from another language whose literal meaning fits the world, borrowed
whole.
**Worked example.** Latin *iter* ("journey, road" — the root of "itinerary") → **Iter**.
**Cost.** Risks the cross-cultural problems `brand-name-critic`'s practicality layer screens for
— a word innocuous in its source language can land badly in a market that doesn't know it's
foreign, or worse, know a different, wrong meaning for the same string. This skill doesn't clear
that; it just shouldn't be surprised by it downstream.
**Produces.** Usually arbitrary in the target market — meaningful in the source language,
meaningless (or accidentally something else) to the target audience.

### Phoneme coinage
**Definition.** No real morphemes at all — syllables assembled from ordinary phonemes into a
legal but previously meaningless string. Meaning attaches later, entirely by use.
**Worked example.** **Torvane** — legal CVC-CVC-e shape, no root, though it happens to echo
"vane" (a real word for a direction-indicator), which is a coincidence worth noticing rather than
planning for.
**Cost.** Buys ownability — nothing to collide with, nothing to dilute — and costs every bit of
cultural familiarity and pre-loaded meaning a real word would have brought for free. The name has
to do all its own work from a standing start.
**Produces.** Fanciful — the strongest trademark tier and the highest education cost, together.
`rare letters, common sounds` is the rule that governs whether a coinage is sayable or a pile of
consonants: a rare letter on a common sound is the sweet spot, and the sounds still have to
assemble into legal syllables (Xerox, not Xzrq).

### Shortest-synonym (the Synomin pattern)
**Definition.** Name the core function plainly, in-world: list the real synonyms already
available inside the world's vocabulary for what the product actually does, and take the
shortest one that's still a real word — no blending, no coining.
**Worked example.** The function is "shows you where you are." In-world synonyms: locate,
position, fix, mark, place, pin, site. The plainest, shortest, and already a genuine term of art
("get a fix on your position") — **Fix**.
**Produces.** Arbitrary-to-suggestive — a real, plain word, so cheap to say and spell, expensive
to own outright because it's common.

### Acronym / initialism
**Definition.** Compress a multi-word description of the world-function to its initials, then
check whether the result resolves as a pronounceable word or only as spoken letters.
**Worked example.** SONAR — *SO*und *N*avigation *A*nd *R*anging — resolves as a pronounceable
word and, once the source phrase is forgotten by most speakers, functions as a plain arbitrary
word. Contrast a phrase whose initials don't resolve (e.g. "Line Of Position" → LOP): that's a
legitimate output of this operator too, just one that stays an initialism rather than becoming a
word — flag it as such rather than forcing a pronunciation.
**Produces.** Fanciful-to-arbitrary once the source phrase is forgotten; stays a plain
initialism (no name-type upgrade) if it never resolves as a word.

---

## Costs, in one place

| Operator | Buys | Costs |
|---|---|---|
| Respell | Distinctiveness | Spellability |
| Phoneme coinage | Ownability | Cultural familiarity, all pre-loaded meaning |
| Foreign-source | A true, fitting meaning most of the audience can't read | Cross-cultural risk (the critic's practicality layer screens this) |

`rare letters, common sounds` is the rule that governs respells and coinages specifically: a rare
*letter* mapped onto a completely common *sound* is the sweet spot (Xerox: X→/z/). A rare letter
that produces an illegal cluster instead — no vowel nucleus, an onset English doesn't license —
fails the rule even though the individual sounds are common (Xzrq). Check both halves before a
respell or coinage advances past Pass 2.
