"""Read-only Harness checks. Configured commands require --run-adapters."""
import argparse
from datetime import datetime, timezone
import fnmatch
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

CORE = {
    "AGENTS.md": ["任务执行前的必读顺序", "工程结构", "业务模块地图", "技术栈", "核心入口", "不确定时", "禁止事项", "任务收尾与文档同步"],
    "docs/architecture.md": ["顶层目录模型", "分层职责", "业务模块", "运行时模型", "状态管理", "接口层", "渲染与扩展", "关键架构约束", "CI/CD 与部署", "强制执行"],
    "docs/conventions.md": ["目录结构约定", "命名约定", "分层职责矩阵", "组件与服务规范", "路由与入口规范", "状态与事务规范", "接口与请求规范", "国际化", "Mixin Hook 与扩展点", "样式规范", "Lint 规则", "注释与日志", "Git 与 PR", "性能与可访问性"],
    "docs/domain.md": ["领域全景", "核心业务实体", "状态机", "核心业务流程", "业务规则速查", "枚举集中位置", "外部系统集成"],
    "docs/golden-rules.md": ["上下文工程原则", "架构约束原则", "熵治理原则", "反模式清单", "任务执行清单", "跨模块改动审批门槛", "文档同步义务", "维护节奏"],
}
EXTENSIONS = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".java"}
DEFAULT_EXCLUDE = ["node_modules", "target", "dist", "build", ".git", ".gradle", ".idea"]
HERE = Path(__file__).resolve().parent


def inside(root, value):
    path = (root / value).resolve()
    if not path.is_relative_to(root):
        raise ValueError("path escapes root: " + str(value))
    return path


def issue(kind, rule, message, path="", line=0):
    return dict(kind=kind, rule=rule, message=message, path=path, line=line)


def excluded(rel, patterns):
    path = Path(rel)
    candidates = [path.as_posix()] + [p.as_posix() for p in path.parents if str(p) != "."]
    return any(fnmatch.fnmatchcase(c, p) for c in candidates for p in patterns)


def sources(root, config):
    roots = config.get("source_roots")
    if not isinstance(roots, list) or not roots:
        raise ValueError("source_roots must contain existing source directories")
    patterns = config.get("exclude", [])
    if not isinstance(patterns, list) or not all(isinstance(x, str) for x in patterns):
        raise ValueError("exclude must be a list of glob strings")
    found = set()
    for value in roots:
        directory = inside(root, value)
        if not directory.is_dir():
            raise ValueError("source root missing: " + value)
        for parent, dirs, names in os.walk(directory, followlinks=False):
            dirs[:] = [d for d in dirs if d not in DEFAULT_EXCLUDE and not excluded(
                (Path(parent) / d).relative_to(root).as_posix(), patterns)]
            for name in names:
                path = Path(parent) / name
                rel = path.relative_to(root).as_posix()
                if path.suffix in EXTENSIONS and not excluded(rel, patterns):
                    inside(root, rel)
                    found.add(rel)
    if not found:
        raise ValueError("no supported source files found; empty scan is not a pass")
    return sorted(found)


def load_config(root, name):
    config = json.loads(inside(root, name).read_text(encoding="utf-8-sig"))
    if not isinstance(config, dict) or config.get("schema") != 1:
        raise ValueError("configuration requires schema=1")
    if config.get("stack") not in ("frontend", "java", "mixed", "other"):
        raise ValueError("invalid stack")
    return config


def docs(root, config):
    findings = []
    owner = config.get("owner", {})
    for key in ("name", "wechat", "account"):
        if not isinstance(owner.get(key), str) or not owner[key].strip() or re.search(r"待确认|\{\{", owner[key]):
            findings.append(issue("gap", "OWNER", "Missing confirmed owner " + key))
    for name, default_sections in CORE.items():
        path = inside(root, name)
        if not path.is_file():
            findings.append(issue("violation", "DOC-MISSING", "Required document missing", name))
            continue
        content = path.read_text(encoding="utf-8-sig")
        plain = re.sub(r"(?ms)^([ \t]*)(\x60{3,}|~{3,})[^\n]*\n.*?^\1\2[ \t]*$", lambda m: re.sub(r"[^\n]", " ", m[0]), content)
        sections = config.get("doc_sections", {}).get(name, default_sections)
        if not isinstance(sections, list) or not sections or not all(isinstance(s, str) and s for s in sections):
            raise ValueError("doc_sections entries must be nonempty title lists")
        headings = list(re.finditer(r"(?m)^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$", plain))
        for title in sections:
            matches = [m for m in headings if re.sub(r"^\d+(?:\.\d+)*[.、\s]+", "", m[2]) == title]
            if not matches:
                findings.append(issue("violation", "DOC-SECTION", "Missing section: " + title, name))
            else:
                start = matches[0].end()
                end = next((m.start() for m in headings if m.start() > start and len(m[1]) <= len(matches[0][1])), len(plain))
                if not content[start:end].strip():
                    findings.append(issue("violation", "DOC-EMPTY", "Empty section: " + title, name))
        if re.search(r"\{\{[^}]*\}\}|待确认|待补充", content):
            findings.append(issue("gap", "DOC-PENDING", "Unresolved evidence or template placeholders", name))
        if name == "AGENTS.md":
            for key in ("name", "wechat", "account"):
                if owner.get(key) and owner[key] not in content:
                    findings.append(issue("gap", "OWNER-DOC", "Owner not reflected in AGENTS: " + key, name))
            order = [content.find("docs/" + f) for f in ("architecture.md", "conventions.md", "domain.md", "golden-rules.md")]
            if -1 in order or order != sorted(order):
                findings.append(issue("violation", "DOC-ORDER", "Required reading order missing or inconsistent", name))
        targets = re.findall(r"!?\[[^\]]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+\"[^\"]*\")?\s*\)", plain)
        targets += re.findall(r"(?m)^\s*\[[^\]]+\]:\s*(<[^>]+>|\S+)", plain)
        for target in targets:
            target = target.strip("<>")
            parts = urlsplit(target)
            if parts.scheme or target.startswith(("#", "//")):
                continue
            local = unquote(parts.path)
            if not local:
                continue
            candidate = (path.parent / local).resolve()
            if not candidate.is_relative_to(root) or not candidate.exists():
                findings.append(issue("violation", "DOC-LINK", "Broken or escaping local link: " + target, name))
    return findings


def run_command(command, root, payload=None):
    if not isinstance(command, list) or not command or not all(isinstance(x, str) and x for x in command):
        raise ValueError("command must be a nonempty argument array")
    result = subprocess.run(command, cwd=root, input=payload, text=True, encoding="utf-8",
                            errors="replace", capture_output=True, timeout=300, shell=False)
    if result.returncode:
        raise RuntimeError("command failed (%s): %s\n%s" % (result.returncode, command, result.stderr[-3000:] + result.stdout[-3000:]))
    return result.stdout


def adapter(root, config, files, language, enabled):
    if not files:
        return {"files": [], "edges": [], "findings": []}
    if not enabled:
        raise ValueError("adapters not executed; review commands then use --run-adapters")
    if language == "frontend":
        command = [config.get("frontend", {}).get("node", "node"), str(HERE / "frontend.cjs")]
    else:
        command = [sys.executable, "-X", "utf8", str(HERE / "java_graph.py")]
    payload = json.dumps(dict(root=str(root), files=files, config=config), ensure_ascii=False)
    result = json.loads(run_command(command, root, payload))
    if result.get("schema") != 1 or sorted(result.get("files", [])) != sorted(files):
        raise ValueError(language + " adapter did not cover exactly the requested files")
    if not isinstance(result.get("edges"), list) or not isinstance(result.get("findings"), list):
        raise ValueError("invalid adapter output")
    return result


def architecture(root, config, files, results):
    findings = []
    rules = config.get("architecture", {}).get("rules")
    if not isinstance(rules, list) or not rules:
        raise ValueError("at least one confirmed architecture rule required")
    seen = set()
    for rule in rules:
        if not all(isinstance(rule.get(k), str) and rule[k] for k in ("id", "from", "to", "reason")) or rule.get("confirmed") is not True:
            raise ValueError("incomplete/unconfirmed architecture rule")
        if rule["id"] in seen:
            raise ValueError("duplicate rule id")
        seen.add(rule["id"])
        for side in ("from", "to"):
            if not any(fnmatch.fnmatchcase(f, rule[side]) for f in files):
                findings.append(issue("gap", "ARCH-SCOPE", rule["id"] + ": pattern matches no source: " + side))
        for result in results:
            for edge in result["edges"]:
                source, target = edge["from"], edge["to"]
                if source not in files or (not target.startswith("external:") and target not in files):
                    raise ValueError("dependency outside scanned source scope: " + source + " -> " + target)
                if fnmatch.fnmatchcase(source, rule["from"]) and fnmatch.fnmatchcase(target, rule["to"]):
                    findings.append(issue("violation", rule["id"], source + " -> " + target, source, edge.get("line", 0)))
    return findings


def entropy(root, config, files, enabled):
    settings = config.get("entropy", {})
    limit = settings.get("max_file_lines")
    if settings.get("confirmed") is not True or type(limit) is not int or limit < 1:
        raise ValueError("confirmed positive entropy.max_file_lines required")
    findings = []
    for name in files:
        lines = inside(root, name).read_text(encoding="utf-8-sig").splitlines()
        if len(lines) > limit:
            findings.append(issue("violation", "ENT-FILE", "File lines %d > %d" % (len(lines), limit), name))
    if any(f.endswith(".java") for f in files):
        java = config.get("java", {})
        if java.get("entropy_coverage_confirmed") is not True:
            raise ValueError("Java Checkstyle/PMD rule coverage not confirmed")
        if not enabled:
            raise ValueError("Java entropy command not executed")
        run_command(java.get("entropy_command"), root)
    return findings


def execute(root, config, mode, enabled):
    findings = []
    if mode in ("docs", "all"):
        findings.extend(docs(root, config))
    if mode == "docs":
        return findings
    stack = config.get("stack")
    if stack == "other":
        return findings + [issue("gap", "UNSUPPORTED", "Code checks do not support this stack")]
    files = sources(root, config)
    java_files = [f for f in files if f.endswith(".java")]
    frontend_files = [f for f in files if not f.endswith(".java")]
    if (java_files and stack == "frontend") or (frontend_files and stack == "java"):
        raise ValueError("stack setting omits detected language")
    results = []
    for language, subset in (("frontend", frontend_files), ("java", java_files)):
        if subset and (language == "frontend" or mode in ("architecture", "all")):
            try:
                result = adapter(root, config, subset, language, enabled)
                results.append(result)
                findings.extend(f for f in result["findings"] if mode != "architecture" or not f["rule"].startswith("ENT-"))
            except (OSError, ValueError, RuntimeError, KeyError, TypeError, subprocess.SubprocessError) as exc:
                findings.append(issue("gap", "ADAPTER-ERROR", language + ": " + str(exc)))
    if mode in ("architecture", "all"):
        try:
            findings.extend(architecture(root, config, files, results))
        except (OSError, ValueError, KeyError, TypeError) as exc:
            findings.append(issue("gap", "ARCH-ERROR", str(exc)))
    if mode in ("entropy", "all"):
        try:
            findings.extend(entropy(root, config, files, enabled))
        except (OSError, ValueError, RuntimeError, KeyError, TypeError, subprocess.SubprocessError) as exc:
            findings.append(issue("gap", "ENTROPY-ERROR", str(exc)))
    return findings


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["docs", "architecture", "entropy", "all"])
    parser.add_argument("--root", default=".")
    parser.add_argument("--config", default="harness.config.json")
    parser.add_argument("--run-adapters", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    try:
        findings = execute(root, load_config(root, args.config), args.mode, args.run_adapters)
    except (OSError, ValueError, RuntimeError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        findings = [issue("gap", "CHECK-ERROR", str(exc))]
    code = 2 if any(f["kind"] in ("gap", "review") for f in findings) else (1 if findings else 0)
    try:
        baseline = run_command(["git", "rev-parse", "HEAD"], root).strip()
        if run_command(["git", "status", "--porcelain"], root).strip():
            baseline += " (dirty)"
    except (OSError, RuntimeError, subprocess.SubprocessError):
        baseline = "unavailable"
    report = dict(schema=1, mode=args.mode, root=str(root), exit_code=code,
                  scanned_at=datetime.now(timezone.utc).isoformat(), baseline=baseline,
                  status="passed" if code == 0 else "failed",
                  scope="automated checks only; semantic and remote acceptance required",
                  findings=findings)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
