# xivl-client-data docs index

This index covers the decoded FFXIV 1.23b CSV corpus, its evidence, derived
findings, and repository policy.

## Corpus model

- [architectural-findings.md](architectural-findings.md) - FFXIV 1.23b corpus boundaries, typed gaps, and seed ownership.
- [corpus-inventory.md](corpus-inventory.md) - family inventory and the pinned extraction reproduction contract.
- [table-families.md](table-families.md) - common CSV families and research uses.

## Evidence and derived findings

- [inventory-cross-check.md](inventory-cross-check.md) - retail inventory observations matched against the three-source item catalog.
- [command-battle-params.md](command-battle-params.md) - getter-verified command-parameter map backing `derived/command_battle_params.csv`.
- [rank-cap-findings.md](rank-cap-findings.md) - rank-indexed BP, attribute-cap, derived-stat, and Cure-column findings.
- [quest-gating-findings.md](quest-gating-findings.md) - active-class quest-offer level form and class/job scope evidence.
- [shop-catalogs.md](shop-catalogs.md) - GC seal catalog fields, generic shop joins, and the seven-sheet fidelity audit.
- [shop-family-audit.md](shop-family-audit.md) - generic shop membership and price comparison plus the chocobo-fee evidence boundary.

## Repository policy

- [ai_agents/README.md](ai_agents/README.md) - tracked contribution, documentation, evidence, comment, and verification policy.

## Products outside docs/

- [../derived/README.md](../derived/README.md) - generated analysis artifacts, outside the source corpus and manifest.
