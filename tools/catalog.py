#!/usr/bin/env python3
"""Validate the catalog and generate navigation. --check never writes files."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {'requirements': 8, 'design': 8, 'engineering': 4, 'development': 4,
            'quality': 7, 'debugging': 7, 'utilities': 2}
START = '<!-- CATALOG:START -->'
END = '<!-- CATALOG:END -->'


def load_catalog(root: Path) -> dict:
    data = json.loads((root / 'catalog.json').read_text(encoding='utf-8'))
    if data.get('schema') != 1 or not re.fullmatch(r'[\w-]+/[\w.-]+', data.get('repository', '')):
        raise ValueError('Invalid catalog schema or repository')
    groups, skills = data['groups'], data['skills']
    if len(groups) != len(EXPECTED) or {g['id'] for g in groups} != set(EXPECTED):
        raise ValueError('Expected the seven approved groups exactly once')
    for group in groups:
        for field in ('title', 'description', 'guidance'):
            if not isinstance(group.get(field), str) or not group[field].strip():
                raise ValueError(f"Missing group {field}: {group['id']}")
    if len(skills) != 40 or len({s['name'] for s in skills}) != 40:
        raise ValueError('Expected exactly 40 unique skill names')
    if dict(Counter(s['group'] for s in skills)) != EXPECTED:
        raise ValueError('Group membership/count differs from approved catalog')
    old_paths = set()
    for skill in skills:
        name = skill['name']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) >= 64:
            raise ValueError(f'Invalid name: {name}')
        if skill['path'] != f"skills/{skill['group']}/{name}":
            raise ValueError(f'Unexpected path: {name}')
        path = (root / skill['path'] / 'SKILL.md').resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            raise ValueError(f'Missing or escaped entrypoint: {name}')
        text = path.read_text(encoding='utf-8-sig')
        parts = text.split('---', 2)
        if not text.startswith('---\n') or len(parts) != 3:
            raise ValueError(f'Missing YAML frontmatter: {name}')
        declared = re.search(r'^name:\s*(.+)$', parts[1], re.M)
        if not declared or declared[1].strip().strip('\"\'') != name:
            raise ValueError(f'Declared name differs from catalog: {name}')
        description = re.search(r'^description:[ \t]*(\S[^\n]*)', parts[1], re.M)
        if not description:
            raise ValueError(f'Missing description: {name}')
        value = description[1].strip()
        if value[0] not in ('"', "'", '|', '>') and re.search(r':(?:\s|$)', value):
            raise ValueError(f'Quote YAML description containing a colon: {name}')
        if not skill.get('summary') or not isinstance(skill.get('tags'), list) or not skill['tags']:
            raise ValueError(f'Missing summary/tags: {name}')
        if not isinstance(skill.get('notes'), list) or any(not isinstance(v, str) for v in skill['tags'] + skill['notes']):
            raise ValueError(f'Invalid tags/notes: {name}')
        old = skill['previous_path']
        if old in old_paths or not skill.get('previous_name'):
            raise ValueError(f'Invalid migration mapping: {name}')
        old_paths.add(old)
    found = {p.parent.relative_to(root).as_posix() for p in root.rglob('SKILL.md') if '.git' not in p.parts}
    if found != {s['path'] for s in skills}:
        raise ValueError('Uncataloged, missing or duplicated skill directories')
    return data


def default_branch(root: Path, repository: str) -> str:
    command = ['git']
    if sys.platform == 'win32':
        command += ['-c', 'http.sslBackend=openssl']
    command += ['-c', 'http.version=HTTP/1.1', 'ls-remote', '--symref',
                f'https://github.com/{repository}.git', 'HEAD']
    try:
        result = subprocess.run(command, cwd=root, capture_output=True, text=True, encoding='utf-8', timeout=30, check=True)
    except (OSError, subprocess.SubprocessError) as exc:
        detail = getattr(exc, 'stderr', None) or str(exc)
        raise ValueError(f'Cannot verify remote default branch; no branch was guessed: {detail}') from exc
    match = re.search(r'^ref: refs/heads/(.+)\tHEAD$', result.stdout, re.M)
    if not match:
        raise ValueError('Remote HEAD has no symbolic default branch; no branch was guessed')
    return match[1]


def install(repository: str, names: list[str]) -> str:
    return f'npx skills add {repository} --skill ' + ' '.join(shlex.quote(n) for n in names) + ' -g -y'


def skill_table(data: dict, skills: list[dict], prefix: str = '') -> str:
    lines = ['| 技能 | 用途 | 标签 / 使用说明 |', '|---|---|---|']
    for s in skills:
        note = '；'.join(s['tags'] + s['notes']).replace('|', '\\|')
        lines.append(f"| [{s['name']}]({prefix}{s['path']}/SKILL.md) | {s['summary']} | {note} |")
    return '\n'.join(lines)


def generated_files(root: Path, data: dict, branch: str) -> dict[Path, str]:
    repo, skills = data['repository'], data['skills']
    readme = ['# AI Skills', '', '按工作阶段分组的 Agent Skills 集合：40 个技能、7 个分组。每个技能只保留一份完整目录，行业与终端通过标签辅助查找。',
              '', '结构为 `skills/<分组>/<技能名>/`。技能内部的 `agents/openai.yaml` 是发现元数据；工作流示例集中在 [docs/workflows](docs/workflows/README.md)。',
              '', '## 分类导航', '', '| 分类 | 数量 | 适用任务 |', '|---|---:|---|']
    for g in data['groups']:
        members = [s for s in skills if s['group'] == g['id']]
        readme.append(f"| [{g['title']}](skills/{g['id']}/README.md) | {len(members)} | {g['description']} |")
    readme += ['', '## 安装', '', '先查看可发现技能，再选择单个或分组安装。`-g` 表示全局安装，`-y` 表示跳过交互确认。', '',
               '```sh', f'npx skills add {repo} --list', install(repo, ['ai-coder']), '```', '',
               '安装全部 40 个技能（包含第三方服务及付费依赖技能；安装本身不表示已授权外部调用）：', '', '```sh', install(repo, ['*']), '```', '',
               '各分类页面提供该组完整安装命令。重新打开会话后使用；目录整理前的旧路径和名称请参见 [迁移说明](docs/migration.md)。', '',
               '## 使用方式', '', '按当前任务选择一个主技能，只有需要时才组合专项技能。需求抽取、功能开发、审查、排错分别承担不同阶段，不要求每次执行完整链路。', '',
               '- WCS 范围梳理：选择 wcs-requirement-extractor。',
               '- WMS 界面：按 PDA 或管理端选择对应样式技能，并与开发技能配合。',
               '- 功能实现：选择 ai-coder；代码审查：选择 code-review；故障定位：选择 diagnosing-bugs。',
               '- NEXUS 错误解释会向第三方发送输入，且涉及支付凭据；agent-git-oracle 也声明外部工具及付费元数据。使用前查看说明。',
               '- 存储扫描只读；网页清理服务可删除文件，属于独立写操作。原技能注明 Windows 未经真实环境验证。', '', '## 全部技能']
    outputs = {}
    for g in data['groups']:
        members = [s for s in skills if s['group'] == g['id']]
        readme += ['', f"### {g['title']}", '', g['guidance'], '', skill_table(data, members)]
        group_text = [f"# {g['title']}", '', g['description'], '', g['guidance'], '',
                      '[返回仓库导航](../../README.md) · [迁移说明](../../docs/migration.md)', '',
                      '## 技能', '', skill_table(data, members, '../../'), '', '## 安装本组', '',
                      '```sh', install(repo, [s['name'] for s in members]), '```', '',
                      '安装后重新打开会话。涉及第三方服务或清理操作时，先阅读该技能的使用说明。']
        outputs[root / 'skills' / g['id'] / 'README.md'] = '\n'.join(group_text) + '\n'
    readme += ['', '## 维护目录', '', '`catalog.json` 是分类、简介、标签、说明和迁移映射的统一来源。修改技能或分类后运行：', '',
               '```sh', 'python tools/catalog.py', 'python tools/catalog.py --check', '```', '',
               '生成器核验远端默认分支，生成本文件、七组导航、迁移说明及展示页数据。无法核验时报告错误；`--check` 只检查、不写文件。', '',
               '生成内容直接提交，GitHub Pages 继续使用 docs 目录，无需新增站点依赖。验证说明见 [维护与验证](docs/maintenance.md)。', '',
               '## 许可', '', '保留各技能和字体自带的许可及来源声明；仓库当前未提供统一 LICENSE。']
    outputs[root / 'README.md'] = '\n'.join(readme) + '\n'
    migration = ['# 目录与名称迁移', '', '[返回仓库导航](../README.md)', '',
                 '全部 40 个技能已归入七个工作阶段分组，原根 agents 领域目录已迁空移除。每个技能的内部资产随目录整体保留。', '',
                 '已有安装不会自动移动或改名。先使用 `npx skills list -g` 查看已装技能；按下表的新名称重新安装。若旧名称仍保留，核对个人修改后自行移除旧条目。', '',
                 '手工复制或通过旧路径链接的使用者需更新到新目录，不提供重复技能副本或旧路径软链接。目标业务项目中的 `agents/prd.json` 等输出路径保持原意。', '',
                 '## 名称变化', '', '| 旧声明名 | 新声明名 |', '|---|---|']
    for s in skills:
        if s['previous_name'] != s['name']:
            migration.append(f"| `{s['previous_name']}` | `{s['name']}` |")
    migration += ['', '重新安装上述四个技能：', '', '```sh', install(repo, [s['name'] for s in skills if s['name'] != s['previous_name']]), '```', '',
                  '## 全部路径映射', '', '| 旧路径 | 新路径 |', '|---|---|']
    for s in skills:
        migration.append(f"| `{s['previous_path']}/` | [{s['path']}/](../{s['path']}/SKILL.md) |")
    migration += ['', '## 领域文档', '', '原五个领域的工作流文档迁入 [workflows](workflows/README.md)。原重复 INSTALL 文档由各组导航中的安装命令替代。', '',
                  '安装命令通过仓库短名和 `--skill` 选择技能，不再依赖旧目录或固定 main 分支。新增两份缺失的 frontmatter；为 prd、superpowers-tdd、superpowers-systematic-debugging 的原 description 加引号，修复冒号导致的 YAML 解析失败，含义和正文不变。', '',
                  '另外修正 system-architect 对三份未随原仓库分发的配置模板的失效链接，改为明确的配置示例说明；没有新增或假造模板。']
    outputs[root / 'docs/migration.md'] = '\n'.join(migration) + '\n'
    site = root / 'docs/index.html'
    text = site.read_text(encoding='utf-8')
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError('Expected one catalog marker pair in docs/index.html')
    payload = dict(data, source_branch=branch)
    blob = json.dumps(payload, ensure_ascii=False, indent=2).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    block = START + '\n<script type="application/json" id="catalog-data">\n' + blob + '\n</script>\n' + END
    outputs[site] = text.split(START)[0] + block + text.split(END)[1]
    return outputs


def validate_links(root: Path, outputs: dict[Path, str], data: dict) -> None:
    documents = {p:t for p,t in outputs.items() if p.suffix == '.md'}
    documents.update({p:p.read_text(encoding='utf-8') for p in (root/'docs/workflows').glob('*.md')})
    documents.update({root/s['path']/'SKILL.md':(root/s['path']/'SKILL.md').read_text(encoding='utf-8') for s in data['skills']})
    for path, text in documents.items():
        text = re.sub(r'```.*?```', '', text, flags=re.S)
        for target in re.findall(r'\]\(([^)]+)\)', text):
            target = target.strip().strip('<>')
            if re.match(r'\w+:|#|/', target):
                continue
            target = unquote(target.split('#')[0])
            destination = (path.parent / target).resolve()
            if not destination.is_relative_to(root.resolve()) or not (destination.exists() or destination in outputs):
                raise ValueError(f'Broken repository link: {path.relative_to(root)} -> {target}')


def sync(outputs: dict[Path, str], check: bool) -> list[Path]:
    stale = []
    for path, content in outputs.items():
        if path.exists() and path.read_text(encoding='utf-8') == content:
            continue
        stale.append(path)
        if not check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8', newline='\n')
    return stale


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Validate without writing any file')
    args = parser.parse_args()
    try:
        data = load_catalog(ROOT)
        branch = default_branch(ROOT, data['repository'])
        outputs = generated_files(ROOT, data, branch)
        validate_links(ROOT, outputs, data)
        stale = sync(outputs, args.check)
    except (ValueError, KeyError, OSError, TypeError) as exc:
        print(f'Catalog error: {exc}', file=sys.stderr)
        return 1
    if args.check and stale:
        print('Stale generated files:\n' + '\n'.join(str(p.relative_to(ROOT)) for p in stale), file=sys.stderr)
        return 1
    print(f"{'Checked' if args.check else 'Generated'} 40 skills / 7 groups; verified default branch: {branch}; changed files: {len(stale)}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
