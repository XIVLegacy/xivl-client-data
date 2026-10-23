# Test authoring

Add a test for a demonstrated defect or distinct supported behavior or failure.
Extend an existing driver before adding another runner. Changed line count
alone does not justify new cases. Keep claims within the
[evidence policy](evidence-and-claims.md).

## Choose the input and assertion

Use small authored CSVs, bytes, or row dictionaries, with label and type headers
for CSV reader tests. Use a temporary tree for publication and archives. Invoke a
CLI when option precedence, environment selection, exit status, or process
output is the claim. Reuse the existing standalone drivers and unittest
modules without requiring a new fixture framework.

Keep literal expected cells, keys, SQL statements, bytes, or errors independent
of the production mapping, projection, or renderer under test. Deterministic
regeneration and round trips complement literal assertions: two operations
can agree on the same wrong result. For rejected input, assert the intended
error and preservation of existing output, or absence of newly published output.

## Preserve decoded-data distinctions

- Distinguish a raw blank from the literal cell `0` and a truncated row.
  SQL numeric coercion deliberately maps an explicit empty cell to zero;
  raw-cell analysis must retain its own blank/zero distinction. See the
  [CSV reader tests](../../tools/test_csv_reader.py) and
  [item/equipment tests](../../tools/test_item_equipment_crosswalk.py).
- Preserve typed layouts, signed values, supported integer bounds, and row
  widths. Make malformed rows reach the intended reader or type check.
- Keep sparse source IDs, empty slots, and iteration ordinals distinct.
  Do not renumber gaps or use a dense index as a source key. The
  [backing-row tests](../../tools/test_fixed_phrase_backing_rows.py) use
  authored bytes and literal sparse keys.
- For localized joins, assert exact source keys and locale cells, including
  duplicate display names, placeholders, quoting, embedded newlines, and
  Unicode preservation where supported. Equal labels do not merge row IDs.
  The [guildleve tests](../../tools/test_guildleve_names.py) separate complete
  joins, locale fidelity, layout failures, and source authentication.

Check every relevant metadata row, join, identity, and row count in its owning
integrity pass when completeness is the claim. Representative integration
cases can cover distinct CLI, parser, source, or publication paths without
repeating the complete pipeline for every row. Retain rows with unique logic.
Before deduplicating cases, map the retained inputs and assertions to every
removed combination. Call a reduction equivalent only when it preserves those
contracts; document omitted combinations and sampling losses for review.

## Keep refusal and source boundaries

Preserve the [external-root tests](../../tools/test_external_csv_root.py):
explicit `--csv-dir` precedence, environment selection, metadata-only listing,
and unsafe-root refusal are separate contracts. Test supported symlink,
junction, reparse-point, nested-directory, and non-file refusals at the owning
boundary. Report platform conditions that prevented a case from executing.
An invalid selected input must not silently fall back to another corpus.

The [archive tests](../../tools/test_private_csv_corpus.py) protect member
names, uniqueness, exact member identities, deterministic packaging, and
hydration. Retain refusal of source-overwriting archive outputs and nonempty
destinations, with byte-preservation assertions. Successful hydration must
reproduce all declared members before publication.

Public metadata, schema, synthetic, and retained-product tests run without
private corpus bytes or credentials and stay outside optional source skips.
Source reproduction and checksum checks require selected inputs; report missing
optional inputs without claiming that their bytes were checked. Public absence
mode does not establish corpus identity. Authored public fixtures must not copy
private CSVs or other retail inputs.

Keep independent checks independent: the manifest builder and corpus validator
recompute record counts separately. Preserve grant schemas, verifier constants,
and the dependency-free attestation checker in their owning roles. Public
mutation tests do not widen the private grants. The
[retail validation policy](retail-input-validation.md) owns approved inputs,
sanitized attestations, retained-file limits, and credentialed execution.

## Cost and verification

Reuse small setup helpers while retaining distinguishing bytes and independent
expected values. For material growth in report scans, filesystem operations,
subprocesses, or source, use relevant runtime, operation-count, or source-cost
evidence to explain the chosen boundary. Do not impose arbitrary case quotas
or benchmark every small test. State unmeasured savings as such.

For tool changes, run the focused driver and applicable repository checks.
Use [tooling](../../tools/README.md) for commands and lint, and
[local verification](retail-input-validation.md#local-verification) for public
absence and hydrated-corpus modes. Report executed checks and source or platform
skips accurately. Fixture economy does not replace the owning validation gate.
