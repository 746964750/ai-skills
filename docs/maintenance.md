# 维护与验证

[返回仓库导航](../README.md) · [迁移说明](migration.md) · [本次验证记录](verification.md)

## 修改分类与导航

编辑根目录 `catalog.json`。每条技能记录包含 `name`、`group`、`path`、`summary`、`tags`、`notes`、`previous_path` 和 `previous_name`；旧路径与名称只用于迁移说明。

当前版本固定为已确认的 40 个技能和七组归属。未来增减技能时，同时调整生成器的数量约束与测试；不要通过复制目录让一个技能出现在多个分类。通用与行业属性使用标签表达。

```sh
python tools/catalog.py
python tools/catalog.py --check
python -m unittest discover -s tools/tests -v
```

生成器只使用 Python 标准库和 Git。生成与检查都会读取远端 HEAD 核验默认分支，不修改 Git 配置或远端仓库；网络失败时明确报错。`--check` 不写入文件，检查分类、名称、归属、维护范围内的 Markdown 链接，以及生成文件是否同步。

生成内容为根 README、七组 README、迁移说明和 `docs/index.html` 的标记数据块。展示页的 CSS、结构和交互代码仍在 HTML 内维护；搜索数据直接嵌入页面，不额外请求根目录的 catalog，也不依赖站点构建工具。

## 技能发现

在仓库根目录运行：

```sh
npx --yes skills add . --list
```

该命令仅列出本地可发现技能，不全局安装。应发现 40 个唯一名称，其中四个名称已按迁移表统一，另两个技能已补齐 frontmatter。

## 现有自测与资产检查

```sh
python skills/design/byd-wms-manage-style/scripts/test_check_style.py
python skills/design/byd-wms-pda-style/scripts/test_check_style.py
python skills/engineering/harness-maintainer/tests/test_harness.py
python skills/design/byd-wms-manage-style/scripts/check_style.py --assets-only
python skills/design/byd-wms-pda-style/scripts/check_style.py --assets-only
```

整理前基线分别为 9、7、38 项。Harness 前端集成测试依赖真实 Babel/Vue 解析器，可按测试文件中的 `HARNESS_NODE_MODULES`、`HARNESS_NODE` 准备环境；Java 集成测试依赖 JDK。环境缺失导致的跳过必须单独报告。

变动受 manifest 管理的文档或资产时，只更新对应文件的散列。维持 UTF-8 文本 CRLF 转 LF、二进制不变的规则；不能通过重算散列掩盖未经确认的主题变化。

## 展示页验收

```sh
python -m http.server 8765 --bind 127.0.0.1 --directory docs
```

打开 `http://127.0.0.1:8765/`，确认初始显示 40 项，七组分别显示 8、8、4、4、7、7、2 项；名称、用途及行业标签可搜索，组合筛选和空结果正常。核对技能链接、工作流链接、单个与分组复制命令，并检查窄屏布局。

页面中的源码链接指向生成时核验的远端默认分支。本地未发布的新路径在远端尚不可访问；提交发布后才能验收远端目标页面。

分类整理不执行外部付费服务或文件清理服务，也不代表这些技能的业务功能已验收。NEXUS、agent-git-oracle 的外部依赖，以及存储工具的扫描/清理模式和 Windows 状态均保留在导航说明中。
