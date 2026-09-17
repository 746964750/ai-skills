"""Preview/apply explicit Markdown sections, preserving manual text; optimistic locking."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile


def digest(data):
    return hashlib.sha256(data).hexdigest()


def prepare(root, entry):
    path = (root / entry["path"]).resolve()
    if not path.is_relative_to(root) or path.suffix.lower() != ".md":
        raise ValueError("only Markdown targets inside root are allowed")
    old = path.read_bytes() if path.exists() else None
    expected = entry.get("expected_sha256")
    if (old is None and expected is not None) or (old is not None and digest(old) != expected):
        raise ValueError("content changed or expected_sha256 absent: " + entry["path"])
    if old is None:
        if not isinstance(entry.get("content"), str):
            raise ValueError("new file requires explicit complete content")
        text = entry["content"]
    else:
        if "content" in entry:
            raise ValueError("whole-file overwrite is not supported for existing documents")
        text = old.decode("utf-8")
        newline = "\r\n" if "\r\n" in text else "\n"
        seen = set()
        for section in entry.get("sections", []):
            ident = section["id"]
            if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", ident) or ident in seen:
                raise ValueError("invalid/duplicate section id")
            seen.add(ident)
            start = "<!-- harness:" + ident + ":start -->"
            end = "<!-- harness:" + ident + ":end -->"
            body = section["content"]
            if "<!-- harness:" in body:
                raise ValueError("nested managed markers are not supported")
            body = body.replace("\r\n", "\n").replace("\n", newline).rstrip()
            replacement = start + newline + body + newline + end
            if text.count(start) == 0 and text.count(end) == 0:
                if entry.get("allow_append") is not True:
                    raise ValueError("section missing; review existing prose before explicit append")
                text = text.rstrip("\r\n") + newline * 2 + replacement + newline
            elif text.count(start) != 1 or text.count(end) != 1 or text.index(end) < text.index(start):
                raise ValueError("ambiguous or malformed managed region")
            else:
                left, right = text.index(start), text.index(end) + len(end)
                if "<!-- harness:" in text[left + len(start):text.index(end)]:
                    raise ValueError("overlapping managed sections")
                text = text[:left] + replacement + text[right:]
    return path, old, text.encode("utf-8")


def apply_plan(root, entries, write=False):
    if not isinstance(entries, list):
        raise ValueError("plan must be a JSON array")
    prepared = [prepare(root, e) for e in entries]
    if len({p for p, _, _ in prepared}) != len(prepared):
        raise ValueError("duplicate targets")
    result = []
    for path, old, new in prepared:
        changed = old != new
        if write and changed:
            current = path.read_bytes() if path.exists() else None
            if current != old:
                raise ValueError("concurrent change before write: " + str(path))
            path.parent.mkdir(parents=True, exist_ok=True)
            fd, temp = tempfile.mkstemp(prefix=".harness-", dir=path.parent)
            try:
                with os.fdopen(fd, "wb") as handle:
                    handle.write(new)
                if (path.read_bytes() if path.exists() else None) != old:
                    raise ValueError("concurrent change before replacement")
                os.replace(temp, path)
            finally:
                if os.path.exists(temp):
                    os.unlink(temp)
        result.append(dict(path=path.relative_to(root).as_posix(), changed=changed,
                           written=write and changed, sha256=digest(new)))
    return result


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--plan", required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        entries = json.loads(Path(args.plan).read_text(encoding="utf-8-sig"))
        result = apply_plan(Path(args.root).resolve(), entries, args.write)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())
