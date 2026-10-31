# Static content values and runtime producers

The decoded `2012.09.19.0001` tables establish stored cells and exact key
joins. [Table identities](../manifests/tables.json) pin their bytes. A static
value needs its own runtime consumer or observation before it can describe
historical encounter behavior.

[Selected content row values](selected-content-value-rows.md) record exact
guildleve tuples, display-name cells and quest-marker selections with their
source field positions and byte identities.

## Guildleve objectives

The [guildleve mapping](../tools/mappings/guildleve.py) separates objective,
`aimNum`, item and mob fields. The
[selected rows](guildleve-selected-row-values.md) preserve raw tuples without
assigning required kills or progress semantics. Nonzero mob keys can join
display-name text, as the [12468 rows](guildleve-12468-client-rows.md) show.
That equality does not establish runtime actor-class selection, an owned
roster, disguise, spawn transform or completion rule. The
[name catalog](guildleve-names.md) preserves
placeholder labels, including `dummy` at 12402.

The client objective and initializer contracts are recorded separately in
`xivl-client-scripts:docs/local-regional-leve-contracts.md`, "Objective
consumption and finish", and
`xivl-client-scripts:docs/guildleve-initializer-arguments.md`. The retained
[12487 lifecycle](https://github.com/XIVLegacy/xivl-captures/blob/main/docs/guildleve-12487-observed-lifecycle.md)
does not authenticate per-objective actor interactions, roster generation or
reward settlement. It supplies no general ring geometry, bonus-chest
probability, tier, lifetime or payout policy for other content.

## Mob identity and combat values

[Identity catalogs](identity-catalogs.md#mob-taxonomy-and-immunity) keep actor
classes, display names, reported taxonomy and application pool IDs separate.
The [appearance crosswalk](actor-appearance-crosswalk.md) establishes static
row correlations and packed appearance words. A weapon-shaped appearance
value does not establish a combat job, skill list or attack delay.

The [reported profile assessment](https://github.com/XIVLegacy/xivl-captures/blob/main/studies/monster-population-reported-observations/derived/stat-model-assessment.md)
identifies supplied stats as unverified values rather than retail
measurements. Neither a nearby class nor a reported family authenticates
combat scaling, detection rules, a campaign or caravan kit, immunity bits or
a numeric link vocabulary. Those values require the exact field consumer
and an attributable observation for the selected subject and conditions.

## Journal marker values

[Selected quest marker rows](quest-marker-rows.md) preserve coordinate cells,
resource strings, numeric references and property references. The two
coordinate cells do not provide terrain height, facing, radius or a complete
world transform. A matching row key establishes the static value even when
its intended quest-phase or campaign-objective use remains unresolved.

The client request route is documented in
`xivl-client-scripts:docs/content-director-ui-contracts.md`, "Requested-data
fixed arguments". It separates the supplied quest ID from the marker tail.
The retained
[journal/map exchange](https://github.com/XIVLegacy/xivl-captures/blob/main/studies/quest-journal-map-wire/derived/evidence-map.md#quest-phase-boundary)
does not assign a phase meaning to a marker suffix or journal input. An alias
that repeats a valid row key adds no independent observation or evidence for
its descriptive name. Activation still needs the exact quest state,
dispatcher or request producer and selected marker list. Raw references do
not establish an NPC binding, private-area type or visible rendering.
