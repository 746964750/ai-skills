# 目录与名称迁移

[返回仓库导航](../README.md)

全部 40 个技能已归入七个工作阶段分组，原根 agents 领域目录已迁空移除。每个技能的内部资产随目录整体保留。

已有安装不会自动移动或改名。先使用 `npx skills list -g` 查看已装技能；按下表的新名称重新安装。若旧名称仍保留，核对个人修改后自行移除旧条目。

手工复制或通过旧路径链接的使用者需更新到新目录，不提供重复技能副本或旧路径软链接。目标业务项目中的 `agents/prd.json` 等输出路径保持原意。

## 名称变化

| 旧声明名 | 新声明名 |
|---|---|
| `prd-writer` | `prd-writer-pro` |
| `PRD to Prototype` | `prd-to-prototype` |
| `bug-fixing-openclaw` | `bug-fixing` |
| `code-error-fixer` | `code-fix` |

重新安装上述四个技能：

```sh
npx skills add maoyao0607/ai-skills --skill prd-writer-pro prd-to-prototype bug-fixing code-fix -g -y
```

## 全部路径映射

| 旧路径 | 新路径 |
|---|---|
| `skills/requirement-extractor/` | [skills/requirements/requirement-extractor/](../skills/requirements/requirement-extractor/SKILL.md) |
| `skills/wcs-requirement-extractor/` | [skills/requirements/wcs-requirement-extractor/](../skills/requirements/wcs-requirement-extractor/SKILL.md) |
| `agents/PRD 撰写/skills/requirements-analysis/` | [skills/requirements/requirements-analysis/](../skills/requirements/requirements-analysis/SKILL.md) |
| `agents/PRD 撰写/skills/software-manager-skill/` | [skills/requirements/software-manager-skill/](../skills/requirements/software-manager-skill/SKILL.md) |
| `agents/PRD 撰写/skills/prd/` | [skills/requirements/prd/](../skills/requirements/prd/SKILL.md) |
| `agents/PRD 撰写/skills/prd-writer-pro/` | [skills/requirements/prd-writer-pro/](../skills/requirements/prd-writer-pro/SKILL.md) |
| `agents/PRD 撰写/skills/prd-reviewer/` | [skills/requirements/prd-reviewer/](../skills/requirements/prd-reviewer/SKILL.md) |
| `agents/PRD 撰写/skills/prd-to-design-doc/` | [skills/requirements/prd-to-design-doc/](../skills/requirements/prd-to-design-doc/SKILL.md) |
| `agents/UI 原型设计/skills/prd-to-prototype/` | [skills/design/prd-to-prototype/](../skills/design/prd-to-prototype/SKILL.md) |
| `agents/UI 原型设计/skills/design-to-code/` | [skills/design/design-to-code/](../skills/design/design-to-code/SKILL.md) |
| `agents/UI 原型设计/skills/ui-design/` | [skills/design/ui-design/](../skills/design/ui-design/SKILL.md) |
| `agents/UI 原型设计/skills/frontend-design-pro/` | [skills/design/frontend-design-pro/](../skills/design/frontend-design-pro/SKILL.md) |
| `agents/UI 原型设计/skills/wireframe/` | [skills/design/wireframe/](../skills/design/wireframe/SKILL.md) |
| `agents/UI 原型设计/skills/afrexai-ui-design-system/` | [skills/design/afrexai-ui-design-system/](../skills/design/afrexai-ui-design-system/SKILL.md) |
| `skills/byd-wms-pda-style/` | [skills/design/byd-wms-pda-style/](../skills/design/byd-wms-pda-style/SKILL.md) |
| `skills/byd-wms-manage-style/` | [skills/design/byd-wms-manage-style/](../skills/design/byd-wms-manage-style/SKILL.md) |
| `skills/harness-maintainer/` | [skills/engineering/harness-maintainer/](../skills/engineering/harness-maintainer/SKILL.md) |
| `agents/代码重构/skills/system-architect/` | [skills/engineering/system-architect/](../skills/engineering/system-architect/SKILL.md) |
| `agents/代码重构/skills/code-analyzer/` | [skills/engineering/code-analyzer/](../skills/engineering/code-analyzer/SKILL.md) |
| `agents/代码重构/skills/agent-git-oracle/` | [skills/engineering/agent-git-oracle/](../skills/engineering/agent-git-oracle/SKILL.md) |
| `skills/ai-coder/` | [skills/development/ai-coder/](../skills/development/ai-coder/SKILL.md) |
| `agents/代码重构/skills/code-refactoring/` | [skills/development/code-refactoring/](../skills/development/code-refactoring/SKILL.md) |
| `agents/代码重构/skills/simplify/` | [skills/development/simplify/](../skills/development/simplify/SKILL.md) |
| `agents/代码重构/skills/uncle-bob/` | [skills/development/uncle-bob/](../skills/development/uncle-bob/SKILL.md) |
| `skills/code-review/` | [skills/quality/code-review/](../skills/quality/code-review/SKILL.md) |
| `agents/自动化测试/skills/test-case-generator/` | [skills/quality/test-case-generator/](../skills/quality/test-case-generator/SKILL.md) |
| `agents/自动化测试/skills/test-patterns/` | [skills/quality/test-patterns/](../skills/quality/test-patterns/SKILL.md) |
| `agents/自动化测试/skills/superpowers-tdd/` | [skills/quality/superpowers-tdd/](../skills/quality/superpowers-tdd/SKILL.md) |
| `agents/自动化测试/skills/api-test-automation/` | [skills/quality/api-test-automation/](../skills/quality/api-test-automation/SKILL.md) |
| `agents/自动化测试/skills/e2e-testing-patterns/` | [skills/quality/e2e-testing-patterns/](../skills/quality/e2e-testing-patterns/SKILL.md) |
| `agents/自动化测试/skills/afrexai-qa-test-plan/` | [skills/quality/afrexai-qa-test-plan/](../skills/quality/afrexai-qa-test-plan/SKILL.md) |
| `skills/diagnosing-bugs/` | [skills/debugging/diagnosing-bugs/](../skills/debugging/diagnosing-bugs/SKILL.md) |
| `agents/Bug 排查/skills/debug-pro/` | [skills/debugging/debug-pro/](../skills/debugging/debug-pro/SKILL.md) |
| `agents/Bug 排查/skills/superpowers-systematic-debugging/` | [skills/debugging/superpowers-systematic-debugging/](../skills/debugging/superpowers-systematic-debugging/SKILL.md) |
| `agents/Bug 排查/skills/bug-fixing/` | [skills/debugging/bug-fixing/](../skills/debugging/bug-fixing/SKILL.md) |
| `agents/Bug 排查/skills/code-fix/` | [skills/debugging/code-fix/](../skills/debugging/code-fix/SKILL.md) |
| `agents/Bug 排查/skills/log-analyzer/` | [skills/debugging/log-analyzer/](../skills/debugging/log-analyzer/SKILL.md) |
| `agents/Bug 排查/skills/nexus-error-explain/` | [skills/debugging/nexus-error-explain/](../skills/debugging/nexus-error-explain/SKILL.md) |
| `skills/hs-warranty-report/` | [skills/utilities/hs-warranty-report/](../skills/utilities/hs-warranty-report/SKILL.md) |
| `skills/storage-analyzer/` | [skills/utilities/storage-analyzer/](../skills/utilities/storage-analyzer/SKILL.md) |

## 领域文档

原五个领域的工作流文档迁入 [workflows](workflows/README.md)。原重复 INSTALL 文档由各组导航中的安装命令替代。

安装命令通过仓库短名和 `--skill` 选择技能，不再依赖旧目录或固定 main 分支。新增两份缺失的 frontmatter；为 prd、superpowers-tdd、superpowers-systematic-debugging 的原 description 加引号，修复冒号导致的 YAML 解析失败，含义和正文不变。

另外修正 system-architect 对三份未随原仓库分发的配置模板的失效链接，改为明确的配置示例说明；没有新增或假造模板。
