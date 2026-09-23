# Grand Company dialogue row variants

The canonical localized tables preserve these distinct text-row pairs:

| Table rows | Bounded text comparison |
| --- | --- |
| `com0l1` `34` / `58` | The English cells are identical, while the Japanese cells differ. Both versions discuss the Archon's prophecies. |
| `com0g1` `34` / `62` | Both versions describe surviving the Archon's attack. Row `34` addresses a reunion; row `62` omits that greeting. |
| `com0u1` `32` / `58` | Both versions refer to Mezaya's poetry. Row `32` offers to recite it; row `58` responds to the listener's surprise. |

These observations establish only that the localized tables contain different
text for the listed rows. A recognition or familiarity interpretation is
plausible, but the rows do not identify which condition selects them or prove
that a character had previously met the speaker. The related bytecode branch
in `xivl-decomp:docs/event/grand-company-mission-bytecode.md` records a
Boolean-`true` fade choice; it does not bind these text rows to that argument.
The historical argument producer and active branch remain unknown.

Sources: `xivl-client-data:csv/com0l1.csv` rows `34` and `58`, SHA-256
`3a70957c1099e45ce5e7e281d1e7e5ddcfc79d08d1f00a78513780d164e93457`;
`xivl-client-data:csv/com0g1.csv` rows `34` and `62`, SHA-256
`aee12f7bf80aab74fd5362a6dd3c09d6cedd209c97d99424b1111ce69fb42ac4`;
and `xivl-client-data:csv/com0u1.csv` rows `32` and `58`, SHA-256
`1101bce35ca6f91fc5536690d56d9f51c3df7a26518fe1a36f60969f46f80aa8`.
The digests are pinned in `manifests/tables.json`; all three tables are from
extraction `2012.09.19.0001`.
