"""Archive a real JSON check report. Preview by default, never commits or pushes."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


def archive(report_bytes, previous):
    report = json.loads(report_bytes.decode("utf-8-sig"))
    if report.get("schema") != 1 or report.get("exit_code") not in (0, 1, 2):
        raise ValueError("not a Harness check report")
    if report.get("mode") != "all" or not isinstance(report.get("findings"), list):
        raise ValueError("monthly archive requires an all-mode report")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T.+", report.get("scanned_at", "")):
        raise ValueError("report lacks scan timestamp")
    ident = hashlib.sha256(report_bytes).hexdigest()
    marker = "<!-- harness-report:" + ident + " -->"
    if marker in previous:
        return previous
    counts = {kind: sum(f.get("kind") == kind for f in report["findings"]) for kind in ("violation", "gap", "review")}
    record = "\n\n" + marker + "\n## " + report["scanned_at"] + "\n\n"
    record += "- 自动检查状态：" + report["status"] + "；退出码：" + str(report["exit_code"]) + "\n"
    record += "- 违规：%(violation)d；覆盖缺口：%(gap)d；人工复核：%(review)d。\n" % counts
    record += "- 报告 SHA256：" + ident + "\n"
    record += "- 版本基线：" + str(report.get("baseline", "unknown")) + "\n"
    record += "- 本记录不是整体规范验收结论；完整报告应保留为 CI artifact。\n"
    return previous.rstrip() + record


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True)
    parser.add_argument("--root", default=".")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        root = Path(args.root).resolve()
        target = (root / "QUALITY_SCORE.md").resolve()
        if not target.is_relative_to(root):
            raise ValueError("archive target escapes root")
        old = target.read_bytes().decode("utf-8") if target.exists() else "# Harness 检查归档\n"
        new = archive(Path(args.report).read_bytes(), old)
        if args.write and new != old:
            target.write_text(new, encoding="utf-8", newline="")
        print(new)
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
