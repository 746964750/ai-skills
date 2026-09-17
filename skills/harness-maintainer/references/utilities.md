# 辅助工具使用

所有示例中的 SKILL_DIR 指实际技能包位置，不假设全局安装。目标是用户指定仓库，不是技能包目录。

## 改动清单

```text
python SKILL_DIR/scripts/changes.py --root TARGET
python SKILL_DIR/scripts/changes.py --root TARGET --base OLD_REF --target NEW_REF
```

输出包含 scope、status、path、old_path。默认并集包含暂存、未暂存与未跟踪文件；两个引用比较是快照差异，不自动计算 PR merge-base。无 Git 返回退出码 2 和 git_available=false。清单只用于定位，必须继续读取实际内容/diff。

## 安全合并

由 Agent 先阅读原文并形成明确编辑，再写 JSON 数组作为 --plan。新建文件示例：

```json
[
  {
    "path": "docs/domain.md",
    "expected_sha256": null,
    "content": "# 项目领域模型\n\n已核实内容由 Agent 根据代码编写。\n"
  }
]
```

以上仅展示格式，不是合格领域文档。已有文件不能传 content 覆盖；使用 sections 更新已明确标记的区块：

```json
[
  {
    "path": "docs/domain.md",
    "expected_sha256": "读取当前原始文件字节计算的 SHA256",
    "sections": [
      {"id": "states", "content": "## 状态机\n\n经核实的实际枚举和流转。"}
    ]
  }
]
```

区块由一对 HTML 注释界定：

```markdown
<!-- harness:states:start -->
## 状态机

内容
<!-- harness:states:end -->
```

不存在区块时先人工定位合并已有章节；确实需要追加而非重复现有正文时，才设置 allow_append=true。模板不强制整篇进入托管区块。

```text
python SKILL_DIR/scripts/merge_sections.py --root TARGET --plan reviewed-edits.json
python SKILL_DIR/scripts/merge_sections.py --root TARGET --plan reviewed-edits.json --write
```

默认预览；--write 才写入。每个既有目标必须提供当前哈希。所有文件先预检，再逐文件原子替换，并再次核对内容；不承诺多文件事务或可抵御任意并发写入。发现冲突停止，重新检查，不自动刷新哈希重试。无内容变化不会改写文件或时间。

## 验证技能自身

在技能目录运行 python -B -m unittest discover -s tests -v。真实前端集成测试需设置 HARNESS_NODE 为 Node 路径、HARNESS_NODE_MODULES 为独立测试依赖目录（@babel/parser、@vue/compiler-sfc、vue-template-compiler）。Java 测试需 PATH 中有 javac、jdeps。缺依赖的集成测试会跳过，交付时必须报告，不能仅凭总状态 OK 宣称验证全部完成。

skill-creator 的 quick_validate.py 验证技能结构，依赖 PyYAML；依赖缺失应如实报告。脚本测试不等于业务语义或实际项目 CI 已验收。
