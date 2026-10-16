#!/usr/bin/env python3
"""Read-only PDA style checks. Python 3.10+, standard library only."""
import argparse
import hashlib
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
VOID = {'img', 'input', 'br', 'hr', 'meta', 'link', 'source', 'wbr'}
PROTECTED = re.compile(
    r'--(?:pda-[\w-]+|el-(?:color-primary[\w-]*|font[\w-]*|component-size[\w-]*))\s*:'
    r'|\.pda-page[\w-]*(?![\w-])'
    r'|\.body\s+\.(?:itemLine|itemName|itemDiv|itemCard)'
    r'|\.el-(?:button|input|select|dialog|message|table|pagination)(?=--|[\s.:#{_>,])'
)


def digest(path):
    raw = path.read_bytes()
    if path.suffix != '.png':
        raw = raw.replace(b'\r\n', b'\n')
    return hashlib.sha256(raw).hexdigest()


class TemplateParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []
        self.nodes = []

    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs), tuple(self.stack), self.getpos()[0]))
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs), tuple(self.stack), self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in self.stack:
            self.stack = self.stack[:len(self.stack) - 1 - self.stack[::-1].index(tag)]


def page_findings(path):
    source = path.read_text(encoding='utf-8-sig')
    prefix = re.split(r'<script\b', source, maxsplit=1)[0]
    if '<template>' not in prefix or '</template>' not in prefix:
        return ['Cannot locate an ordinary Vue SFC template; compile/review this file manually.']
    template = prefix[prefix.index('<template>') + 10:prefix.rindex('</template>')]
    parser = TemplateParser()
    parser.feed(template)
    nodes = parser.nodes
    issues = []
    classes = ' '.join(attrs.get('class', '') for _, attrs, _, _ in nodes)
    shells = [attrs for tag, attrs, _, _ in nodes if tag in {'pdapage', 'pda-page'}]
    if shells:
        if len(shells) != 1 or not any(k in shells[0] for k in (':title', 'title')) or '@back' not in shells[0]:
            issues.append('Use one PdaPage with title and @back bound to the original return handler.')
        if not any('#actions' in attrs or 'v-slot:actions' in attrs for _, attrs, _, _ in nodes):
            issues.append('Place operation buttons in the #actions slot.')
    elif not ({'loginbox', 'menubox', 'page404', 'pda-home'} & set(classes.split())):
        issues.append('Use PdaPage, or the canonical login/menu/result page pattern.')
    for tag, attrs, ancestors, line in nodes:
        at = f'template:{line}: '
        if tag in {'button', 'input', 'select', 'textarea'}:
            issues.append(at + f'Replace native {tag} control with Element Plus.')
        if attrs.get('size') in {'mini', 'small'} or attrs.get('type') == 'text':
            issues.append(at + 'Do not restore compact controls or deprecated type=text.')
        if 'slot' in attrs or any('.sync' in key for key in attrs):
            issues.append(at + 'Replace Vue 2 slot/.sync syntax with Vue 3 APIs.')
        if any(re.search(r'\bel-icon-[\w-]+', value or '') for value in attrs.values()):
            issues.append(at + 'Use SVG icon components instead of legacy font classes.')
        if 'style' in attrs:
            value = re.sub(r'\s+', '', attrs['style'] or '').rstrip(';')
            if not (tag == 'el-table' and value == 'width:100%'):
                issues.append(at + 'Use canonical classes instead of inline style overrides.')
        if any(key in attrs for key in (':style', 'v-bind:style')):
            issues.append(at + 'Dynamic inline styles require manual baseline review.')
        if tag in {'el-input', 'el-select', 'el-autocomplete', 'el-input-number'}:
            if not any(k in attrs for k in ('aria-label', ':aria-label', 'aria-labelledby', ':aria-labelledby')) and 'el-form-item' not in ancestors:
                issues.append(at + 'Give this field an accessible label.')
        if tag == 'el-dialog' and 'width' in attrs:
            issues.append(at + 'Let the canonical responsive dialog width apply.')
    return issues


def bundle_findings(manifest):
    findings = []
    for item in manifest['files']:
        path = SKILL / item['path']
        if not path.is_file() or digest(path) != item['sha256']:
            findings.append(f"Asset drift or missing file: {item['path']}")
    for path in [SKILL / 'SKILL.md', *sorted((SKILL / 'references').glob('*.md'))]:
        source = path.read_text(encoding='utf-8-sig')
        for link in re.findall(r'\]\(([^)]+)\)', source):
            if '://' not in link and not (path.parent / link.split('#')[0]).exists():
                findings.append(f'Broken local link in {path.name}: {link}')
    for path in sorted((SKILL / 'assets/templates').glob('*.vue')):
        findings.extend(f'{path.name}: {item}' for item in page_findings(path))
    return findings


def project_findings(root, args, manifest):
    findings = []
    mapping = {'assets/runtime/base.css': args.theme, 'assets/runtime/PdaPage.vue': args.shell}
    items = {item['path']: item for item in manifest['files']}
    for asset, target in mapping.items():
        path = (root / target).resolve()
        if not path.is_file():
            raise FileNotFoundError(f'Missing target asset: {path}')
        if digest(path) != items[asset]['sha256']:
            findings.append(f'{target}: differs from canonical {asset}; review drift before continuing.')
    canonical = {item['sha256'] for item in manifest['files'] if item['path'].startswith('assets/runtime/')}
    for path in sorted((root / 'src').rglob('*')):
        if path.suffix not in {'.vue', '.css', '.scss', '.sass', '.js', '.ts', '.mjs'} or not path.is_file():
            continue
        if digest(path) in canonical:
            continue
        source = path.read_text(encoding='utf-8-sig')
        label = path.relative_to(root).as_posix()
        if path.suffix in {'.js', '.ts', '.mjs', '.vue'}:
            source_without_comments = re.sub(r'/\*.*?\*/|^\s*//[^\n]*', '', source, flags=re.S | re.M)
            if re.search(r'(?:import|require)[^\n]*(?:lib-flexible|legacy-icons\.css|iconfont\.css)', source_without_comments):
                findings.append(f'{label}: active legacy scaling/icon import.')
        styles = re.findall(r'<style\b[^>]*>(.*?)</style>', source, re.S) if path.suffix == '.vue' else [source] if path.suffix in {'.css', '.scss', '.sass'} else []
        for style in styles:
            style = re.sub(r'/\*.*?\*/', '', style, flags=re.S)
            # 表格容器填满可用宽度不改变视觉 token，等同于模板允许的 width:100%。
            style = re.sub(r'\.table-box\s+\.el-table\s*\{\s*width\s*:\s*100%\s*;?\s*\}', '', style)
            if PROTECTED.search(style):
                findings.append(f'{label}: overrides protected PDA/Element Plus theme or layout selectors.')
    for name in ('vite.config.js', 'vite.config.mjs', 'vite.config.ts'):
        path = root / name
        if path.exists() and re.search(r'plugins\s*:\s*\[[^\]]*px2rem\s*\(', path.read_text(encoding='utf-8-sig'), re.S):
            findings.append(f'{name}: global px2rem conflicts with the native CSS baseline.')
    for name in args.page:
        path = (root / name).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise FileNotFoundError(f'Page must be an existing file inside project: {name}')
        findings.extend(f'{name}: {item}' for item in page_findings(path))
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assets-only', action='store_true')
    parser.add_argument('--project', type=Path)
    parser.add_argument('--theme', default='src/css/base.css')
    parser.add_argument('--shell', default='src/components/PdaPage/index.vue')
    parser.add_argument('--page', action='append', default=[])
    args = parser.parse_args()
    if not args.assets_only and (not args.project or not args.page):
        parser.error('Use --assets-only, or --project with at least one --page.')
    try:
        manifest = json.loads((SKILL / 'manifest.json').read_text(encoding='utf-8'))
        findings = bundle_findings(manifest)
        if args.project:
            findings.extend(project_findings(args.project.resolve(), args, manifest))
        result = {'style': manifest['style_id'], 'version': manifest['version'], 'status': 'failed' if findings else 'passed', 'findings': findings, 'scope': 'Static checks only; browser and business verification are separate.'}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if findings else 0
    except (OSError, ValueError, KeyError) as error:
        print(json.dumps({'status': 'incomplete', 'error': str(error)}, ensure_ascii=False))
        return 2


if __name__ == '__main__':
    sys.exit(main())
