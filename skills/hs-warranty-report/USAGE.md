# hs-warranty-report 使用说明

面向人的操作手册。Agent 执行细节见同目录 [`SKILL.md`](SKILL.md)。

**作者**：@Cong  
**用途**：按豪森售后/质保报工填写要求，生成可直接粘贴的报工文案。

---

## 1. 做什么

根据**当前对话**或**近一周 Agent session**，生成报工两项核心字段：

1. **项目名称** — 与备案一致的完整标准名称  
2. **具体工作内容** — 须同时包含 **问题现象、处理过程、输出物**  

不代替考勤/工时系统录入，只产出文案（及可选的项目名称记忆规则）。

## 2. 安装

本仓库源码：`hs-warranty-report/`

安装到本机全局：

```powershell
Copy-Item -Recurse -Force .\hs-warranty-report $env:USERPROFILE\.cursor\skills\hs-warranty-report
```

全局路径：`%USERPROFILE%\.cursor\skills\hs-warranty-report\`

## 3. 何时用

在业务项目仓库中打开 Cursor，需要：

- 写质保 / 售后报工描述  
- 把本周智能体干活记录整理成合规报工  
- 固定本仓库对应的备案项目名称，避免每次手填  

## 4. 怎么调用

| 方式 | 示例 |
|------|------|
| Slash 命令 | `/hs-warranty-report` |
| 当前上下文报工 | 「根据当前对话写质保报工」「帮我生成售后报工」 |
| 近一周整理 | 「整理近一周报工」「根据这周智能体会话写具体工作内容」 |
| 绑定项目名 | 「当前项目是 XX 集团 ERP 系统建设项目」再报工 |

### 两种模式

| 模式 | 何时用 | 证据从哪来 |
|------|--------|------------|
| **A · 当前上下文**（默认） | 刚做完一轮售后处理 | 本轮对话、打开的文件、相关 git 变更 |
| **B · 近一周 Session** | 周报 / 批量补报工 | 当前项目近 7 天 `agent-transcripts` |

可要求「按天拆成多条」或「合并成一条」。

## 5. 输出长什么样

```markdown
## 质保报工

**项目名称**：XX 集团 ERP 系统建设项目

**具体工作内容**：
处理客户报障：计划模块统计报错，排查为脚本版本不一致，升级至 V2.3 后验证通过。
```

复制到工时系统即可。项目名未知时会出现：`【待补：项目标准名称】`，需人工按备案补齐。

## 6. 项目名称记忆（推荐）

在对话里说明一次备案全名，例如：

> 当前项目是 XX 集团 ERP 系统建设项目

Agent 会写入（或更新）当前仓库：

`.cursor/rules/hs-warranty-project.mdc`

之后在同一仓库再调用本 Skill，会自动使用该名称。改项目名时再说一次即可覆盖。

Agent **不会**在未声明时猜测写入。

## 7. 填写红线（提交前自检）

- 具体工作内容能读出：问题现象 → 处理过程 → 输出物  
- 不要用笼统词：「维护」「支持」「跟进」「日常运维」等无细节空话  
- 不要编造对话/session 里没发生的事；不确定处应标 `【待确认：…】`  
- 不要写入密钥、口令、未公开客户敏感数据  

反例 → 正例见 skill 内 `references/examples.md`。

## 8. 使用注意

- 模式 B 依赖本机 Cursor 项目下的 session 记录；没有实质会话时 Agent 应拒绝编造，并列出需你补充的三要素。  
- 多事项默认合并为一条；要分条时请明确说「按天拆分」或「多条报工」。  
- 规范原文：`references/filling-spec.md`。

## 9. 更新 Skill

```powershell
Copy-Item -Recurse -Force .\hs-warranty-report $env:USERPROFILE\.cursor\skills\hs-warranty-report
```

<!-- hs-warranty-report · author @Cong -->
