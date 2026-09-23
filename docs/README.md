# xivl-client-data docs index

This index covers the decoded FFXIV 1.23b CSV corpus, its evidence, derived
findings, and repository policy.

## Corpus model

- [architectural-findings.md](architectural-findings.md) - FFXIV 1.23b corpus boundaries, typed gaps, and seed ownership.
- [corpus-inventory.md](corpus-inventory.md) - family inventory and the pinned extraction reproduction contract.
- [table-families.md](table-families.md) - common CSV families and research uses.

## Evidence and derived findings

- [actor-appearance-crosswalk.md](actor-appearance-crosswalk.md) - Exhaustive census and canonical crosswalk for the seven packed actor appearance words.
- [deepvoid-class-appearance.md](deepvoid-class-appearance.md) - Distinct Deepvoid class, display, and appearance rows behind one English label.
- [quest-replay-rows.md](quest-replay-rows.md) - Selected cutscene replay keys and literal argument rows.
- [quest-marker-rows.md](quest-marker-rows.md) - Selected quest marker row fields and bounded interpretation.
- [hamlet-supply-rows.md](hamlet-supply-rows.md) - Hamlet supply-list keys, item IDs, and quantities.
- [ifrit-appearance-boundary.md](ifrit-appearance-boundary.md) - Ifrit Bowl candidate IDs, appearance bases, and missing NPC class-path join.
- [substat-status-join.md](substat-status-join.md) - Retail status-table join for the two numeric SubStat status-word nibbles.
- [status-row-absence.md](status-row-absence.md) - Exact-key coverage check for one ID in both status tables.
- [inventory-cross-check.md](inventory-cross-check.md) - retail inventory observations matched against the three-source item catalog.
- [command-battle-params.md](command-battle-params.md) - getter-verified command-parameter map backing `derived/command_battle_params.csv`.
- [rank-cap-findings.md](rank-cap-findings.md) - rank-indexed BP, attribute-cap, derived-stat, and Cure-column findings.
- [quest-gating-findings.md](quest-gating-findings.md) - active-class quest-offer level form and class/job scope evidence.
- [shop-catalogs.md](shop-catalogs.md) - GC seal catalog fields, generic shop joins, and the seven-sheet fidelity audit.
- [shop-family-audit.md](shop-family-audit.md) - generic shop membership and price comparison plus the chocobo-fee evidence boundary.
- [map-marker-resources.md](map-marker-resources.md) - static map-marker resource, UI-class, property-reference, and coordinate-domain crosswalk.
- [shposhae-map-identity.md](shposhae-map-identity.md) - Shposhae zone, place-name, and five-page layout join.
- [seeker-disappearance-message-rows.md](seeker-disappearance-message-rows.md) - Localized Seeker disappearance text and its actor, location, and event boundary.
- [copperbell-map-identity.md](copperbell-map-identity.md) - Copperbell Mines zone, layout, and two map-page rows.
- [job-quest-marker-joins.md](job-quest-marker-joins.md) - job-quest marker display IDs and bounded actor-class joins.
- [job-journal-phase-text.md](job-journal-phase-text.md) - Bounded job journal objective text and localization conflict.
- [alc200-journal-phase-text.md](alc200-journal-phase-text.md) - Alc200 quest-to-journal rich-text links and unresolved expression semantics.
- [grand-company-enlistment-notices.md](grand-company-enlistment-notices.md) - Paired city-variant enlistment notices and their runtime boundary.
- [grand-company-journal-text.md](grand-company-journal-text.md) - Distinct campaign interaction-item instructions and later journal phases.
- [grand-company-reward-rows.md](grand-company-reward-rows.md) - Literal seal-item IDs and count-shaped values in selected quest reward rows.
- [raid-message-rows.md](raid-message-rows.md) - Dzemael progression and terminal text rows with dispatch unknowns.
- [job-quest-combat-display-joins.md](job-quest-combat-display-joins.md) - selected job-fight actor-class and display-name joins.
- [item-equipment-columns.md](item-equipment-columns.md) - retail item/equipment formula-column census, parameter-name joins, and grow-table boundary.

## Repository policy

- [style-guide.md](style-guide.md) - authored code, structured-data, and
  documentation conventions.
- [ai_agents/README.md](ai_agents/README.md) - tracked contribution, documentation, evidence, and comment policy.

## Products outside docs/

- [../derived/README.md](../derived/README.md) - generated analysis artifacts, outside the source corpus and manifest.
