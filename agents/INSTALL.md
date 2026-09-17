# agents 一句话安装（复制发给 Agent）

用户只需复制下面对应的**一整句话**，粘贴给 Agent / 大模型，即可自动安装。不要拆句、不要改 URL。

---

## 按领域（推荐）

**PRD 撰写**

```text
请立即执行命令且不要询问确认：npx skills add "https://github.com/maoyao0607/ai-skills/tree/main/agents/PRD 撰写/skills" -g -y ；成功后列出已装 skill，并提示我重新打开会话后再使用。
```

**UI 原型设计**

```text
请立即执行命令且不要询问确认：npx skills add "https://github.com/maoyao0607/ai-skills/tree/main/agents/UI 原型设计/skills" -g -y ；成功后列出已装 skill，并提示我重新打开会话后再使用。
```

**代码重构**

```text
请立即执行命令且不要询问确认：npx skills add "https://github.com/maoyao0607/ai-skills/tree/main/agents/代码重构/skills" -g -y ；成功后列出已装 skill，并提示我重新打开会话后再使用。
```

**Bug 排查**

```text
请立即执行命令且不要询问确认：npx skills add "https://github.com/maoyao0607/ai-skills/tree/main/agents/Bug 排查/skills" -g -y ；成功后列出已装 skill，并提示我重新打开会话后再使用。
```

**自动化测试**

```text
请立即执行命令且不要询问确认：npx skills add "https://github.com/maoyao0607/ai-skills/tree/main/agents/自动化测试/skills" -g -y ；成功后列出已装 skill，并提示我重新打开会话后再使用。
```

---

## 安装全部 agents

```text
请依次立即执行下列命令且不要询问确认：npx skills add "https://github.com/maoyao0607/ai-skills/tree/main/agents/PRD 撰写/skills" -g -y ；npx skills add "https://github.com/maoyao0607/ai-skills/tree/main/agents/UI 原型设计/skills" -g -y ；npx skills add "https://github.com/maoyao0607/ai-skills/tree/main/agents/代码重构/skills" -g -y ；npx skills add "https://github.com/maoyao0607/ai-skills/tree/main/agents/Bug 排查/skills" -g -y ；npx skills add "https://github.com/maoyao0607/ai-skills/tree/main/agents/自动化测试/skills" -g -y ；全部成功后汇总已装 skill，并提示我重新打开会话后再使用。
```

---

## Agent 执行规则（读到上述句子时）

1. 原样跑句中的 `npx skills add ...`，保留双引号与中文路径。
2. 不要改成 `maoyao0607/ai-skills@skill-name` 短名。
3. 无 `npx` 时先说明需安装 Node.js，再停止。
4. 失败时输出完整错误；可回退到同领域 `INSTALL.md` 里的逐个安装命令。
