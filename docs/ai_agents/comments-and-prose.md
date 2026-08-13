# Comments and prose

Delete explanatory comments unless they preserve a current fact that the
code, names, or types do not make clear. Deletion is the default.

Keep a comment only when it records one of these:

- a current invariant
- a client quirk
- a wire or packet fact
- an evidence citation
- a safety constraint
- an API or file-format contract not inferable from names and types

Keep source identifiers, evidence citations, extraction versions, and dates
verbatim. Compress other survivors to one line when practical. Move a
longer contract to the owning documentation page or declaration and leave a
short pointer. When unsure, keep one line and flag it in the maintainer review
record.

This rule applies to the Python and PowerShell tools, the tracked Rust
extractor sources, JSON Schema descriptions, and workflow comments. Generated
comments are generated output: preserve them exactly, or update the owning
generator and regenerate the product.

Python docstrings and command help are runtime text. Keep them when they
define a public tool or file-format contract. Tighten narration to one line while
preserving any contract that users or mappings rely on.

Examples of valid survivors:

```text
# Match build-manifest.ps1's CR/LF/CRLF line-terminator convention.
# Bounds-check typed integers so bad corpus values fail before SQL generation.
```

Examples of deletion-default narration include comments that only repeat a
function name, restate the following assignment, or preserve old investigation
history. The [documentation policy](README.md) governs tracked prose around
those comments. [Evidence and claims](evidence-and-claims.md) governs the
facts they are allowed to assert.

## Authored public prose

Public tier prose, meaning the README, CONTRIBUTING, the docs index, and any
page a stranger reads, uses a plain, direct register.

All tracked authored prose and structured descriptions state current evidence or
contracts. They are not prompts, assignments, review summaries, checkout state,
internal milestones, or work-session plans.

- Avoid over-hyphenation and invented compound modifiers. Established
  technical terms keep their hyphens.
- Use semicolons sparingly, preferring periods, commas, or short lists.
- Cut parenthetical asides. If the aside matters, make it a short sentence
  of its own. If it does not, delete it.
- Short declarative sentences, one idea each. A rule gets one line of
  practical justification, then stops.
- Do not use slang for hazards or critical structure. Name the actual hazard,
  required order, or dependency.

Internal working docs are out of scope. These rules govern the public tier.
