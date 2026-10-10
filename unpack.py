#!/usr/bin/env python3
"""Unpack the CACTUS-speaks Zenodo download into the original folder layout and verify checksums.

Put this script next to the downloaded files and run:

    python3 unpack.py                 # unpack here, then verify
    python3 unpack.py --out DIR       # unpack into DIR instead
    python3 unpack.py --delete-zips   # remove each zip after it has been extracted

It needs only Python 3.8+ (standard library), so it works on Linux, macOS and Windows.

Steps
  1. If SHA256SUMS_zips.txt is present, checks every downloaded file against it (skip with --skip-zip-check).
  2. Extracts <corpus>_<part>[.partNN].zip into <corpus>/<part>/, e.g. D1_CactusVoice_audio.part01.zip ->
     D1_CactusVoice/audio/ (all parts of one folder unpack into the same place).
     analysis.zip -> analysis/.
  3. Copies human_evaluation_ratings.csv and human_evaluation_sessions.csv into human_evaluation/.
  4. Verifies every file listed in SHA256SUMS_metadata.txt and reports any mismatch.
Files that are missing are reported, so a partial download (e.g. only the meta zips) can still be checked.
"""
import argparse
import hashlib
import os
import re
import shutil
import sys
import zipfile
from pathlib import Path

PART = re.compile(r"^(D\d_[A-Za-z]+)_(audio|meta|turns|voice_seeds|tags)(\.part\d+)?\.zip$")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def check(sums, root):
    """Verify '<sha256>  <relative path>' lines; return (ok, bad, missing)."""
    ok, bad, missing = 0, [], []
    for line in sums.read_text().splitlines():
        if not line.strip():
            continue
        digest, rel = line.split(None, 1)
        p = root / rel.strip()
        if not p.exists():
            missing.append(rel)
        elif sha256(p) == digest:
            ok += 1
        else:
            bad.append(rel)
    return ok, bad, missing


def extract(zpath, dest):
    dest.mkdir(parents=True, exist_ok=True)
    root = dest.resolve()
    with zipfile.ZipFile(zpath) as z:
        for name in z.namelist():  # refuse entries that would land outside dest
            if os.path.commonpath([root, (root / name).resolve()]) != str(root):
                sys.exit(f"unsafe path {name!r} in {zpath.name}")
        z.extractall(dest)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", type=Path, default=Path(__file__).resolve().parent, help="folder with the downloaded files")
    ap.add_argument("--out", type=Path, default=None, help="where to unpack (default: --src)")
    ap.add_argument("--delete-zips", action="store_true", help="delete each zip after successful extraction")
    ap.add_argument("--skip-zip-check", action="store_true", help="do not verify the downloads against SHA256SUMS_zips.txt")
    a = ap.parse_args()
    src, out = a.src.resolve(), (a.out or a.src).resolve()
    out.mkdir(parents=True, exist_ok=True)

    zsums = src / "SHA256SUMS_zips.txt"
    if zsums.exists() and not a.skip_zip_check:
        print("Checking downloaded files against SHA256SUMS_zips.txt (this reads ~42 GB) ...", flush=True)
        ok, bad, missing = check(zsums, src)
        print(f"  {ok} ok, {len(bad)} corrupted, {len(missing)} not downloaded")
        if bad:
            sys.exit("Corrupted download, please re-download: " + ", ".join(bad))

    zips = sorted(src.glob("*.zip"))
    for z in zips:
        m = PART.match(z.name)
        if m:
            dest = out / m.group(1)
        elif z.name == "analysis.zip":
            dest = out
        else:
            print(f"  skipping unknown archive {z.name}")
            continue
        print(f"Extracting {z.name} -> {dest.relative_to(out) if dest != out else '.'}/", flush=True)
        extract(z, dest)
        if a.delete_zips:
            z.unlink()

    he = out / "human_evaluation"
    for name in ("ratings.csv", "sessions.csv"):
        f = src / f"human_evaluation_{name}"
        if f.exists():
            he.mkdir(exist_ok=True)
            shutil.copy2(f, he / name)
    for name in ("benchmark_split.jsonl", "stats.json", "README.md", "SHA256SUMS_metadata.txt"):
        if (src / name).exists() and src != out:
            shutil.copy2(src / name, out / name)

    msums = out / "SHA256SUMS_metadata.txt"
    if not msums.exists():
        sys.exit("SHA256SUMS_metadata.txt not found; cannot verify.")
    print("Verifying SHA256SUMS_metadata.txt ...", flush=True)
    ok, bad, missing = check(msums, out)
    print(f"  {ok} ok, {len(bad)} mismatched, {len(missing)} missing")
    for rel in bad[:20]:
        print("  MISMATCH", rel)
    if missing:
        print("  missing files come from zips that were not downloaded, e.g.", missing[0])
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
