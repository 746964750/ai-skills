# test-case-generator（测试用例生成器 · 传统功能）

> 版本 1.2.0 · 可移植技能包：拷贝本文件夹到任意 WorkBuddy 环境即可使用，无本机路径依赖、无需配置密钥。

## 用途

根据需求描述 / 需求文档 / API 文档 / 文档链接 / UI 截图 / **XMind 测试点分析文档（.xmind）**，生成 **6 列标准测试用例**并以 **Excel（.xlsx）默认交付**。
覆盖功能正常、边界、异常、模糊查询、精准查询、排序筛选、组合查询、安全、性能、UI 交互、金融专项等测试类型；
内置测试设计方法指引（等价类+边界值 / 场景法 / 判定表 / 正交试验 / 状态迁移 / 错误推测）。
支持读取 `.xmind` 思维导图（如 `test-analysis-xmind` 产出）并将导图内测试点扩写为完整用例。

## 输出规格

| 项目 | 规范 |
|------|------|
| 字段 | 6 列：测试用例编号 / 测试用例名称 / 测试用例类型 / 前置条件 / 执行步骤 / 预期结果 |
| 交付 | Excel（.xlsx）默认交付；Markdown 表格仅作回复预览 |
| 样式 | 深蓝表头(1F4E78)白字、冻结首行、开启筛选、自动换行并估算行高 |

## 目录结构

```
test-case-generator/
├── SKILL.md                            # 技能主文件（含 Excel 生成器完整源码）
├── scripts/
│   ├── build_testcase_xlsx.py          # Excel 生成器（JSON → xlsx，通用可复用）
│   └── parse_xmind.py                  # XMind 解析器（.xmind → Markdown 大纲/JSON，兼容 Zen 与 XMind8）
├── references/
│   └── ai-testing-scenarios.md         # AI 必测场景参考（仅涉及 AI 时加载）
├── package.json                        # 技能元信息
└── README.md                           # 本说明
```

## 安装（在目标机器上，三选一）

1. **个人级**：将本文件夹放入 `~/.workbuddy/skills/`
   （Windows 即 `C:\Users\<你的用户名>\.workbuddy\skills\`）。
2. **项目级**：放入 `<项目目录>/.workbuddy/skills/`，仅该项目可见。
3. 拿到的是 zip：先解压得到 `test-case-generator/` 文件夹，再按上面路径放置。

放置后重启 / 刷新 WorkBuddy，或在对话中直接 `@test-case-generator` 触发。

## 环境要求（首次使用自动检测并提示）

- Python 3.8+：`python` / `python3` / `py -3` 任一可用即可。
- openpyxl：缺失时执行 `pip install openpyxl`（建议 `python -m venv` 隔离安装）。
- 无需联网、无需任何本机专属路径或密钥。

## 使用方式

在 WorkBuddy 对话中给 AI 一份需求 / 截图 / 文档 / **.xmind 测试点分析文件**，AI 将自动完成：
分析输入 → 选用设计方法 → 编写 `testcases.json` → 调用内置生成器 `build_testcase_xlsx.py` → 交付 Excel。

人工使用（可选）：

```bash
python scripts/build_testcase_xlsx.py testcases.json               # 生成同名 .xlsx
python scripts/build_testcase_xlsx.py testcases.json 指定名称.xlsx # 指定输出文件
python scripts/parse_xmind.py 测试点分析.xmind                    # 打印导图 Markdown 大纲
python scripts/parse_xmind.py 测试点分析.xmind -o out.md          # 大纲写入文件（可再交给 AI 扩写）
```

## 技能边界

本技能以**传统系统功能测试**为主（功能逻辑、字段校验、接口校验、UI 交互、金融专项）。
若被测功能以 **AI/NLP 能力**为主（自然语言查询、大模型交互、意图识别、槽位抽取），请使用配套技能 **test-case-generator-ai**（5 列话术驱动、12 类 AI 必测场景）。
