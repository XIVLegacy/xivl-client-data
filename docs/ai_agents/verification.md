# Verification

`.github/workflows/checks.yml` is the authoritative list of CI-covered checks,
and CI runs them on every pull request and push to `main`.

## Corpus-present check

CI declares `XIVL_CORPUS_ABSENT=1` because the decoded corpus is unavailable.
With the matching `csv/` corpus restored locally, leave that variable unset and
run:

```powershell
Remove-Item Env:XIVL_CORPUS_ABSENT -ErrorAction SilentlyContinue
python tools/validate_corpus.py
```

Exit 0 proves all 803 corpus files match their declared hashes and row counts,
and that the schemas, referential integrity, derived counts, icon products,
provenance, and docs indexes agree with those bytes. CI proves only the public
manifest and repository shape.

## Claim limits

A green gate proves repository integrity for the inputs that were present. It
does not prove behavior against a live database, network session, retail
client, or uninspected upstream source. Report the environment mode and any
unverified external track.
