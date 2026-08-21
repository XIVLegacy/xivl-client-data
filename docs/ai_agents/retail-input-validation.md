# Retail input validation

The normal asset-free repository checks remain the merge gate. The additional
manual retail-input workflow asks one narrow question: does the exact approved
1.23b static-actor SAN file reproduce the already tracked class-path catalog?

## Fixed lane

| Contract | Value |
|---|---|
| Branch | `retail-staticactor-ci` |
| Workflow | `.github/workflows/retail-checks.yml` |
| Check | `staticactor-class-paths-v1` |
| Input declaration | `manifests/retail_inputs.json` |
| Expected result | `manifests/retail_staticactor_check.json` |
| Product | `manifests/staticactor_class_paths.json` |
| Verifier | `tools/verify_retail_staticactor.py` |
| Tracked pass attestation | `manifests/retail_evidence/staticactor-class-paths-v1.json` |
| Protected environment | `retail-evidence` |
| Private input repository | `XIVLegacy/xivl-private-assets` |

The approved input is `staticactor-san-1.23b`: private path
`client-data/ffxiv-1.23b/client/script/rq9q1797qvs.san` at immutable commit
`aeb52f6dbde95a793ee6d52be28de9f28a885b15`, installed as
`client/script/rq9q1797qvs.san`. It is 108911 bytes with SHA-256
`bb7306461b1728493242016a16d9dd5257d7512c60e423b017de5ec7aced3d14`.

## Exact assertion

The workflow stages that one file at its expected install-relative path and
runs `tools/extract_staticactor_san.py`. The generated product must be
byte-identical to `manifests/staticactor_class_paths.json`: 248434 bytes,
SHA-256 `d612438827e5997422ab6f64a807e567ddf1b953c532e8a319d67b93c53c9db0`,
and exactly 2812 unique ID-to-class-path records.

This proves only exact reproduction of the tracked catalog from the named
retail file. It does not prove NPC server bindings, actor behavior, catalog
completeness outside the decoder's limitations, or semantic correctness of a
class path.

## Credential and output boundary

Execution is manual `workflow_dispatch` from the reviewed revision on
protected `main`. A credential-free preflight rejects other events, refs, or
checkout revisions before the environment-bearing job is eligible. The
workflow has only `contents: read`; the environment variable is
`RETAIL_INPUTS_REPOSITORY=XIVLegacy/xivl-private-assets` and the secret
is `RETAIL_INPUTS_TOKEN`.

The fetch step resolves only the manifest-pinned private commit, tree, path,
size, and SHA-256. Raw input, API responses, and generated products remain
under one disposable private root. Cleanup runs on every outcome. The only
retained file is the schema-valid `retail-evidence-attestation.json`, uploaded
as artifact `retail-staticactor-attestation` for 30 days. Failure attestations
are reviewable artifacts and are never tracked.

## Local verification

Run the mutation suite and both repository modes before a credentialed run:

```powershell
python tools\test_retail_staticactor.py
python tools\validate_corpus.py
$env:XIVL_CORPUS_ABSENT = "1"
python tools\validate_corpus.py
Remove-Item Env:XIVL_CORPUS_ABSENT -ErrorAction SilentlyContinue
python tools\validate_corpus.py
```

The SAN file is not required for the normal gate. With an approved local
client install, two clean extractor runs must produce byte-identical products.
The mutation suite rejects a changed record, output byte, grant, expected
hash, extra attestation field, and retained-file violation.

Stop on input, private-tree, product, determinism, cleanup, allowlist,
protected-ref, artifact, or normal-CI drift. Do not retain SAN bytes, raw
intermediate products, private API responses, or sensitive logs.
