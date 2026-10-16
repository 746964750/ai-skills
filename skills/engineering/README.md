# 架构与工程规范

认识现有架构、识别技术债并维护工程约束。

仓库摸底选 code-analyzer；架构设计选 system-architect；工程文档与检查机制选 harness-maintainer。

[返回仓库导航](../../README.md) · [迁移说明](../../docs/migration.md)

## 技能

| 技能 | 用途 | 标签 / 使用说明 |
|---|---|---|
| [harness-maintainer](../../skills/engineering/harness-maintainer/SKILL.md) | 初始化、更新或审计工程文档、检查工具和责任机制。 | Harness；工程规范 |
| [system-architect](../../skills/engineering/system-architect/SKILL.md) | 设计系统架构、模块边界和适用工程标准。 | 架构设计；工程规范 |
| [code-analyzer](../../skills/engineering/code-analyzer/SKILL.md) | 分析架构、数据流、业务规则和 DDD 模式。 | 代码分析；DDD |
| [agent-git-oracle](../../skills/engineering/agent-git-oracle/SKILL.md) | 分析仓库技术债和架构反模式。 | 技术债；架构分析；原技能声明 x402 付费元数据及 OpenClaw 命令；使用前核验外部工具和费用条件。 |

## 安装本组

```sh
npx skills add maoyao0607/ai-skills --skill harness-maintainer system-architect code-analyzer agent-git-oracle -g -y
```

安装后重新打开会话。涉及第三方服务或清理操作时，先阅读该技能的使用说明。
