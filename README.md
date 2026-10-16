# AI Skills

按工作阶段分组的 Agent Skills 集合：40 个技能、7 个分组。每个技能只保留一份完整目录，行业与终端通过标签辅助查找。

结构为 `skills/<分组>/<技能名>/`。技能内部的 `agents/openai.yaml` 是发现元数据；工作流示例集中在 [docs/workflows](docs/workflows/README.md)。

## 分类导航

| 分类 | 数量 | 适用任务 |
|---|---:|---|
| [需求与产品](skills/requirements/README.md) | 8 | 从原始材料或产品想法建立可追溯、可评审的需求。 |
| [设计与界面](skills/design/README.md) | 8 | 完成原型、设计稿还原、界面质量改进和行业样式落地。 |
| [架构与工程规范](skills/engineering/README.md) | 4 | 认识现有架构、识别技术债并维护工程约束。 |
| [开发与重构](skills/development/README.md) | 4 | 实现功能，或在既有行为约束下改进代码结构。 |
| [审查与测试](skills/quality/README.md) | 7 | 核对需求与实现，设计测试并建立质量反馈。 |
| [故障诊断](skills/debugging/README.md) | 7 | 通过症状、日志与复现证据定位故障并验证修复。 |
| [工作与系统工具](skills/utilities/README.md) | 2 | 整理工作记录和分析本机存储。 |

## 安装

先查看可发现技能，再选择单个或分组安装。`-g` 表示全局安装，`-y` 表示跳过交互确认。

```sh
npx skills add maoyao0607/ai-skills --list
npx skills add maoyao0607/ai-skills --skill ai-coder -g -y
```

安装全部 40 个技能（包含第三方服务及付费依赖技能；安装本身不表示已授权外部调用）：

```sh
npx skills add maoyao0607/ai-skills --skill '*' -g -y
```

各分类页面提供该组完整安装命令。重新打开会话后使用；目录整理前的旧路径和名称请参见 [迁移说明](docs/migration.md)。

## 使用方式

按当前任务选择一个主技能，只有需要时才组合专项技能。需求抽取、功能开发、审查、排错分别承担不同阶段，不要求每次执行完整链路。

- WCS 范围梳理：选择 wcs-requirement-extractor。
- WMS 界面：按 PDA 或管理端选择对应样式技能，并与开发技能配合。
- 功能实现：选择 ai-coder；代码审查：选择 code-review；故障定位：选择 diagnosing-bugs。
- NEXUS 错误解释会向第三方发送输入，且涉及支付凭据；agent-git-oracle 也声明外部工具及付费元数据。使用前查看说明。
- 存储扫描只读；网页清理服务可删除文件，属于独立写操作。原技能注明 Windows 未经真实环境验证。

## 全部技能

### 需求与产品

文档抽取选 requirement-extractor；WCS 范围选专项抽取；需求探索选 requirements-analysis；PRD 撰写与评审按产物选择。

| 技能 | 用途 | 标签 / 使用说明 |
|---|---|---|
| [requirement-extractor](skills/requirements/requirement-extractor/SKILL.md) | 从 Word、Excel、PDF 等材料抽取指定主体的功能、接口、歧义及出处。 | 需求抽取；出处追溯 |
| [wcs-requirement-extractor](skills/requirements/wcs-requirement-extractor/SKILL.md) | 抽取 WCS 功能并区分上游业务系统、PLC 与设备控制层职责。 | 工业仓储；WCS；职责边界 |
| [requirements-analysis](skills/requirements/requirements-analysis/SKILL.md) | 通过需求探索拆分 EPIC、需求和用户故事并排序。 | 用户故事；优先级 |
| [software-manager-skill](skills/requirements/software-manager-skill/SKILL.md) | 提供产品规划、路线图、竞品分析、PRD 和原型工作流。 | 产品规划；PRD；完整流程需要可用的网络搜索及资料检索能力；按当前任务选择阶段。 |
| [prd](skills/requirements/prd/SKILL.md) | 生成面向开发执行的用户故事、验收标准及结构化 PRD。 | PRD；验收标准 |
| [prd-writer-pro](skills/requirements/prd-writer-pro/SKILL.md) | 将需求整理为结构清晰、内容完整的产品需求文档。 | PRD；文档撰写 |
| [prd-reviewer](skills/requirements/prd-reviewer/SKILL.md) | 按明确评分维度评审 PRD 并说明扣分与改进项。 | PRD；需求评审 |
| [prd-to-design-doc](skills/requirements/prd-to-design-doc/SKILL.md) | 将 PRD 转为信息架构、交互、布局和视觉设计需求。 | PRD；设计交付 |

### 设计与界面

通用原型选 prd-to-prototype；设计还原选 design-to-code；WMS 项目按终端选择 PDA 或管理端样式。

| 技能 | 用途 | 标签 / 使用说明 |
|---|---|---|
| [prd-to-prototype](skills/design/prd-to-prototype/SKILL.md) | 从产品想法生成 PRD 和 HTML/Tailwind 可交互原型。 | 原型；HTML |
| [design-to-code](skills/design/design-to-code/SKILL.md) | 将 Figma、Sketch 或图片设计稿还原为前端代码。 | 设计稿还原；前端 |
| [ui-design](skills/design/ui-design/SKILL.md) | 提供布局、字体、色彩、无障碍和动效的界面设计指导。 | UI；无障碍 |
| [frontend-design-pro](skills/design/frontend-design-pro/SKILL.md) | 审视并改进前端界面质量与视觉细节。 | 前端；界面优化 |
| [wireframe](skills/design/wireframe/SKILL.md) | 生成 ASCII/SVG 线框、用户流程及 HTML 展示。 | 线框；用户流程 |
| [afrexai-ui-design-system](skills/design/afrexai-ui-design-system/SKILL.md) | 提供从设计调研到组件、交互和响应式落地的设计方法。 | 设计系统；响应式 |
| [byd-wms-pda-style](skills/design/byd-wms-pda-style/SKILL.md) | 复用 WMS PDA 主题、页面骨架、扫码模板和样式检查。 | 工业仓储；WMS；PDA；比亚迪 |
| [byd-wms-manage-style](skills/design/byd-wms-manage-style/SKILL.md) | 复用 WMS 管理端主题、查询表格、弹窗、抽屉和样式检查。 | 工业仓储；WMS；管理端；比亚迪 |

### 架构与工程规范

仓库摸底选 code-analyzer；架构设计选 system-architect；工程文档与检查机制选 harness-maintainer。

| 技能 | 用途 | 标签 / 使用说明 |
|---|---|---|
| [harness-maintainer](skills/engineering/harness-maintainer/SKILL.md) | 初始化、更新或审计工程文档、检查工具和责任机制。 | Harness；工程规范 |
| [system-architect](skills/engineering/system-architect/SKILL.md) | 设计系统架构、模块边界和适用工程标准。 | 架构设计；工程规范 |
| [code-analyzer](skills/engineering/code-analyzer/SKILL.md) | 分析架构、数据流、业务规则和 DDD 模式。 | 代码分析；DDD |
| [agent-git-oracle](skills/engineering/agent-git-oracle/SKILL.md) | 分析仓库技术债和架构反模式。 | 技术债；架构分析；原技能声明 x402 付费元数据及 OpenClaw 命令；使用前核验外部工具和费用条件。 |

### 开发与重构

功能实现选 ai-coder；完整重构选 code-refactoring；小范围精简选 simplify；原则性指导选 uncle-bob。

| 技能 | 用途 | 标签 / 使用说明 |
|---|---|---|
| [ai-coder](skills/development/ai-coder/SKILL.md) | 遵循现有仓库约定实现前后端功能并完成验证。 | 功能开发；全栈 |
| [code-refactoring](skills/development/code-refactoring/SKILL.md) | 运用重构模式改善结构并保持既有行为。 | 重构；遗留代码 |
| [simplify](skills/development/simplify/SKILL.md) | 对局部代码做清晰、可维护的精简重构。 | 重构；代码精简 |
| [uncle-bob](skills/development/uncle-bob/SKILL.md) | 将 Clean Code、SOLID 与整洁架构原则用于代码改进。 | SOLID；整洁代码 |

### 审查与测试

改动审查选 code-review；用例交付选 test-case-generator；按单测、接口、E2E 或 TDD 目标选择测试技能。

| 技能 | 用途 | 标签 / 使用说明 |
|---|---|---|
| [code-review](skills/quality/code-review/SKILL.md) | 分别核对工程规范和需求实现，报告有证据的发现。 | 代码审查；需求核验 |
| [test-case-generator](skills/quality/test-case-generator/SKILL.md) | 从需求、API、截图或 XMind 生成标准 Excel 测试用例。 | 测试用例；Excel；文中提及的 test-case-generator-ai 不包含在本仓库。 |
| [test-patterns](skills/quality/test-patterns/SKILL.md) | 提供跨语言单元、集成、E2E 测试和覆盖率实践。 | 单元测试；集成测试 |
| [superpowers-tdd](skills/quality/superpowers-tdd/SKILL.md) | 通过 RED-GREEN-REFACTOR 流程实施测试驱动开发。 | TDD；回归测试 |
| [api-test-automation](skills/quality/api-test-automation/SKILL.md) | 提供 REST、GraphQL、性能、契约测试及 Mock 工具。 | API；接口测试；运行工具前按技能 requirements.txt 准备依赖。 |
| [e2e-testing-patterns](skills/quality/e2e-testing-patterns/SKILL.md) | 构建 Playwright/Cypress 端到端测试并减少不稳定失败。 | E2E；Playwright；Cypress |
| [afrexai-qa-test-plan](skills/quality/afrexai-qa-test-plan/SKILL.md) | 生成测试计划、覆盖矩阵和自动化策略。 | 测试计划；QA |

### 故障诊断

一般故障先选 diagnosing-bugs；日志分析选 log-analyzer；其余调试流程按任务选一个，避免重复串联。

| 技能 | 用途 | 标签 / 使用说明 |
|---|---|---|
| [diagnosing-bugs](skills/debugging/diagnosing-bugs/SKILL.md) | 从症状、复现和证据定位根因，并按请求修复与回归。 | 故障诊断；根因分析 |
| [debug-pro](skills/debugging/debug-pro/SKILL.md) | 使用七步调试协议及多语言调试命令定位问题。 | 调试；多语言 |
| [superpowers-systematic-debugging](skills/debugging/superpowers-systematic-debugging/SKILL.md) | 按根因调查、模式分析、假设验证和修复执行调试。 | 调试；根因分析 |
| [bug-fixing](skills/debugging/bug-fixing/SKILL.md) | 提供分流、复现、影响分析、修复和回归流程。 | Bug修复；回归验证 |
| [code-fix](skills/debugging/code-fix/SKILL.md) | 诊断编译、运行时、类型、逻辑和依赖错误。 | 构建失败；异常排查 |
| [log-analyzer](skills/debugging/log-analyzer/SKILL.md) | 解析多格式日志、关联服务事件并分析堆栈。 | 日志；堆栈 |
| [nexus-error-explain](skills/debugging/nexus-error-explain/SKILL.md) | 调用 NEXUS 第三方服务解释错误信息。 | 第三方服务；付费依赖；输入会发送至 NEXUS 外部服务；需支付凭据或服务提供的测试模式，调用前确认数据与费用条件。 |

### 工作与系统工具

报工选 hs-warranty-report；磁盘占用选 storage-analyzer，先区分只读报告和执行清理。

| 技能 | 用途 | 标签 / 使用说明 |
|---|---|---|
| [hs-warranty-report](skills/utilities/hs-warranty-report/SKILL.md) | 根据对话、Git 和会话证据整理售后或质保报工。 | 售后；报工；工作记录 |
| [storage-analyzer](skills/utilities/storage-analyzer/SKILL.md) | 只读扫描磁盘占用，生成静态报告或启动交互式清理服务。 | 存储；Windows；macOS；扫描只读；清理服务支持回收站及永久删除，属于独立写操作。原技能注明 Windows 未经真实环境验证。 |

## 维护目录

`catalog.json` 是分类、简介、标签、说明和迁移映射的统一来源。修改技能或分类后运行：

```sh
python tools/catalog.py
python tools/catalog.py --check
```

生成器核验远端默认分支，生成本文件、七组导航、迁移说明及展示页数据。无法核验时报告错误；`--check` 只检查、不写文件。

生成内容直接提交，GitHub Pages 继续使用 docs 目录，无需新增站点依赖。验证说明见 [维护与验证](docs/maintenance.md)。

## 许可

保留各技能和字体自带的许可及来源声明；仓库当前未提供统一 LICENSE。
