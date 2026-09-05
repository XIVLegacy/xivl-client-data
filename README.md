<h1 align="center">XIVLegacy Client Data</h1>

<p align="center">
Decoded client data manifests, schemas, and research products.<br>
Preservation and evidence for Final Fantasy XIV 1.23b.
</p>

<p align="center">
<a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
<a href="https://github.com/XIVLegacy/xivl-client-data/actions/workflows/checks.yml"><img src="https://github.com/XIVLegacy/xivl-client-data/actions/workflows/checks.yml/badge.svg" alt="Checks"></a>
</p>

## About

This repository preserves metadata and research products derived from the
decoded static client data corpus for Final Fantasy XIV 1.23b. The decoded CSV
corpus remains private and is not distributed by this repository. Authorized
maintainers normally hydrate its private snapshot outside the checkout and
point the tools at that directory; the ignored repository-local `csv/`
directory remains an optional compatibility cache. The workflow is documented
in `docs/corpus-inventory.md`.

## Documentation

- [Documentation home](docs/README.md)
- [Corpus model](docs/architectural-findings.md)
- [Corpus inventory](docs/corpus-inventory.md)
- [Table families](docs/table-families.md)
- [Retail inventory cross-check](docs/inventory-cross-check.md)
- [Command battle parameters](docs/command-battle-params.md)
- [Icon evidence map](derived/icons-1.23b/evidence-map.md)
- [Evidence and claims](docs/ai_agents/evidence-and-claims.md)
- [Derived products](derived/README.md)
- [Tooling and regeneration](tools/README.md)

## Contributing

Pull requests are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before you
open one.

## License

Project-authored material uses the [MIT License](LICENSE), including tools,
schemas, documentation, manifests, derived products, and original arrangements.
Retail client material is not covered.
Vendored material retains the source license recorded in its provenance file.
This project is unaffiliated with and unendorsed by the publisher. All
trademarks belong to their respective owners.
