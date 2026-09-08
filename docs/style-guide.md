# Style guide

Repository style covers authored Python, PowerShell, schemas, derived data,
and documentation. It does not establish decoded field meaning, evidence
strength, source names, or corpus provenance.

## General

- Prefer existing local patterns once they exist.
- Keep changes scoped to the table family, derived product, or tool being
  changed.
- Use small, explicit functions and modules before adding abstractions.
- Follow the [comment policy](ai_agents/comments-and-prose.md) for source
  comments.
- Do not reformat the immutable source corpus or generated products for style
  alone.

### Documentation

The public [documentation policy](ai_agents/README.md#documentation-policy) is
canonical for authored documentation. The
[evidence policy](ai_agents/evidence-and-claims.md) owns claim wording,
citations, confidence, and provenance.

## Python

- Use Ruff 0.15.21 as the Python formatter and linter. Run `ruff format` to
  format authored tools and `ruff check` to lint them.
- Use 4 spaces for indentation and no tabs.
- Use `lower_snake_case` for modules, functions, and variables,
  `UpperCamelCase` for classes, and `UPPER_SNAKE_CASE` for constants.
- Group imports as standard library, third-party packages, then local modules.
- Prefer `pathlib.Path` for filesystem paths and explicit text encodings.
- Keep command entry points thin; put reusable work in importable functions.
- Raise or report specific failures instead of using broad exception handlers.
- Add type annotations where they clarify row shapes, path boundaries, or
  public helper contracts.

## PowerShell

- Use approved verb-noun names for functions and 4 spaces for indentation.
- Pass paths as parameters and use literal-path operations for repository
  inputs.
- Set terminating error behavior deliberately at command boundaries.
- Keep orchestration in PowerShell and data transformation in the owning
  Python module when one exists.

## Structured data

- Preserve schema-defined names, field order, identifiers, and null behavior.
- Edit canonical mappings, manifests, and tools, then regenerate owned output.
- Preserve the local indentation and ordering of hand-authored JSON.
- Keep CSV headers stable and never normalize files under `csv/`.

## Verification

Use the owning commands in [tools/README.md](../tools/README.md). Formatting is
not a substitute for schema, corpus, or evidence validation.
