# 审查与测试

核对需求与实现，设计测试并建立质量反馈。

改动审查选 code-review；用例交付选 test-case-generator；按单测、接口、E2E 或 TDD 目标选择测试技能。

[返回仓库导航](../../README.md) · [迁移说明](../../docs/migration.md)

## 技能

| 技能 | 用途 | 标签 / 使用说明 |
|---|---|---|
| [code-review](../../skills/quality/code-review/SKILL.md) | 分别核对工程规范和需求实现，报告有证据的发现。 | 代码审查；需求核验 |
| [test-case-generator](../../skills/quality/test-case-generator/SKILL.md) | 从需求、API、截图或 XMind 生成标准 Excel 测试用例。 | 测试用例；Excel；文中提及的 test-case-generator-ai 不包含在本仓库。 |
| [test-patterns](../../skills/quality/test-patterns/SKILL.md) | 提供跨语言单元、集成、E2E 测试和覆盖率实践。 | 单元测试；集成测试 |
| [superpowers-tdd](../../skills/quality/superpowers-tdd/SKILL.md) | 通过 RED-GREEN-REFACTOR 流程实施测试驱动开发。 | TDD；回归测试 |
| [api-test-automation](../../skills/quality/api-test-automation/SKILL.md) | 提供 REST、GraphQL、性能、契约测试及 Mock 工具。 | API；接口测试；运行工具前按技能 requirements.txt 准备依赖。 |
| [e2e-testing-patterns](../../skills/quality/e2e-testing-patterns/SKILL.md) | 构建 Playwright/Cypress 端到端测试并减少不稳定失败。 | E2E；Playwright；Cypress |
| [afrexai-qa-test-plan](../../skills/quality/afrexai-qa-test-plan/SKILL.md) | 生成测试计划、覆盖矩阵和自动化策略。 | 测试计划；QA |

## 安装本组

```sh
npx skills add maoyao0607/ai-skills --skill code-review test-case-generator test-patterns superpowers-tdd api-test-automation e2e-testing-patterns afrexai-qa-test-plan -g -y
```

安装后重新打开会话。涉及第三方服务或清理操作时，先阅读该技能的使用说明。
