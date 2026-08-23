# Contributing

Focused contributions are welcome from collaborators. Work in a fork, open a
pull request against `main`, and keep all CI checks green.

## Before contributing

This repository catalogs decoded retail data and the tooling that extracts,
maps, validates, and promotes it. Keep each change focused on one finding,
tooling improvement, mapping, or derived product.

The source corpus is immutable evidence. Never hand-edit, normalize, or re-emit
files under `csv/`. Changes belong in extraction or mapping tooling, derived
products, manifests, schemas, or evidence notes. A replacement extraction is a
new versioned corpus with provenance, not an in-place refresh.

Do not submit client binaries, client assets, packet or capture archives,
credentials, local settings, database dumps, generated build output, or private
working material.

## Evidence and citations

Follow the [evidence and claims doctrine](docs/ai_agents/evidence-and-claims.md).
Use the narrowest claim the identified artifact supports, keep raw evidence
distinct from interpretation, and place durable citations with the manifest,
derived product, tool, or document that relies on them. Pull request prose is
not a durable citation.

## Pull requests

Keep commits and review scope small enough to audit. Explain what changed and
why the evidence supports it. A contributor who could not
explain their own diff should not open it.
