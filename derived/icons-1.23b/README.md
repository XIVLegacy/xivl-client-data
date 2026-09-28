# icons-1.23b

## What this is

The full icon texture set was extracted from the retail FFXIV 1.23b client,
then decoded to PNG. It contains 9,960 files across 10 folders (`0..9`). Of these,
7,115 are real icons and 2,845 are the client's shared red "Undefined"
placeholder padding empty slots. Real icons span system/UI + playable-race face
portraits, status effects, crests/heraldry, materials, weapons, and armor.

Its use here is as the icon-id -> image reference for `itemData.csv` column 36.
The ability-icon column remains unpinned.

## Load first

- [`evidence-map.md`](evidence-map.md) - ID scheme, the band -> content-class
  assignments, how to join it to the client sheets, and gaps.
- [`range-samples.png`](range-samples.png) - one representative icon per band.
- [`id-ranges.csv`](id-ranges.csv) - per-band bounds, counts, pixel sizes, class.
- [`file-inventory.csv`](file-inventory.csv) - one row per file, with a
  `placeholder` flag so the real set can be filtered.

## The archive

The export is packaged as `xiv-icons-1.23b.zip` (81,219,028 bytes). It is
cold-stored and gitignored at `archive/icons-1.23b/xiv-icons-1.23b.zip`.
Restore by extracting it; internal layout is `<folder>/icon<NNNNN>.png` with
`folder = floor(icon_id / 10000)`.

Provenance, the zip's sha256, per-band counts, and a sha256 for each derived
table above live in [`manifests/icons_1_23b.json`](../../manifests/icons_1_23b.json).
`tools/validate_corpus.py` re-verifies every checksum against the file on disk.
It checks the zip only when the clone actually has it, since `archive/` is
gitignored, and recomputes the counts from `file-inventory.csv`.

## Consumers

Downstream publication has used curated subsets of the real icons. Recorded
promotion counts are:

- 171 action icons, rendered inline in the class/job/crafter/gatherer
  Actions tables.
- 3,198 item icons, one per icon the wiki's item pages use, reached
  through Template:Item.
- 170 status icons, one per status-effect page.

Its page generators read `file-inventory.csv` here to skip placeholder ids.

## Gaps

- Folders `50xxx` and `90xxx` hold no real icons (only the Undefined
  placeholder) - genuinely empty bands, not a capture gap.
- No per-icon entity labels; band -> class is a dominant-content claim, not a
  per-icon one.
- See the evidence map's Gaps section for the full list.

## Provenance

This repository owns the icon catalog, manifest, inventory, and evidence map
derived from the full FFXIV 1.23b client icon export.
