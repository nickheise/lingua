# The fidelity test

`breadth × fidelity`. This is the step the whole skill exists to force. It is also the step most
likely to get rushed, because Step 2 is fun and this step is where a favorite candidate dies.
Run it in full on every world that survived Step 2 — no shortcuts for the one that feels obviously
right.

## The two halves

- **Breadth** — does the domain supply sibling vocabulary? The `six-siblings test`: can you name
  at least six distinct terms from this world without straining? If you're inventing by the
  fourth term, the domain is thin, not deep — discard it before running fidelity at all.
- **Fidelity** — does the vocabulary *mean the right things*? Does the metaphor's internal
  structure map onto the product's actual structure, or is it being bent to fit?

**Breadth without fidelity is the dangerous failure, because it feels productive.** Call a
database tool "Garden" and you get seeds, soil, pruning, harvest, compost in ten seconds — six
siblings, easy. Now ask what "pruning" is. If the answer is "uh, deleting rows I guess," you have
not built a naming system, you have built a decoder ring users must memorize. **Arbitrary mapping
is worse than a plain name, because plain names don't ask anyone to learn anything.** A world that
passes breadth and fails fidelity is not a weaker version of a good world — it is actively worse
than no metaphor at all.

The positive case, for calibration: Scout passes both. A waypoint genuinely *is* a saved position
you will return to. A route genuinely *is* a path through material. A blaze genuinely *is* a mark
left for whoever comes next. Nothing is being translated — the metaphor and the product have the
same shape. That "nothing is being translated" feeling is the target. If you catch yourself
writing a justification for a mapping, that's the tell it isn't fidelity — a true mapping doesn't
need defending.

## The procedure — five concepts, mechanical threshold

Take **five real product concepts** from the brief (not generic placeholders — actual features or
objects this product will have) and ask, for each, what it would be called in this world.

1. List the five concepts before testing any world, so the same five get used across all
   candidates — otherwise it's too easy to cherry-pick flattering concepts per world.
2. For each concept, in each surviving world, write down the answer in one of two forms only:
   - **A mapped term**, with a one-clause reason the mapping is true rather than merely evocative.
   - **A shrug** — the honest admission that no term in this world names the concept without
     inventing a justification for it.
3. **Count the shrugs. If three of five require a shrug, discard the world.** This threshold is
   mechanical, not a judgment call — do not round in the world's favor because the domain is
   otherwise appealing. A 3/5 or worse shrug rate is a fail, full stop, and gets recorded as a
   discard with the reason, not softened into "promising but needs more thought."

Do this for every world still alive after Step 2's breadth check, not just the leading
candidate — a world that looks weaker at first can outperform the favorite once real concepts are
run through it, and the favorite can be the one that shrugs three times.

## Breaking-point probes

Every metaphor fails somewhere. The point of probing for it now, deliberately, is to know where
in advance rather than discover it after the name has shipped. Run these three specific probes on
every world that passed the five-concept test — they are chosen because they are unglamorous and
therefore reliable; a metaphor's proponents rarely think to stress-test them on their own:

1. **What is an error state in this world?**
2. **What is a permissions setting in this world?**
3. **What is the billing page in this world?**

Cartography handles "you're lost" beautifully and usually has nothing to say about invoicing.
That is not automatically disqualifying — a world doesn't have to name every last surface for
its vocabulary to be worth having. What matters is **where** it breaks:

- Breaking on a **peripheral** surface (billing, an obscure settings page) is a real but minor
  finding — note it, move on. Most good worlds break somewhere peripheral.
- Breaking on a **core** surface (the primary action the product performs, the main object it
  manipulates) is a serious problem, close to disqualifying on its own even if the five-concept
  test passed. A world that can't name the thing the product is *for* has failed at the one job
  that mattered most, regardless of how well it handles everything else.

Record the breaking point explicitly for every surviving world, even the ones that pass cleanly —
"no core-surface break found; billing has no natural term, treated as peripheral" is a real,
useful finding, not a null result to skip.

## Keep the metaphor off the buttons

One more check, applied to whichever worlds are still standing: the metaphor should name
**concepts**, not necessarily **UI actions**. Scout can have "waypoints" as a first-class concept
in its data model and marketing while the button in the product still says "Save." A user does not
need to learn what "waypoint" means to use the save button; they only encounter the term when it
helps them, in navigation, in documentation, in the mental model.

Metaphor-as-vocabulary aids memory. Metaphor-as-UI-label costs discoverability — a button that
says "Blaze a trail" instead of "Publish" makes a new user stop and decode it. Note, for each
concept mapped in the five-concept test, whether it's the kind of term that belongs on a button
(rare — reserve for signature, load-bearing moments) or the kind that belongs in the underlying
vocabulary only (the common case). This isn't a pass/fail gate; it's a note that keeps Step 4's
survivors from reading as "rename every button in the app."

## What to carry into Step 4

For every world that survives the 3-of-5 threshold: the five-concept mapping table, the
breaking-point findings (surface + peripheral/core), and the button/concept note. Worlds that
fail the threshold get recorded too, with the shrug count and which concepts shrugged — a
documented rejection is more useful later than a silent one, including for the free-proposal
domain from `02-world-sourcing.md`.
