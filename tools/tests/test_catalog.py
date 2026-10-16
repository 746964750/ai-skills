"""Regression tests for discovery integrity and non-writing navigation checks."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

TOOL = Path(__file__).resolve().parents[1] / 'catalog.py'
spec = importlib.util.spec_from_file_location('catalog_tool', TOOL)
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='skills-catalog-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.data = json.loads((TOOL.parents[1] / 'catalog.json').read_text(encoding='utf-8'))
        for s in self.data['skills']:
            entry = self.root / s['path'] / 'SKILL.md'
            entry.parent.mkdir(parents=True)
            entry.write_text(f"---\nname: {s['name']}\ndescription: Test capability\n---\n", encoding='utf-8')
        (self.root/'docs/workflows').mkdir(parents=True)
        for name in ('docs/maintenance.md', 'docs/workflows/README.md'):
            (self.root/name).write_text('# Reference\n', encoding='utf-8')
        (self.root/'docs/index.html').write_text(catalog.START+'\n'+catalog.END, encoding='utf-8')
        self.save()

    def save(self):
        (self.root/'catalog.json').write_text(json.dumps(self.data), encoding='utf-8')

    def test_complete_catalog_resolves_every_skill_once(self):
        self.assertEqual(len(catalog.load_catalog(self.root)['skills']), 40)

    def test_duplicate_and_missing_skills_are_rejected(self):
        self.data['skills'][1] = copy.deepcopy(self.data['skills'][0])
        self.save()
        with self.assertRaisesRegex(ValueError, 'unique'):
            catalog.load_catalog(self.root)

    def test_missing_entrypoint_and_name_drift_are_rejected(self):
        entry = self.root/self.data['skills'][0]['path']/'SKILL.md'
        entry.write_text('---\nname: wrong\ndescription: Test\n---\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Declared name'):
            catalog.load_catalog(self.root)
        entry.unlink()
        with self.assertRaisesRegex(ValueError, 'Missing or escaped'):
            catalog.load_catalog(self.root)

    def test_uncataloged_skill_and_path_escape_are_rejected(self):
        rogue = self.root/'skills/extra/SKILL.md'
        rogue.parent.mkdir()
        rogue.write_text('---\nname: extra\ndescription: Extra\n---\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Uncataloged'):
            catalog.load_catalog(self.root)
        self.data['skills'][0]['path'] = '../outside'
        self.save()
        with self.assertRaisesRegex(ValueError, 'Unexpected path'):
            catalog.load_catalog(self.root)

    def test_plain_description_with_yaml_colon_is_rejected(self):
        entry = self.root/self.data['skills'][0]['path']/'SKILL.md'
        entry.write_text(f"---\nname: {self.data['skills'][0]['name']}\ndescription: Use when: feature work\n---\n", encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Quote YAML description'):
            catalog.load_catalog(self.root)

    def test_check_reports_drift_without_writing_any_file(self):
        outputs = catalog.generated_files(self.root, self.data, 'feature/current')
        catalog.sync(outputs, False)
        path = self.root/'README.md'
        path.write_text('# Local edit\n', encoding='utf-8')
        before = {p.relative_to(self.root):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(catalog.sync(outputs, True), [path])
        after = {p.relative_to(self.root):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)
        catalog.sync(outputs, False)
        self.assertEqual(catalog.sync(catalog.generated_files(self.root, self.data, 'feature/current'), True), [])

    def test_links_allow_generated_targets_but_reject_missing_files(self):
        outputs = catalog.generated_files(self.root, self.data, 'feature/current')
        catalog.validate_links(self.root, outputs, self.data)
        outputs[self.root/'README.md'] += '\n[missing](missing.md)\n'
        with self.assertRaisesRegex(ValueError, 'Broken repository link'):
            catalog.validate_links(self.root, outputs, self.data)

    def test_remote_branch_is_verified_and_failure_never_guesses_main(self):
        result = type('Result', (), {'stdout':'ref: refs/heads/feature/current\tHEAD\nabc\tHEAD\n'})()
        with patch.object(catalog.subprocess, 'run', return_value=result):
            self.assertEqual(catalog.default_branch(self.root, 'owner/repo'), 'feature/current')
        result.stdout = 'abc\tHEAD\n'
        with patch.object(catalog.subprocess, 'run', return_value=result):
            with self.assertRaisesRegex(ValueError, 'no branch was guessed'):
                catalog.default_branch(self.root, 'owner/repo')

    def test_embedded_catalog_cannot_close_its_script_element(self):
        self.data['skills'][0]['summary'] = '</script><script>bad()</script>'
        site = catalog.generated_files(self.root, self.data, 'feature/current')[self.root/'docs/index.html']
        self.assertNotIn('</script><script>bad()', site)
        self.assertIn('\\u003c/script\\u003e', site)


if __name__ == '__main__':
    unittest.main()
