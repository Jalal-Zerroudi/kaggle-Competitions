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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a deterministic SHA-256 manifest for competition data."
    )
    parser.add_argument("data_dir", type=Path, help="Directory containing local data files")
    parser.add_argument("output", type=Path, help="Manifest file to create")
    args = parser.parse_args()

    try:
        count = write_manifest(args.data_dir, args.output)
    except ValueError as error:
        parser.error(str(error))

    print(f"Wrote {count} checksums to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
