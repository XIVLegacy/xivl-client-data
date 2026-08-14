# Evidence and claims

Use the narrowest claim supported by an identified artifact. Agent output,
summaries, search snippets, and unattributed statements are leads. Inspect the
underlying file before promoting a fact into a tracked document, manifest, or
derived product.

## Evidence classes

Use the exact class vocabulary required by the owning schema. Current products
use:

- `client_extraction` for the client CSV corpus and manifests
  decoded from client assets, such as zone names, static-actor paths, and
  icons.
- `observation_derived` for observations reconstructed from gameplay or other
  historical tables. It is not client extraction.
- `live_validated` for claims validated against the retail client in a recorded
  live session. The authoritative session record must be cited. It does not
  live in this repository.

Packet-capture inputs are evidence artifacts in their own right. Their vendor
provenance records state the evidence tier, source path, source license, and
sha256. A packet
observation must not be presented as a client-extraction fact. A derived CSV
is an interpretation of its inputs, not a new evidence class. Keep its raw
inputs and finding document visible.

## Claims and names

State uncertainty when a value, name, version, region, or interpretation is
not resolved. Do not merge conflicting sources into one confident assertion.
Live validation against the retail client is the applicable cross-check for
mechanics claims. Its authoritative session record must be cited rather than
reconstructed in this repository.

Keep `csv/` rows distinct from `derived/` rows. A raw CSV value is client
evidence for this catalog. A derived value needs a generator, a finding or
manifest link, and any relevant limitation. Keep interpretation beside the
raw value when the interpretation is not independently verified.

## Numbers in prose

Every figure in authored prose must support its sentence's claim.

Figures that carry claims stay verbatim. Row counts, coverage ratios, per-file
byte sizes and hashes, offsets, and extraction diffs are the claim itself.
Removing one destroys evidence.

Remove incidental figures without weakening the claim. A count that does not
support the finding creates maintenance work without adding evidence.

Do not use approximate figures when an exact source exists. Cite the source
instead of restating a number that does not carry the claim.

This governs prose the repository authors. A figure inside a quoted or
transcribed source is source content and stays verbatim, hedge included.

## Citations

Facts promoted from another repository use:

```text
repository-name:path/to/file
```

Add a row, symbol, or section locator when useful. When byte identity matters,
record a sha256 in the local provenance or checksum record rather than in the
citation string. Commit hashes and date pins are not citations: repository
histories are rewritten before publication, and dated "as of" claims rot.
Branch names, live working tree paths, and sibling paths are not citations.
For the client CSV extraction, preserve version `2012.09.19.0001` and rely on
the local manifest checksums for the committed bytes. Preserve source dates
when they are part of the provenance record.

A record that carries evidence but makes no citation-grade external claims stays in
maintainer material until its citations are refreshed. Tracked documents
should point to the repository's manifests, schemas, tools, and findings, not
to a sibling checkout or a departed source tree.
