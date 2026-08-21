# Contribution and documentation policy

This policy governs changes to the tracked surface of the private decoded
client-data catalog. AI-assisted work follows the same standard as any other
change. The contributor owns the result, can explain the claim or edit, and can
name the checks that support it.

## Contribution policy

- Keep `csv/` as the as-imported extraction. Never hand-edit, re-emit, or normalize
  its rows.
- Keep generated manifests, derived tables, and seed fragments under the
  ownership of their generators. Imported reference products keep their
  provenance instead of being presented as generated client data.
- Preserve extraction versions, source paths, evidence classes, and dates.
  Keep stable citations verbatim when they identify an input or claim.
- Keep the CSV-to-SQL pipeline self-contained. It emits repo-local seed
  fragments. This repository does not own consumer DDL or a server checkout.
- Keep the tracked surface free of client binaries, capture archives,
  credentials, database dumps, or generated build output.

Evidence and claim rules are in [Evidence and claims](evidence-and-claims.md).
The repository checks and their limits are in [Verification](verification.md).

## Documentation policy

Tracked prose describes the current durable contract. Keep it concise, use a
human voice, and write ASCII-only authored text. Do not add branch state,
progress reports, migration breadcrumbs, or maintainer working history to a
durable product page. Source-version and provenance facts are allowed when
they support a current claim.

Link the canonical manifest, schema, tool page, or finding instead of copying
inventories into several documents. Use paths that exist in this repository.
Do not cite sibling checkouts, departed trees, or machine-local paths in
tracked prose.

The root `docs/README.md` indexes every direct Markdown document under `docs/`
in both directions. This policy shelf indexes every page in this directory.
Add a policy page only when a real repository surface needs a durable rule.
Do not keep empty shells for subjects this repository does not have.

## Policy shelf

Read these pages when the change touches their subject:

1. [Evidence and claims](evidence-and-claims.md)
2. [Comments and prose](comments-and-prose.md)
3. [Verification](verification.md)

The repository README, `tools/README.md`, manifests, schemas, and finding
documents remain canonical for their own surfaces.

[Retail input validation](retail-input-validation.md) describes the optional
credentialed SAN reproduction check and its exact claim boundary.
