# Reconstruction roadmap

## Scope of this branch

This branch bootstraps an auditable modernisation of the historical
`despens/Geocities` pipeline. It is not yet a replacement for the complete
Archive Team restoration tools. The historical implementation stays on
`2022-archived` and must not be modified.

## Milestone 1: small-corpus foundation

- Read-only preflight that rejects missing or unsafe source roots.
- A fixture with case collisions, unusual filenames and a symlink loop.
- Capped, non-destructive SHA-256 inventory, including original path bytes.
- Collision reporting without deleting or renaming files.
- A new-file-only manifest writer refusing output inside the source.
- CI on Ubuntu 24.04 and 26.04 using disposable fixture data.

The inventory has a default 10,000-entry cap and holds its records in memory.
It must not be used against the full collection.

## Later milestones (not yet implemented)

1. Inventory source collections with verified archival checksums and metadata.
2. Stream inventories to SQLite/PostgreSQL with checkpoints and resuming.
3. Safely extract 7z/tar sources with path traversal, symlink, hardlink,
   special-file and archive bomb protections.
4. Preserve all conflicting variants and document merge precedence.
5. Port or replace legacy Perl filename routines using golden fixtures.
6. Add PostgreSQL migrations and safe credentials; never use trust auth or
   application superuser access.
7. Restore historic URL routing with isolated static serving, not an open proxy.
8. Benchmark batches and plan storage before a full-corpus run.

## Data preservation contract

- Treat originals as immutable.
- Never execute scripts from archived GeoCities pages.
- Never silently discard duplicate or conflicting versions.
- Destructive operations require a separately reviewed implementation,
  a dry-run report and explicit approval before use.
- Do not commit torrent contents, reconstructed sites, databases or secrets.
