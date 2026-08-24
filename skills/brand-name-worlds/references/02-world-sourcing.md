# World sourcing

## Fixed catalogue, plus one free proposal

PRD open question 4 asked whether to ship a fixed list of semantic domains or generate them
freely each run. This skill does both: **draw primarily from the catalogue below, then propose
exactly one domain not on this list.**

Why hybrid rather than either pure form: a fixed catalogue is consistent (the same domain gets
evaluated the same way run to run) and prunable (a domain that keeps failing fidelity tests can
be edited or removed once, here, rather than re-discovered as a bad idea every run). A free-form
catalogue is more surprising and can fit an unusual product better than any of these fifteen
domains do. The explicit "propose one not on this list" step buys the surprise back without
paying for consistency everywhere else.

## The rule this file exists to enforce

**Semantic domains, not tonal directions.** "Trustworthy," "playful," "premium," "bold" — these
are tones. A tone gives you nothing to name a permissions setting or a billing page with. A world
is a coherent human practice with its own vocabulary: cartography is a world because it has
waypoints, contour lines, legends, and scale bars; "adventurous" is not, because there is nothing
concrete to hang a second name on once the first one is picked. If a proposed domain can be fully
described in one adjective, it is a tone in disguise — reject it and look for the underlying
practice instead. A quick gut check before running the real `six-siblings test` in Step 3: could
you list six terms from this domain right now without inventing any? If not, don't bother carrying
it forward.

## The catalogue

For each domain: the vocabulary it actually supplies, what it maps onto well, what it is bad at,
and whether the imagery is already drawn (an icon that already exists culturally — a compass
rose, a beehive — is worth more than one that has to be commissioned from nothing).

| Domain | Vocabulary (sample) | Maps well onto | Bad at | Imagery pre-drawn? |
|---|---|---|---|---|
| **Cartography** | waypoint, legend, contour, scale, bearing, survey, landmark, atlas | Navigation, progress-tracking, saved state, exploration UIs | Billing, permissions, anything transactional | Yes — compass, pin, grid line |
| **Seafaring** | anchor, harbor, tide, crew, log(book), bearing, ballast, port | Collaboration tools, stability/reliability framing, milestones ("ports of call") | Precision/technical settings, error states (storms are too catastrophic a metaphor for a form validation error) | Yes — anchor, wheel, wave |
| **Masonry** | foundation, cornerstone, mortar, scaffold, keystone, course, blueprint | Infrastructure tools, platforms other things get built on, structural/architecture products | Anything fast-moving or ephemeral; masonry vocabulary is slow and permanent by connotation | Partial — trowel, brick, arch |
| **Printing** | typeface, proof, galley, press, plate, edition, imprint, folio | Publishing, document/content tools, versioning ("editions") | Real-time or collaborative surfaces; printing is a solitary, sequential craft | Yes — press, type block |
| **Birding** | field guide, sighting, plumage, migration, nest, flock, call, roost | Discovery/curation tools, community/social products (flock), pattern-recognition features | Destructive actions, security, anything adversarial | Partial — binoculars, feather |
| **Geology** | stratum, fault line, bedrock, core sample, sediment, fossil, tectonic | Data/history tools (strata = layers of history), foundational infrastructure, anything about depth over time | Speed, real-time features; geological time is the wrong register for anything instant | Weak — no strong pre-existing icon set |
| **Husbandry** | breed, herd, pasture, graze, shepherd, yield, stock, tend | Resource management, fleets of things needing ongoing care (device fleets, agent fleets) | Anything one-shot or transactional; husbandry implies ongoing tending, not a single action | Weak, mildly rural-coded |
| **Archery** | draw, nock, quiver, fletching, bullseye, loose, range | Precision/targeting tools, goal-setting products, single decisive actions | Anything continuous or collaborative; archery is a solitary, instant-release metaphor | Yes — target, arrow |
| **Weather** | forecast, front, pressure, gust, calm, squall, clear skies | Predictive/analytics tools, status/monitoring dashboards | Anything requiring precision or control — weather is inherently something that happens *to* you | Yes — cloud, sun, storm icons (also heavily overused — check for genericness) |
| **Textiles** | weave, thread, warp, weft, loom, splice, bolt (of cloth), pattern | Integration tools, products that combine many inputs into one output, design systems | Discrete/binary actions; textile vocabulary is about continuous combination | Weak — loom/shuttle icons uncommon outside the craft |
| **Horology (clockmaking)** | escapement, gear train, mainspring, tick, calibrate, complication | Scheduling, precision-timing, workflow-orchestration products | Anything spatial or exploratory | Partial — gear, clock face |
| **Apiary (beekeeping)** | hive, comb, swarm, forage, queen, brood, super | Multi-agent/swarm products, community platforms, resource-pooling tools | Solo-user products; the metaphor is inherently collective | Yes — hive, honeycomb |
| **Brewing** | batch, ferment, mash, cask, proof, brew, tap | Pipeline/build tools (batches, fermentation = processing time), iterative-release products | Instant or synchronous features; brewing implies waiting | Partial — cask, bubbles |
| **Joinery / carpentry** | joint, grain, plane, chisel, dovetail, workbench, finish | Component/composition tools (joints = how pieces fit), craftsmanship-forward products | Abstract or purely digital products with no assembly step | Weak — tool icons exist but are generic |
| **Astronomy / celestial navigation** | star chart, orbit, horizon, transit, ephemeris, zenith, parallax | Long-range planning tools, observability/monitoring products, "big picture" dashboards | Small, fast, everyday actions — astronomy's timescale is wrong for routine UI | Yes — star, orbit, telescope |
| **Falconry** | mews, jess, lure, hood, cast off, quarry | Search/retrieval tools, agent-dispatch products (an agent "cast off" to fetch something) | Community/social features; falconry is a solitary, hierarchical practice | Weak — niche imagery |
| **Gardening** | seed, soil, prune, harvest, compost, graft, bed | **Danger case — see below.** Rarely passes fidelity on anything but literal growth/content-lifecycle products | Almost everything else; this is the PRD's own worked failure | Yes, which is exactly why it's tempting |

**On gardening specifically:** it is in the catalogue because it will be proposed constantly —
the imagery is vivid and arrives in seconds. It is flagged here because that speed is the trap.
"Pruning" a database means what, concretely? If the answer requires a shrug, this domain fails
Step 3 immediately. Keep it in the catalogue precisely so it gets tested and discarded on the
record, rather than silently avoided or silently loved.

## The free-proposal step

After drawing 4-6 candidates from the table above, propose exactly one domain not listed here.
It should come from the brief itself — a domain the product's own subject matter suggests (a
medical scheduling tool might suggest triage or pharmacology; a climbing app might suggest
mountaineering specifically rather than the more generic cartography). Run it through Step 3
exactly like every catalogue entry — a free proposal earns no exemption from the fidelity test.

If a freely-proposed domain survives Step 3 with a clean pass, note in the final brief that it is
a candidate for addition to this catalogue on a future pruning pass — but do not edit this file
during a run. Catalogue maintenance happens deliberately, not mid-session.
