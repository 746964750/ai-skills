# Output Schema

## Default report

When the user does not specify a format, create `WCS功能清单.md` with these sections:

1. 分析范围与口径
2. 文档清单与覆盖状态
3. WCS重点关注项
4. WCS功能清单
5. 接口与外部系统协同
6. 非功能要求
7. 待澄清与冲突
8. 非WCS职责/排除项
9. 出处追溯表
10. 覆盖统计与已知限制

## Function-list fields

| Field | Required | Rule |
|---|---:|---|
| `功能ID` | yes | Stable prefix: `WCS-FN`, `WCS-IF`, `WCS-NFR`, or `WCS-Q` |
| `一级模块` | yes | Use a stable functional grouping; do not copy arbitrary document headings when they mix concerns |
| `二级功能` | yes | Concise behavior name, normally verb + object |
| `功能说明` | yes | One atomic, testable behavior; preserve source constraints |
| `触发/前置条件` | when known | Leave blank or `待澄清`; do not invent |
| `输入` | when known | Message/data/state/equipment event |
| `处理/规则` | when known | Decisions, constraints, sequence, validation, retry, routing |
| `输出/结果` | when known | Command/message/state/data/observable result |
| `相关系统/设备` | when known | Upstream, downstream, controller, or equipment |
| `分类` | yes | `WCS功能`, `接口/协同`, `非功能要求`, `待澄清`, `非WCS职责` |
| `证据强度` | yes | `明确`, `推断`, `歧义` |
| `置信度` | yes | `高`, `中`, `低` with notes for medium/low |
| `重点标注` | yes | `是/否`; set to `是` for vague or boundary-ambiguous WCS-related passages |
| `关注级别` | when emphasized | Analyst signal `高/中/低`; never copy into customer priority |
| `模糊类型` | when emphasized | One or more controlled ambiguity types from the classification reference |
| `可能责任方/解释` | when emphasized | Plausible owners or interpretations; do not choose without evidence |
| `优先级` | no | Only copy a sourced priority; otherwise blank |
| `验收要点` | no | Only source-backed or explicitly labeled as proposed |
| `出处ID` | yes for all claims | One or more evidence IDs such as `EV-001; EV-017` |
| `假设/备注` | when needed | Boundary assumptions, conflicts, gaps, version issues |

## Evidence table fields

| `出处ID` | `来源文件` | `版本/日期` | `精确位置` | `原文摘录或忠实概述` | `提取方式` | `备注` |
|---|---|---|---|---|---|---|

`提取方式` values may include `原生文本`, `单元格`, `公式/批注`, `渲染核对`, `OCR`, or `视觉解读`.

## Priority-review fields

Use these fields in `WCS重点关注项`. A passage may appear here even when it cannot yet become a function row.

| `关注ID` | `关注级别` | `原文主题/忠实概述` | `模糊类型` | `可能责任方/解释` | `范围或实现影响` | `建议确认问题` | `关联功能ID` | `出处ID` | `状态` |
|---|---|---|---|---|---|---|---|---|---|

- `关注ID`: use `WCS-FOCUS-001` style IDs.
- `状态`: `未确认`, `暂定`, `已确认`, or `已关闭`; default to `未确认`.
- Sort `高 → 中 → 低`, then by source workflow order.
- In Markdown, prefix the attention level with visible text such as `⚠ 高`, `⚠ 中`, or `注意-低`; never rely on color alone.
- Keep the original wording or a faithful short summary beside the exact source so reviewers can judge the ambiguity directly.

## Clarification fields

| `问题ID` | `关注级别` | `模糊类型` | `待确认问题` | `可能责任方/解释` | `范围或实现影响` | `影响功能ID` | `建议确认对象` | `相关出处ID` |
|---|---|---|---|---|---|---|---|---|

Questions should be specific enough to answer, for example: owner, trigger, schema, timeout, retry, priority rule, exception disposition, acceptance threshold, or version authority.

## Coverage fields

For every corpus file record: `来源ID`, `文件`, `版本`, `格式`, `状态`, `已分析范围`, `未覆盖内容`, `备注`.

Allowed status values: `已分析`, `部分分析`, `重复`, `疑似旧版`, `受保护`, `不支持`, `无法读取`.

## Excel output

If an `.xlsx` is requested, create these sheets:

- `功能清单`: one row per normalized function/requirement
- `重点关注`: all vague or responsibility-ambiguous WCS passages, sorted by `关注级别` and linked to provisional functions/questions
- `出处追溯`: one row per evidence occurrence; do not collapse multiple sources into one long cell
- `待澄清`: open questions and conflicts
- `覆盖统计`: corpus file status and counts by classification/evidence strength/module

Use filters, frozen headers, wrapped text, deliberate widths, and readable row heights. Keep IDs as text. In `重点关注`, use restrained visual emphasis (for example red accent for `高`, amber for `中`, pale yellow for `低`) and include a text label so color is not the only signal. Include no formulas or priority scores unless they improve auditing and are clearly explained.

## ID and sorting conventions

- Assign IDs after deduplication so they remain stable within the delivered baseline.
- Sort functions by `分类 → 一级模块 → workflow order`, not alphabetically when sequence matters.
- Keep evidence IDs independent of function IDs; one evidence record can support multiple rows only when it truly contains multiple atomic requirements.
- Do not renumber existing IDs during an incremental update unless the user requests a clean re-baseline.

## Minimum summary

Report counts for analyzed files, partial/unreadable files, WCS anchor hits, accounted anchor hits, emphasized high/medium/low items, confirmed WCS functions, inferred functions, interfaces, non-functional requirements, open questions, conflicts, and exclusions. State the main analysis limitations.
