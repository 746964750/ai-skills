"""Deterministic and real-adapter regression tests; all mutations stay in temp dirs."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

BASE = Path(__file__).resolve().parents[1]
TOOLS = BASE / "assets/project/tools/harness"
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(BASE / "scripts"))
import check
import changes
import merge_sections
import archive_quality
import java_graph


class Workspace(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="harness-中文-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.config = json.loads((BASE / "assets/project/harness.config.json").read_text(encoding="utf-8"))
        self.config["owner"] = dict(name="测试负责人", wechat="test-owner", account="@test-owner")
        self.config["entropy"]["confirmed"] = True
        self.config["frontend"]["resolution_reviewed"] = True
        self.config["architecture"]["rules"][0]["confirmed"] = True

    def put(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def source_pair(self):
        self.put("src/store/a.ts", "export const value = 1;\n")
        self.put("src/views/a.ts", "export const view = 2;\n")

    def documents(self):
        for name in check.CORE:
            template = (BASE / "assets/documents" / Path(name).name).read_text(encoding="utf-8")
            import re
            text = re.sub(r"\{\{.*?\}\}", "已核实的项目事实，来源 src/store/a.ts。", template)
            if name == "AGENTS.md":
                text += "\n测试负责人 test-owner @test-owner\n"
            self.put(name, text)
        return check.docs(self.root, self.config)


class DocumentTests(Workspace):
    def test_generated_templates_pass_structure(self):
        self.assertEqual(self.documents(), [])

    def test_missing_documents_and_owner(self):
        self.config["owner"] = {}
        result = check.docs(self.root, self.config)
        self.assertEqual(sum(x["rule"] == "DOC-MISSING" for x in result), 5)
        self.assertEqual(sum(x["rule"] == "OWNER" for x in result), 3)

    def test_deleted_link_is_detected(self):
        self.documents()
        self.put("docs/entity.md", "实体")
        with (self.root / "docs/domain.md").open("a", encoding="utf-8") as f:
            f.write("\n[实体](entity.md)\n")
        self.assertEqual(check.docs(self.root, self.config), [])
        (self.root / "docs/entity.md").unlink()
        self.assertTrue(any(f["rule"] == "DOC-LINK" for f in check.docs(self.root, self.config)))

    def test_links_spaces_and_reference_style(self):
        self.documents()
        self.put("docs/实体 说明.md", "说明")
        with (self.root / "docs/domain.md").open("a", encoding="utf-8") as f:
            f.write("\n[实体](<实体 说明.md>)\n[另一处][entity]\n[entity]: <实体 说明.md>\n")
        self.assertEqual(check.docs(self.root, self.config), [])

    def test_pending_is_not_pass(self):
        self.documents()
        with (self.root / "docs/domain.md").open("a", encoding="utf-8") as f:
            f.write("\n状态转换待确认\n")
        self.assertTrue(any(f["rule"] == "DOC-PENDING" for f in check.docs(self.root, self.config)))

    def test_code_block_body_is_not_empty(self):
        self.documents()
        path = self.root / "docs/architecture.md"
        text = path.read_text(encoding="utf-8")
        import re
        text = re.sub(r"(## 顶层目录模型\n).*?(\n## 分层职责)", r"\1\n" + "\x60\x60\x60text\nsrc/ # 源码\n\x60\x60\x60\n" + r"\2", text, flags=re.S)
        path.write_text(text, encoding="utf-8")
        self.assertFalse(any(f["rule"] == "DOC-EMPTY" for f in check.docs(self.root, self.config)))

    def test_fenced_fake_headings_do_not_count(self):
        self.documents()
        path = self.root / "docs/domain.md"
        text = path.read_text(encoding="utf-8").replace("## 状态机", "## 不同标题")
        text += "\n\x60\x60\x60\n## 状态机\n假内容\n\x60\x60\x60\n"
        path.write_text(text, encoding="utf-8")
        self.assertTrue(any(f["rule"] == "DOC-SECTION" for f in check.docs(self.root, self.config)))


class MergeTests(Workspace):
    def entry(self, path, **fields):
        data = (self.root / path).read_bytes() if (self.root / path).exists() else None
        return dict(path=path, expected_sha256=merge_sections.digest(data) if data is not None else None, **fields)

    def test_create_preview_then_apply_and_preserve_manual(self):
        entry = self.entry("docs/domain.md", content="# 人工说明\n保留这行\n")
        merge_sections.apply_plan(self.root, [entry])
        self.assertFalse((self.root / "docs/domain.md").exists())
        merge_sections.apply_plan(self.root, [entry], True)
        update = self.entry("docs/domain.md", allow_append=True,
                            sections=[dict(id="states", content="## 状态机\nDRAFT → DONE")])
        merge_sections.apply_plan(self.root, [update], True)
        self.assertIn("保留这行", (self.root / "docs/domain.md").read_text(encoding="utf-8"))

    def test_enum_update_and_repeat_noop(self):
        self.put("docs/domain.md", "人工段落\n<!-- harness:states:start -->\nDRAFT\n<!-- harness:states:end -->\n")
        update = self.entry("docs/domain.md", sections=[dict(id="states", content="DRAFT → DONE")])
        result = merge_sections.apply_plan(self.root, [update], True)
        self.assertTrue(result[0]["changed"])
        path = self.root / "docs/domain.md"
        old_stat = path.stat().st_mtime_ns
        again = self.entry("docs/domain.md", sections=[dict(id="states", content="DRAFT → DONE")])
        self.assertFalse(merge_sections.apply_plan(self.root, [again], True)[0]["changed"])
        self.assertEqual(path.stat().st_mtime_ns, old_stat)
        self.assertTrue(path.read_text(encoding="utf-8").startswith("人工段落\n"))

    def test_concurrent_edit_rejected(self):
        self.put("AGENTS.md", "人工内容")
        entry = self.entry("AGENTS.md", allow_append=True, sections=[dict(id="sync", content="同步")])
        self.put("AGENTS.md", "用户刚刚新增的内容")
        with self.assertRaises(ValueError):
            merge_sections.apply_plan(self.root, [entry], True)
        self.assertEqual((self.root / "AGENTS.md").read_text(encoding="utf-8"), "用户刚刚新增的内容")

    def test_existing_file_full_overwrite_rejected(self):
        self.put("AGENTS.md", "人工内容")
        with self.assertRaises(ValueError):
            merge_sections.apply_plan(self.root, [self.entry("AGENTS.md", content="替换")], True)

    def test_escape_and_duplicate_targets_rejected(self):
        with self.assertRaises(ValueError):
            merge_sections.apply_plan(self.root, [dict(path="../escape.md", content="x", expected_sha256=None)])
        entry = dict(path="new.md", content="x", expected_sha256=None)
        with self.assertRaises(ValueError):
            merge_sections.apply_plan(self.root, [entry, entry])

    def test_crlf_outside_region_preserved(self):
        path = self.root / "AGENTS.md"
        path.write_bytes(b"manual\r\n<!-- harness:test:start -->\r\nold\r\n<!-- harness:test:end -->\r\n")
        entry = self.entry("AGENTS.md", sections=[dict(id="test", content="new")])
        merge_sections.apply_plan(self.root, [entry], True)
        self.assertEqual(path.read_bytes(), b"manual\r\n<!-- harness:test:start -->\r\nnew\r\n<!-- harness:test:end -->\r\n")


class EngineTests(Workspace):
    def test_historical_violation_blocks_without_git(self):
        self.source_pair()
        files = check.sources(self.root, self.config)
        result = [{"edges": [{"from": "src/store/a.ts", "to": "src/views/a.ts", "line": 1}]}]
        findings = check.architecture(self.root, self.config, files, result)
        self.assertEqual(findings[0]["rule"], "ARCH-01")

    def test_stale_rule_patterns_gap(self):
        self.source_pair()
        self.config["architecture"]["rules"][0]["to"] = "missing/**"
        result = check.architecture(self.root, self.config, check.sources(self.root, self.config), [])
        self.assertEqual(result[0]["kind"], "gap")

    def test_no_execution_without_flag(self):
        self.source_pair()
        findings = check.execute(self.root, self.config, "architecture", False)
        self.assertTrue(any(f["kind"] == "gap" and "not executed" in f["message"] for f in findings))

    def test_unknown_stack_never_passes(self):
        self.config["stack"] = "other"
        self.assertEqual(check.execute(self.root, self.config, "architecture", False)[0]["kind"], "gap")

    def test_empty_and_escaping_roots_rejected(self):
        self.put("src/.keep", "")
        with self.assertRaises(ValueError):
            check.sources(self.root, self.config)
        self.config["source_roots"] = ["../"]
        with self.assertRaises(ValueError):
            check.sources(self.root, self.config)

    def test_exclude_directory_and_posix_paths(self):
        self.source_pair()
        self.put("src/generated/ignore.ts", "debugger;")
        self.config["exclude"] = ["src/generated"]
        result = check.sources(self.root, self.config)
        self.assertEqual(result, ["src/store/a.ts", "src/views/a.ts"])

    def test_command_failure_never_passes(self):
        with self.assertRaises(RuntimeError):
            check.run_command([sys.executable, "-c", "raise SystemExit(1)"], self.root)

    def test_file_length_real_violation(self):
        self.put("src/a.ts", "x\n" * 5)
        self.config["entropy"]["max_file_lines"] = 4
        self.assertEqual(check.entropy(self.root, self.config, ["src/a.ts"], False)[0]["kind"], "violation")

    def test_cli_json_and_exit_two_for_missing_config(self):
        p = subprocess.run([sys.executable, str(TOOLS / "check.py"), "all", "--root", str(self.root)], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(p.returncode, 2)
        self.assertEqual(json.loads(p.stdout)["exit_code"], 2)


class GitTests(Workspace):
    @unittest.skipUnless(shutil.which("git"), "Git unavailable")
    def test_staged_rename_unstaged_and_chinese_untracked(self):
        def run(*args):
            return changes.git(self.root, *args)
        run("init")
        run("config", "user.name", "Harness Test")
        run("config", "user.email", "harness@example.invalid")
        self.put("old.txt", "original\n")
        self.put("working.txt", "original\n")
        run("add", ".")
        run("-c", "core.hooksPath=/dev/null", "commit", "-m", "fixture")
        run("mv", "old.txt", "new.txt")
        self.put("working.txt", "modified\n")
        self.put("中文 新模块.ts", "export const state = 1")
        items = changes.collect(self.root)
        self.assertTrue(any(x["old_path"] == "old.txt" and x["path"] == "new.txt" for x in items))
        self.assertTrue(any(x["scope"] == "unstaged" and x["path"] == "working.txt" for x in items))
        self.assertTrue(any(x["scope"] == "untracked" and x["path"] == "中文 新模块.ts" for x in items))

    @unittest.skipUnless(shutil.which("git"), "Git unavailable")
    def test_no_git_reports_unavailable(self):
        with self.assertRaises(RuntimeError):
            changes.collect(self.root)


class ArchiveTests(unittest.TestCase):
    def test_real_report_idempotent_and_failure_preserved(self):
        report = json.dumps(dict(schema=1, mode="all", exit_code=1, status="failed",
            scanned_at="2026-09-17T00:00:00+00:00", baseline="test",
            findings=[dict(kind="violation")])).encode()
        text = archive_quality.archive(report, "# 归档\n")
        self.assertIn("failed", text)
        self.assertEqual(archive_quality.archive(report, text), text)

    def test_missing_timestamp_rejected(self):
        with self.assertRaises(ValueError):
            archive_quality.archive(b'{"schema":1,"mode":"all","exit_code":0,"findings":[]}', "")


class FrontendIntegration(Workspace):
    def setUp(self):
        super().setUp()
        self.node = os.environ.get("HARNESS_NODE", shutil.which("node"))
        if not self.node or not os.environ.get("HARNESS_NODE_MODULES"):
            self.skipTest("Set HARNESS_NODE_MODULES to real Babel/Vue parser dependencies")
        self.config["frontend"]["node"] = self.node

    def run_adapter(self):
        files = check.sources(self.root, self.config)
        return check.adapter(self.root, self.config, files, "frontend", True)

    def test_vue_ts_real_cross_module_and_debugger(self):
        self.put("src/store/a.ts", "export const state: number = 1;")
        self.put("src/views/a.vue", '<template><div/></template>\n<script lang="ts">\nimport {state} from "../store/a";\ndebugger;\nexport default {name:"A"};\n</script>')
        result = self.run_adapter()
        self.assertIn({"from":"src/views/a.vue", "to":"src/store/a.ts", "line":3}, result["edges"])
        self.assertTrue(any(x["rule"] == "ENT-DEBUGGER" for x in result["findings"]))
        self.assertFalse(any(x["kind"] == "gap" for x in result["findings"]), result)

    def test_commented_import_not_dependency_and_string_not_console(self):
        self.put("src/store/a.ts", '// import "../views/a";\nconst text = "console.log(1)";\nexport {text};')
        self.put("src/views/a.ts", "export {};")
        result = self.run_adapter()
        self.assertFalse(result["edges"])
        self.assertFalse(any(x["rule"] == "ENT-CONSOLE" for x in result["findings"]))
        self.assertTrue(any(x["kind"] == "review" for x in result["findings"]))

    def test_dynamic_import_gap(self):
        self.put("src/a.ts", "const p = './a'; import(p);")
        self.assertTrue(any(x["rule"] == "JS-DYNAMIC" for x in self.run_adapter()["findings"]))

    def test_vue2_real_parser(self):
        self.config["frontend"]["vue_parser"] = "vue2"
        self.put("src/a.vue", '<template><div/></template>\n<script>export default {name:"A"};</script>')
        self.assertEqual(self.run_adapter()["findings"], [])

    def test_reviewed_comment_requires_exact_content(self):
        comment = ' import "../views/a";'
        self.put("src/store/a.ts", "//" + comment + "\nexport {};")
        self.put("src/views/a.ts", "export {};")
        self.config["entropy"]["reviewed_comments"] = [
            dict(path="src/store/a.ts", sha256=hashlib.sha256(comment.encode()).hexdigest(),
                 reviewer="@confirmed-owner", reason="Documented example, not abandoned code")]
        self.assertEqual(self.run_adapter()["findings"], [])
        self.put("src/store/a.ts", "//" + comment + " changed\nexport {};")
        self.assertTrue(any(f["kind"] == "review" for f in self.run_adapter()["findings"]))

    def test_all_mode_preserves_docs_findings_on_adapter_error(self):
        self.source_pair()
        self.config["frontend"]["node"] = "nonexistent-harness-node"
        findings = check.execute(self.root, self.config, "all", True)
        self.assertTrue(any(f["rule"] == "DOC-MISSING" for f in findings))
        self.assertTrue(any(f["rule"] == "ADAPTER-ERROR" for f in findings))

    def test_unresolved_import_gap(self):
        self.put("src/a.ts", "import './missing';")
        self.assertTrue(any(x["rule"] == "JS-RESOLVE" for x in self.run_adapter()["findings"]))

    def test_real_architecture_red_then_green(self):
        self.source_pair()
        self.put("src/store/a.ts", "import '../views/a';")
        files = check.sources(self.root, self.config)
        findings = check.architecture(self.root, self.config, files, [self.run_adapter()])
        self.assertTrue(any(x["rule"] == "ARCH-01" for x in findings))
        self.put("src/store/a.ts", "export const x = 1;")
        self.assertEqual(check.architecture(self.root, self.config, files, [self.run_adapter()]), [])

    def test_missing_dependency_reports_gap(self):
        self.source_pair()
        original = os.environ.pop("HARNESS_NODE_MODULES")
        try:
            result = self.run_adapter()
        finally:
            os.environ["HARNESS_NODE_MODULES"] = original
        self.assertTrue(any(x["rule"] == "FRONTEND-ERROR" for x in result["findings"]))


class JavaIntegration(Workspace):
    def setUp(self):
        super().setUp()
        self.javac, self.jdeps = shutil.which("javac"), shutil.which("jdeps")
        if not self.javac or not self.jdeps:
            self.skipTest("JDK javac/jdeps unavailable")
        self.config["stack"] = "java"
        self.config["source_roots"] = ["src"]
        self.config["java"].update(dict(class_dirs=["classes"], clean_build_confirmed=True, jdeps=self.jdeps))
        self.config["architecture"]["rules"] = [dict(id="JAVA-01", **{"from":"src/repository/**", "to":"src/controller/**"},
            reason="repository cannot reference controller", confirmed=True)]
        self.put("src/controller/Api.java", "package controller; public class Api {}")
        self.put("src/repository/Repo.java", "package repository; public class Repo { public controller.Api api; }")
        # Test-only full build; remove ONLY this test's classes directory.
        self.put("build_fixture.py", "from pathlib import Path\nimport shutil,subprocess\np=Path('classes')\nif p.exists(): shutil.rmtree(p)\np.mkdir()\nsubprocess.run(" +
                 repr([self.javac, "-encoding", "UTF-8", "-d", "classes"]) +
                 "+[str(p) for p in Path('src').rglob('*.java')],check=True)\n")
        self.config["java"]["build"] = [sys.executable, "build_fixture.py"]

    def graph(self):
        return java_graph.analyze(dict(root=str(self.root), config=self.config, files=check.sources(self.root, self.config)))

    def test_real_java_dependency_red_then_green(self):
        files = check.sources(self.root, self.config)
        result = self.graph()
        self.assertEqual(result["findings"], [])
        findings = check.architecture(self.root, self.config, files, [result])
        self.assertTrue(any(x["rule"] == "JAVA-01" for x in findings), result)
        self.put("src/repository/Repo.java", "package repository; public class Repo {}")
        self.assertEqual(check.architecture(self.root, self.config, files, [self.graph()]), [])

    def test_compile_failure_not_pass(self):
        self.put("src/repository/Repo.java", "not valid Java")
        with self.assertRaises(RuntimeError):
            self.graph()

    def test_unconfirmed_clean_build_rejected(self):
        self.config["java"]["clean_build_confirmed"] = False
        with self.assertRaises(ValueError):
            self.graph()


if __name__ == "__main__":
    unittest.main()
