---
name: test-case-generator
description: "软件测试专家技能：根据用户输入（需求描述、需求文档、API文档、文档链接、UI页面截图、XMind测试点分析文档(.xmind)等）生成可执行、格式规整、默认交付Excel(.xlsx)的标准测试用例（6列标准字段）。覆盖功能正常/边界/异常/模糊查询/精准查询/排序筛选/组合查询/安全/性能/UI交互等测试类型，内置金融业务专项（对账/监管合规/数据一致性/审计轨迹/资金安全）与测试设计方法指引（等价类+边界值/场景法/判定表/正交试验/状态迁移/错误推测）。当用户要求生成/编写/设计测试用例、创建测试计划、产出测试用例表、准备提测交付物或测试归档时使用本技能。被测功能若以AI/NLP能力为主（自然语言查询、大模型交互、意图识别），请改用 test-case-generator-ai 技能。触发词：生成测试用例、编写测试用例、设计测试用例、创建测试计划、生成测试场景、测试用例、Excel用例、提测用例、用例归档、读取xmind生成用例、思维导图转测试用例等。"
agent_created: true
---

# 测试用例生成器（Test Case Generator）

## 概述

本技能将任意形式的软件需求输入——需求描述、需求文档、API文档、文档链接、UI页面截图——转化为结构化、可执行的标准测试用例。所有生成的测试用例严格遵循 **6 列标准字段**，**默认交付为 Excel 文件（.xlsx）**，可直接用于测试执行、提测交付与用例归档；Markdown 表格仅作为回复内预览。

技能符合软件测试规范与金融软件测试要求（数据校验、审计轨迹、对账、监管合规）。Excel 生成采用「数据 JSON + 内置生成器」方式，**无本机路径依赖**，整个技能文件夹可拷贝到任意环境直接使用。

## 快速开始

1. 接收用户输入（需求文本、API 文档、文档链接或 UI 截图）。
2. 分析输入，识别所有可测试功能点、业务规则、边界条件与异常路径。
3. 按「测试用例设计方法」选用合适方法（等价类+边界值/场景法/判定表/正交试验/状态迁移/错误推测）逐场景设计用例。
4. 按 **6 列标准格式** 设计测试用例，覆盖识别出的全部场景。
5. **默认生成 Excel 文件（.xlsx）**：在回复中先以 Markdown 表格预览，再按「Excel 生成」章节编写 `testcases.json` 并运行内置生成器产出 `.xlsx`，使用 `present_files` 交付。
6. 自查完整性：用例不重复、不遗漏，场景颗粒度中等。

## 输入类型与处理方式

### 需求描述 / 需求文档

- 提取全部功能点、业务规则、约束条件与验收标准。
- 识别输入字段、数据类型、取值范围与依赖关系。
- 将每个功能点映射为一个或多个测试场景（正常、边界、异常）。

### API 文档

- 解析接口地址、请求方法、参数（必填/选填）、数据类型与响应结构。
- 设计参数校验、类型校验、边界值、缺失必填字段、非法值、认证/鉴权相关用例。
- 按接口规范同时覆盖成功响应（2xx）与错误响应（4xx/5xx）。

### 文档链接

- 抓取并解析链接文档内容。
- 将提取内容视为需求文档，按同一流程处理。

### UI 页面截图

- 识别所有交互元素：输入框、按钮、下拉框、页签、筛选器、分页等。
- 依据可见标签、占位符与 UI 模式推断字段约束。
- 设计字段校验、按钮状态、导航流程与 UI 交互序列相关用例。

### XMind 测试分析文档（.xmind）

用户提供 `.xmind` 测试点分析文档（典型来源：`test-analysis-xmind` 技能产出的「功能模块 > 测试分析类型/方法 > 测试点」三级导图，或任意手绘测试点导图）时，将导图中的测试点扩写为完整 6 列用例：

1. **解析导图**：运行本技能自带解析器（纯标准库，无需安装 XMind）：
   ```bash
   python scripts/parse_xmind.py 输入.xmind            # 打印 Markdown 大纲
   python scripts/parse_xmind.py 输入.xmind -o out.md  # 大纲写入文件
   ```
   解析器自动兼容 XMind Zen/2020+（content.json）与 XMind 8（content.xml）两种格式，多 Sheet 依次输出。
2. **读取大纲**：确认层级结构——根标题（功能/页面名）> 第 1 层子节点（功能模块/业务场景）> 第 2 层（测试分析类型：场景法/等价类/边界值/错误推测等）> 叶子（测试点）。将每个功能模块对应到独立 Excel Sheet。
3. **扩写用例**：将每个**叶子测试点**扩写为 ≥1 条完整 6 列用例。测试用例类型按测试点内容判定（上游方法仅作线索，不硬映射）：
   - 场景法 → 流程类多为「功能正常场景」；含取消/关闭/按钮置灰/导航类为「UI交互」；
   - 等价类 → 有效输入类为「功能正常场景」；空值/非法值/纯空格/格式不支持等拦截类为「异常场景」；
   - 边界值 → 「边界场景」（长度 min/max±1、大小临界、日期先后）；
   - 错误推测 → SQL 注入/XSS/越权/未授权/图片马等为「安全」；并发连点/超时/断网/会话过期/超长输入为「异常场景」；弹窗交互/刷新/分辨率适配为「UI交互」。
   - 复杂测试点（如某字段的等价类集合）可按细分场景拆成多条用例；必要时补充上游遗漏的关键场景（如校验失败后已填内容不丢失、重复提交幂等），并在用例中体现。
4. **前置/步骤/预期补全**：前置条件写明模块级前提（登录、权限、入口）+ 本用例数据准备；执行步骤从测试点动作拆分出 2~5 步可操作指令；预期结果明确成功/拦截/提示文案级行为。测试点原文常含「动作，结果」两段，结果段可直接落到预期列。
5. **生成 Excel**：按「Excel 生成」章节编写 `testcases.json`（每功能模块一个 sheet，编号跨 sheet 连续递增）并运行生成器，使用 `present_files` 交付。

> 与 test-analysis-xmind 形成闭环：分析用导图（探索/评审）→ 本技能读导图出用例（执行/提测/归档），同一份测试点分析不需二次录入。

### 金融业务专项（识别到金融场景时强制覆盖）

涉及以下金融场景时，在通用测试类型之外**强制补充**对应专项用例：

- **清算/对账**：自动对账、退票、长款/短款、跨境支付、SWIFT、外汇买卖等。
- **监管合规**：反洗钱（AML）、KYC、客户身份识别、可疑交易上报、大额交易报送。
- **数据一致性**：总分核对、余额平衡、流水与台账一致、跨系统数据同步。
- **审计轨迹**：操作日志完整、不可篡改、可追溯。
- **资金安全**：幂等性、并发控制、金额边界（0.01 分/亿级）、负数拒绝、超限拦截。

## 测试用例设计方法

设计测试用例时，根据功能特征选用合适的设计方法。主流方法及其使用场景如下：

| 方法 | 使用场景 | 设计要点 |
|------|---------|---------|
| **等价类 + 边界值** | 输入框、表单字段，几乎必用 | 把输入域划分为有效/无效等价类，每类选代表性值；对每个边界（最小、略小于最小、刚好、略大于最大、最大）单独设计用例 |
| **场景法** | 业务流程、业务主功能 | 按主流程 / 备选流程 / 异常流程组织用例，每条用例覆盖一条端到端业务路径 |
| **判定表 / 因果图** | 条件少、逻辑规则复杂 | 列出全部条件桩与动作桩，合并相似规则，覆盖每条规则条目；适合审批、计费、计息等组合判定 |
| **正交试验** | 多参数多选项组合 | 用正交表从全组合中筛选代表性组合，显著减少用例数同时保持覆盖率；适合筛选、搜索、配置项组合 |
| **状态迁移** | 有状态机的业务（订单、工单、审批）| 列出全部状态与触发事件，覆盖合法迁移与非法迁移；从每个状态出发验证正向/逆向/越级流转 |
| **错误推测** | 补充异常、经验性 bug | 基于经验猜测可能缺陷：并发、时序、超时、资源竞争、依赖异常、边界交叉、组合异常等 |

### 方法选用原则

- **表单 / 输入字段**：等价类+边界值 必用。
- **业务主流程**：场景法 必用。
- **业务规则 / 审批 / 计费 / 计息**：判定表 / 因果图。
- **多条件筛选 / 搜索 / 配置项组合**：正交试验。
- **订单 / 工单 / 审批流转 / 任务调度**：状态迁移。
- **任何模块**：错误推测 作为补充。

### 组合使用实践

实际工作中通常多方法组合：

1. 用 **场景法** 搭骨架，把业务主流程拆成端到端用例。
2. 用 **等价类+边界值** 填字段，覆盖每条用例中的输入校验。
3. 用 **判定表 / 因果图** 理清规则组合（审批、计费、权限矩阵）。
4. 用 **状态迁移** 覆盖有状态机的流程全路径。
5. 用 **正交试验** 压多参数多选项的组合筛选。
6. 用 **错误推测** 补漏，叠加并发、时序、依赖、兼容性等经验性异常。

输出测试用例时，在测试范围与覆盖情况简述中明确说明所采用的方法与覆盖度（例如：场景法×N，等价类+边界值×N，判定表覆盖规则数 N/M）。

## 测试用例输出格式（6 列标准字段）

所有生成的测试用例严格包含以下 6 列，字段顺序固定，便于直接落库：

| 序号 | 字段名称 | 规则说明 |
|------|---------|---------|
| 1 | 测试用例编号 | 统一规则递增编写（TC-XXX），如 TC-001、TC-002、TC-003…… |
| 2 | 测试用例名称 | 简洁清晰，精准描述本条用例测试场景。推荐格式：`[功能模块]-[场景描述]`，例如「用户登录-正确账号密码登录成功」 |
| 3 | 测试用例类型 | 取值见下文「测试用例类型定义」 |
| 4 | 前置条件 | 明确系统环境、数据准备、功能可用状态；需具体到可复现 |
| 5 | 执行步骤 | 分步清晰、可直接手动执行，步骤无歧义。格式：`1. ... 2. ... 3. ...` |
| 6 | 预期结果 | 结果精准、贴合业务规则。区分**正常返回逻辑**（成功响应、数据正确性）与**异常返回逻辑**（错误提示、状态码、拒绝行为） |

### 输出表格模板

```
| 测试用例编号 | 测试用例名称 | 测试用例类型 | 前置条件 | 执行步骤 | 预期结果 |
|-------------|-------------|-------------|---------|---------|---------|
| TC-001 | ... | ... | ... | 1. ... 2. ... | ... |
```

### Excel 列对应关系（落库映射）

6 列 Markdown 表格 → Excel 列对应如下，**列顺序不可调换**：

| Excel 列 | 来源字段 | 列宽建议 |
|---------|---------|---------|
| A | 测试用例编号 | 12 |
| B | 测试用例名称 | 38 |
| C | 测试用例类型 | 16 |
| D | 前置条件 | 40 |
| E | 执行步骤 | 50 |
| F | 预期结果 | 50 |

## 测试用例类型定义

- **功能正常场景**：标准条件下的核心正常流程（happy path）。
- **边界场景**：输入范围边界值、分页边界、日期边界、TopN 限制、金额边界。
- **异常场景**：非法输入、缺失必填项、权限拒绝、网络异常、服务端错误。
- **模糊查询**：部分输入匹配、通配符搜索、近似/模糊字符串匹配。
- **精准查询**：精确匹配条件、全参数检索、确定性结果。
- **排序筛选**：按各字段排序、多条件过滤、排序稳定性。
- **组合查询**：多查询条件组合、跨字段搜索、多维度过滤。
- **安全**：SQL 注入、XSS、未授权访问、越权、数据泄露。
- **性能**：负载下响应时间、并发查询、大数据量结果集处理。
- **UI 交互**：元素可见性、按钮状态、响应式布局、导航正确性。
- **金融专项**：对账、监管报送、审计轨迹、资金安全、数据一致性（识别到金融场景时强制覆盖）。

> 若被测功能以 AI/NLP 能力为主（自然语言查询、意图识别、槽位抽取），请使用 **test-case-generator-ai** 技能（5 列话术驱动、12 类 AI 必测场景）；本技能遇少量 AI 交互时亦可参考 `references/ai-testing-scenarios.md`。

## 设计原则

1. **用例不重复、不遗漏**：每条用例针对唯一场景；通过场景分解保证全覆盖且无冗余。
2. **场景颗粒度中等**：每条用例聚焦单一明确目标——不过粗（多个无关断言）也不过细（琐碎变体）。
3. **符合金融软件测试规范**：严格数据校验、审计轨迹验证、交易完整性检查，涉及监管合规时予以覆盖。
4. **语言专业、标准化**：使用清晰、专业的测试术语；用例可直接用于测试执行、提测交付、用例归档。
5. **可追溯性**：每条用例可追溯至需求点或业务规则；必要时在用例名称中标注来源需求。
6. **可复现性**：前置条件与执行步骤足够具体，任何测试人员无需额外背景即可复现。

## 输出形式

### 默认交付：Excel 文件（.xlsx）

最终交付物为 Excel 文件，回复中同时给出 Markdown 表格预览。

**Excel 规范：**

| 项目 | 规范 |
|------|------|
| Sheet 名 | 功能或模块名称（中文，≤20 字），如「投放活动查询」「用户登录」 |
| 表头行 | 6 列标准字段名（粗体、白字、深蓝底 1F4E78） |
| 数据行 | 按测试用例类型分组排列；编号递增连续 |
| 列宽 | A=12 / B=38 / C=16 / D=40 / E=50 / F=50（按上表） |
| 冻结 | 冻结首行（表头） |
| 筛选 | 首行开启筛选 |
| 单元格 | 自动换行、垂直居顶；执行步骤与预期结果列允许长文本，行高自动估算 |
| 文件名 | `[功能模块]测试用例.xlsx`（中文模块名）或遵循用户指定 |
| 路径 | 写入当前 workspace 输出目录，便于 present_files 展示 |

### Excel 生成（JSON 数据 + 内置生成器）

采用「数据与样式分离」：每次只需编写一份 `testcases.json` 数据文件，样式由内置生成器统一处理，**任何机器输出完全一致**；不依赖网络与本机专属路径，整个技能文件夹可拷到任意环境直接使用（仅需 Python + openpyxl）。

**第 1 步：编写用例数据文件 `testcases.json`**（UTF-8 编码）

```json
{
  "file_name": "功能模块名测试用例",
  "sheets": [
    {
      "name": "功能模块名",
      "headers": ["测试用例编号", "测试用例名称", "测试用例类型", "前置条件", "执行步骤", "预期结果"],
      "col_widths": [12, 38, 16, 40, 50, 50],
      "rows": [
        ["TC-001", "用户登录-正确账号密码登录成功", "功能正常场景",
         "系统已部署，用户账号 test_user 已注册且密码正确",
         "1. 打开登录页 2. 输入账号 test_user 3. 输入正确密码 4. 点击登录",
         "登录成功，跳转首页，顶部展示用户名"]
      ]
    }
  ]
}
```

字段说明：
- `file_name`：默认输出文件名（不含扩展名）；也可在命令行第 2 个参数指定输出文件。
- `sheets`：支持多 Sheet（多模块/多套用例归档到同一文件）。
- `headers` / `col_widths`：与上文「Excel 列对应关系」一致（6 列，列序不可调换）。
- `rows`：每条为一个数组，元素按 `headers` 顺序；单元格内换行用 `\n`。

**第 2 步：保存生成器并运行**

将下方「生成器源码」保存为工作目录下的 `build_testcase_xlsx.py`
（本技能自带 `scripts/build_testcase_xlsx.py`，与内嵌源码完全一致，任选其一使用）：

```bash
python build_testcase_xlsx.py testcases.json                # 输出到 testcases.json 同目录、同名 .xlsx
python build_testcase_xlsx.py testcases.json 指定名称.xlsx  # 指定输出文件
```

**第 3 步：环境自检（任意机器仅首次执行）**

```bash
python --version              # 若无 python 命令，尝试 python3 或 py -3
python -c "import openpyxl"   # 若报 ModuleNotFoundError：
pip install openpyxl          # Windows 可加 --user；建议在 python -m venv 隔离环境安装
```

生成器在缺少 openpyxl 时会输出同样中文提示后退出。表头深蓝底(1F4E78)白字、冻结首行、开启筛选、自动换行与行高估算均由生成器统一处理，勿手工修改样式。

**生成器源码（`build_testcase_xlsx.py`）**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试用例 Excel 生成器（通用版）：python build_testcase_xlsx.py <用例数据.json> [输出.xlsx]
仅依赖 openpyxl（缺失: pip install openpyxl）。"""

import json
import math
import os
import sys


def display_width(text):
    """估算显示宽度：中文字符按 2 计，ASCII 按 1 计（用于行高估算）。"""
    return sum(2 if ord(ch) > 127 else 1 for ch in text)


def main():
    if len(sys.argv) < 2:
        print("用法: python build_testcase_xlsx.py <用例数据.json> [输出文件.xlsx]")
        sys.exit(1)

    input_path = sys.argv[1]
    if not os.path.isfile(input_path):
        print(f"[错误] 找不到输入文件: {input_path}")
        sys.exit(1)

    with open(input_path, encoding="utf-8") as f:
        spec = json.load(f)

    default_name = spec.get("file_name") or os.path.splitext(os.path.basename(input_path))[0]
    out_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(os.path.abspath(input_path)), default_name + ".xlsx"
    )

    try:
        from openpyxl import Workbook
        from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
        from openpyxl.utils import get_column_letter
    except ImportError:
        print("[错误] 缺少 openpyxl 库，请先执行: pip install openpyxl")
        sys.exit(1)

    header_font = Font(name="微软雅黑", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill("solid", fgColor="1F4E78")
    header_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    data_font = Font(name="微软雅黑", size=10)
    data_align = Alignment(wrap_text=True, vertical="top", horizontal="left")
    thin = Side(style="thin", color="999999")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    wb = Workbook()
    wb.remove(wb.active)  # 删除默认空 Sheet

    total_rows = 0
    for sheet in spec.get("sheets", []):
        headers = sheet["headers"]
        widths = sheet.get("col_widths") or [16] * len(headers)
        rows = sheet.get("rows", [])
        if len(headers) != len(widths):
            raise ValueError(f"Sheet[{sheet.get('name')}] headers 与 col_widths 长度不一致")

        ws = wb.create_sheet(sheet.get("name", "Sheet1")[:31])

        for col, (name, width) in enumerate(zip(headers, widths), start=1):
            cell = ws.cell(row=1, column=col, value=str(name))
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_align
            cell.border = border
            ws.column_dimensions[get_column_letter(col)].width = width
        ws.row_dimensions[1].height = 24

        for r, row in enumerate(rows, start=2):
            if len(row) != len(headers):
                raise ValueError(
                    f"Sheet[{sheet.get('name')}] 第 {r - 1} 条数据列数({len(row)})"
                    f"与表头({len(headers)})不一致"
                )
            max_lines = 1
            for col, value in enumerate(row, start=1):
                text = "" if value is None else str(value)
                cell = ws.cell(row=r, column=col, value=text)
                cell.font = data_font
                cell.alignment = data_align
                cell.border = border
                usable = max(widths[col - 1] - 2, 4)
                lines = sum(max(1, math.ceil(display_width(seg) / usable)) for seg in text.split("\n"))
                max_lines = max(max_lines, lines)
            ws.row_dimensions[r].height = max(18, min(16 * max_lines + 8, 320))

        total_rows += len(rows)
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    wb.save(out_path)
    print(f"已生成: {out_path}")
    print(f"汇总: {len(spec.get('sheets', []))} 个 Sheet，共 {total_rows} 条用例")


if __name__ == "__main__":
    main()
```

### 回复内预览

生成 Excel 的同时，在回复中以 Markdown 表格附上用例预览（用例数较多时可展示按类型分组的汇总 + 代表性用例），便于用户快速审阅。

## 完成前检查清单

输出测试用例前逐项核验：

- [ ] 输入中的全部功能点均已覆盖。
- [ ] 无重复测试用例。
- [ ] 每条用例 6 列字段全部填写完整。
- [ ] 测试用例编号递增且连续（TC-XXX）。
- [ ] 前置条件具体、可复现。
- [ ] 执行步骤无歧义、可直接手动执行。
- [ ] 预期结果精准，区分正常/异常返回逻辑。
- [ ] 每个输入字段均包含边界与异常场景。
- [ ] 查询/输入类功能包含安全用例。
- [ ] 涉及金融场景时，对账/监管/审计/资金安全/数据一致性专项用例已覆盖。
- [ ] 已在简述中说明所采用的测试设计方法与覆盖度。
- [ ] 已生成 Excel 文件（默认交付），列宽、冻结、筛选、文件名规范。
- [ ] 已用 present_files 展示 Excel 给用户。
- [ ] 语言专业、标准化。

## 环境要求

- Python 3.8+（Windows / macOS / Linux 均可），仅需标准库 + openpyxl。
- openpyxl 缺失时：`pip install openpyxl`（生成器会自动检测并给出中文提示）。
- 无网络、无密钥、无本机专属路径依赖。

## 目录结构与分发

技能目录结构：

```
test-case-generator/
├── SKILL.md                            # 技能主文件（含 Excel 生成器完整源码）
├── scripts/
│   ├── build_testcase_xlsx.py          # Excel 生成器（JSON → xlsx，通用可复用）
│   └── parse_xmind.py                  # XMind 解析器（.xmind → Markdown 大纲/JSON，兼容 Zen 与 XMind8）
├── references/
│   └── ai-testing-scenarios.md         # AI 必测场景参考（仅涉及 AI 时加载）
├── package.json                        # 技能元信息
└── README.md                           # 安装与使用说明
```

**分发/安装到其他环境**：将整个文件夹（或解压 `test-case-generator.zip` 得到的文件夹）放入
`<用户主目录>/.workbuddy/skills/`（个人级）或 `<项目>/.workbuddy/skills/`（项目级），
重启 / 刷新 WorkBuddy 即可在对话中 @test-case-generator 触发。所有依赖（Python + openpyxl）在目标机器首次使用时自动检测并提示安装。

## 参考资料

- `references/ai-testing-scenarios.md` — AI 功能必测场景详细设计指导（含每类场景的目标、设计指导、测试要点）。当被测功能涉及 AI/NLP 能力时加载本文件。
