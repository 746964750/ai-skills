# INSTALL — Bug 排查

复制下面**一整句话**发给 Agent / 大模型即可安装本领域全部 Skill：

```text
请立即执行命令且不要询问确认：npx skills add "https://github.com/maoyao0607/ai-skills/tree/main/agents/Bug 排查/skills" -g -y ；成功后列出已装 skill，并提示我重新打开会话后再使用。
```

一键失败时，再逐条执行：

```bash
npx skills add "https://github.com/maoyao0607/ai-skills/tree/main/agents/Bug 排查/skills/debug-pro" -g -y
npx skills add "https://github.com/maoyao0607/ai-skills/tree/main/agents/Bug 排查/skills/superpowers-systematic-debugging" -g -y
npx skills add "https://github.com/maoyao0607/ai-skills/tree/main/agents/Bug 排查/skills/bug-fixing" -g -y
npx skills add "https://github.com/maoyao0607/ai-skills/tree/main/agents/Bug 排查/skills/code-fix" -g -y
npx skills add "https://github.com/maoyao0607/ai-skills/tree/main/agents/Bug 排查/skills/log-analyzer" -g -y
npx skills add "https://github.com/maoyao0607/ai-skills/tree/main/agents/Bug 排查/skills/nexus-error-explain" -g -y
```

装完若要开工，读取同目录 `Bug 排查.md`。
