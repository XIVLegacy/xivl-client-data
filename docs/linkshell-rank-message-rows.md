# Linkshell ranks and rank-message rows

The 1.23b sheets distinguish linkshell member, leader, and master. They
contain generic rank-change messages, but these rows do not bind a manual
master-transfer request, its completion packet, or its recipients.

## Rank and menu labels

`communityMember.csv` has `s32` columns labeled `0` and `1`. Its four rows
pair the value 1 with ranks 1, 4, 7, and 10. The matching
`xtx_communityMember.csv` English singular column, labeled `4`, reads:

| Row ID | Rank in `communityMember` column `1` | English singular |
| ---: | ---: | --- |
| 100001 | 1 | guest |
| 100004 | 4 | member |
| 100007 | 7 | leader |
| 100010 | 10 | master |

`xtx__text_ui.csv` English column `1` supplies the corresponding UI labels:

| Row IDs | Meaning |
| --- | --- |
| 79203, 79218 | Linkshell master |
| 79222 | Appoint the selected player as linkshell leader |
| 79223 | Remove the selected player from the leader position |
| 79246, 79247 | Linkshell leader |

In particular, the appoint tooltip names the leader role. It is not a
master-transfer label. A label alone does not establish which request a
widget sends.

## Generic rank messages

`worldMaster.csv` English column `1` contains these messages. The descriptions
below summarize the literal text and preserve the relevant control operands.
They are not observed server deliveries.

| Row ID | Text meaning | Encoded formatting references |
| ---: | --- | --- |
| 25168 | Member privileges changed | No control token |
| 25169 | Confirm changing the selected member's rank | Target/display-name controls; `xtx/communityMember` sheet reference |
| 25172 | The selected member's rank has changed to the supplied rank | Target/display-name controls; `xtx/communityMember` sheet reference |
| 25173 | Confirm revoking the selected member's rank privileges | Target/display-name controls; `xtx/communityMember` sheet reference |
| 25176 | The selected member's privileges have been revoked | Target/display-name controls; `xtx/communityMember` sheet reference |
| 25177 | The reader lacks authority to alter the selected member's privileges | Target/display-name controls |
| 25178 | Unable to alter the selected member's privileges | Target/display-name controls |
| 25179 | The reader's privileges for the named linkshell/company have changed | Linkshell/company selector; group-name string control |

The rank reference in 25169, 25172, 25173, and 25176 is exactly
`[@head-all:022d1fff1d022819ff147874782f636f6d6d756e6974794d656d626572e802050303]`.
It names `xtx/communityMember`, followed by expression `E8 02` and integer
expression `05`. The latter decodes to 4, matching the English singular
column label. The source does not encode the literal rank 10 at this site.

The display-name controls name `xtx/displayName` and retain expression
`E9 09`. Conditions retain `EB 04`. Row 25179 contains a string control
with operand `EB 32`, and its linkshell/company switch uses `E8 02`.
The expression grammar in
`xivl-tools:docs/formats/ssd-sheet.md`, "Rich-string read and text-export
contract", at revision `fd4c97d89eab3bbbf657021297e3d78156c63319`
preserves these unary expressions without establishing their runtime
parameter banks. They must not be converted into packet offsets, character
IDs, names, or a typed reply tuple without a native formatter/receiver join.

The rank reference is variable, and the sheet contains a master label.
Neither proves that a transfer invokes these rows. No actor/new-master/other-member
delivery split or transfer-specific success/refusal binding is established
by the sheets.

## Source identity and reproduction

Source extraction: `2012.09.19.0001`. The member identities below are pinned
in [tables.json](../manifests/tables.json) at source revision
`7fcf323209b40f01bdc783a150bc542edcf92752`.

| CSV member | Bytes | SHA-256 |
| --- | ---: | --- |
| `communityMember.csv` | 61 | `955051ae53e2da87dae8d9dae0403ed7e4d4c30d596e6427237b8254cfe38a5e` |
| `xtx_communityMember.csv` | 583 | `592fe78b1e87d33b59e9d7d000eea02984a1b936fb68e66a125c9dc60d047a08` |
| `xtx__text_ui.csv` | 1284564 | `23762a422118d99c4144a48b3495c52511b1b1b865e4fc50fdc61a973e3c6ece` |
| `worldMaster.csv` | 1851138 | `2e2e2dd5cd9651388f6fa575b4229081ad0452165e78b725df0a5b5b7cf7c643` |

Use the archive declared by
[private_csv_corpus.json](../manifests/private_csv_corpus.json), verify its
size and SHA-256, then verify each named member against `tables.json`.
Parse the two header records and select the row IDs above with Python's
`zipfile` and `csv` modules. Column labels exclude the leading row-ID field:
English column `1` is physical field index 2, and column `4` is index 5.
Select by row ID rather than CSV record or physical line number. Retain
the encoded controls when checking parameter references.
