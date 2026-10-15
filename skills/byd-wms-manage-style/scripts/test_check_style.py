#!/usr/bin/env python3
"""Behavioral regression of the read-only checker using isolated fixtures."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from check_style import inspect_page, validate_assets, within

GOOD = '''<template><main class="wms-page"><el-card><template #header>
<div class="card-btn"><el-button size="small" type="primary">查询</el-button></div>
</template><el-table><el-table-column type="index" width="40" align="center" header-align="center" />
<el-table-column type="selection" width="40" align="center" header-align="center" /></el-table>
<el-pagination :current-page="page" :page-size="size" :total="total ?? 0"
@update:current-page="onPage" @update:page-size="onSize" /></el-card>
<el-dialog class="wms-dialog"><el-form size="default"><el-input /></el-form></el-dialog>
</main></template><script setup>const example = '<Card>'</script>'''


class StyleChecks(unittest.TestCase):
    def errors(self, source):
        return [x['rule'] for x in inspect_page(source, 'Example.vue')[0]]

    def test_native_page_and_nested_header_slot(self):
        self.assertEqual(self.errors(GOOD), [])
        # The table is after the first closing template, so truncation is caught.
        self.assertIn('COMPACT-COLUMN', self.errors(GOOD.replace('type="index" width="40"', 'type="index" min-width="50"')))

    def test_selection_and_header_alignment(self):
        self.assertIn('COLUMN-ALIGN', self.errors(GOOD.replace('header-align="center"', 'header-align="left"')))

    def test_old_font_and_toolbar_density(self):
        self.assertIn('TOOLBAR-SIZE', self.errors(GOOD.replace('size="small" type="primary"', 'size="default" type="primary"')))
        self.assertIn('BUTTON-FONT', self.errors(GOOD.replace('size="small" type="primary"', 'class="iconfont-shpt" size="small" type="primary"')))

    def test_icon_child_is_allowed_but_icon_only_button_needs_a_name(self):
        self.assertEqual(self.errors(GOOD.replace('>查询</el-button>', '><i class="iconfont-shpt shpt-custom" />查询</el-button>')), [])
        self.assertIn('ICON-NAME', self.errors(GOOD.replace('type="primary">查询</el-button>', 'type="primary" :icon="View" />')))

    def test_form_size_inheritance(self):
        self.assertIn('FORM-SIZE', self.errors(GOOD.replace('<el-form size="default">', '<el-form>')))

    def test_teleport_scope(self):
        self.assertIn('TELEPORT-SCOPE', self.errors(GOOD.replace('class="wms-dialog"', 'class="edit-dialog"')))

    def test_pagination_listener(self):
        self.assertIn('PAGINATION-CONTROL', self.errors(GOOD.replace('@update:current-page="onPage"', '@current-change="onPage"')))

    def test_global_override_and_wrapper(self):
        self.assertIn('GLOBAL-OVERRIDE', self.errors(GOOD + '<style>.el-button { font-size: 30px }</style>'))
        self.assertIn('NATIVE-COMPONENT', self.errors(GOOD.replace('<el-card>', '<Card>').replace('</el-card>', '</Card>')))

    def test_asset_drift_lf_normalization_and_path_boundary(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            asset = root / 'theme.scss'
            asset.write_bytes(b'a\r\nb\r\n')
            (root / 'manifest.json').write_text(json.dumps({'files': [{'path': 'theme.scss', 'sha256': hashlib.sha256(b'a\nb\n').hexdigest()}]}), encoding='utf-8')
            self.assertEqual(validate_assets(root), [])
            asset.write_text('changed', encoding='utf-8')
            self.assertEqual(validate_assets(root)[0]['rule'], 'ASSET-DRIFT')
            with self.assertRaises(ValueError):
                within(root, '../outside.scss')


if __name__ == '__main__':
    unittest.main()
