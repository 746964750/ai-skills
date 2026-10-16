"""Collect staged, unstaged and untracked files without mutating Git state."""
import argparse
import json
from pathlib import Path
import subprocess
import sys


def git(root, *args):
    completed = subprocess.run(["git", "-C", str(root), *args], capture_output=True, timeout=30)
    if completed.returncode:
        raise RuntimeError(completed.stderr.decode("utf-8", "replace").strip())
    return completed.stdout.decode("utf-8", "surrogateescape")


def parse_status(data, scope):
    parts = data.split("\0")
    result = []
    i = 0
    while i < len(parts) and parts[i]:
        status = parts[i]
        i += 1
        old = parts[i]
        i += 1
        new = None
        if status[0] in ("R", "C"):
            new = parts[i]
            i += 1
        result.append(dict(scope=scope, status=status, path=new or old,
                           old_path=old if new else None))
    return result


def collect(root, base=None, target=None):
    git(root, "rev-parse", "--show-toplevel")
    if bool(base) != bool(target):
        raise ValueError("base and target must be supplied together")
    if base:
        # Resolve refs first; do not let ref-like strings become Git options.
        a = git(root, "rev-parse", "--verify", "--end-of-options", base + "^{commit}").strip()
        b = git(root, "rev-parse", "--verify", "--end-of-options", target + "^{commit}").strip()
        return parse_status(git(root, "diff", "--name-status", "-z", "--find-renames", a, b, "--"), "range")
    items = []
    items += parse_status(git(root, "diff", "--name-status", "-z", "--find-renames", "--"), "unstaged")
    items += parse_status(git(root, "diff", "--cached", "--name-status", "-z", "--find-renames", "--"), "staged")
    items += [dict(scope="untracked", status="?", path=p, old_path=None)
              for p in git(root, "ls-files", "--others", "--exclude-standard", "-z").split("\0") if p]
    return items


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--base")
    parser.add_argument("--target")
    args = parser.parse_args()
    try:
        items = collect(Path(args.root).resolve(), args.base, args.target)
        print(json.dumps(dict(git_available=True, changes=items), ensure_ascii=True, indent=2))
        return 0
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as exc:
        print(json.dumps(dict(git_available=False, error=str(exc), changes=None), ensure_ascii=True))
        return 2


if __name__ == "__main__":
    sys.exit(main())
