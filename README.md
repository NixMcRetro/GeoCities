# GeoCities Reconstruction

Modern, preservation-first reconstruction tooling for the Archive Team
GeoCities collections. This is a work in progress, not yet a production
restoration pipeline.

This repository descends from
[Dragan Espenschied's original work](https://github.com/despens/Geocities),
through `kyledrake/Geocities`. The original tools were developed for Ubuntu
12.04 and released under AGPL-3.0-or-later. The historic project licence is
retained in `LICENSE` and `agpl3.txt`.

The earlier NixMcRetro reconstruction scripts and history live on
[`2022-archived`](../../tree/2022-archived). Do not run the old
scripts against originals without separate review: some delete, move or
rewrite archive files.

## Current status

The `develop-ubuntu-2604` branch contains a **read-only pilot**:
- source preflight checks and a deliberately small test fixture;
- SHA-256 inventory, timestamps and original filename-byte recording;
- reporting of case-insensitive filename collisions;
- symlink recording without following directory symlinks;
- refusal to overwrite manifests or write them inside the source;
- compatibility tests for Ubuntu 24.04 and 26.04.

**Not implemented:** extracting real 7z/tar collections, full-scale
reconstruction, database migrations, archive serving or resumable batches.

## Platforms

Primary target: Ubuntu 26.04 LTS on a case-sensitive Linux filesystem.
Secondary CI target: Ubuntu 24.04 LTS. The pilot uses only the Python 3.12+
standard library and does not require PostgreSQL yet.

For the N100 NUC, keep original GeoCities files on the external 2 TB SSD,
with small test data and manifests on the internal SSD. Do not attempt a full
archive run without checking capacity. Avoid exFAT for archive working data.

## Try the non-destructive pilot

From the repository root on Ubuntu (Python 3.12 or newer):

```sh
python3 scripts/create_fixture.py /tmp/geocities-fixture
python3 -m geocities_rebuild preflight --source /tmp/geocities-fixture
python3 -m geocities_rebuild scan --source /tmp/geocities-fixture --output /tmp/geocities-test.manifest.json
python3 -m unittest discover -s tests -v
```

The fixture generator refuses to reuse an existing directory. The scan reads
and hashes files but never changes the source. The manifest is created only
if the requested output does not already exist. Remove the temporary fixture
and manifest manually when finished.

For local paths, copy `config.example.toml` to `config.local.toml` and edit
it. The local config is excluded from Git.

```sh
python3 -m geocities_rebuild --config config.local.toml preflight
python3 -m geocities_rebuild --config config.local.toml scan --output /tmp/my-test.manifest.json
```

The default scan limit is 10,000 entries and is deliberately unsuitable for
the full GeoCities collection. The preflight does not yet establish the disk
capacity needed for complete reconstruction.

## Roadmap and review

See [docs/ROADMAP.md](docs/ROADMAP.md). Develop on a separate branch and
review before merging into `main`. Historical branches remain unchanged.

## Licence and attribution

AGPL-3.0-or-later. Preserve original author and contributor attribution when
carrying forward historical scripts. Archive content may have different rights
and is **not** part of this Git repository.
