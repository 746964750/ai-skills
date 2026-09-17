# AI Skills

通用 Agent Skills 集合。每个 skill 提供可复用的工作流、规范引用与辅助脚本，覆盖需求分析、Harness 治理、全栈开发、代码审查、缺陷诊断与售后报工等场景。

## 仓库结构

```text
ai-skills/
└── skills/
    ├── requirement-extractor/      # 通用需求抽取
    ├── wcs-requirement-extractor/  # WCS 专项需求抽取
    ├── harness-maintainer/         # Harness 初始化 / 增量维护 / 审计
    ├── ai-coder/                   # 按仓库约定落地功能开发
    ├── code-review/                # Standards × Spec 双轴审查
    ├── diagnosing-bugs/            # 症状驱动的根因定位与修复
    └── hs-warranty-report/         # 豪森质保/售后报工文案生成
```

每个 skill 目录至少包含：

| 文件 / 目录 | 说明 |
|-------------|------|
| `SKILL.md` | Agent 执行入口（frontmatter + 工作流） |
| `references/` | 规范、分类规则、输出 schema 等权威引用 |
| `scripts/` | 可选辅助脚本（如文档抽取、文档合并） |
| `agents/` | 可选的 Agent 元数据（如 `openai.yaml`） |
| `USAGE.md` | 面向人的使用说明（部分 skill 提供） |

## Skills 一览

| Skill | 用途 | 典型触发 |
|-------|------|----------|
| **requirement-extractor** | 从 Word / Excel / PDF 等文档抽取目标主体功能清单，可追溯出处，标注边界歧义 | 功能清单整理、RFP/规格分析、范围澄清 |
| **wcs-requirement-extractor** | 同上，锚定 WCS 职责边界与分类口径 | WCS 需求抽取、WCS 功能清单 |
| **harness-maintainer** | 按 Harness 构建规范初始化五篇核心文档、检查工具与 CI；或增量更新 / 只读审计 | 新项目接入、存量改造、任务收尾文档同步 |
| **ai-coder** | 在现有项目中按仓库约定实现前后端/全栈功能并验证 | 新增功能、页面、接口、范围明确的重构 |
| **code-review** | 对分支 / PR / 提交 / 未提交改动做规范与需求双轴审查（默认只报告不改代码） | 合并前检查、review since X |
| **diagnosing-bugs** | 以可复现症状与证据定位故障；仅诊断时不自动改代码 | debug、根因分析、性能回退 |
| **hs-warranty-report** | 按售后报工规范生成「项目名称」与「具体工作内容」（现象 / 过程 / 输出物） | 质保报工、整理近一周 session |

## 安装

使用 [skills.sh](https://skills.sh/) CLI（仓库：`maoyao0607/ai-skills`）。`-g` 表示全局安装，`-y` 跳过确认。

### 安装全部

```bash
npx skills add maoyao0607/ai-skills -g -y
```

### 按 skill 安装

```bash
npx skills add maoyao0607/ai-skills@requirement-extractor -g -y
npx skills add maoyao0607/ai-skills@wcs-requirement-extractor -g -y
npx skills add maoyao0607/ai-skills@harness-maintainer -g -y
npx skills add maoyao0607/ai-skills@ai-coder -g -y
npx skills add maoyao0607/ai-skills@code-review -g -y
npx skills add maoyao0607/ai-skills@diagnosing-bugs -g -y
npx skills add maoyao0607/ai-skills@hs-warranty-report -g -y
```

| Skill | 安装命令 |
|-------|----------|
| requirement-extractor | `npx skills add maoyao0607/ai-skills@requirement-extractor -g -y` |
| wcs-requirement-extractor | `npx skills add maoyao0607/ai-skills@wcs-requirement-extractor -g -y` |
| harness-maintainer | `npx skills add maoyao0607/ai-skills@harness-maintainer -g -y` |
| ai-coder | `npx skills add maoyao0607/ai-skills@ai-coder -g -y` |
| code-review | `npx skills add maoyao0607/ai-skills@code-review -g -y` |
| diagnosing-bugs | `npx skills add maoyao0607/ai-skills@diagnosing-bugs -g -y` |
| hs-warranty-report | `npx skills add maoyao0607/ai-skills@hs-warranty-report -g -y` |

安装后重新打开会话，在对话中描述目标即可触发对应 skill（例如「帮我写质保报工」「为当前仓库初始化 Harness」）。

## 使用建议

1. **先读 `SKILL.md`**：Agent 应按其中工作流与必读 references 执行，不要跳过质量门禁。
2. **Harness 优先**：`ai-coder` / `code-review` / `diagnosing-bugs` 会优先遵循目标仓库的 `AGENTS.md` 与 `docs/{architecture,conventions,domain,golden-rules}.md`。
3. **需求抽取先声明主体**：通用抽取须明确目标主体、相邻系统与权属口径；WCS 专项则固定 WCS 边界模型。
4. **报工勿编造**：`hs-warranty-report` 只基于对话 / session / git 证据生成文案，不代替考勤系统录入。

## 开发约定

- 新增 skill：在 `skills/<name>/` 下提供完整的 `SKILL.md`（含 YAML frontmatter：`name`、`description`）。
- 规范类条文放在 `references/`，示例与脚本分别放在 `references/`、`scripts/`、`assets/`，保持 `SKILL.md` 精炼可执行。
- 面向人的操作说明可另写 `USAGE.md`，与 Agent 入口分离。
- 不在 skill 中硬编码密钥、真实客户数据或未授权的生产操作。

## License

以仓库实际声明为准；未声明时默认仅供内部使用与协作改进。
