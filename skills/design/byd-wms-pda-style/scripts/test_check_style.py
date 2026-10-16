"""Portable behavioral regression for the read-only checker. Run with Python 3.10+."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
CHECK = SKILL / 'scripts/check_style.py'
TEMP_BASE = Path(os.environ.get('WMS_PDA_STYLE_TEST_TMP', tempfile.gettempdir())).resolve()


class StyleCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='wms-pda-skill-test-', dir=TEMP_BASE)
        self.root = Path(self.temp.name).resolve()
        assert self.root.parent == TEMP_BASE
        self.addCleanup(self.temp.cleanup)
        for source, target in [
            ('assets/runtime/base.css', 'src/css/base.css'),
            ('assets/runtime/PdaPage.vue', 'src/components/PdaPage/index.vue'),
            ('assets/templates/OperationPage.vue', 'src/views/Operation.vue')
        ]:
            path = self.root / target
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SKILL / source, path)

    def run_check(self, *extra, checker=CHECK):
        result = subprocess.run([sys.executable, str(checker), '--project', str(self.root), '--page', 'src/views/Operation.vue', *extra], capture_output=True, text=True, encoding='utf-8')
        return result.returncode, json.loads(result.stdout)

    def test_canonical_page_and_crlf_assets_pass(self):
        path = self.root / 'src/css/base.css'
        path.write_bytes(path.read_bytes().replace(b'\r\n', b'\n').replace(b'\n', b'\r\n'))
        self.assertEqual(self.run_check()[0], 0)

    def test_modified_theme_and_shell_fail(self):
        for name in ('src/css/base.css', 'src/components/PdaPage/index.vue'):
            with self.subTest(name=name):
                path = self.root / name
                original = path.read_text(encoding='utf-8')
                path.write_text(original + '\n/* local change */\n', encoding='utf-8')
                self.assertEqual(self.run_check()[0], 1)
                path.write_text(original, encoding='utf-8')

    def test_old_native_controls_and_inline_styles_fail(self):
        path = self.root / 'src/views/Operation.vue'
        for change in ('<button>确认</button>', '<el-input style="height:25px" />', '<i class="el-icon-user"></i>'):
            with self.subTest(change=change):
                path.write_text('<template><PdaPage title="扫码" @back="back">' + change + '<template #actions><el-button>确认</el-button></template></PdaPage></template><script>export default {}</script>', encoding='utf-8')
                self.assertEqual(self.run_check()[0], 1)

    def test_global_theme_override_fails_but_table_width_is_allowed(self):
        path = self.root / 'src/css/extension.css'
        path.write_text('.table-box .el-table { width: 100%; }', encoding='utf-8')
        self.assertEqual(self.run_check()[0], 0)
        path.write_text('.other { --el-color-primary: #ff0000; }', encoding='utf-8')
        self.assertEqual(self.run_check()[0], 1)

    def test_active_scaling_import_fails_and_comment_is_ignored(self):
        path = self.root / 'src/main.js'
        path.write_text("// import 'lib-flexible/flexible'\n", encoding='utf-8')
        self.assertEqual(self.run_check()[0], 0)
        path.write_text("import 'lib-flexible/flexible'\n", encoding='utf-8')
        self.assertEqual(self.run_check()[0], 1)

    def test_missing_page_reports_incomplete(self):
        code, report = self.run_check('--page', 'src/views/Missing.vue')
        self.assertEqual(code, 2)
        self.assertEqual(report['status'], 'incomplete')

    def test_asset_tampering_is_detected_in_a_portable_copy(self):
        bundle = self.root / 'portable-skill'
        shutil.copytree(SKILL, bundle, ignore=shutil.ignore_patterns('__pycache__'))
        (bundle / 'assets/runtime/base.css').write_text('body { color: red; }', encoding='utf-8')
        code, report = self.run_check(checker=bundle / 'scripts/check_style.py')
        self.assertEqual(code, 1)
        self.assertTrue(report['findings'])


if __name__ == '__main__':
    unittest.main()
