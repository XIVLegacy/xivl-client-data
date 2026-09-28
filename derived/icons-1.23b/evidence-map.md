# Evidence Map - 1.23b Client Icons

## What this is

A full extraction of the icon texture set from the retail FFXIV 1.23b client,
decoded to PNG. 9,960 files across 10 folders (`0..9`), ~78 MB zipped.
This is a client asset capture, not a gameplay observation - its value is as an
icon-id -> image reference for the icon fields carried by the decoded client
sheets in `xivl-client-data`.

This export supersedes an earlier sparse `xiv_icons.rar` dump (7,089 files). The
new export is a strict ID superset: it contains every icon the rar had, exports
each icon-number band as a contiguous range, and fills unused slots with the
client's red **"Undefined" placeholder**. See "Real vs placeholder" below.

## ID scheme

Each icon is stored as `<folder>\icon<NNNNN>.png`, where `folder =
floor(icon_id / 10000)`. The ID is the client's icon number - the same number
the item / status / command sheets store in their icon column.

## Real vs placeholder

The export writes a file for (nearly) every slot in each band and pads empty
slots with one shared red "Undefined" image. Deduplicating by a size-invariant
perceptual signature:

- **9,960 files total.**
- **2,845 are the "Undefined" placeholder** (one shared image, emitted at
  several pixel sizes). These are empty slots, not content.
- **~7,115 are distinct real icons.**

Placeholder-heavy bands and empty bands both mean "no icon here"; only the real
count matters. [`file-inventory.csv`](file-inventory.csv) carries a
`placeholder` flag (1 = Undefined) per file so the real set is filterable;
[`id-ranges.csv`](id-ranges.csv) gives per-band file / real / placeholder counts.

## Ranges

| Range | IDs (real) | Real icons | Pixel size | Content class |
|---|---|---|---|---|
| `0xxxx` | 0-1150 | 885 | 8-520 (mixed) | System / UI: cursors, class-guild badges, target-panel faces, **playable-race character face/portrait icons (~134-189)**, misc |
| `10xxx` | 10001-10230 | 192 | 32 / 128 | Status-effect icons (buffs / debuffs) |
| `20xxx` | 20001-20100 | 49 | 64/128/256 | Large art: decorative frames + stained-glass class/soul emblems |
| `30xxx` | 30001-30600 | 476 | 64/128 | Crest / rank emblem badges |
| `40xxx` | 40001-42000 | 876 | 44/64/128 | Heraldry: shield fields + charges (company/guild crest parts) + emblem badges |
| `50xxx` | - | 0 | - | **Empty** - only the Undefined placeholder |
| `60xxx` | 60001-61741 | 1495 | 64/128 | Crafting materials / reagents |
| `70xxx` | 70001-70632 | 613 | 64/128 | Weapons |
| `80xxx` | 80001-82636 | 2529 | 64/128 | Armor / accessories / gear |
| `90xxx` | - | 0 | - | **Empty** - only the Undefined placeholder |

Classes come from sampling icons across each range and reading them visually;
they are the dominant content of each range, not a per-icon claim.
[`range-samples.png`](range-samples.png) shows one representative per band. The
`30xxx`/`40xxx` split reads as finished rank/guild badges (`30xxx`) vs the
shield-field-plus-charge building blocks of the company crest system (`40xxx`),
with a few full-emblem / action-style icons at the top of `40xxx`.

## What the rar was missing

The rar dropped ~26 real icons this export recovers, dominated by one block:

- **folder 0, ids ~134-189: playable-race character face / portrait icons**
  (Hyur / Elezen / Lalafell / Roegadyn face thumbnails - the character-creation
  face selection art). This is the meaningful addition.
- `20011-20014` (large frame/emblem art) and `61270` (one material).

Every other rar "gap" is a genuinely empty slot the export fills with the
Undefined placeholder - i.e. the rar was right to omit them.

## Confirmed

- The band->class assignments above (visual sampling across each range).
- `folder = floor(icon_id / 10000)` layout.
- `50xxx` and `90xxx` hold no real icons (only the Undefined placeholder). This
  settles the earlier "missing consumables range" question: 1.23b's icon set has
  no populated `50xxx`/`90xxx` band - it is not a capture gap.
- The export is a strict ID superset of the rar (0 rar icons absent from it).

## Gaps / not done

- **No per-id labels.** This set maps ranges to classes, not each icon id to the
  specific item/status/action/face it depicts. The id -> entity-name join against
  the `xivl-client-data` sheets is unbuilt.
- **Status and command icon-column positions are unpinned.** The item join uses
  `itemData.csv` column 36, as recorded in `tools/mappings/items.py`; pin the
  remaining columns by cross-referencing known entities against this set.
- Class labels for the `0xxxx` band beyond the identified face block are coarse
  (it mixes cursors, UI, small emblems, and large art across many pixel sizes).

## Provenance

- Source: full retail client icon export, folders `0..9`,
  `<folder>\icon<NNNNN>.png`.
- Packaged as `xiv-icons-1.23b.zip`, sha256 and per-band counts in
  [`manifests/icons_1_23b.json`](../../manifests/icons_1_23b.json).
- Cold-stored (gitignored) at `archive/icons-1.23b/xiv-icons-1.23b.zip` - over
  the in-repo size threshold. Restore by extracting that zip; layout is as
  inventoried in [`file-inventory.csv`](file-inventory.csv).
- Catalog owner: `xivl-client-data`, derived from the full FFXIV 1.23b client
  icon export.
