#!/usr/bin/env python3
"""Read-only, dependency-free checks; not a substitute for rendered UI QA."""
import argparse
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    data = path.read_bytes()
    if path.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.webp', '.zip'}:
        data = data.replace(b'\r\n', b'\n')
    return hashlib.sha256(data).hexdigest()


def within(root, name):
    path = (root / name).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        raise ValueError('Path must remain inside its declared root: ' + str(name))
    return path


def finding(file, line, rule, message):
    return {'file': str(file), 'line': line, 'rule': rule, 'message': message}


def validate_assets(root):
    errors = []
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8-sig'))
    if not manifest.get('files'):
        return [finding('manifest.json', 0, 'ASSET-MANIFEST', 'No locked files')]
    for entry in manifest['files']:
        path = within(root, entry['path'])
        if not path.is_file() or digest(path) != entry['sha256']:
            errors.append(finding(entry['path'], 0, 'ASSET-DRIFT', 'Missing or changed locked file; verify the approved baseline'))
    return errors


class TemplateParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.nodes = []
        self.stack = []

    def add(self, tag, attrs, closed):
        raw = re.match(r'<\s*([^\s/>]+)', self.get_starttag_text()).group(1)
        node = {'tag': tag, 'raw': raw, 'attrs': dict(attrs), 'parents': list(self.stack), 'line': self.getpos()[0], 'text': ''}
        self.nodes.append(node)
        if not closed and tag not in {'input', 'img', 'br', 'hr', 'meta', 'link'}:
            self.stack.append(node)

    def handle_starttag(self, tag, attrs):
        self.add(tag, attrs, False)

    def handle_startendtag(self, tag, attrs):
        self.add(tag, attrs, True)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]['tag'] == tag:
                del self.stack[i:]
                break

    def handle_data(self, text):
        for node in self.stack:
            node['text'] += text


def class_tokens(node):
    return set((node['attrs'].get('class') or '').split())


def inspect_page(source, name):
    errors, reviews = [], []
    # Keep line positions and nested Vue slot templates; never cut at the first
    # </template>, which would silently omit most of a real SFC.
    markup = re.sub(r'<(script|style)\b[^>]*>[\s\S]*?</\1\s*>', lambda m: '\n' * m.group(0).count('\n'), source, flags=re.I)
    parser = TemplateParser()
    parser.feed(markup)
    legacy = {'Card', 'Dialog', 'DialogForm', 'SearchBox', 'GeneralGrid', 'MainBody', 'ActionBar'}
    basic = {'el-input', 'el-select', 'el-cascader', 'el-date-picker', 'el-time-picker', 'el-input-number'}
    for node in parser.nodes:
        tag, attrs, parents, line = node['tag'], node['attrs'], node['parents'], node['line']
        add_error = lambda rule, msg: errors.append(finding(name, line, rule, msg))
        add_review = lambda rule, msg: reviews.append(finding(name, line, rule, msg))
        if node['raw'] in legacy:
            add_error('NATIVE-COMPONENT', 'Replace the visual wrapper with native Element Plus markup')
        if attrs.get('size') in {'mini', 'medium'}:
            add_error('SIZE-API', 'Use supported default/small sizes')
        if tag == 'el-button':
            if any(re.fullmatch(r'iconfont[\w-]*', c) for c in class_tokens(node)):
                add_error('BUTTON-FONT', 'Keep legacy business glyph classes on the inner icon only')
            toolbar = any(class_tokens(p) & {'card-btn', 'wms-action-bar', 'searchbox'} for p in parents)
            if toolbar and attrs.get('size') != 'small':
                add_error('TOOLBAR-SIZE', 'Toolbar buttons must explicitly use size=small')
            has_icon = 'icon' in attrs or ':icon' in attrs or any(p['tag'] == 'el-icon' and node in p['parents'] for p in parser.nodes)
            if has_icon and not node['text'].strip() and not (attrs.get('aria-label') or attrs.get(':aria-label')):
                add_error('ICON-NAME', 'Icon-only button needs an accessible name')
            if node['text'].strip() in {'取消', '重置'} and attrs.get('type') == 'primary':
                add_error('BUTTON-SEMANTICS', 'Cancel/reset uses default type')
            if node['text'].strip() == '删除' and attrs.get('type') not in {'danger', None}:
                add_error('BUTTON-SEMANTICS', 'Delete uses danger type')
            if ':type' in attrs or 'v-for' in attrs:
                add_review('DYNAMIC-ACTIONS', 'Verify resolved labels, colors, filtering and original click objects with actual configuration')
        if tag in basic:
            in_table = any(p['tag'] == 'el-table' for p in parents)
            size = attrs.get('size')
            if not size:
                for parent in reversed(parents):
                    if parent['tag'] in {'el-form-item', 'el-form'} and parent['attrs'].get('size'):
                        size = parent['attrs']['size']
                        break
            if not in_table and size != 'default':
                add_error('FORM-SIZE', 'Ordinary fields need explicit/inherited size=default, independent of the global default')
        if tag == 'el-table-column':
            kind = attrs.get('type')
            if kind in {'index', 'selection'}:
                if attrs.get('width') != '40' or 'min-width' in attrs:
                    add_error('COMPACT-COLUMN', 'Index/selection column uses fixed width=40, not min-width')
                if attrs.get('align') != 'center' or attrs.get('header-align') != 'center':
                    add_error('COLUMN-ALIGN', 'Both header and body must align center')
            elif ':type' in attrs:
                add_review('DYNAMIC-COLUMN', 'Check conditional selection/index widths and centering in each active mode')
        if tag in {'el-dialog', 'el-drawer'}:
            expected = 'wms-dialog' if tag == 'el-dialog' else 'wms-drawer'
            if expected not in class_tokens(node):
                if ':class' in attrs:
                    add_review('TELEPORT-SCOPE', 'Verify the bound class includes ' + expected)
                else:
                    add_error('TELEPORT-SCOPE', 'Teleported overlay needs ' + expected)
        if tag == 'el-pagination':
            for prop in ('current-page', 'page-size'):
                controlled = ':' + prop in attrs
                listeners = {'@update:' + prop, '@update:' + ''.join([prop.split('-')[0], prop.split('-')[1].title()]).lower()}
                if controlled and not (listeners & set(attrs)):
                    add_error('PAGINATION-CONTROL', 'Pair controlled ' + prop + ' with its update event')
            if ':total' not in attrs and 'total' not in attrs and ':page-count' not in attrs:
                add_error('PAGINATION-TOTAL', 'Provide a valid total/page-count, including the initial state')
            add_review('PAGINATION-RUNTIME', 'Verify null total, page reset, value types and one request per interaction')
    for style in re.finditer(r'<style\b([^>]*)>([\s\S]*?)</style>', source, re.I):
        if 'scoped' not in style.group(1) and re.search(r'(?:^|})\s*\.el-(?:button|input|form-item|table)\b', style.group(2)):
            errors.append(finding(name, source[:style.start()].count('\n') + 1, 'GLOBAL-OVERRIDE', 'Anchor global Element Plus overrides to the management/overlay scope'))
    return errors, reviews


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assets-only', action='store_true')
    parser.add_argument('--project', type=Path)
    parser.add_argument('--page', action='append', default=[])
    parser.add_argument('--theme', default='src/css/native-management.scss')
    parser.add_argument('--foundation')
    args = parser.parse_args()
    if not args.assets_only and (not args.project or not args.page):
        parser.error('Use --assets-only, or --project ROOT with at least one --page')
    try:
        errors, reviews = validate_assets(SKILL_ROOT), []
        if not args.assets_only:
            project = args.project.resolve()
            for target, baseline in [(args.theme, 'assets/runtime/native-management.scss')] + ([(args.foundation, 'assets/runtime/portable-layout.scss')] if args.foundation else []):
                path = within(project, target)
                if not path.is_file() or digest(path) != digest(SKILL_ROOT / baseline):
                    errors.append(finding(target, 0, 'THEME-DRIFT', 'Theme differs from the locked asset; reuse it or document an explicitly approved deviation'))
            for page in args.page:
                path = within(project, page)
                if not path.is_file():
                    errors.append(finding(page, 0, 'PAGE-MISSING', 'Requested page does not exist'))
                    continue
                page_errors, page_reviews = inspect_page(path.read_text(encoding='utf-8-sig'), page)
                errors.extend(page_errors)
                reviews.extend(page_reviews)
        result = {'ok': not errors, 'errors': errors, 'reviews': reviews, 'coverage': 'Static asset and parsable template invariants only; rendered geometry, runtime configuration and business behavior still require acceptance'}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if errors else 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'ok': False, 'error': str(exc)}, ensure_ascii=False))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
