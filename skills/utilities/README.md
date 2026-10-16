# 工作与系统工具

整理工作记录和分析本机存储。

报工选 hs-warranty-report；磁盘占用选 storage-analyzer，先区分只读报告和执行清理。

[返回仓库导航](../../README.md) · [迁移说明](../../docs/migration.md)

## 技能

| 技能 | 用途 | 标签 / 使用说明 |
|---|---|---|
| [hs-warranty-report](../../skills/utilities/hs-warranty-report/SKILL.md) | 根据对话、Git 和会话证据整理售后或质保报工。 | 售后；报工；工作记录 |
| [storage-analyzer](../../skills/utilities/storage-analyzer/SKILL.md) | 只读扫描磁盘占用，生成静态报告或启动交互式清理服务。 | 存储；Windows；macOS；扫描只读；清理服务支持回收站及永久删除，属于独立写操作。原技能注明 Windows 未经真实环境验证。 |

## 安装本组

```sh
npx skills add maoyao0607/ai-skills --skill hs-warranty-report storage-analyzer -g -y
```

安装后重新打开会话。涉及第三方服务或清理操作时，先阅读该技能的使用说明。
