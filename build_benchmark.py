#!/usr/bin/env python3
"""Build a deduplicated PB benchmark from the normalized competition archives.

Instances are grouped by the category directory in each archive (DEC-LIN,
OPT-LIN, DEC-NLC, OPT-NLC, WBO, ...). Two files are the same instance when
the non-comment lines of the decompressed instance are identical. The copy
kept is the one from the earliest archive in competition order.
"""

from __future__ import annotations

import hashlib
import io
import lzma
import os
import sys
import tarfile
from pathlib import Path

ROOT = Path("/home/soh/02_prog/pb")
SRC = ROOT / "src-archives"
OUT = ROOT / "benchmarks"

# Earliest source wins on a content collision.
ARCHIVES = [
    "normalized-PB06.tar",
    "normalized-PB07.tar",
    "normalized-PB09.tar",
    "normalized-PB10.tar",
    "normalized-PB11.tar",
    "normalized-PB12.tar",
    "normalized-extraPB12.tar",
    "normalized-PB15eval.tar",
    "normalized-PB16.tar",
    "normalized-PB24.tar",
    "normalized-PB25.tar",
    "normalized-PB26.tar",
    "normalized-WBO.tar",
]

INSTANCE_SUFFIXES = (".opb.xz", ".opb", ".wbo.xz", ".wbo")


def category_of(parts: tuple[str, ...]) -> str | None:
    # Prefer the track directory. normalized-WBO.tar wraps PARTIAL-LIN and
    # SOFT-LIN under a WBO/ directory, so WBO itself is not a category.
    for part in parts:
        if part.startswith(("DEC-", "OPT-", "PARTIAL-", "SOFT-", "PBS", "PBO")):
            return part
    return None


def body_digest(data: bytes) -> str:
    h = hashlib.sha256()
    for line in data.splitlines():
        if line.startswith(b"*") or not line.strip():
            continue
        h.update(line)
        h.update(b"\n")
    return h.hexdigest()


def decompress(name: str, raw: bytes) -> bytes:
    if name.endswith(".xz"):
        return lzma.decompress(raw)
    return raw


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    seen: dict[str, str] = {}
    kept = 0
    dup = 0
    skipped = 0
    manifest = OUT / "manifest.tsv"
    duplog = OUT / "duplicates.tsv"

    with manifest.open("w", encoding="utf-8") as man, duplog.open("w", encoding="utf-8") as dups:
        man.write("status\tcategory\tsha256\tkept_path\tsource_archive\tsource_member\n")
        dups.write("sha256\tkept_path\tduplicate_archive\tduplicate_member\n")

        for archive_name in ARCHIVES:
            path = SRC / archive_name
            if not path.is_file():
                print(f"missing {path}", file=sys.stderr)
                return 1
            print(f"scanning {archive_name}", flush=True)
            with tarfile.open(path, "r:") as tar:
                for member in tar:
                    if not member.isfile():
                        continue
                    name = member.name
                    if not name.endswith(INSTANCE_SUFFIXES):
                        skipped += 1
                        continue
                    parts = tuple(p for p in name.split("/") if p and p != ".")
                    category = category_of(parts)
                    if category is None:
                        print(f"no category: {archive_name}:{name}", file=sys.stderr)
                        skipped += 1
                        continue
                    raw = tar.extractfile(member).read()
                    digest = body_digest(decompress(name, raw))
                    rel_under_cat = "/".join(parts[parts.index(category) + 1 :])
                    dest_rel = f"{category}/{archive_name.removesuffix('.tar')}/{rel_under_cat}"
                    if digest in seen:
                        dup += 1
                        dups.write(f"{digest}\t{seen[digest]}\t{archive_name}\t{name}\n")
                        man.write(
                            f"duplicate\t{category}\t{digest}\t{seen[digest]}\t{archive_name}\t{name}\n"
                        )
                        continue
                    dest = OUT / dest_rel
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(raw)
                    seen[digest] = dest_rel
                    kept += 1
                    man.write(f"kept\t{category}\t{digest}\t{dest_rel}\t{archive_name}\t{name}\n")
                    if kept % 2000 == 0:
                        print(f"  kept={kept} dup={dup}", flush=True)

    print(f"kept={kept} duplicates={dup} skipped={skipped}")
    counts: dict[str, int] = {}
    for rel in seen.values():
        cat = rel.split("/", 1)[0]
        counts[cat] = counts.get(cat, 0) + 1
    for cat in sorted(counts):
        print(f"  {cat}: {counts[cat]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
