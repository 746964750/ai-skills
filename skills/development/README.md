# 开发与重构

实现功能，或在既有行为约束下改进代码结构。

功能实现选 ai-coder；完整重构选 code-refactoring；小范围精简选 simplify；原则性指导选 uncle-bob。

[返回仓库导航](../../README.md) · [迁移说明](../../docs/migration.md)

## 技能

| 技能 | 用途 | 标签 / 使用说明 |
|---|---|---|
| [ai-coder](../../skills/development/ai-coder/SKILL.md) | 遵循现有仓库约定实现前后端功能并完成验证。 | 功能开发；全栈 |
| [code-refactoring](../../skills/development/code-refactoring/SKILL.md) | 运用重构模式改善结构并保持既有行为。 | 重构；遗留代码 |
| [simplify](../../skills/development/simplify/SKILL.md) | 对局部代码做清晰、可维护的精简重构。 | 重构；代码精简 |
| [uncle-bob](../../skills/development/uncle-bob/SKILL.md) | 将 Clean Code、SOLID 与整洁架构原则用于代码改进。 | SOLID；整洁代码 |

## 安装本组

```sh
npx skills add maoyao0607/ai-skills --skill ai-coder code-refactoring simplify uncle-bob -g -y
```

安装后重新打开会话。涉及第三方服务或清理操作时，先阅读该技能的使用说明。
