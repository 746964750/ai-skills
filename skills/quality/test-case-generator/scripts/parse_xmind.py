#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""parse_xmind.py — 将 .xmind 思维导图解析为 Markdown 缩进大纲或 JSON 树

用途：
    把 XMind（.xmind）测试点分析文档转换为文本大纲/JSON，供测试用例生成
    （test-case-generator / test-case-generator-ai）读取，作为扩写完整测试
    用例的输入。纯标准库实现，零第三方依赖，任何机器可直接运行。

支持格式：
    - XMind Zen / 2020+（content.json，优先）
    - XMind 8 / 经典版（content.xml，自动回退）

用法：
    python parse_xmind.py input.xmind                # 打印 Markdown 大纲
    python parse_xmind.py input.xmind -o out.md      # 大纲写入文件
    python parse_xmind.py input.xmind --json -o out.json   # 输出 JSON 树

输出说明（Markdown）：
    根节点标题为一级标题 `# xxx`，其余节点为逐层缩进的无序列表
    `- 标题`（缩进 2 空格/层）。多 Sheet 时依次输出多个一级标题段。

退出码：
    0 成功；1 文件不存在或不是合法 xmind；2 未解析到任何节点。
"""

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

try:
    import xml.etree.ElementTree as ET
except ImportError:  # pragma: no cover
    ET = None


def _clean_title(raw):
    """标题清洗：去空白、折叠换行；None -> ''。"""
    if raw is None:
        return ""
    return re.sub(r"\s+", " ", str(raw)).strip()


def walk_json_topic(topic, depth=0):
    """递归遍历 content.json 中的 topic 节点，产出 (depth, title) 序列。"""
    title = _clean_title(topic.get("title"))
    if title:
        yield depth, title
    children = topic.get("children") or {}
    for key in ("attached", "detached"):
        for child in children.get(key, []) or []:
            yield from walk_json_topic(child, depth + 1)


def walk_xml_topic(elem, depth=0):
    """递归遍历 XMind 8 content.xml 的 <topic> 元素。"""
    title = ""
    for t in elem.findall("{http://xmind.net/xmind/8}title"):
        title = _clean_title(t.text)
        break
    if not title:
        # 部分老文件无命名空间
        for t in elem.findall("title"):
            title = _clean_title(t.text)
            break
    if title:
        yield depth, title
    # 子主题可能在 <children><topics type="attached"> 内
    for children in elem:
        if children.tag.endswith("}children") or children.tag == "children":
            for topics in children:
                if topics.tag.endswith("}topics") or topics.tag == "topics":
                    for child in topics:
                        if child.tag.endswith("}topic") or child.tag == "topic":
                            yield from walk_xml_topic(child, depth + 1)


def parse_content_json(raw: bytes):
    """解析 content.json -> [(sheet_title, [(depth, title)])]。"""
    data = json.loads(raw.decode("utf-8-sig", "replace"))
    sheets = []
    for sheet in data or []:
        rt = sheet.get("rootTopic") or {}
        items = list(walk_json_topic(rt))
        if items:
            sheets.append((_clean_title(sheet.get("title")) or items[0][1], items))
    return sheets


def parse_content_xml(raw: bytes):
    """解析 XMind8 content.xml -> [(sheet_title, [(depth, title)])]。"""
    if ET is None:
        return []
    root = ET.fromstring(raw)
    sheets = []
    for sheet in root:
        if not (sheet.tag.endswith("}sheet") or sheet.tag == "sheet"):
            continue
        sheet_title = ""
        rt = None
        for child in sheet:
            tag = child.tag.split("}")[-1]
            if tag == "title" and child.text:
                sheet_title = _clean_title(child.text)
            elif tag == "topic":
                rt = child
        if rt is None:
            continue
        items = list(walk_xml_topic(rt))
        if items:
            sheets.append((sheet_title or items[0][1], items))
    return sheets


def sheets_to_markdown(sheets) -> str:
    """[(sheet_title, [(depth, title)])] -> Markdown 大纲文本。"""
    parts = []
    for sheet_title, items in sheets:
        # 根标题（depth=0）作为一级标题
        root_depth, root_title = items[0]
        parts.append(f"# {root_title}")
        for depth, title in items[1:]:
            parts.append("  " * (depth - root_depth) + f"- {title}")
        parts.append("")
    return "\n".join(parts).strip() + "\n"


def sheets_to_json_tree(sheets):
    """[(sheet_title, items)] -> 树形 JSON（含标题去重层级）。"""
    result = []
    for sheet_title, items in sheets:
        root_depth, root_title = items[0]
        root = {"title": root_title, "children": []}
        stack = [(root_depth, root)]
        for depth, title in items[1:]:
            node = {"title": title, "children": []}
            while stack and depth <= stack[-1][0]:
                stack.pop()
            if stack:
                stack[-1][1]["children"].append(node)
            else:
                root["children"].append(node)
            stack.append((depth, node))
        result.append({"sheet": sheet_title or root_title, "root": root})
    return result


def load_sheets(path: Path):
    """从 xmind 文件加载 sheets，兼容 content.json / content.xml。"""
    try:
        with zipfile.ZipFile(path) as zf:
            names = set(zf.namelist())
            if "content.json" in names:
                return parse_content_json(zf.read("content.json"))
            if "content.xml" in names:
                return parse_content_xml(zf.read("content.xml"))
            # 兜底：按前缀查找
            for n in names:
                if n.endswith("content.json"):
                    return parse_content_json(zf.read(n))
                if n.endswith("content.xml"):
                    return parse_content_xml(zf.read(n))
    except (zipfile.BadZipFile, KeyError, ValueError, ET.ParseError if ET else Exception) as exc:
        print(f"[错误] 无法解析 xmind 文件: {exc}", file=sys.stderr)
    return []


def count_nodes(sheets) -> int:
    return sum(len(items) for _, items in sheets)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=".xmind 思维导图解析器 → Markdown 大纲 / JSON 树")
    ap.add_argument("input", help="输入 .xmind 文件路径")
    ap.add_argument("-o", "--output", help="输出文件路径（默认打印到 stdout）")
    ap.add_argument("--json", action="store_true", help="输出 JSON 树而非 Markdown 大纲")
    args = ap.parse_args(argv)

    src = Path(args.input)
    if not src.is_file():
        print(f"[错误] 输入文件不存在: {src}", file=sys.stderr)
        return 1

    sheets = load_sheets(src)
    if not sheets:
        print("[错误] 未解析到任何节点：文件为空或结构不受支持", file=sys.stderr)
        return 2

    if args.json:
        text = json.dumps(sheets_to_json_tree(sheets), ensure_ascii=False, indent=2)
    else:
        text = sheets_to_markdown(sheets)

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"[完成] 已生成 {out}")
    else:
        sys.stdout.write(text)

    total = count_nodes(sheets)
    kind = "JSON 树" if args.json else "Markdown 大纲"
    print(f"[汇总] {len(sheets)} 个 Sheet / {total} 个节点（含根），输出格式: {kind}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
