# Raid progression message rows

The decoded `worldMaster.csv` English text column has these Dzemael-related
rows. The source is `xivl-client-data:csv/worldMaster.csv` at the listed IDs;
its `manifests/tables.json` SHA-256 is
`2e2e2dd5cd9651388f6fa575b4229081ad0452165e78b725df0a5b5b7cf7c643`.

| Row ID | English text content |
| ---: | --- |
| 52015 | Gate-unlocked message with switch alternatives: chocobo stables, Gullet, Grand Hall |
| 52016 | Magitek transporter activated |
| 52017 | Magitek field deactivated with switch alternatives: Level I through Level V |
| 52026 | Terminal activated; cool wind |
| 52028 | Terminal activated; gentle wind |
| 52029 | Terminal activated; crisp wind |
| 52030 | Terminal activated; soothing wind |
| 52032 | Nearby creatures retreat to the void |
| 52033 | New wave emerges from the void |
| 52034 | Nearby creatures retreat and a new wave emerges |
| 52069 | Generic magitek-terminal activation |

The alternatives in rows 52015 and 52017 are encoded in the CSV's
`@switch` rich text. These rows identify available localized text, not the
historical selector argument, which specific terminal or encounter emitted
each wind line, packet timing, recipient scope, or progression rule.
