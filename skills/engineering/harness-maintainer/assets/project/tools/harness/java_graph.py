"""Java bytecode dependencies via the project's JDK jdeps; no regex source parser."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from check import inside, issue, run_command


def analyze(data):
    root = Path(data["root"]).resolve()
    config = data["config"]
    java = config.get("java", {})
    files = data["files"]
    result = dict(schema=1, files=files, edges=[], findings=[])
    if not java.get("class_dirs"):
        raise ValueError("Java class_dirs missing")
    if java.get("clean_build_confirmed") is not True:
        raise ValueError("Java build must be reviewed as full clean compile")
    started = time.time()
    run_command(java.get("build"), root)
    mapping = {}
    class_dirs = [inside(root, value) for value in java["class_dirs"]]
    source_roots = [inside(root, value) for value in config["source_roots"]]
    for directory in class_dirs:
        if not directory.is_dir():
            raise ValueError("class directory missing: " + str(directory))
        for compiled in directory.rglob("*.class"):
            inside(root, compiled.relative_to(root))
            if compiled.stat().st_mtime < started - 3:
                raise ValueError("stale class file; build did not recreate all classes: " + str(compiled))
            stem = compiled.relative_to(directory).with_suffix("").as_posix()
            simple = stem.split("$", 1)[0] + ".java"
            candidates = [d / simple for d in source_roots if (d / simple).is_file()]
            if len(candidates) != 1:
                raise ValueError("class cannot be mapped uniquely to source: " + stem)
            class_name = stem.replace("/", ".")
            if class_name in mapping:
                raise ValueError("duplicate class across build modules: " + class_name)
            mapping[class_name] = candidates[0].relative_to(root).as_posix()
    covered = set(mapping.values())
    missing = set(files) - covered
    if missing or not mapping:
        raise ValueError("compiled source coverage incomplete: " + ", ".join(sorted(missing)))
    if covered - set(files):
        raise ValueError("compiled code excluded from source manifest")
    classpath = [str(d) for d in class_dirs]
    classpath.extend(str(inside(root, p)) for p in java.get("classpath", []))
    command = [java.get("jdeps", "jdeps"), "-cp", os.pathsep.join(classpath),
               "-verbose:class", "-filter:none", *[str(d) for d in class_dirs]]
    output = run_command(command, root)
    parsed = 0
    current_source = None
    for line in output.splitlines():
        match = re.match(r"^\s+([\w.$]+)\s+->\s+([\w.$]+)\s+", line)
        if match:
            source, target = match.groups()
        else:
            header = re.match(r"^\s+([\w.$]+)\s+\(", line)
            if header:
                current_source = header[1]
            dependency = re.match(r"^\s+->\s+([\w.$]+)(?:\s|$)", line)
            if not dependency or not current_source:
                continue
            source, target = current_source, dependency[1]
        if source not in mapping:
            continue
        parsed += 1
        result["edges"].append({"from": mapping[source], "to": mapping.get(target, "external:" + target), "line": 0})
    if not parsed:
        raise ValueError("jdeps output contained no recognized class dependencies")
    if re.search(r"\bnot found\b", output):
        result["findings"].append(issue("gap", "JAVA-CLASSPATH", "jdeps reports missing dependencies; supply java.classpath"))
    return result


def main():
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")
        sys.stdout.reconfigure(encoding="utf-8")
    data = json.load(sys.stdin)
    try:
        result = analyze(data)
    except (OSError, ValueError, RuntimeError, KeyError, subprocess.SubprocessError) as exc:
        result = dict(schema=1, files=data["files"], edges=[], findings=[issue("gap", "JAVA-ERROR", str(exc))])
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
