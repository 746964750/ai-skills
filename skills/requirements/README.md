# 需求与产品

从原始材料或产品想法建立可追溯、可评审的需求。

文档抽取选 requirement-extractor；WCS 范围选专项抽取；需求探索选 requirements-analysis；PRD 撰写与评审按产物选择。

[返回仓库导航](../../README.md) · [迁移说明](../../docs/migration.md)

## 技能

| 技能 | 用途 | 标签 / 使用说明 |
|---|---|---|
| [requirement-extractor](../../skills/requirements/requirement-extractor/SKILL.md) | 从 Word、Excel、PDF 等材料抽取指定主体的功能、接口、歧义及出处。 | 需求抽取；出处追溯 |
| [wcs-requirement-extractor](../../skills/requirements/wcs-requirement-extractor/SKILL.md) | 抽取 WCS 功能并区分上游业务系统、PLC 与设备控制层职责。 | 工业仓储；WCS；职责边界 |
| [requirements-analysis](../../skills/requirements/requirements-analysis/SKILL.md) | 通过需求探索拆分 EPIC、需求和用户故事并排序。 | 用户故事；优先级 |
| [software-manager-skill](../../skills/requirements/software-manager-skill/SKILL.md) | 提供产品规划、路线图、竞品分析、PRD 和原型工作流。 | 产品规划；PRD；完整流程需要可用的网络搜索及资料检索能力；按当前任务选择阶段。 |
| [prd](../../skills/requirements/prd/SKILL.md) | 生成面向开发执行的用户故事、验收标准及结构化 PRD。 | PRD；验收标准 |
| [prd-writer-pro](../../skills/requirements/prd-writer-pro/SKILL.md) | 将需求整理为结构清晰、内容完整的产品需求文档。 | PRD；文档撰写 |
| [prd-reviewer](../../skills/requirements/prd-reviewer/SKILL.md) | 按明确评分维度评审 PRD 并说明扣分与改进项。 | PRD；需求评审 |
| [prd-to-design-doc](../../skills/requirements/prd-to-design-doc/SKILL.md) | 将 PRD 转为信息架构、交互、布局和视觉设计需求。 | PRD；设计交付 |

## 安装本组

```sh
npx skills add maoyao0607/ai-skills --skill requirement-extractor wcs-requirement-extractor requirements-analysis software-manager-skill prd prd-writer-pro prd-reviewer prd-to-design-doc -g -y
```

安装后重新打开会话。涉及第三方服务或清理操作时，先阅读该技能的使用说明。
