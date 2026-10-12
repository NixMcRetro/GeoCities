"""Small-corpus inventory CLI. Never modifies the source tree."""

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tomllib


class InputError(Exception):
    """Expected validation error, reported without a traceback."""


def source_directory(raw):
    if not raw:
        raise InputError("Provide --source or [paths].source in --config.")
    path = Path(raw).expanduser()
    if path.is_symlink():
        raise InputError("Source root may not be a symlink.")
    try:
        root = path.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise InputError(f"Cannot resolve source: {exc}") from exc
    if root == Path(root.anchor) or not root.is_dir():
        raise InputError("Source must be an existing directory other than filesystem root.")
    return root


def within(path, root):
    return path == root or root in path.parents


def load_settings(filename):
    if not filename:
        return {}, {}
    try:
        with open(filename, "rb") as stream:
            data = tomllib.load(stream)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise InputError(f"Cannot load config: {exc}") from exc
    paths, limits = data.get("paths", {}), data.get("limits", {})
    if not isinstance(paths, dict) or not isinstance(limits, dict):
        raise InputError("Config [paths] and [limits] must be tables.")
    return paths, limits


def file_digest(path):
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    with os.fdopen(fd, "rb") as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode):
            raise InputError(f"File changed type during scan: {path}")
        digest = hashlib.sha256()
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
        after = os.fstat(stream.fileno())
        if before.st_size != after.st_size or before.st_mtime_ns != after.st_mtime_ns:
            raise InputError(f"File changed while hashing: {path}")
        return digest.hexdigest(), after.st_size


def inventory(root, max_entries=10000):
    if type(max_entries) is not int or max_entries < 1:
        raise InputError("max_entries must be a positive integer.")
    records = []
    def walk_error(exc):
        raise InputError(f"Cannot inspect directory: {exc}") from exc

    for current, dirs, files in os.walk(root, topdown=True, followlinks=False, onerror=walk_error):
        dirs.sort()
        files.sort()
        for name in sorted(dirs + files):
            path = Path(current) / name
            rel = path.relative_to(root).as_posix()
            info = path.lstat()
            row = {
                "path": rel,
                "path_bytes_base64": base64.b64encode(os.fsencode(rel)).decode("ascii"),
                "mtime_ns": info.st_mtime_ns,
            }
            if stat.S_ISLNK(info.st_mode):
                row["type"] = "symlink"
                row["target_bytes_base64"] = base64.b64encode(
                    os.fsencode(os.readlink(path))
                ).decode("ascii")
            elif stat.S_ISREG(info.st_mode):
                row["type"] = "file"
                row["sha256"], row["size"] = file_digest(path)
            elif stat.S_ISDIR(info.st_mode):
                row["type"] = "directory"
            else:
                row["type"] = "special"
            records.append(row)
            if len(records) > max_entries:
                raise InputError(
                    f"Entry limit of {max_entries} exceeded. "
                    "This pilot scanner is not for the full archive."
                )
    records.sort(key=lambda item: os.fsencode(item["path"]))
    groups = {}
    for row in records:
        groups.setdefault(row["path"].casefold(), []).append(row["path"])
    collisions = [sorted(group) for group in groups.values() if len(group) > 1]
    collisions.sort(key=lambda group: group[0])
    return {
        "format_version": 1,
        "source": str(root),
        "entry_count": len(records),
        "casefold_collisions": collisions,
        "entries": records,
    }


def preflight(root, paths):
    checks = {"source": str(root), "source_exists": True, "source_is_symlink": False}
    for key in ("work", "archive"):
        raw = paths.get(key)
        if not raw:
            continue
        destination = Path(raw).expanduser().resolve(strict=False)
        if within(destination, root):
            raise InputError(f"{key} cannot be inside the read-only source.")
        checks[key] = str(destination)
    if sys.platform.startswith("linux"):
        result = subprocess.run(
            ["stat", "-f", "-c", "%T", str(root)],
            capture_output=True, text=True, check=False
        )
        checks["source_filesystem"] = result.stdout.strip() if result.returncode == 0 else "unknown"
        if checks["source_filesystem"] in ("exfat", "vfat", "fuseblk", "ntfs"):
            checks["filesystem_warning"] = "Check case sensitivity and Unix filename semantics."
    return checks


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", help="Local TOML configuration file")
    sub = parser.add_subparsers(dest="command", required=True)
    pf = sub.add_parser("preflight", help="Read-only path and filesystem checks")
    pf.add_argument("--source")
    pf.add_argument("--work")
    pf.add_argument("--archive")
    scan = sub.add_parser("scan", help="Read-only, capped SHA-256 inventory")
    scan.add_argument("--source")
    scan.add_argument("--output", help="New JSON manifest outside source; never overwrites")
    scan.add_argument("--max-entries", type=int, help="Pilot inventory safety limit")
    args = parser.parse_args(argv)
    try:
        paths, limits = load_settings(args.config)
        root = source_directory(args.source or paths.get("source"))
        if args.command == "preflight":
            checks = dict(paths)
            checks.update({key: getattr(args, key) for key in ("work", "archive") if getattr(args, key)})
            result = preflight(root, checks)
        else:
            limit = args.max_entries if args.max_entries is not None else limits.get("max_entries", 10000)
            result = inventory(root, limit)
            if args.output:
                output = Path(args.output).expanduser().resolve(strict=False)
                if within(output, root):
                    raise InputError("Manifest output must be outside the source tree.")
                serialized = json.dumps(result, indent=2, ensure_ascii=True, sort_keys=True) + "\n"
                try:
                    with output.open("x", encoding="utf-8") as stream:
                        stream.write(serialized)
                except FileExistsError as exc:
                    raise InputError("Manifest exists; refusing to overwrite it.") from exc
                print(f"Created manifest: {output} ({result['entry_count']} entries)")
                return 0
        print(json.dumps(result, indent=2, ensure_ascii=True, sort_keys=True))
        return 0
    except (InputError, OSError) as exc:
        print(f"geocities-rebuild: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
