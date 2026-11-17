#!/usr/bin/env python3
"""Read-only Git and file snapshots for workflow handoffs; never an approval gate."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys


class EvidenceError(Exception):
    pass


def git(repo, *args):
    result = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True,
        env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
    )
    if result.returncode:
        raise EvidenceError(result.stderr.decode(errors="replace").strip())
    return result.stdout


def commit_sha(repo, ref):
    return git(repo, "rev-parse", "--verify", "--end-of-options",
               ref + "^{commit}").decode().strip()


def is_ancestor(repo, base, head):
    result = subprocess.run(
        ["git", "-C", str(repo), "merge-base", "--is-ancestor", base, head],
        capture_output=True, env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
    )
    if result.returncode not in (0, 1):
        raise EvidenceError(result.stderr.decode(errors="replace").strip())
    return result.returncode == 0


def records(raw):
    return [os.fsdecode(part) for part in raw.split(b"\0") if part]


def file_evidence(repo, name):
    relative = Path(name)
    if relative.is_absolute() or ".." in relative.parts or ".git" in relative.parts:
        raise EvidenceError(f"Not a repository-relative source path: {name}")
    path = repo / relative
    # Do not follow a parent symlink outside the checkout or hash its targets.
    if path.parent.resolve() != path.parent:
        raise EvidenceError(f"Symlinked parent is outside supported scope: {name}")
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        return {"kind": "missing"}
    if stat.S_ISLNK(mode):
        return {"kind": "symlink", "target": os.readlink(path)}
    if not stat.S_ISREG(mode):
        raise EvidenceError(f"Expected a file, not a directory/submodule/special file: {name}")
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return {"kind": "file", "sha256": digest.hexdigest(),
            "executable": bool(mode & 0o111)}


def read_state(repo, base, paths, remote_base):
    head = commit_sha(repo, "HEAD")
    remote_sha = commit_sha(repo, remote_base) if remote_base else None
    return {
        "repo": str(repo),
        "branch": git(repo, "rev-parse", "--abbrev-ref", "HEAD").decode().strip(),
        "base": base,
        "head": head,
        "base_is_ancestor": is_ancestor(repo, base, head),
        "remote_base_ref": remote_base,
        "remote_base_sha": remote_sha,
        "remote_base_is_ancestor": is_ancestor(repo, remote_sha, head) if remote_sha else None,
        # Whole-checkout status/index exposes unrelated staged work without claiming ownership.
        "status": records(git(repo, "status", "--porcelain=v1", "-z",
                              "--untracked-files=all", "--ignore-submodules=none")),
        "index": records(git(repo, "ls-files", "--stage", "-z")),
        "commits": git(repo, "rev-list", "--reverse", base + ".." + head).decode().splitlines(),
        "committed_paths": records(git(repo, "diff", "--no-ext-diff", "--no-textconv",
                                       "--name-only", "-z", base, head, "--")),
        "files": {name: file_evidence(repo, name) for name in paths},
    }


def capture(repo, base_ref, paths, remote_base=None):
    repo = Path(repo).resolve()
    root = Path(os.fsdecode(git(repo, "rev-parse", "--show-toplevel")).strip()).resolve()
    if root != repo:
        raise EvidenceError("--repo must be the checkout root")
    if not paths:
        raise EvidenceError("Select the files/contracts behind this evidence")
    paths = sorted(set(str(Path(path)) for path in paths))
    base = commit_sha(repo, base_ref)
    state = read_state(repo, base, paths, remote_base)
    if state != read_state(repo, base, paths, remote_base):
        raise EvidenceError("Checkout changed during capture; freeze writers and retry")
    return {"schema_version": 1, "captured_at": datetime.now(timezone.utc).isoformat(), **state}


def check(previous):
    if previous["schema_version"] != 1:
        raise EvidenceError("Unsupported evidence schema")
    current = capture(previous["repo"], previous["base"], list(previous["files"]),
                      previous["remote_base_ref"])
    changed = sorted(key for key in set(previous) | set(current)
                     if key != "captured_at" and previous.get(key) != current.get(key))
    return {"status": "changed" if changed else "unchanged", "changed_fields": changed,
            "note": "Snapshot comparison only; approval, freshness, ownership and readiness require coordinator checks."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    snapshot = commands.add_parser("snapshot")
    snapshot.add_argument("--repo", required=True)
    snapshot.add_argument("--base", required=True, help="Immutable ticket starting SHA")
    snapshot.add_argument("--remote-base", help="Locally fetched ref; this helper never fetches")
    snapshot.add_argument("--paths", nargs="+", required=True, help="Concrete relative file paths")
    verify = commands.add_parser("check")
    verify.add_argument("snapshot", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "snapshot":
            result = capture(args.repo, args.base, args.paths, args.remote_base)
        else:
            result = check(json.loads(args.snapshot.read_text()))
        print(json.dumps(result, indent=2, ensure_ascii=True))
        return 1 if result.get("status") == "changed" else 0
    except (EvidenceError, OSError, ValueError, KeyError, TypeError) as error:
        print(f"Evidence error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
