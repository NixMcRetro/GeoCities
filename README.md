# GeoCities Reconstruction

Modern reconstruction pipeline for the Archive Team GeoCities collection.

This branch is the active rebuild of the project for current operating systems, with Ubuntu 26.04 LTS as the primary target and macOS support planned for case-sensitive APFS volumes.

The previous 2022 implementation is preserved in the [`2022-archived`](../../tree/2022-archived) branch.

## Goals

- rebuild the GeoCities preservation pipeline on current operating systems
- preserve the original Archive Team data without silently losing filenames or case distinctions
- replace obsolete platform dependencies such as `gvfs-info`
- support modern PostgreSQL and 7-Zip tooling
- make destructive operations safer and easier to audit
- add dry-run support, preflight checks, resumable stages and validation
- build a small representative test corpus before processing the full archive
- retain useful algorithms and preservation work from the 2022 implementation where they still make sense

## Platform targets

### Ubuntu 26.04 LTS

This will be the primary supported platform.

### macOS

macOS support is planned, but the source and working data must live on a case-sensitive APFS volume. The GeoCities archive contains paths whose names differ only by case, so a normal case-insensitive macOS volume is not suitable for reconstruction work.

## Project history

This repository derives from the GeoCities preservation work originally developed by Dragan Espenschied and other contributors to the One Terabyte of Kilobyte Age project.

NixMcRetro's 2022 reconstruction pipeline expanded that work to merge and process several Archive Team GeoCities collections. That implementation and its full history are retained in the `2022-archived` branch.

The `main` branch is a fresh modernisation effort started in 2026.

## Archive sources

The rebuild is intended to work with the major preserved GeoCities collections used by the earlier pipeline, including:

- Archive Team GeoCities Snapshot
- GeoCities Chronomex
- GeoCities JCN Grab
- GeoCities Latecomer
- GeoCities Santiago Grab

The exact source manifests, checksums and acquisition instructions will be documented as the modern pipeline is rebuilt.

## Status

Early rebuild.

The first priority is to create a safe, reproducible development fixture that exercises the difficult parts of the original archive before running any code against the full dataset.

## Historical implementation

For the Ubuntu 12.04 based 2022 implementation, scripts and notes, see:

[`2022-archived`](../../tree/2022-archived)

## License

Licensing and attribution from the original project and the 2022 implementation will be preserved as code is brought forward into the modern branch.
