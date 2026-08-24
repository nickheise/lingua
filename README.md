# Lingua

**Naming as a repeatable process.** A Claude Code plugin of three skills that either critique a
name you have already fallen for, or generate candidates from a description — grounded in
linguistics and practitioner method rather than taste.

> Status: **in development.** See [`docs/BUILD-MAP.md`](docs/BUILD-MAP.md) for the full plan and
> what is built so far, and [`CHANGELOG.md`](CHANGELOG.md) for the progression.

---

## Why

Naming is the bottleneck that gates everything downstream — the repo name, the domain, the icon
set, the feature vocabulary. It usually happens in thirty seconds on vibes, and then either
quietly constrains the project for years or gets changed late and expensively.

Existing generators emit flat lists of brandable-sounding strings with no reasoning, no
positioning input, and no notion of whether a name can support a system of sibling names. Naming
guides cover trademark and memorability but skip *speakability* almost entirely, and skip
*generativity* completely.

## The five ideas

Everything here is built out of five principles. They are written as **leading words** — short,
high-density phrases repeated verbatim throughout the skill files, because agents echo them back
in reasoning traces and steer themselves with them.

**`world, not word`** — The most valuable property of a name is generativity: does it come with a
vocabulary and an iconography attached? *Scout* gives you waypoints, blazes, cairns, routes,
contour lines, base camp, field notes — each arriving with an icon already drawn. That is not a
name, it is a nomenclature system acquired for the price of one word.

**`breadth × fidelity`** — A world can supply plenty of vocabulary and still be the wrong world.
Breadth asks whether it supplies sibling vocabulary. Fidelity asks whether that vocabulary *means
the right things*. Breadth without fidelity is the dangerous failure, because it feels
productive: call a database tool "Garden" and you get seeds, soil, pruning, harvest in ten
seconds — then ask what "pruning" is, and if the answer is "uh, deleting rows I guess," you have
built a decoder ring users must memorise. Arbitrary mapping is worse than a plain name.

**`rare letters, common sounds`** — Xerox, Kodak, Coke, Zillow all map a rare *letter* onto a
completely common *sound*. You get orthographic distinctiveness without paying an articulatory
cost. This is also what separates Xerox from Xzrq.

**`read the ending`** — Names with lore have a plot, and the plot comes attached whether you want
it or not. Icarus is the compact version: gorgeous name, means *flew too close to the sun and
drowned*. If a name has depth, something is down there.

**`flag, never block`** — Trademark, domain, SEO, and namespace crowding are reported with a
severity note and have no power to sink a candidate. Generativity and familiarity both push
*against* distinctiveness. The context profile sets the volume; nothing sets a veto.

## The three skills

| Skill | Invoked by | Job | Terminates at |
|---|---|---|---|
| `brand-name-worlds` | you | Brief → 3–5 stress-tested semantic worlds | A chosen world. **No names produced.** |
| `brand-name-generator` | you | Chosen world → clustered shortlist | ~12 candidates, each with three sibling names and a usage sentence |
| `brand-name-critic` | the model, automatically | Candidate → three-layer evaluation | An argued recommendation |

**Critics are model-invoked. Makers are user-invoked.** Critique is cheap, fast, and welcome — it
should fire when you float a name mid-conversation. Generation is a heavyweight interactive
process that takes over the conversation; if it fired every time you described a project idea,
you would hate it within a week.

**The worlds skill terminating before any names exist is the whole point.** As a single skill it
would fail predictably: the agent sees "produce names" as the terminal goal, does thirty seconds
of world-building, and rushes to the list. Hiding the future step forces the real leg work onto
the mapping stress-test, which is where the value is.

## The evaluation model

Three layers, and each outputs a **different shape**, because each has different epistemic status.

| Layer | Output | Computed by |
|---|---|---|
| **Ergonomics** | Numeric score, 6 dimensions | `scripts/phonetics.py` — deterministic |
| **Brandability** | Argued judgment + counter-argument | model reasoning |
| **Practicality** | Pass/fail flags with severity | checks and lookups |

There is deliberately **no composite score**. `Ergonomics 89 · Brandability: exceptional world,
crowded namespace · Practicality: 2 flags` is more honest and more actionable than one number
averaging a fact with an opinion. Run "Lingua" through it and you get *comfortable, unoriginal,
and it doesn't matter* — three separate verdicts a composite would have blended into a
meaningless 84.

Syllable count, phonotactic legality, stress pattern, and phonetic neighbourhood density are
exactly the things an LLM estimates inconsistently and a script gets right every time. So they
are computed in Python against a vendored CMUdict-derived lexicon, and the skill reasons over the
resulting JSON. That is what makes the numeric layer trustworthy — and why the other two layers
are deliberately not scored.

### Context profiles

Feature naming and product naming are opposite problems. Same rubric, three weighting profiles:

| Profile | Weights up | Weights down | Special rule |
|---|---|---|---|
| **Venture / product** | Distinctiveness, generativity, verbability, ownability | Instant descriptiveness | Tolerate opacity |
| **Feature / UI** | Spellability, clarity, sibling consistency, international | Distinctiveness, cleverness | Penalise coined names hard |
| **Internal codename** | Memorability, fun | Nearly everything else | Must never leak into UI |

## Install

```
/plugin marketplace add nickheise/lingua
/plugin install lingua@lingua
```

Then:

```
/lingua:brand-name-worlds        # start from a description
/lingua:brand-name-generator     # once you have a world
```

`brand-name-critic` needs no invocation — mention a candidate name and it fires.

`phonetics.py` requires Python 3.8+ and **nothing else**. The lexicon ships with the plugin; there
is no install step, no network call, and no API key.

## What this is not

- **Not a legal tool.** Flags trademark risk heuristically; never gives clearance. Real clearance
  is an attorney.
- **Not a domain registrar.** No live availability checks in v1.
- **Not a logo or identity tool.** Stops at the name and the vocabulary it implies.
- **Not an oracle.** Outputs an argued recommendation, not a verdict. You decide.

## Where the name came from, and where it is going

`Lingua` is the **module name, not a skill name.** Skill names are feature names — the model
matches on them, so they are boring on purpose. `brand-name-critic` is what the model needs to
see; *Lingua* is what the folder is called.

Run through its own rubric, honestly: ergonomically strong (two syllables, DA-da, clean CVC-CV,
unambiguous spelling), brandability weak — descriptive-suggestive Latin for "tongue", the first
word anyone reaches for in this space, sitting in a dense namespace with Linguee, Lingua Franca,
and Lingua.ly. Low generativity: tongue, Babel, Rosetta, grammar, none of which maps onto
anything you would build. Practicality: irrelevant, it is a personal toolkit.

So the first real job for the finished plugin is to name itself, and to name the umbrella above
it — positioning + naming + content + pitch collectively still have no name, and "Lingua" is too
narrow semantically to be it. That prior work is seeded in
[`shared/naming-decisions-log.md`](shared/naming-decisions-log.md) so the run starts warm.
Renaming is expected; nothing in the build makes it painful.

## Roadmap beyond v1

Laying the suite out as `brand-{object}-{mode}` exposes two real gaps:

|  | Make (user-invoked) | Evaluate (model-invoked) | Produce (user-invoked) |
|---|---|---|---|
| **positioning** | facilitator | critic | — |
| **name** | worlds 🆕 · generator 🆕 | critic 🆕 | — |
| **content** | — | critic | writer |
| **pitch** | — | *gap* | builder |

`brand-pitch-critic` is a missing cell worth filling. More importantly, **there is no
brand-architecture skill**, and that is the one governing whether a portfolio of many projects
hangs together — the input that makes feature naming decidable in the first place.

## Documentation

- [`docs/PRD.md`](docs/PRD.md) — the source specification
- [`docs/BUILD-MAP.md`](docs/BUILD-MAP.md) — every file, who builds it, and the exit criteria
- [`docs/DECISIONS.md`](docs/DECISIONS.md) — every judgment call made during the build, with rationale
- [`CHANGELOG.md`](CHANGELOG.md) — the progression

## License

MIT
