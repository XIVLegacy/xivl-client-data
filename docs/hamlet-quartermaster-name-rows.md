# Hamlet quartermaster name rows

The pinned client tables contain four actor-class rows whose display-name
values resolve to Jeanne or Bebetta. `populaceHamletPushEvent` also retains
those names in its German Hamlet supply text; its English wording is the
generic "quartermaster". These are static table and localization facts, not
proof that a particular class spawned as a quartermaster in retail.

| Actor class row | Display-name row | English name |
| ---: | ---: | --- |
| `1500316` | `1100341` | Militia Quartermaster Jeanne |
| `1500318` | `1500156` | Militia Quartermaster Bebetta |
| `1500385` | `1100341` | Militia Quartermaster Jeanne |
| `1500386` | `1500156` | Militia Quartermaster Bebetta |

German `populaceHamletPushEvent.csv` rows `24`, `51`, and `52` mention Jeanne,
Bebetta, and Dhebi Polaali. This localized text supports the presence of all
three names in the client data, but does not associate any one name with a
specific hamlet, actor class, script path, or historical spawn. The rows do
not replace the separate `PopulaceHamletSupply` actor-class lookups documented
in `xivl-client-scripts:docs/hamlet-supply-ui-contract.md`.

Sources are the `2012.09.19.0001` extraction pinned in
`manifests/tables.json`: `actorclass.csv` rows `1500316`, `1500318`,
`1500385`, and `1500386` (SHA-256
`3ac9f8d1812d49101f367e2a41356be96b5d64b1fc5ca29949195f50ebe1d984`);
`xtx_displayName.csv` rows `1100341` and `1500156` (SHA-256
`36c5dfba312695d9f4ee090dbA123dfd7792feba55d88b0062c070d98abc0505`); and
`populaceHamletPushEvent.csv` rows `24`, `51`, and `52` (SHA-256
`7a6ea288aea906f518615c87013c4e0571384b5206ae875c37ba2a5fad16ea8b`).
