# 🌐 GeoCities Reconstruction

**Rebuilding a little corner of the old web, one preserved file at a time.**

A modern reconstruction pipeline for the Archive Team GeoCities collection, bringing the 2022 preservation work forward to current operating systems.

🚧 **Status: Early rebuild.** The modern pipeline is still being developed. A small, reproducible test corpus comes first, before processing the full archive.

[📼 Explore the 2022 implementation](../../tree/2022-archived)

## 🛠️ What are we rebuilding?

- 💾 Preserve original archive data, filenames, and case distinctions.
- 🐧 Replace obsolete dependencies such as `gvfs-info` with modern tooling.
- 🗃️ Support modern PostgreSQL and 7-Zip.
- 🛡️ Make destructive operations safer with dry runs, preflight checks, and validation.
- 🔁 Add resumable stages and reproducible test fixtures.
- 🧩 Retain useful algorithms and preservation work from the earlier implementation.

## 💻 Platform targets

| Platform | Status |
| --- | --- |
| Ubuntu 26.04 LTS | Primary target |
| macOS | Planned, requires case-sensitive APFS |

⚠️ The GeoCities archive contains paths whose names differ only by case. A normal case-insensitive macOS volume is not suitable for reconstruction.

## 📦 The digital time capsules

The rebuild is intended to process these preserved collections:

- Archive Team GeoCities Snapshot
- GeoCities Chronomex
- GeoCities JCN Grab
- GeoCities Latecomer
- GeoCities Santiago Grab

Exact source manifests, checksums, and acquisition instructions will be documented as the modern pipeline is rebuilt.

## 📼 A little history

This repository derives from the GeoCities preservation work originally developed by Dragan Espenschied and other contributors to One Terabyte of Kilobyte Age.

Nix McRetro's 2022 reconstruction pipeline expanded that work to merge and process several Archive Team collections. Its full history, scripts, and Ubuntu 12.04 notes live in the [2022-archived branch](../../tree/2022-archived).

The main branch is a fresh modernisation effort started in 2026.

## ❤️ Preservation and licensing

Licensing and attribution from the original project and the 2022 implementation will be preserved as code is brought forward into the modern branch.

**The old web deserves a second life. 💾**
