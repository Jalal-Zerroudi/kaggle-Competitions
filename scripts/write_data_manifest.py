#!/usr/bin/env python3
"""Write a deterministic SHA-256 manifest for a local competition dataset."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_manifest(data_dir: Path, output: Path) -> int:
    data_dir = data_dir.resolve()
    output = output.resolve()

    if not data_dir.is_dir():
        raise ValueError(f"Data directory does not exist: {data_dir}")

    files = sorted(
        path for path in data_dir.rglob("*")
        if path.is_file() and path.resolve() != output
    )
    if not files:
        raise ValueError(f"No files found under: {data_dir}")

    lines = [
        f"{sha256_file(path)}  {path.relative_to(data_dir).as_posix()}"
        for path in files
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(files)


def verify_manifest(data_dir: Path, manifest: Path) -> int:
    """Verify local files against a previously generated SHA-256 manifest."""
    data_dir = data_dir.resolve()
    manifest = manifest.resolve()

    if not data_dir.is_dir():
        raise ValueError(f"Data directory does not exist: {data_dir}")
    if not manifest.is_file():
        raise ValueError(f"Manifest file does not exist: {manifest}")

    entries = []
    for line_number, line in enumerate(
        manifest.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line:
            continue
        try:
            expected, relative_path = line.split("  ", 1)
        except ValueError as error:
            raise ValueError(f"Malformed manifest line {line_number}") from error

        if len(expected) != 64 or any(
            character not in "0123456789abcdefABCDEF" for character in expected
        ):
            raise ValueError(f"Invalid SHA-256 on manifest line {line_number}")

        path = (data_dir / relative_path).resolve()
        try:
            path.relative_to(data_dir)
        except ValueError as error:
            raise ValueError(
                f"Manifest path escapes the data directory: {relative_path}"
            ) from error

        if not path.is_file():
            raise ValueError(f"Manifest file is missing: {relative_path}")

        actual = sha256_file(path)
        if actual != expected.lower():
            raise ValueError(f"Checksum mismatch: {relative_path}")
        entries.append(relative_path)

    if not entries:
        raise ValueError(f"No checksum entries found in: {manifest}")

    listed_files = set(entries)
    actual_files = {
        path.relative_to(data_dir).as_posix()
        for path in data_dir.rglob("*")
        if path.is_file() and path.resolve() != manifest
    }
    unlisted_files = sorted(actual_files - listed_files)
    if unlisted_files:
        raise ValueError(f"Unlisted data file: {unlisted_files[0]}")

    return len(entries)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a deterministic SHA-256 manifest for competition data."
    )
    parser.add_argument("data_dir", type=Path, help="Directory containing local data files")
    parser.add_argument("output", type=Path, help="Manifest file to create or verify")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify data files against the existing manifest instead of writing it",
    )
    args = parser.parse_args()

    try:
        if args.check:
            count = verify_manifest(args.data_dir, args.output)
        else:
            count = write_manifest(args.data_dir, args.output)
    except ValueError as error:
        parser.error(str(error))

    action = "Verified" if args.check else "Wrote"
    print(f"{action} {count} checksums using {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
