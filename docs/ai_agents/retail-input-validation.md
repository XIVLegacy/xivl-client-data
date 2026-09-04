# Retail input validation

The normal asset-free repository checks remain the merge requirement. The
additional manual retail-input workflow verifies two independently granted
private inputs: the static-actor SAN reproduces its tracked class-path catalog,
and the decoded CSV archive reproduces the complete tracked corpus identity.

## Approved checks

| Check | Input declaration | Verifier | Assertion |
|---|---|---|---|
| `staticactor-class-paths-v1` | `manifests/retail_inputs.json` | `tools/verify_retail_staticactor.py` | Exact tracked class-path catalog |
| `decoded-csv-corpus-v1` | `manifests/private_csv_corpus.json` | `tools/verify_retail_csv_corpus.py` | 803 files, 70029056 expanded bytes, and the complete tree digest |

Both checks run from protected `main` through
`.github/workflows/retail-checks.yml`, use the `retail-evidence` environment,
and read only from `XIVLegacy/xivl-private-assets`.

The approved input is `staticactor-san-1.23b`: private path
`client-data/ffxiv-1.23b/client/script/rq9q1797qvs.san` at immutable commit
`aeb52f6dbde95a793ee6d52be28de9f28a885b15`, installed as
`client/script/rq9q1797qvs.san`. It is 108911 bytes with SHA-256
`bb7306461b1728493242016a16d9dd5257d7512c60e423b017de5ec7aced3d14`.

## Exact assertion

The workflow stages that one file at its expected install-relative path and
runs `tools/extract_staticactor_san.py`. The generated product must be
byte-identical to `manifests/staticactor_class_paths.json`: 248434 bytes,
SHA-256 `d612438827e5997422ab6f64a807e567ddf1b953c532e8a319d67b93c53c9db0`.
The catalog contains exactly 2812 unique ID-to-class-path records.

This proves only exact reproduction of the tracked catalog from the named
retail file. It does not prove NPC server bindings, actor behavior, catalog
completeness outside the decoder's limitations, or semantic correctness of a
class path.

## Decoded CSV assertion

The approved input `decoded-csv-corpus-1.23b` is private path
`extracted/ffxiv-1.23b/client-data/csv.zip` at immutable commit
`8b38a02ce8ebf662b931092e46273251b38c58f0`. It is 70110686 bytes with
SHA-256
`006f9438a8cfd9277376f0ab28474500c67e4665050aa631cae64c9e6f38a5b0`.

The verifier checks the archive identity and every member against
`manifests/manifest.json` and `manifests/tables.json`. Its expanded identity is
803 files, 70029056 bytes, and tree SHA-256
`33e51c468b85b3d27b628ca4f5ff49e0bd10a8778812085f2bcdfdfd0cbd84bb`.
The workflow hydrates the archive only inside disposable runner storage and
runs the complete corpus validator against that directory. This proves the
stored snapshot matches the canonical static-data corpus; it does not rerun the
client DAT extractor or establish new semantic claims.

## Credential and output boundary

Execution is manual `workflow_dispatch` from the reviewed revision on
protected `main`. A credential-free preflight rejects other events, refs, or
checkout revisions before the environment-bearing job is eligible. The
workflow has only `contents: read`; the shared fetch action receives the
`RETAIL_INPUTS_TOKEN` secret.

The workflow invokes the shared `fetch-retail-input` action from
`XIVLegacy/xivl-tools` at an immutable commit.
It receives each job's manifest-pinned private commit, path, size, SHA-256, and
output path. It validates that one authorized blob's path, type, mode, size,
and SHA-256, then fetches only that blob. Raw inputs and generated products
remain under a disposable private root. The shared
`finalize-retail-attestation` action removes that root on every outcome. Each
job retains only its schema-valid `retail-evidence-attestation.json`; failure
attestations are reviewable artifacts and are never tracked.

## Local verification

Run the mutation suite and both repository modes before a credentialed run:

```powershell
python tools\test_retail_staticactor.py
python tools\test_private_csv_corpus.py
python tools\test_retail_csv_corpus.py
python tools\validate_corpus.py
$env:XIVL_CORPUS_ABSENT = "1"
python tools\validate_corpus.py
Remove-Item Env:XIVL_CORPUS_ABSENT -ErrorAction SilentlyContinue
python tools\validate_corpus.py
```

Neither private input is required for normal checks. To exercise the complete
archive locally, set `XIVL_PRIVATE_CSV_ARCHIVE` to an explicitly supplied ZIP
before running `test_retail_csv_corpus.py`. The mutation suites reject changed
records, archive identities, expanded-tree identities, grants, extra
attestation fields, and retained-file violations.

## Reproduced result

[Retail Checks run 32513796625](https://github.com/XIVLegacy/xivl-client-data/actions/runs/32513796625)
reproduced the tracked
[`staticactor-class-paths.json`](../../manifests/retail_evidence/staticactor-class-paths.json)
attestation byte-for-byte.
The retained file is 310 bytes with SHA-256
`b3014faf9279e083acb1c66023b302685612ce4fabcb50d56a79252d7ef7f225`.
Artifact allowlist, schema, cleanup, negative-control, and public-log leakage
reviews passed.

Stop on input, private-tree, product, determinism, cleanup, allowlist,
protected-ref, artifact, or normal-CI drift. Do not retain SAN bytes, raw
intermediate products, private API responses, or sensitive logs.
