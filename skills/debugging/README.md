# 故障诊断

通过症状、日志与复现证据定位故障并验证修复。

一般故障先选 diagnosing-bugs；日志分析选 log-analyzer；其余调试流程按任务选一个，避免重复串联。

[返回仓库导航](../../README.md) · [迁移说明](../../docs/migration.md)

## 技能

| 技能 | 用途 | 标签 / 使用说明 |
|---|---|---|
| [diagnosing-bugs](../../skills/debugging/diagnosing-bugs/SKILL.md) | 从症状、复现和证据定位根因，并按请求修复与回归。 | 故障诊断；根因分析 |
| [debug-pro](../../skills/debugging/debug-pro/SKILL.md) | 使用七步调试协议及多语言调试命令定位问题。 | 调试；多语言 |
| [superpowers-systematic-debugging](../../skills/debugging/superpowers-systematic-debugging/SKILL.md) | 按根因调查、模式分析、假设验证和修复执行调试。 | 调试；根因分析 |
| [bug-fixing](../../skills/debugging/bug-fixing/SKILL.md) | 提供分流、复现、影响分析、修复和回归流程。 | Bug修复；回归验证 |
| [code-fix](../../skills/debugging/code-fix/SKILL.md) | 诊断编译、运行时、类型、逻辑和依赖错误。 | 构建失败；异常排查 |
| [log-analyzer](../../skills/debugging/log-analyzer/SKILL.md) | 解析多格式日志、关联服务事件并分析堆栈。 | 日志；堆栈 |
| [nexus-error-explain](../../skills/debugging/nexus-error-explain/SKILL.md) | 调用 NEXUS 第三方服务解释错误信息。 | 第三方服务；付费依赖；输入会发送至 NEXUS 外部服务；需支付凭据或服务提供的测试模式，调用前确认数据与费用条件。 |

## 安装本组

```sh
npx skills add maoyao0607/ai-skills --skill diagnosing-bugs debug-pro superpowers-systematic-debugging bug-fixing code-fix log-analyzer nexus-error-explain -g -y
```

安装后重新打开会话。涉及第三方服务或清理操作时，先阅读该技能的使用说明。
