# The brief

Three paths in. Take whichever applies — never run two, and never ask for input a path you are
already on has already supplied.

| You have | Path | The asking budget |
|---|---|---|
| A positioning canvas | **A** | Ask nothing |
| A project document — PRD, spec, README, design doc, brief | **C** | Extract first; ask only about what it did not answer |
| Neither | **B** | Four questions, one message, plus at most one targeted follow-up round |

`${CLAUDE_PLUGIN_ROOT}/shared/velocity.md` §3 `earn the question` governs every ask on every
path: as many questions as the work genuinely needs, none that would not change the output, each
one naming what it unblocks, batched rather than dripped. And never stall — a field you cannot
fill is a stated assumption, not a blocker.

## Path A — a positioning canvas exists

Auto-populate from it. Ask nothing. Map these canvas fields directly into the brief fields below:

These are the **actual section headings** of the positioning canvas, not paraphrases. Match on
them literally; if a heading is missing, treat that field as absent rather than guessing which
nearby section meant it.

| Canvas section | Brief field | Why it matters here |
|---|---|---|
| **Best-fit customers** | Who for | Sets the register a world's vocabulary needs to land with |
| **Market category** | What it does | The functional shape the metaphor has to map onto |
| **Unique capabilities** | What it does (specifics) | The concrete things the metaphor must be able to name. Feed these straight into the five-concept fidelity test in Step 3 — they are the real product concepts, so they beat any you would invent. |
| **Value themes** | One-word personality (inferred) | The angle a world should sharpen, not flatten. Dunford's chain runs capabilities → value themes, so infer personality from the themes, not from the capability list. |
| **Competitive alternatives** | What it's replacing | **Especially valuable** — see below |
| **Relevant trends** (optional) | Era check | If present, use it against the eras section of `${CLAUDE_PLUGIN_ROOT}/shared/example-bank.md` — a world that sounds like 2011 dates the product before it ships. |

**Competitive alternatives are worth more than the other fields combined for this
purpose.** They define the phonetic and semantic white space to avoid — if three competitors
already lean nautical, a fourth nautical world isn't distinctive, it's confirmation. Read the
alternatives list before proposing worlds in Step 2, not after.

State plainly that the canvas was found and used, and name the file or source. Do not re-ask
anything the canvas already answers.

## Path B — nothing exists

Ask the compressed four-question mini-brief, in this order, as one message. Each question carries
the clause saying what it unblocks — ask it with the clause, not bare:

1. **What does it do?** One or two sentences, functional, not aspirational. *Unblocks: the
   functional shape a metaphor has to map onto.*
2. **Who is it for?** A person or role, not a market segment abstraction. *Unblocks: the register
   the world's vocabulary has to land with.*
3. **What is it replacing?** An existing tool, habit, or workaround — this doubles as the
   competitive-alternatives field a canvas would have supplied, so press for a real answer here
   rather than "nothing, it's new." *Unblocks: the semantic white space to avoid in Step 2.*
4. **One-word personality.** A single adjective. Resist a sentence — the compression is the
   point; a world-sourcing pass on a paragraph produces mush. *Unblocks: which worlds are even
   eligible.*

**Four questions is the core, and it stays four.** The compression is doing real work: it is why
this path takes one message instead of an interview.

### The one follow-up round

The compression fails when an answer is too vague to run Step 3 on. That is the *only* licence to
ask again, and it buys exactly one more message.

**The vagueness test:** could you take this answer, pull five real product concepts out of it, and
run them through a world? If not, it is too vague and the follow-up is earned. If yes, it is
answered — accept it and move.

| Too vague to drive Step 3 | Concrete enough |
|---|---|
| "It's for developers" | "Staff engineers debugging someone else's service at 2am" |
| "It helps teams collaborate" | "Turns a Slack thread into a decision record with an owner and a date" |
| "It's replacing spreadsheets" | "Replacing the one shared tracker nobody trusts because three people edit it" |
| "Modern" | "Unhurried" |

Rules for the round:

1. **One message, batched.** Every vague answer gets re-asked at once, never one at a time.
2. **Name the vagueness.** "'Developers' could mean a hobbyist on a weekend project or an SRE on
   call — those want opposite worlds. Which is it?" A follow-up that just repeats the question
   has not earned itself.
3. **Only genuinely vague answers.** Applying the deletion test: if the answer as given can drive
   the fidelity test, do not re-ask it to get a nicer version.
4. **Then stop.** After one round, proceed on what you have. Fill the remaining gaps with stated
   assumptions — write them into the brief block marked as assumptions, so Step 4's reader can see
   what the worlds were tested against. There is no second round.

## Path C — a project document exists, but no canvas

A PRD, spec, README, design doc, or written brief. This is the common case, and re-asking Path B's
four questions over a document that already answers three of them is the friction to avoid.

### 1. Extract before asking

Read the document and fill every brief field it can. Then **state plainly which fields came from
the document and where** — quote the phrase or cite the section for each. A field you cannot point
at is not extracted.

| Brief field | Where it usually lives in a project document |
|---|---|
| What it does | The problem/overview/summary section, or the first paragraph of a README |
| Who for | The user, persona, or audience section; sometimes only implicit in the problem statement |
| What it's replacing | Occasionally in "alternatives considered" or "why now" — **usually thin or absent** |
| One-word personality | **Almost never present.** Do not manufacture it from tone. |

### 2. The extraction test — extracted vs. must ask

A field counts as **extracted** only if both hold:

- **You can cite it.** A specific passage in the document, quotable. Not a synthesis across five
  sections, not an inference from tone.
- **It survives the Step 3 test.** The same vagueness test as Path B: could you run five real
  product concepts through a world using this? A PRD that says "for enterprise teams" has stated
  the field and still not answered it.

Cite but too vague → it is a **gap**, and say so: "the doc names the audience but only as
'enterprise teams,' which cannot drive a fidelity test." Inferred but not citable → fill it as a
**stated assumption**, marked as one, and only ask if the assumption would change which worlds are
eligible.

### 3. Then ask only about the gaps

One message, one question per gap, each naming what it unblocks. Do not re-ask anything extracted.

**Where the gaps almost always are.** A project document is written to build the thing, not to
name it, so it is systematically strong on function and systematically weak on positioning:

- **Competitive alternatives are the gap to press hardest on.** They are the highest-value field
  for world-sourcing — they define the semantic white space to avoid — and a PRD's "alternatives
  considered" section, when it exists at all, is usually about implementation choices rather than
  what a user does today instead. Ask for the real incumbent: the tool, habit, or workaround being
  displaced. Ask it even if the document has a section that looks like it covers this.
- **One-word personality almost never appears.** Ask for it. Do not infer an adjective from the
  document's prose style — that measures the writer, not the product.
- Audience is often present but abstracted to a segment. Apply the extraction test rather than
  accepting the heading.

Then proceed. Unanswered after one message is a stated assumption, not a blocker.

### 4. Harvest the five concepts from the document

**This is the biggest win on this path.** A project document already contains the product's real
concepts — its features, its objects, its states. Those are strictly better inputs to Step 3's
five-concept fidelity test than concepts an agent invents, for exactly the reason the canvas's
`Unique capabilities` section is (ADR-015): they are what the product actually has, so a world
that cannot name them has genuinely failed rather than merely failed a straw test.

Pull **five** and say which ones you took and where from.

- **Take:** nouns the product's users will encounter — features, objects, states, the primary
  action. "A saved query," "a run," "a stale index," "the review queue."
- **Don't take:** benefits, adjectives, goals, or section headings. "Faster onboarding" is not a
  concept, it is an outcome; no world names it and no world should have to.
- **Spread them.** Not five variations of the same object. Include the primary action, the main
  object it operates on, and at least one state or lifecycle stage — those are where metaphors
  break, which is the point of testing them.
- Fix the five before testing any world, per `03-fidelity-test.md`. The harvest happens once.

If the document yields fewer than five real concepts, take what it has and derive the rest from
the extracted "what it does," stating which are harvested and which are derived.

### 5. When the document is thin or off-target

A one-paragraph idea sketch is a document, but it is closer to Path B. Do not perform extraction
theatre over prose that has nothing in it.

**The fallback rule.** Count what the document actually yields. If it gives **fewer than three of
the four brief fields**, or **fewer than three harvestable concepts**, stop treating it as Path C:

> Say so in one line — "the doc is an idea sketch; it gives me *what it does* and nothing else" —
> then run **Path B**, with the fields it did give already filled in and not re-asked.

That is the whole fallback: Path B's four questions minus whatever was genuinely extracted. It is
never a reason to ask more than Path B would have.

**Off-target documents** — a document about something adjacent (an infra design doc for a system
the product sits on, a research memo, a competitor teardown) — get the same treatment. Extract
only what is about *this* product. A document that is 90% about something else usually yields one
field and should be treated as thin, not mined harder.

## Every path — this brief is provisional

State this explicitly in the output, once, and move on:

> A name chosen at idea stage is cheap to change. A name chosen after positioning exists is
> expensive to change. This brief was built [from an existing canvas | from a project document |
> without either]; if it was not built from a canvas, re-validate the chosen world against a real
> positioning canvas once one exists — the world that fit a four-question guess, or a PRD written
> to build rather than to position, may not survive contact with the actual best-fit customer and
> competitive set.

Structure the brief's own output (what it does / who for / what it's replacing / personality,
plus competitive alternatives if known, plus any stated assumptions) as a small standalone block
at the top of the eventual `world-brief-template.md`. It should be legible on its own to a future
positioning facilitator run — this leg work seeds that step, it isn't thrown away once naming is
done.
