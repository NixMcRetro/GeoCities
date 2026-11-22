# Agent instructions for NixMcRetro/GeoCities

These instructions apply to all contributors and coding agents. Consult
`docs/HANDOVER-2026-11-23.md` and `docs/ROADMAP.md` before proposing changes.

## Scope and environment

- Primary target: **Ubuntu Server 26.04 LTS** (x86-64); secondary: **Ubuntu 24.04 LTS**.
- Project phase: early, **non-destructive, synthetic-fixture-only modernisation**.
- The N100 (16 GB RAM, 1 TB internal SSD) currently has **other important workloads**. It is not available for GeoCities deployment until the user explicitly approves it.
- There is **only one 2 TB external SSD**. Do not assume a second one or free internal capacity. Consider all external/archive disks protected.
- Prefer working in this repo and GitHub Actions on disposable fixtures; optionally use a Mac-local checkout.

## Hard safety requirements

1. **Never** format, repartition, reboot, upgrade, install an OS on, change services on, or change networking of the N100 without a specific, prior approval. Preserve any NIX AI Auto and other existing services.
2. Never mount or write to the external SSD, remove historical archive data, or perform an irreversible migration without prior approval and a backup/recovery plan.
3. Treat originals as immutable. Do not execute preserved GeoCities website code or unreviewed legacy scripts. Several archived scripts use recursive deletion and mutating filename/merge commands.
4. Keep `main`, `2022-archived` and all other historical branches intact. Work on reviewable branches, keep PRs in draft until ready, and do not merge or push to `main` without explicit approval.
5. Do not download source collections or large datasets as a convenience. Request approval for all original archive downloads and downloads **over 100 MB**. Explain expected bandwidth/disk impact before installing packages or starting a substantial operation.
6. Before privileged commands, deletions, system changes or writing outside the working tree, explain the specific commands, effects, risks and rollback, and ask permission.
7. Never commit secrets, API keys, personal credentials, actual archive dumps, databases or generated large manifests.
8. Never report a test or deployment as complete without actual results.

## Engineering expectations

- Python 3.12+ standard library is sufficient for the current pilot.
- Keep the synthetic fixture small, deterministic and independent of original collections.
- Test historical filename bytes, mixed encodings, whitespace/newlines, case conflicts, timestamp preservation, symlink loops, path traversal, special files and error handling.
- Make processing resumable and provenance-preserving; explicit checksums, immutable source manifests, dry-run plans and conflict quarantine precede any mutation.
- No automatic deduplication that discards conflicting file variants.
- Prefer safe, isolated static presentation of historic sites over exposing the old Python 2/Twisted proxy.
- Ensure workflows pass on Ubuntu 24.04 and Ubuntu 26.04 before recommending a PR for merge.
- Document changes, limitations, verified test results, storage requirements and proposed next actions in GitHub.

## When starting a session

Read `docs/HANDOVER-2026-11-23.md`, this file, the README and `docs/ROADMAP.md`.
Inspect the current repository and draft PR #1. Ask whether the N100 remains
occupied **before proposing machine-level work**. If it is, stay within GitHub
and synthetic CI fixtures. Do not assume a fresh Ubuntu installation is needed.
