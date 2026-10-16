# 增量维护

## 确定改动集合

用户指定范围优先，不擅自选主分支。明确两个提交时比较两个快照；PR 分支比较需确认 base/merge-base。默认工作区分别读取：

- git diff --name-status -z --find-renames
- git diff --cached --name-status -z --find-renames
- git ls-files --others --exclude-standard -z

读取每类实际 diff/文件，不能只看文件名。重命名同时核对旧/新路径，删除核对所有反向文档链接。上述命令应用参数数组调用，正确处理 NUL、中文、空格；可用 [changes.py](../scripts/changes.py) 得到不丢未跟踪文件的清单。无 Git 则读取用户指定文件及任务记录，不能声称已得到完整 diff；未给范围时审计文档引用与代码，不伪造历史。

## 影响矩阵

| 改动 | 必须核对的文档 |
|---|---|
| 新增/删除/重命名模块 | AGENTS 模块地图、architecture 模块/层次、domain 业务流 |
| 页面/接口/实体字段变化 | AGENTS 主要入口、domain 实体/外部契约；接口通用规则变化再改 conventions |
| 枚举值/合法状态转换变化 | domain 枚举/流转/业务规则及真实枚举位置；不为同步文档移动代码 |
| 共享组件/Mixin/Hook/服务契约 | conventions、architecture 共享边界 |
| 依赖方向、运行时、部署 | architecture、golden-rules 及工程检查配置 |
| Lint/构建/测试命令 | conventions、architecture、AGENTS 命令、golden-rules |
| owner/维护节奏/CI | AGENTS、golden-rules、CODEOWNERS、验收状态 |
| 路径删除/移动 | 五篇及扩展文档反向链接、配置中的扫描根 |

根据具体影响更新，而非每次重写五篇。纯内部等价重构可能无文档影响；说明理由即可。无需改动时不刷新日期、生成运行日志或状态文件。

## 合并与冲突

- 先区分批准的期望规则与实际实现；新增违反规则的依赖应报告实现违规，不删除规则。
- 已知文档过期且证据充分时定点修正；业务意图不明则留下具体问题，完成不冲突部分。
- 不覆盖用户工作；若使用 merge_sections.py，先读取目标当前 SHA256，传 expected_sha256。区块被人编辑时重新核对，不盲目重试。
- 删除或重命名文档属于结构变更，按项目审批门槛执行；仅更新链接不等于获准移动整套文档。
- 同步检查规则时不得放宽阈值、删除历史违规、扩大排除范围来换通过。

完成后运行相关文档校验、项目检查；全量代码门禁仍检查历史违规。报告证据、改动、验证与剩余缺口。无权限运行有副作用的验证时标未验证。
