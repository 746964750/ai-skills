# Source Location Rules

## Evidence record

Each evidence record needs:

- `source_id`: stable file identifier such as `SRC-001`
- `file`: exact file name and, when useful, relative path
- `version`: version/date/revision found in the file name or content; otherwise blank
- `locator`: format-specific location that another reviewer can open directly
- `evidence`: a short quote or faithful paraphrase containing the operative requirement
- `evidence_strength`: `明确`, `推断`, or `歧义`
- `notes`: table/header context, diagram interpretation, conflict, or extraction limitation

Keep quotes short and sufficient. Do not paste entire pages or large tables into the output.

## WCS anchor sweep

Before classification, search case-insensitively for `WCS`, `Warehouse Control System`, Chinese warehouse-control names, project-defined aliases, and WCS-scoped headings/table titles. For each hit:

1. Capture enough surrounding context to resolve the subject: the full paragraph, table row with headers, sheet row/column headers, PDF section, or complete diagram legend/arrow.
2. Assign an evidence record even when the passage is too vague to become a committed function.
3. Record whether the hit became a function, interface, non-functional requirement, priority-review item, or exclusion.
4. Reconcile `锚点命中数 = 已归类数`; explain any extraction limitation rather than leaving unmatched hits.

Do not treat every generic “系统” as WCS. It is a WCS alias only when the document defines it or the enclosing section/table/diagram makes the referent clear.

## Word / DOCX

Preferred locator order:

1. Verified rendered page number, if page layout was rendered and inspected.
2. Heading path plus paragraph sequence, for example `3.2 任务调度 > 段落 4`.
3. Table number/index plus row and cell header, for example `表 6 / 行 12 / “功能要求”列`.
4. Header, footer, comment, text box, caption, or drawing label when requirement text appears there.

Do not infer a Word page number from XML paragraph order. If page rendering is unavailable, omit the page and use structural locators. Inspect tracked changes/comments when they can change meaning. Record whether deleted or proposed text was included.

## Excel / XLSX

Use exact A1 locators:

- single cell: `SheetName!F27`
- contiguous range: `SheetName!B12:G12`
- named table/range when present: `需求清单[功能描述]`, plus the A1 cells when possible

Record the displayed value and formula/comment when relevant. Preserve row/column headers needed to understand the cell. Note hidden sheets/rows/columns, merged cells, filters, and multiple versions. For a merged range, cite the full merged range and its top-left value. Never cite only a worksheet name.

## PDF

Use 1-based pages verified from the actual PDF:

- `第 14 页 / 4.3.2 异常处理`
- `第 22 页 / 表 8 / 行“输送机故障”`
- `第 9 页 / 图 3 / WCS→PLC 箭头`

For scanned or low-text pages, render the page and visually inspect it. State when OCR or visual interpretation was used. Preserve footnotes, legends, callouts, table continuations, and diagram arrows that affect meaning.

## Text, Markdown, CSV, and TSV

- text/Markdown: line range plus nearest heading, for example `lines 88-93 / ## Exceptions`
- CSV/TSV: 1-based data row and column header; include raw line number if the file may be opened as text

## Other formats

- PowerPoint: slide number plus title and shape/table identifier.
- Image: file name plus visible region/label; record that the locator is visual.
- Email/chat/export: message timestamp, sender/channel/thread, and a short anchor.
- Legacy `.doc`/`.xls`: convert to a reviewable copy, cite the converted location, and retain a link to the original source/version.

## Multiple sources and conflicts

- Store each source occurrence as a separate evidence record.
- A function row may reference multiple evidence IDs.
- When sources disagree, preserve both statements, name the conflicting fields, and add a clarification item. Do not choose the newest file unless version authority is established.

## Verification gate

Before delivery, sample-check at least one locator from every analyzed file and every location type used (page, paragraph, table, sheet/cell, diagram, comment). Check all high-risk, inferred, ambiguous, and conflicting items, not just a sample.
